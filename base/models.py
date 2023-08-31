from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    # description =
    updated = models.DateTimeField(auto_now=True) # Takes a snapshot of the time when the model is updated
    created = models.DateTimeField(auto_now_add=True) # Initial time when the model is createdp

    def __str__(self):
        return self.name

class Room(models.Model):
    # id is automatically created 
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # This will delete all the rooms created by the user when the user is deleted
    topic = models.ForeignKey(Topic, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True) # Difference of blank and null = blank is for form validation, null is for database validation
    participants = models.ManyToManyField(User, related_name='participants', blank=True) # This will allow us to add participants to the room
    updated = models.DateTimeField(auto_now=True) # Takes a snapshot of the time when the model is updated
    created = models.DateTimeField(auto_now_add=True) # Initial time when the model is createdp

    class Meta:
        ordering = ['-updated', '-created'] # This will order the rooms by the updated and created fields in descending order

    def __str__(self):
        return self.name
        

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ForeignKey is a one to many relationship
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # This will delete all the messages in the room when the room is deleted 
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) # Takes a snapshot of the time when the model is updated
    created = models.DateTimeField(auto_now_add=True) # Initial time when the model is createdp

    def __str__(self):
        return self.body[0:50] # This will return the first 50 characters of the message body
    

    class Meta:
        ordering = ['-updated', '-created'] # This will order the rooms by the updated and created fields in descending order