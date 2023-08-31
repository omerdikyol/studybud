from django.shortcuts import render, redirect # This will allow us to render html files and redirect to other pages
from django.http import HttpResponse # This will allow us to return an http response
from django.contrib.auth.decorators import login_required # This will make it so that you have to be logged in to view the page
from django.contrib.auth.models import User # This will allow us to use the User model
from django.contrib import messages # This will allow us to send messages to the user
from django.contrib.auth import authenticate, login, logout # This will allow us to authenticate, login, and logout users
from django.contrib.auth.forms import UserCreationForm # This will allow us to use the UserCreationForm form (for registration)
from django.db.models import Q # This will allow us to use the Q object to search for rooms by topic name or room name or room description
from .models import Room, Topic, Message # This will allow us to use the Room and Topic models
from .forms import RoomForm, UserForm # This will allow us to use the RoomForm and UserForm forms

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn Python!'},
#     {'id': 2, 'name': 'Design with me!'},
#     {'id': 3, 'name': 'FrontEnd Dev'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated: # This will make it so that if the user is already logged in, they will be redirected to the home page    
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')
        

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    form = UserCreationForm() # This will create a form with the fields username, password1, and password2

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # This will create the user but not save it to the database yet  
            user.username = user.username.lower() # This will make the username lowercase
            user.save() # This will save the user to the database

            login(request, user) # This will log the user in after they register
            return redirect('home')
        
        else:
            messages.error(request, 'An error has occurred during registration')
        
    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    #rooms = Room.objects.all() # This will get all the rooms from the database | Model name - Model objects attribute - method (all, get, filter, exclude)
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )  # Filter rooms by the topic name or room name or room description
    
    topics = Topic.objects.all()[:5]
    
    room_count = rooms.count() # This will count the number of rooms
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) # This will get all the messages from the rooms filtered by the topic name or room name or room description

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk): # pk is the primary key of the room (from the url.py file)
    room = Room.objects.get(id=pk) # This will get the room with the id of pk
    room_messages = room.message_set.all().order_by('-created') # This will get all the messages from the room and order them by the most recent
    participants = room.participants.all()

    if request.method == "POST": # if user sends a message
        message = request.POST.get('body') # This will get the message from the form
        Message.objects.create(
            user=request.user,
            room=room,
            body=message
        )
        room.participants.add(request.user) # This will add the user to the room participants
        return redirect('room', pk=room.id) # This will redirect the user to the same room after they send a message

    context = {'room': room,'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() # room_set: This will get all the rooms created by the user
    room_messages = user.message_set.all() # message_set: This will get all the messages sent by the user
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login') # This will make it so that you have to be logged in to view the page
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) # This will get the topic from the database or create it if it doesn't exist

        Room.objects.create( # This will create the room and save it to the database
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    
        # Old approach (user cannot create a topic)
        # form = RoomForm(request.POST) # This will get the data from the form
        # if form.is_valid():
        #     room = form.save(commit=False) # This will create the room but not save it to the database yet
        #     room.host = request.user # This will make the user the host of the room
        #     room.save() # This will save the room to the database
            # return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)
    

@login_required(login_url='login') # This will make it so that you have to be logged in to view the page
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # This will prefill the form with the room data

    if request.user != room.host: # This will make it so that only the host of the room can update the room
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) # This will get the topic from the database or create it if it doesn't exist
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('home')

        # Old approach (user cannot create a topic)
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        #     return redirect('home')
        
    context = {'form': form, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login') # This will make it so that you have to be logged in to view the page
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
        
    context = {'obj': room}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login') # This will make it so that you have to be logged in to view the page
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    
    if request.method == "POST":
        message.delete()
        return redirect('home')
    
    context = {'obj': message}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login') # This will make it so that you have to be logged in to view the page
def updateUser(request):
    user = request.user
    form = UserForm(instance=user) # This will prefill the form with the user data
    context = {'form': form}

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update_user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})