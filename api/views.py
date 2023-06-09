import api.models

from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import *
from .serializers import *


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        try:
            if 'guest' in request.build_absolute_uri():
                serializer = self.serializer_class(data=request.data,
                                                   context={'request': request})
                user = CustomUser.objects.get(guest_identifier=request.data['guest_identifier'])
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'guest_identifier': user.guest_identifier
                })
            if 'google' in request.build_absolute_uri():
                serializer = self.serializer_class(data=request.data,
                                                   context={'request': request})

                user = CustomUser.objects.get(email=request.data['username'])
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                })
            if 'discord' in request.build_absolute_uri():
                serializer = self.serializer_class(data=request.data,
                                                   context={'request': request})

                user = CustomUser.objects.get(discord_id=request.data['discord_id'])
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                })

            if 'steam' in request.build_absolute_uri():
                serializer = self.serializer_class(data=request.data,
                                                   context={'request': request})

                user = CustomUser.objects.get(steam_hex=request.data['steam_hex'])
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                })
        except api.models.CustomUser.DoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)


class CustomUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = []
    parser_classes = (MultiPartParser, FormParser)


@permission_classes((AllowAny,))
class CustomUserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            user = self.queryset.get(id=kwargs['pk'])
            user = self.serializer_class(user)
            return Response(user.data)
        else:
            user_id = Token.objects.get(key=request.auth.key).user_id
            user = self.queryset.get(id=user_id)
            user = self.serializer_class(user)
            return Response(user.data)

    @permission_classes((IsAdminUser,))
    def delete(self, request, *args, **kwargs):
        user = self.queryset.get(id=kwargs['pk'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data=f"{user} has been deleted")

    def put(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.id == self.get_object().id:
            return self.update(request, args, kwargs)


class CustomDoctorList(generics.ListAPIView):
    queryset = CustomDoctor.objects.all()
    serializer_class = CustomDoctorSerializer
    permission_classes = []
    parser_classes = (MultiPartParser, FormParser)


@permission_classes((AllowAny,))
class CustomDoctorCreate(generics.CreateAPIView):
    queryset = CustomDoctor.objects.all()
    serializer_class = CustomDoctorSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomDoctorDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomDoctor.objects.all()
    serializer_class = CustomDoctorSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            user = self.queryset.get(id=kwargs['pk'])
            user = self.serializer_class(user)
            return Response(user.data)
        else:
            user_id = Token.objects.get(key=request.auth.key).user_id
            user = self.queryset.get(id=user_id)
            user = self.serializer_class(user)
            return Response(user.data)

    @permission_classes((IsAdminUser,))
    def delete(self, request, *args, **kwargs):
        user = self.queryset.get(id=kwargs['pk'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data=f"{user} has been deleted")

    def put(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.id == self.get_object().id:
            return self.update(request, args, kwargs)


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        if 'sysid' in kwargs and 'system' in request.build_absolute_uri():
            categories = self.queryset.filter(sys_id=kwargs['sysid'])
            categories = self.serializer_class(categories, many=True)
            return Response(categories.data)
        if 'pk' in kwargs:
            return self.retrieve(request, args, kwargs)
        else:

            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class ChatList(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ChatDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        if 'send/defaultmessage/' in request.build_absolute_uri():
            try:
                cm = self.queryset.get(cat_id=request.data['cat_id'])
            except api.models.Message.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            resv = Reservation.objects.get(id=request.data['reservation_id'])
            msg = self.queryset.create()
            msg.content = cm.content
            msg.ticket_id = resv
            msg.save()
            # attachments
            achs = Attachment.objects.filter(message_id=cm.id)
            for a in achs:
                _attch = Attachment.objects.create()
                _attch.media = a.media
                _attch.message_id = msg.id
                _attch.save()
            msg = self.serializer_class(msg)
            return Response(msg.data)
        else:
            return self.create(request, args, kwargs)


class MessageDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        if 'tid' in kwargs:
            messages = self.queryset.filter(ticket_id=kwargs['tid'])
            messages = self.serializer_class(messages, many=True)
            return Response(messages.data)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class AttachmentList(generics.ListCreateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    parser_classes = (MultiPartParser, FormParser)


class AttachmentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        if 'mid' in kwargs:
            attachments = self.queryset.filter(message_id=kwargs['mid'])
            attachments = self.serializer_class(attachments, many=True)
            return Response(attachments.data)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
