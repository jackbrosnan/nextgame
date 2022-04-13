from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import GameList, Game

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LikedGamesForm(forms.ModelForm):
    class Meta:
        model = GameList
        fields = ('liked_game',)

        labels = {
            'liked_game': 'Add Games:',
        }
        widgets = {
            'liked_game': forms.TextInput(attrs={'class': 'form-control autocomplete-input', 'form': 'game-form', 'placeholder': 'Search for Game...',}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

