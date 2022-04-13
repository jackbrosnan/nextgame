from backend.scripts.utilities import read_pickle_file, get_genres, get_weights, find_genre_index

class GameSimilarityInfo():

    def __init__(self):
        self.game_map = read_pickle_file('../djangoProject/backend/data/game_sim_map.pkl')

    """
    Function that returns the most similar games in terms of aesthetics given a user's list of liked games
    """
    def find_similar_games(self, liked_games, limit=None):
        temp = []

        for game in liked_games:
            if game in self.game_map:
                temp.append(self.game_map[game])
            else:
                print(f"Game: {game} does not have any similarities computed!")  

        most_similar_games = sorted([item for sublist in temp for item in sublist], key=lambda item: item[1])

        # Limit ensures that we are getting the top 20% of games (ranked by their aesthetic value)
        if limit == None:
            limit = len(most_similar_games) // 5

        return most_similar_games[:limit]
    
    """
    Function that takes in the most similar games (aesthetics wise)
    This function ranks the list of similar games based on how closely the genre of those games matches the user's liked game's genres
    Returns a more refined list of recommended games (in Game_ID form)
    """
    def get_recommendations(self, user_liked_games, no_of_recommendations=5):
        most_similar_games = self.find_similar_games(user_liked_games)

        temp = [get_genres(game_id) for game_id in user_liked_games]
        genre_list = [item for sublist in temp for item in sublist]
        weights = get_weights(genre_list)

        recommended_games = []
        for game_id, score in most_similar_games:
            genres_arr = get_genres(game_id)
            genres_arr_indx = [find_genre_index(genre) for genre in genres_arr]

            rele_weights = [item[0] for item in weights if item[1] in genres_arr_indx]
            total_weight = sum(rele_weights)
            modified_score = score * total_weight

            recommended_games.append((game_id, (score - modified_score)))
        
        recommended_games.sort(key=lambda item: item[1])

        recommended_game_ids = [item[0] for item in recommended_games]

        return recommended_game_ids[:no_of_recommendations]
