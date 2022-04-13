import unittest

from scripts.utilities import *
import pandas as pd

class TestUtilities(unittest.TestCase):
    
    def test_read_pickle_file(self):
        self.assertIsInstance(read_pickle_file('./data/game_sim_map.pkl'), dict)
        self.assertIsInstance(read_pickle_file('./data/game_sim_map.pkl'), dict)
        self.assertIsInstance(read_pickle_file('./data/pc_vector_df.pkl'), pd.DataFrame)
        self.assertIsInstance(read_pickle_file('./data/dataset.pkl'), pd.DataFrame)
    
    def test_reduce_dupes(self):
        dummy_list_a = [(100, 35), (5, 19), (100, 55), (5, 31), (20, 50), (45, 90), (100, 30)]
        dummy_list_b = [(50, 10), (50, 40)]

        self.assertEqual(reduce_dupe(dummy_list_a), [(5, 25), (100, 40), (20, 50), (45, 90)])
        self.assertNotEqual(reduce_dupe(dummy_list_b), [(50, 50)]) # Expected: [(50, 25)]

    def test_get_image_ids(self):
        path = './data/dataset.pkl'
        expected_result = ['fnymr7nmagyhaycwkftg.jpg', 'mrhprawxqcaidwvhszch.jpg', 'sgbhfpclrk5udlowkpyq.jpg', 'u9m4lnfpkv3u9sh1ufsw.jpg', 'zeqv7lvh8aaemeaa2bhl.jpg']
        self.assertCountEqual(get_image_ids(4, path), expected_result)
    
    def test_find_genre_index(self):
        self.assertEqual(find_genre_index('Adventure'), 0)
        self.assertNotEqual(find_genre_index('Indie'), 10)
    
    def test_get_genres(self):
        path = './data/dataset.pkl'
        self.assertCountEqual(get_genres(4, path), ['Adventure', 'Shooter'])
    
    def test_get_weights(self):
        # Genre Idxs: [0, 1, 0, 9, 16]
        genres = ['Adventure', 'Arcade', 'Adventure', 'Platform', 'Shooter']
        expected_result = [(0.4, 0), (0.2, 1), (0.2, 16), (0.2, 9)]
        self.assertCountEqual(get_weights(genres), expected_result)
    
