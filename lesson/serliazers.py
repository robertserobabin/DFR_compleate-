from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lesson.models import Course, Lesson, Payments, Subscribe
from lesson.validators import LinkValidator


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('pk', 'title', 'description', 'course', 'user', 'link_video',)
        validators = [LinkValidator(fields='link_video')]


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)
    lesson_count = SerializerMethodField()
    subscribe = SubscribeSerializer(source='subscribe_set', many=True, read_only=True)


    def get_lesson_count(self, obj):
        return obj.lesson_set.all().count()


    def get_subscribe(self, obj):
        return obj.subscribe_set.all()

    class Meta:
        model = Course
        fields = '__all__'





