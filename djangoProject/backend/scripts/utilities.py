import pickle
from itertools import groupby
import pandas as pd

"""
Function that reads in a pickled file and stores it in the variable data
:param filename: Name of the file (str)
:returns: data variable (Any type)
"""
def read_pickle_file(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    
    return data

def serialize(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

"""
Function that returns a sorted list of tuples based on the score (at 1th index)
:param game_ids: List of Game IDs & Scores as tuples where 0th index is the Game ID and 1th index is the score (aesthetic score)
:returns: Sorted list of tuples (Game ID, Score) with duplicates reduced
"""
def reduce_dupe(game_ids):
    game_ids.sort(key=lambda item: item[0])
    
    groups = groupby(game_ids, lambda item: item[0])

    reduced_scores_t = []

    for game_id, grouptuples in groups:
        current_scores = [item[1] for item in grouptuples]
        reduced_score = sum(current_scores) // len(current_scores)

        reduced_scores_t.append((game_id, reduced_score))
    
    reduced_scores_t.sort(key=lambda item: item[1])

    return reduced_scores_t

"""
Function that returns all of the associated Image IDs for a given Game ID
:param game_id: Game ID (int)
:param path: there to allow unittest to access the DataFrame df
:returns: Image IDs (list)
"""
def get_image_ids(game_id:int, path=None):
    if path == None:
        path = '../djangoProject/backend/data/dataset.pkl'
    df = pd.read_pickle(path)
    rows = df.loc[df['Game ID'] == game_id, 'Image IDs']
    
    return rows.values.tolist()

# All current genres in our database of games
all_genres = ['Adventure', 'Arcade', 'Card_BoardGame', 'Fighting', 'HackandSlash_Beatemup', 'Indie', 'MOBA', 'Music', 'Pinball', 'Platform', 'Point-and-click', 'Puzzle', 'Quiz_Trivia', 'Racing', 'RealTimeStrategy(RTS)', 'Role-playing(RPG)', 'Shooter', 'Simulator', 'Sport', 'Strategy', 'Tactical', 'Turn-basedstrategy(TBS)', 'VisualNovel']

"""
Function that returns the index at which the genre occurs in the all_genres list
:param genre: genre (str)
:returns: index at which genre is found (int)
"""
def find_genre_index(genre):
    return all_genres.index(genre)

"""
Function that returns a list of the genre tags associated with the given Game ID
:param game_id: Game ID (int)
:param path: there to allow unittest to access the DataFrame df
:returns: list of genres [str_1, str_2, ..., etc]
"""
def get_genres(game_id, path=None):
    if path == None:
        path = '../djangoProject/backend/data/dataset.pkl'
    df = read_pickle_file(path)

    genre_str = df.loc[df['Game ID'] == game_id, 'Labels'].iloc[0]
    genres = genre_str.split(' ')

    return genres

"""
Function that returns the individual weightings of genres, as a list of tuples (weight, Genre Index),
given the cummulative list of genres collected from the user's liked games
The weight calculation: (number of time the genre occurs in this cummulative list divided by the total length of that cummulative list)
:param genre: Genres List (list)
:returns: List of Tuples of the form: (weight, Genre Index)
"""
def get_weights(genres):
    total_genres = len(genres)
    norm_genres = list(set(genres))

    weights = [(genres.count(genre) / total_genres, find_genre_index(genre)) for genre in norm_genres]

    return weights