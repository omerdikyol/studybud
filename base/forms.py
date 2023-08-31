from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        # fields = ['name', 'topic', 'description'] # This will only show the name, topic, and description fields in the form
        fields = '__all__' # This will show all the fields in the form
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']