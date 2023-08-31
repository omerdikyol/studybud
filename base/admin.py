from django.contrib import admin

# Register your models here.

from .models import Room, Message, Topic, User

admin.site.register(User) # This will register the User model to the admin site
admin.site.register(Room) # This will register the Room model to the admin site
admin.site.register(Message) # This will register the Message model to the admin site
admin.site.register(Topic) # This will register the Topic model to the admin site