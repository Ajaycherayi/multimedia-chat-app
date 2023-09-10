from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.JoinRoom.as_view(),name="home"),
    path('chatroom/<slug:user>/',views.ChatRoomView.as_view(),name='chatroom_view'),
    path('chatroom/<slug:user>/update_last_view_message/',views.ManageRoom.update_last_view_message,name='update_last_room_message'),
    path('chatroom/<slug:user>/send_message/',views.ManageChat.insert_message,name='send_message'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)