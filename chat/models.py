from django.db import models

# Create your models here.

from django.db import models

class User(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100,default='')

class Room(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200,default='')
    participants = models.ManyToManyField(User)
    extra = models.JSONField(max_length=100,default={},null=True)

class Message(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField()
    extra = models.JSONField(max_length=100,default={},null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
