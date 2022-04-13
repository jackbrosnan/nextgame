from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from .models import GameList, Game
from .forms import LikedGamesForm, RegisterForm
import json
# Create your tests here.


# Testing forms
class TestForms(TestCase):

    def test_valid_form(self):
        form = LikedGamesForm(data={
            'liked_game': 16,
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = LikedGamesForm(data={
            'liked_game': '',
        })
        self.assertFalse(form.is_valid())

    def test_valid_registration_form(self):
        form = RegisterForm(data={
            'email': 'jack@mail.dcu.ie',
            'username': 'Testuser',
            'password1': 'Testpword',
            'password2': 'Testpword',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_password_registration_form(self):
        form = RegisterForm(data={
            'email': 'jack@mail.dcu.ie',
            'username': 'Testuser',
            'password1': 'Testpword',
            'password2': 'Testpword-not-same',
        })
        form_invalid_email = RegisterForm(data={
            'email': 'jack.mail.dcu',
            'username': 'Testuser',
            'password1': 'Testpword',
            'password2': 'Testpword',
        })
        self.assertFalse(form.is_valid())
        self.assertFalse(form_invalid_email.is_valid())

    def test_empty_form(self):
        form = RegisterForm(data={
            'email': '',
            'username': '',
            'password1': '',
            'password2': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

# class ModelTest(TestCase):
#
#     def test_game(self):
#         game1 = Game.objects.filter(id=4).values_list('id', flat=True)
#         self.assertEqual(game1, 4)

class ViewsTest(TestCase):

    def test_project_home(self):
        client = self.client.get('http://127.0.0.1:8000/home/', follow=True)
        self.assertEquals(client.status_code, 200)
        self.assertTemplateUsed(client, 'main/index.html')