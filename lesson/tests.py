from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lesson.models import Lesson, Course, Subscribe
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='5@mail.ru',
            is_staff=True,
            is_active=True,
            is_superuser=False,
            first_name='Rufat',
            last_name='Geydarov'

        )
        self.user.set_password('12345')
        self.user.save()
        self.course = Course.objects.create(
            title='test1',
            description='test1',

        )
        self.lesson_data = Lesson.objects.create(
            title='test1',
            description='test1',
            link_video='https://youtube.com',
            user=self.user,
            course=self.course
            )

    def test_lesson_create(self):
        """Test lesson"""
        response = self.client.post(
            '/lesson/lesson/create/',
            data={'pk': 2, 'title': 'test1', 'description': 'test1', 'course': self.course.pk, 'user': self.user.id, 'link_video': 'https://youtube.com'}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {'pk': 4, 'title': 'test1', 'description': 'test1', 'course': self.course.pk, 'user': self.user.pk, 'link_video': 'https://youtube.com'}
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_lesson(self):
        """Test List"""

        response = self.client.get(
            '/lesson/lesson/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
           {'count': 1, 'next': None, 'previous': None, 'results': [{'pk': 2, 'title': 'test1', 'description': 'test1', 'course': self.course.pk, 'user': self.user.pk, 'link_video': 'https://youtube.com'}]})

    def test_delete(self):
        """Удаление урока"""

        response = self.client.delete(
            '/lesson/lesson/1/delete/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update(self):
        """обновление урока"""
        data = {'pk': 1, 'title': 'test1123123123123123123', 'description': 'test1', 'course': self.course.pk, 'user': self.user.id,
                'link_video': 'https://youtube.com'}

        response = self.client.put(
            '/lesson/lesson/5/update/',
            data=data
        )

        self.assertEquals(response.json(),
                          {'pk': 1
                              , 'title': 'test1123123123123123123', 'description': 'test1', 'course':  self.course.pk, 'user': self.user.id, 'link_video': 'https://youtube.com'}
                          )


class SubscribeTestCase(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='test1',
            description='test1',

        )

        self.user = User.objects.create(
            email='5@mail.ru',
            is_staff=True,
            is_active=True,
            is_superuser=False,
            first_name='Rufat',
            last_name='Geydarov'

        )
        self.user.set_password('12345')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.subscribe = Subscribe.objects.create(
            user=self.user,
            is_active=True,
            course=self.course
        )

    def test_create_subscribe(self):

        response = self.client.post(
            '/lesson/subscribe/',
            data={'user': self.user.pk, 'is_active': True, 'course': self.course.pk}
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {'id': 2, 'is_active': True, 'user': self.user.pk, 'course': self.course.pk}

        )

    def test_subscribe_list(self):
        """Test List"""

        response = self.client.get(
            '/lesson/subscribe/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
           [{'id': 5, 'is_active': True, 'user': self.user.pk, 'course': self.user.pk}]
        )

    def test_update(self):
        """обновление урока"""
        response = self.client.post(
            '/lesson/subscribe/',
            data={'user': self.user.pk, 'is_active': True, 'course': self.course.pk}
        )
        print(response.json())
        response = self.client.put(
            '/lesson/subscribe/7/',

        )

        self.assertEquals(response.json(),
                          {'id':7, 'is_active': True, 'user': 8, 'course': 8}

                          )

    def test_delete_subscribe(self):
        response = self.client.post(
            '/lesson/subscribe/',
            data={'user': self.user.pk, 'is_active': True, 'course': self.course.pk}
        )
        print(response.json())
        response = self.client.delete(
            '/lesson/subscribe/2/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


