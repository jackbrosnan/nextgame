from django.contrib import admin
from .models import Game, GameList
from .forms import *


# Register your models here.

admin.site.register(Game)
admin.site.register(GameList)