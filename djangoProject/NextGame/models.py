from django.db import models
from django.contrib.auth.models import User

PLAT_CHOICES = [
    ('PlayStation 3', 'Playstation 3'),
    ('PlayStation 4', 'Playstation 4'),
    ('PlayStation 5', 'Playstation 5'),
    ('PC (Microsoft Windows)', 'PC'),
    ('Xbox 360', 'Xbox 360'),
    ('Xbox One', 'Xbox One'),
    ('Nintendo Switch', 'Nintendo Switch'),
]

class Game(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    title = models.TextField(db_column='Title', blank=True, null=True)
    genres = models.TextField(db_column='Genres', null=True, blank=True)
    age_rating = models.TextField(db_column='Age Rating', blank=True, null=True)
    platforms = models.TextField(db_column='Platforms', blank=True, null=True)
    summary = models.TextField(db_column='Summary', blank=True, null=True)
    player_persp = models.TextField(db_column='Player Perspective', blank=True, null=True)
    release_date = models.TextField(db_column='Release Date', blank=True, null=True)
    images = models.TextField(db_column='images', blank=True, null=True)
    cover = models.TextField(db_column='CoverID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'games'

    def __str__(self):
        return self.title

class GameList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gamelist")
    name = models.CharField(max_length=200)
    liked_game = models.CharField(max_length=100, db_column='liked_game', null=True)


    class Meta:
        managed = False
        db_table = 'game_list'

    def __str__(self):
        return self.name