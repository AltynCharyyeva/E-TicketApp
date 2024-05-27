from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from mainapp import models

class VenueForm(forms.ModelForm):
    class Meta:
        model = models.Venue
        fields = ['name', 'address', 'map_location']


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']