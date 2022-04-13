# Generated by Django 4.0.2 on 2022-04-08 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, db_column='Title', null=True)),
                ('genres', models.TextField(blank=True, db_column='Genres', null=True)),
                ('age_rating', models.TextField(blank=True, db_column='Age Rating', null=True)),
                ('platforms', models.TextField(blank=True, db_column='Platforms', null=True)),
                ('summary', models.TextField(blank=True, db_column='Summary', null=True)),
                ('player_persp', models.TextField(blank=True, db_column='Player Perspective', null=True)),
                ('release_date', models.TextField(blank=True, db_column='Release Date', null=True)),
                ('images', models.TextField(blank=True, db_column='images', null=True)),
                ('cover', models.TextField(blank=True, db_column='CoverID', null=True)),
            ],
            options={
                'db_table': 'games',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GameList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('liked_game', models.CharField(db_column='liked_game', max_length=100, null=True)),
            ],
            options={
                'db_table': 'game_list',
                'managed': False,
            },
        ),
    ]