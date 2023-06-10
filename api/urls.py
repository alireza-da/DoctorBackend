from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # Authentications
    path('ata/', obtain_auth_token, name='ata'),
    path('ata/google/',  views.CustomAuthToken.as_view(), name='ata_google'),
    path('ata/discord/', views.CustomAuthToken.as_view(), name='ata_discord'),
    path('ata/steam/', views.CustomAuthToken.as_view(), name='ata_steam'),
    path('ata/guest/', views.CustomAuthToken.as_view(), name='ata_guest'),
    # CRUD for User and Doctor
    path('users/list/', views.CustomUserList.as_view()),
    path('users/create/', views.CustomUserCreate.as_view()),
    path('users/details/<int:pk>', views.CustomUserDetails.as_view()),
    path('doctors/list/', views.CustomDoctorList.as_view()),
    path('doctors/create/', views.CustomDoctorCreate.as_view()),
    path('doctors/details/<int:pk>', views.CustomDoctorDetails.as_view()),
    path('users/details/ata/', views.CustomUserDetails.as_view()),
    # Get Categories (Professions/Fields)
    path('system/categories/list/', views.CategoryList.as_view()),
    path('system/categories/details/<int:sysid>', views.CategoryDetails.as_view()),
    path('categories/details/<int:pk>', views.CategoryDetails.as_view()),
    # Get Doctors of a Field
    path('categories/doctors/<int:cid>', views.CategoryDetails.as_view()),
    # Get Fields of a Doctor
    path('categories/doctor/<int:did>', views.CategoryDetails.as_view()),
    # Chats
    path('chat/list/', views.ChatList.as_view()),
    path('chat/details/<int:pk>', views.ChatDetails.as_view()),
    # Messages & Attachments
    path('messages/list/', views.MessageList.as_view()),
    path('messages/details/<int:tid>', views.MessageDetails.as_view()),
    path('messages/details/attachment/list/', views.AttachmentList.as_view()),
    path('messages/details/attachment/<int:mid>', views.AttachmentDetails.as_view()),
    path('messages/details/<int:pk>', views.MessageDetails.as_view()),
    path('attach/details/<int:pk>', views.AttachmentDetails.as_view()),
    # find a doctors scheduling
    path('reservation-data/doctor/<int:did>', views.ReservationDataDetails.as_view()),
    # CRUD a reservation data
    path('reservation-data/list/', views.ReservationDataList.as_view()),
    # CRUD for category doctor management
    path('category-doctor/list/', views.CategoryDoctorList.as_view()),
    path('category-doctor/details/<int:pk>', views.CategoryDoctorDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)


