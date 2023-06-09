import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .utils import content_file_name, message_file_name, upload_to


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True, null=True)
    guest_identifier = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=255, default=f"User")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    pfp = models.FileField(null=True, upload_to=content_file_name)
    phone = models.CharField(max_length=255)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email} - {self.phone}'


class CustomDoctor(CustomUser):
    personnel_code = models.CharField(max_length=255)
    rank = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(default="عمومی", max_length=255)


class Reservation(models.Model):
    doctor = models.ForeignKey(to=CustomDoctor, on_delete=models.SET_NULL)
    patience = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=datetime.datetime.now())
    rating = models.IntegerField(default=0)
    comment = models.TextField(default="")
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL)


class Chat(models.Model):
    class ChatType(models.TextChoices):
        vid = 'video'
        audio = 'audio'
        text = 'text'
        other = 'other'

    participant1 = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL)
    participant2 = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL)
    reservation = models.ForeignKey(to=Reservation, on_delete=models.SET_NULL)
    type = models.CharField(choices=ChatType.choices, default=ChatType.text, max_length=10)


class Message(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    edite_at = models.DateTimeField(default=timezone.now)
    content = models.TextField(default="", null=True)
    user_id = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL, null=True)
    ticket_id = models.ForeignKey(to=Chat, on_delete=models.CASCADE, null=True)
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
