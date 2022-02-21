# -*- coding: utf-8 -*-

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from base.models import Room, User, Topic, Message


def create_user_alex():
    return User.objects.create(
        name='Alex',
        email='alex@alex.com',
        bio='Jestem Alex',
    )


def create_topics(name='Django'):
    return Topic.objects.create(
        name=name,
    )


def create_room(name: str, topic: str, name_room: str = 'Pogadanki o Django') -> Room:
    host = User.objects.get(name=name)
    topic = Topic.objects.get(name=topic)
    return Room.objects.create(
        host=host,
        topic=topic,
        name=name_room,
        description="Jesteśmy tutaj, aby pogadać o Django",
    )


def create_message(user: str, room: str, message: str = 'Witaj') -> Message:
    user = User.objects.get(name=user)
    room = Room.objects.get(name=room)
    return Message.objects.create(
        user=user,
        room=room,
        body=message
    )


class TestHome(TestCase):
    def setUp(self):
        create_user_alex()
        create_topics(name="Django")
        create_room(name='Alex', topic="Django")
        create_message(user='Alex', room="Pogadanki o Django")

    def test_home_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # self.assertEqual(response.)

    def test_home_q_is_not_empty(self):
        response = self.client.get(reverse('home'), {'q': 'django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


