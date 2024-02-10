from datetime import datetime
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from lesson.models import Course, Lesson, Payments, Subscribe
from lesson.paginations import LessonPagination
from lesson.serliazers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscribeSerializer
from users.permissions import IsModerator, IsUser
import stripe


class CourseViewSet(viewsets.ModelViewSet):
    """Вьюсет на курсы"""
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated | IsModerator | IsUser]
    pagination_class = LessonPagination

    def partial_update(self, request, pk=None):
        course = self.get_object()
        course.date_update = datetime.now()
        course.save(update_fields=['date_update'])
        serializer = self.get_serializer(course)
        return Response(serializer.data)

    def get_queryset(self):
        if self.request.user.role == "member":
            return Course.objects.filter(user=self.request.user)
        elif self.request.user.role == 'moderator':
            return Course.objects.all()

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsModerator]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsUser]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated | IsUser | IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsModerator, IsUser]
        return [permission() for permission in permission_classes]


class LessonListAPIView(generics.ListAPIView):
    """Список уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsModerator, IsUser]
    permission_classes = [AllowAny]
    pagination_class = LessonPagination

    def get_queryset(self):
        if self.request.user.role == "member":
            return Lesson.objects.filter(user=self.request.user)
        elif self.request.user.role == 'moderator':
            return Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]


class LessonCreateAPIView(generics.CreateAPIView):
    """Добавление урока"""
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated, IsModerator, IsUser]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Апгрейд урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated, IsModerator]


class PaymentsListAPIView(generics.ListAPIView):
    """Вывод списка платежей"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('data_payments',)
    filterset_fields = ('paid_course', 'payment_method',)


class PaymentsCreateApiView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer

    class PaymentsCreateApiView(generics.CreateAPIView):
        serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_payment = serializer.save()
        stripe.api_key = 'sk_test_51OdoXSHC8LUh8NqZQboynIwfP7znL7qfNqCOqOYkl7k3pzAKN8QU45ye5RpnABJ2MRjLBfk6tWWisTmY9QoiXJNR00NP3ImbNV'
        payment_intent = stripe.PaymentIntent.create(
            amount=2000,
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )
        new_payment.session_id = payment_intent.id
        new_payment.amount = payment_intent.amount
        new_payment.save()

        return super().perform_create(new_payment)


class GetPaymentView(APIView):
    serializer_class = PaymentsSerializer

    def get(self, request, payment_id):
        payment = Payments.objects.get(pk=payment_id)
        payment_id = payment.session_id
        stripe.api_key = 'sk_test_51OdoXSHC8LUh8NqZQboynIwfP7znL7qfNqCOqOYkl7k3pzAKN8QU45ye5RpnABJ2MRjLBfk6tWWisTmY9QoiXJNR00NP3ImbNV'
        payment_intent = stripe.PaymentIntent.retrieve(payment_id)
        print(payment_intent)
        return Response({'status': payment_intent.status, 'body': payment_intent})


class SubscribeViewSet(viewsets.ModelViewSet):
    """Вьюсет подписки"""
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated, IsUser]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()
