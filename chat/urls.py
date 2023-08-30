from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.JoinRoom.as_view(),name="home"),
    path("chat/",views.ChatView.as_view(),name="chat"),
    path("chat/",views.ChatView.as_view(),name="chat")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)