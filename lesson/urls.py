from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lesson.apps import LessonConfig
from lesson.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonDestroyAPIView, \
    LessonUpdateAPIView, PaymentsListAPIView, SubscribeViewSet, PaymentsCreateApiView, GetPaymentView

app_name = LessonConfig.name
router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')
router.register(r'subscribe', SubscribeViewSet, basename='subscribe')


urlpatterns = [

    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),
    path('payments/create/', PaymentsCreateApiView.as_view(), name='payments-create'),
    path('payments/<str:payment_id>/', GetPaymentView.as_view(), name='payment_get'),
    path('lesson/subscribe/', include(router.urls)),
]+router.urls