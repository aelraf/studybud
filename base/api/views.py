# -*- coding: utf-8 -*-

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Room
from .serializers import RoomSerializer


@api_view(['GET'])
def get_route(request):
    routes = [
        'GET /api,',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)

    return Response(serializer)
