from .models import *
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        self.is_valid()
        user = Users.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = Users.objects.create(
                email=self.validated_data['email'],
                full_name=self.validated_data['full_name'],
                phone=self.validated_data['phone']
            )
            new_user.save()
            return new_user

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
    images = ImagesSerializer(many=True, allow_null=True)

    def update(self, instance, validated_data):
        instance.beautyTitle = validated_data.get("beautyTitle", instance.beautyTitle)
        instance.title = validated_data.get("title", instance.title)
        instance.other_titles = validated_data.get("other_titles", instance.other_titles)
        instance.connect = validated_data.get("connect", instance.connect)
        instance.status = validated_data.get("status", instance.status)
        instance.add_time = validated_data.get("add_time", instance.add_time)

        coord_data = validated_data.pop('coord_id', None)
        if coord_data:
            coord = Coords.objects.get_or_create(**coord_data)[0]
            validated_data['coord_id'] = coord
        instance.coord_id = validated_data.get("coord_id", instance.coord_id)

        level_data = validated_data.pop('level_id', None)
        if level_data:
            level = Level.objects.get_or_create(**level_data)[0]
            validated_data['level_id'] = level
        instance.level_id = validated_data.get("level_id", instance.level_id)

        instance.save()
        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user_id', None)
        coord_data = validated_data.pop('coord_id', None)
        level_data = validated_data.pop('level_id', None)

        if user_data:
            user = Users.objects.get_or_create(**user_data)[0]
            validated_data['user_id'] = user
        if coord_data:
            coord = Coords.objects.get_or_create(**coord_data)[0]
            validated_data['coord_id'] = coord
        if level_data:
            level = Level.objects.get_or_create(**level_data)[0]
            validated_data['level_id'] = level
        return Perevals.objects.create(**validated_data)

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user_id
            data_user = data.get('user_id')
            user_fields_for_validation = [
                instance_user.email != data_user['email'],
                instance_user.phone != data_user['phone'],
                instance_user.full_name != data_user['full_name']
            ]
            if data_user is not None and any(user_fields_for_validation):
                raise serializers.ValidationError(
                    {
                        'Ошибка': 'Данные пользователя заменить нельзя'
                    }
                )
        return data

    class Meta:
        model = Perevals
        fields = ['beautyTitle', 'title', 'connect', 'status', 'add_time', 'level_id', 'coord_id', 'user_id', 'images']