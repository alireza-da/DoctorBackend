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


class SystemSerializer(serializers.ModelSerializer):
    banner = serializers.FileField(required=False)
    pfp = serializers.FileField(required=False)

    class Meta:
        model = System
        fields = ('id', 'name', 'ref_url', 'expires_at', 'staff_limit', 'member_limit', 'is_private', 'about_system',
                  'ticket_prefix', 'banner', 'pfp')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('name', 'sys_id', 'user_id', 'read_messages', 'write_messages', 'delete_messages', 'read_history',
                  'upload_media', 'delete_ticket', 'create_ticket', 'update_ticket', 'manage_system', 'manage_role',
                  'manage_members', 'owner', 'id', 'color', 'level', 'parent')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('name', 'sys_id', 'category', 'id', 'is_closed', 'created_at', 'is_deleted')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'color', 'sys_id', 'id', 'custom_fields')


class TicketRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketRole
        fields = (
            'name', 'sys_id', 'user_id', 't_id', 'read_messages', 'write_messages', 'delete_messages', 'read_history',
            'upload_media', 'delete_ticket', 'create_ticket', 'update_ticket', 'manage_system', 'manage_role',
            'manage_members', 'level', 'id', 'is_creator')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('content', 'user_id', 'ticket_id', 'reply_to', 'id', 'created_at', 'edite_at', 'cat_id')


class AttachmentSerializer(serializers.ModelSerializer):
    media = serializers.FileField(required=True)

    class Meta:
        model = Attachment
        fields = ('type', 'message_id', 'media', 'id')


class CategoryRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryRole
        fields = ('id', 'category', 'role', 'for_closed')


class PredefinedMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredefinedMessage
        fields = ('title', 'content', 'sys', 'id')
