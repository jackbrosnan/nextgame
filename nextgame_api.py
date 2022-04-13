import json
from operator import index
import os
from sqlalchemy import create_engine, update, func, delete, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from nextgame_orm import *
import os
import pandas
import csv

WAREHOUSE_DB_USER = "postgres"
WAREHOUSE_DB_PASS = "root"
WAREHOUSE_DB_HOST = "localhost"
WAREHOUSE_DB_PORT = "5432"
WAREHOUSE_DB = "NextGame"

conn_string = 'postgresql://{}:{}@{}:{}/{}'.format(WAREHOUSE_DB_USER, WAREHOUSE_DB_PASS, WAREHOUSE_DB_HOST,
                                                   WAREHOUSE_DB_PORT, WAREHOUSE_DB)

engine = create_engine(conn_string)
connection = engine.connect()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
'''
new_game = Game(igdb_id=1, Title="test", Genres="Shooter", age_rating="18", platforms="PC", Summary="This is a test")
session.add(new_game)
'''


def delete_rows():
    session.query(Game) \
        .delete(synchronize_session=False)
    session.commit()


def add_games():
    with open('game_info_v2.csv', encoding='utf-8') as data_file:
        x = csv.reader(data_file)
        next(x)
        for row in x:
            # ['Game ID', 'name', 'genre', 'modes', 'platform', 'release_date', 'summary', coverID]
            igdb_id = row[0]
            title = row[1]
            genres = row[2]
            modes = row[3]
            platform = row[4]
            release_date = row[5]
            summary = row[6]
            image_list = get_id_images(int(igdb_id))
            coverID = row[7]

            if title != "":
                new_game = Game(id=int(igdb_id), Title=title, Genres=genres, player_persp=modes, platforms=platform,
                                release_date=release_date, Summary=summary, images=image_list, cover=coverID)
                session.add(new_game)
        session.commit()


def get_id_images(id):
    # put into database location of images
    dir = os.listdir(r"D:\4th yr project\NextGame\downloaded_images")
    image_list = [''] * 5
    for game in dir:
        game_id = game.split('_')[-1]

        if int(game_id) == id:
            for i,image in enumerate(os.listdir(fr"D:\4th yr project\NextGame\downloaded_images\{game}")):
                image_list[i] = image
    return image_list


add_games()