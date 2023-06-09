from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('ata/', obtain_auth_token, name='ata'),
    path('ata/google/',  views.CustomAuthToken.as_view(), name='ata_google'),
    path('ata/discord/', views.CustomAuthToken.as_view(), name='ata_discord'),
    path('ata/steam/', views.CustomAuthToken.as_view(), name='ata_steam'),
    path('ata/guest/', views.CustomAuthToken.as_view(), name='ata_guest'),

    path('users/list/', views.CustomUserList.as_view()),
    path('users/create/', views.CustomUserCreate.as_view()),
    path('users/details/<int:pk>', views.CustomUserDetails.as_view()),
    path('users/details/<str:steamhex>', views.CustomUserDetails.as_view()),
    path('users/details/ata/', views.CustomUserDetails.as_view()),
    path('users/details/tickets/<int:uid>', views.TicketDetails.as_view()),

    path('systems/list/', views.SystemList.as_view()),
    path('systems/details/<int:pk>', views.SystemDetails.as_view()),
    path('systems/details/referral/<str:refferal>/<int:uid>', views.SystemDetails.as_view()),
    path('systems/details/referral/<str:refferal>', views.SystemDetails.as_view()),
    path('systems/details/user/<int:uid>', views.SystemDetails.as_view()),
    path('systems/details/users/<int:sysid>', views.SystemDetails.as_view()),
    path('systems/details/users/withroles/<int:sysid>', views.SystemDetails.as_view()),
    path('systems/details/tickets/<int:sysid>', views.TicketDetails.as_view()),
    path('system/categories/list/', views.CategoryList.as_view()),
    path('system/categories/details/<int:sysid>', views.CategoryDetails.as_view()),
    path('system/predefinedmsg/<int:sysid>', views.PredefinedMessageDetails.as_view()),

    path('categories/details/<int:pk>', views.CategoryDetails.as_view()),
    path('categories/defaultmessage/<int:cid>', views.MessageDetails.as_view()),

    path('roles/list/', views.RoleList.as_view()),
    path('roles/details/<int:pk>', views.RoleDetails.as_view()),
    path('roles/details/<int:sysid>/<int:uid>', views.RoleDetails.as_view()),
    path('roles/details/system/<int:sysid>', views.RoleDetails.as_view()),
    path('roles/details/delete/<int:sysid>/<int:uid>/<int:rid>', views.RoleDetails.as_view()),
    path('roles/details/delete/<int:sysid>/<int:rid>', views.RoleDetails.as_view()),
    path('roles/details/deleteallroles/<int:sysid>/<int:uid>', views.RoleDetails.as_view()),

    path('tickets/list/', views.TicketList.as_view()),
    path('tickets/details/<int:pk>', views.TicketDetails.as_view()),
    path('tickets/roles/list/', views.TicketRoleList.as_view()),
    path('tickets/roles/details/<int:tid>', views.TicketRoleDetails.as_view()),
    path('ticketsroles/details/<int:pk>', views.TicketRoleDetails.as_view()),
    path('tickets/add/<int:tid>/<int:uid>', views.TicketRoleDetails.as_view()),
    path('tickets/roles/ticketowner/<int:tid>', views.TicketRoleDetails.as_view()),
    path('tickets/messages/list/', views.MessageList.as_view()),
    path('tickets/messages/details/<int:tid>', views.MessageDetails.as_view()),
    path('tickets/send/defaultmessage/', views.MessageList.as_view()),

    path('tickets/messages/details/attachment/list/', views.AttachmentList.as_view()),
    path('tickets/messages/details/attachment/<int:mid>', views.AttachmentDetails.as_view()),

    path('messages/details/<int:pk>', views.MessageDetails.as_view()),

    path('attach/details/<int:pk>', views.AttachmentDetails.as_view()),

    path('category/role/list/', views.CategoryRoleList.as_view()),
    path('category/role/details/<int:pk>', views.CategoryRoleDetails.as_view()),
    path('category/role/delete/<int:cat>', views.CategoryRoleDetails.as_view()),
    path('category/role/user/<int:uid>/<int:sysid>', views.CategoryRoleDetails.as_view()),

    path('predefinedmsg/list/', views.PredefinedMessageList.as_view()),
    path('predefinedmsg/details/<int:pk>', views.PredefinedMessageDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)


