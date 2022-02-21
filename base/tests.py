# -*- coding: utf-8 -*-
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from base.models import Room, User, Topic, Message


def create_user(name='Alex', email='alex@alex.com', bio='Jestem Alex', password=1234):
    return User.objects.create(
        name=name,
        email=email,
        bio=bio,
        password=password,
    )


def create_topics(name='Django'):
    return Topic.objects.create(
        name=name,
    )


def create_room(
        name: str,
        topic: str,
        name_room: str = 'Pogadanki o Django',
        desc: str = "Jesteśmy tutaj, aby pogadać o Django",
) -> Room:
    host = User.objects.get(name=name)
    topic = Topic.objects.get(name=topic)

    return Room.objects.create(
        host=host,
        topic=topic,
        name=name_room,
        description=desc,
    )


def create_message(user: str, room: str, message: str = 'Witaj') -> Message:
    user = User.objects.get(name=user)
    room = Room.objects.get(name=room)
    return Message.objects.create(
        user=user,
        room=room,
        body=message
    )


class TestHomeView(TestCase):
    def setUp(self) -> None:
        create_user(name='Alex', email='alex@alex.com', bio='Jestem Alex')
        create_topics(name="Django")
        create_topics(name="Java")
        create_topics(name="C++")
        create_room(name='Alex', topic="Django")
        create_room(name='Alex', topic="Java", name_room="pogadanki o Javie", desc='tylko Java')
        create_message(user='Alex', room="Pogadanki o Django")

    def test_home_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rooms = Room.objects.all()
        rooms_count = rooms.count()

        self.assertIsInstance(response.context['rooms'], QuerySet)
        self.assertNotEqual(response.context['rooms'], [])
        self.assertEqual(response.context['rooms'].count(), rooms_count)
        self.assertQuerysetEqual(response.context['rooms'], rooms)

        self.assertNotEqual(response.context['topics'], [])
        self.assertEqual(response.context['topics'].count(), 3)

        self.assertNotEqual(response.context["room_count"], [])
        self.assertEqual(response.context["room_count"], rooms_count)

        self.assertNotEqual(response.context['room_messages'], [])
        self.assertEqual(response.context["room_messages"].count(), 1)

    def test_home_q_is_django(self):
        response = self.client.get(reverse('home'), {'q': 'django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_count = response.context['rooms'].count()
        self.assertEqual(response_count, 1)

        self.assertEqual(response.context['room_count'], 1)

        self.assertEqual(response.context['topics'].count(), 3)

    def test_home_q_is_not_valid(self):
        response = self.client.get(reverse('home'), {'q': '*234ksQO__5$'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_count = response.context['rooms'].count()
        self.assertEqual(response_count, 0)


class TestRoomView(TestCase):
    # https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
    # https://iheanyi.com/journal/user-registration-authentication-with-django-django-rest-framework-react-and-redux/
    # https://docs.djangoproject.com/en/4.0/topics/testing/tools/
    # https://realpython.com/testing-in-django-part-1-best-practices-and-examples/
    # https://www.youtube.com/watch?v=ljG1WzBAboQ
    def setUp(self) -> None:
        create_user(name='Alex', email='alex@alex.com', bio='Jestem Alex')
        # create_user(name='John', email='john@john.com', bio="Starzec")
        create_topics(name="Django")
        create_topics(name="Java")
        create_topics(name="C++")
        create_room(name='Alex', topic="Django")
        create_room(name='Alex', topic="Java", name_room="pogadanki o Javie", desc='tylko Java')
        create_message(user='Alex', room="Pogadanki o Django")
        create_message(user='Alex', room="Pogadanki o Django", message="to zaczynamy?")

    def test_room_get(self):
        pk = 1
        response = self.client.get(reverse('room', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.context['room_messages'].count(), 2)

    def test_room_post_message(self):
        pk = 1
        user = User.objects.get(name='Alex')
        self.assertIsInstance(user, User)
        self.user = user
        login = self.client.login(username='Alex', password='1234')
        print("user: {}, {}, {}, {},".format(user, user.email, user.pk, user.password))
        response = self.client.post(reverse('room', kwargs={'pk': pk}), {'body': 'Witam witam'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

