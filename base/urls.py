from django.urls import path
from . import views

# we need to add the paths of the functions we created in views.py

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('', views.home, name='home'), # We put name= because even if we change the url, the name will stay the same and we can use it in the html files
    path('room/<str:pk>', views.room, name='room'), # <str:pk> is a path converter that takes a string and assigns it to the variable pk
    path('profile/<str:pk>', views.userProfile, name='user-profile'),

    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),

    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),

    path('update-user/', views.updateUser, name='update-user'),

    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity')
]