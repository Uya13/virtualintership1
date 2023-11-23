from .models import *
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'full_name', 'phone']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['title', 'date_added', 'image']


class PerevalsSerializer(serializers.ModelSerializer):
    user_id = UsersSerializer()
    coord_id = CoordsSerializer()
    level_id = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True)

    class Meta:
        model = Perevals
        fields = ['beautyTitle', 'title', 'connect', 'status', 'add_time', 'level_id', 'coord_id', 'user_id']