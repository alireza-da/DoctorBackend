from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .utils import content_file_name, message_file_name, upload_to


class CustomUser(AbstractBaseUser, PermissionsMixin):
    steam_hex = models.CharField(max_length=255, unique=True, null=True)
    email = models.EmailField(_("email address"), unique=True, null=True)
    discord_id = models.CharField(max_length=20, unique=True, null=True)
    guest_identifier = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=255, default=f"User")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    pfp = models.FileField(null=True, upload_to=content_file_name)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email} - {self.steam_hex}'


class Message(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    edite_at = models.DateTimeField(default=timezone.now)
    content = models.TextField(default="", null=True)
    user_id = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL, null=True)
    ticket_id = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, null=True)
    reply_to = models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True)


class Attachment(models.Model):
    class AttachmentType(models.TextChoices):
        vid = 'video'
        audio = 'audio'
        picture = 'picture'
        other = 'other'

    uploaded_at = models.DateTimeField(default=timezone.now)
    type = models.CharField(choices=AttachmentType.choices, default=AttachmentType.other, max_length=10)
    message_id = models.ForeignKey(to=Message, on_delete=models.CASCADE)
    media = models.FileField(null=True, upload_to=message_file_name)
