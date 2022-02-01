# -*- coding: utf-8 -*-

# klasa bierze obiekt pythonowy i zmienia na obiekt JSONowy
# pracuje analogicznie jak ModelForm

from rest_framework.serializers import ModelSerializer
from base.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
