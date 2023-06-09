from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    pfp = serializers.FileField(required=False)

    class Meta:
        model = CustomUser
        fields = (
            'steam_hex', 'email', 'discord_id', 'name', 'is_staff', 'is_banned', 'id', 'date_joined', 'pfp', 'password',
            'guest_identifier')

    # def create(self, validated_data):
    #     user = super().create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(CustomUserSerializer, self).create(validated_data)


class CustomDoctorSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    pfp = serializers.FileField(required=False)

    class Meta:
        model = CustomUser
        fields = (
            'steam_hex', 'email', 'discord_id', 'name', 'is_staff', 'is_banned', 'id', 'date_joined', 'pfp', 'password',
            'guest_identifier', 'personnel_code', 'rank')

    # def create(self, validated_data):
    #     user = super().create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(CustomDoctorSerializer, self).create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('content', 'user_id', 'chat_id', 'reply_to', 'id', 'created_at', 'edite_at')


class AttachmentSerializer(serializers.ModelSerializer):
    media = serializers.FileField(required=True)

    class Meta:
        model = Attachment
        fields = ('type', 'message_id', 'media', 'id')


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('doctor', 'patience', 'date', 'rating', 'comment', 'category')


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('participant1', 'participant2', 'reservation')
