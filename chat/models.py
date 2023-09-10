from django.db import models

# Create your models here.

from django.db import models
from django.contrib.postgres.fields import JSONField

class User(models.Model):
    name = models.CharField(max_length=100,default='')

class Room(models.Model):
    name         = models.CharField(max_length=200,default='')
    extra        = JSONField(default=dict, blank=True, null=True)
    participants = models.ManyToManyField(User)

class Message(models.Model):
    room      = models.ForeignKey(Room, on_delete=models.CASCADE)
    extra     = JSONField(default=dict, blank=True, null=True)
    sender    = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # viewed_by = models.ManyToManyField(User, related_name='viewed_messages', blank=True)

class Documents(models.Model):
    document = models.CharField(max_length=255,default='', null=True)
    created  = models.DateTimeField(auto_now_add=True)
    message  = models.TextField(max_length=255, blank=True, null=True)
    status   = models.IntegerField(default=0,null=True)
    room     = models.ForeignKey(Room, on_delete=models.CASCADE)
    extra    = JSONField(default=dict, blank=True, null=True)

class LastMessage(models.Model):
    room     = models.ForeignKey(Room, on_delete=models.CASCADE)
    message  = models.IntegerField(default=0,null=True, blank=True)

class LastSeenMessage(models.Model):
    room     = models.ForeignKey(Room, on_delete=models.CASCADE)
    user     = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message  = models.IntegerField(default=0,null=True, blank=True)
class RoomSession(models.Model):
    room     = models.ForeignKey(Room, on_delete=models.CASCADE)
    user     = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    extra    = JSONField(default=dict, blank=True, null=True)