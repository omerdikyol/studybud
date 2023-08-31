from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm # This will allow us to use the UserCreationForm form (for registration)


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        # fields = ['name', 'topic', 'description'] # This will only show the name, topic, and description fields in the form
        fields = '__all__' # This will show all the fields in the form
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']