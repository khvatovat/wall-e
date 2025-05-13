from rest_framework import serializers
from .models import Robot, Trash

class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ['id', 'x', 'y', 'hasTrash']

class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trash
        fields = ['id', 'x', 'y']