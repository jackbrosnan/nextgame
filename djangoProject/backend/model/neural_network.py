from fastai.vision.all import *
from fastcore import *
from torch import *
from annoy import AnnoyIndex
from backend.scripts.utilities import get_image_ids, reduce_dupe, serialize

import pandas as pd
import numpy as np

IMAGES_PATH = '../data/images'

"""
The following Classes & Functions were written with the help of:
FastAI Multi Category: https://colab.research.google.com/github/fastai/fastbook/blob/master/06_multicat.ipynb#scrollTo=SBpuzDroPkiY
Python Image Similarity w/ FastAI & ANNOY: https://towardsdatascience.com/similar-images-recommendations-using-fastai-and-annoy-16d6ceb3b809
"""

# NeuralNetwork Class that can be trained on a dataset of images
class NeuralNetwork():

    def __init__(self, df):
        self.df = df
        self.learner = None
        self.model = None
    

    # Trains the NeuralNetwork's CNN Learner 
    def train(self, epochs=4):
        _, dls = createDataLoader(self.df, splitter=splitter)
        self.learner = cnn_learner(dls, resnet50, metrics=partial(accuracy_multi, thresh=0.2))
        self.learner.fine_tune(3, base_lr=3e-3, freeze_epochs=epochs)

    # Exports the CNN Learner
    def export_learner(self):
        if self.learner == None:
            print(f'There is no model to export')
        else:
            self.learner.export('../data/model.pkl')
    
    # Imports a CNN Learner
    def import_learner(self, path_to_model):
        if self.learner == None & path_to_model != '':
            self.learner = load_learner(path_to_model)
            self.learner.to('cuda') # When a learner is exported it is saved as CPU
        else:
            print(f'A model already exists: {self.learner}')
    
    # Gets the output of the second last fully connected layer
    def get_linear_out_layer(self):
        return get_named_module_from_model(self.model, '1.4')
    
    """
    Using the second last fully connected layer
    we extract the feature vectors of each image which is stored in a (512, 1) Tensor Array
    These feature vectors are then stored in a Map:
        Image ID -> Feature Vector
    """
    def extract_feature_vectors(self, inf_dls, datablock):
        self.model = init_model(self.learner)
        
        batches = next(iter(datablock))
        img_repr_map = {}
        linear_out_layer = self.get_linear_out_layer()

        with Hook(linear_out_layer, get_output, True, True) as hook:
            
            for i, (xb, _) in enumerate(batches):
                bs = xb.shape[0]
                img_ids = inf_dls.items[i*bs : (i+1)*bs]['Image IDs']
                result = self.model.eval()(xb)
                img_reprs = hook.stored.cpu().numpy()
                img_reprs = img_reprs.reshape(bs, -1)

                for img_id, img_repr in zip(img_ids, img_reprs):
                    img_repr_map[img_id] = img_repr
        
        return img_repr_map

"""
Function that Splits Dataset into two lists of row indexes as integers
:param df: Pandas DataFrame
:returns: Two lists of row indexes as integers, one for the training split and the other for the validation split

"""
def splitter(df):
    train = df.index[~df['is_valid']].tolist()
    valid = df.index[df['is_valid']].tolist()
    return train, valid

"""
Function that returns the Path object for a specific DataFrame row
:param r: Pandas DataFrame row
:returns: Path object to the Image ID
"""
def get_x(r):
    return Path(f"{IMAGES_PATH}\{r['Image IDs']}")

"""
Function that returns the list of genres for a specific DataFrame row
:param r: Pandas DataFrame row
:returns: Genres of the specific Image ID
"""
def get_y(r):
    return r['Labels'].split(' ')

"""
Function that returns the list of genres for a specific DataFrame row
:param inp: Tensor Array containing values from an activation layer 
:param targ: Tensor Array which contains target indexes corresponding to each genre in our Dataset
:param thresh: Float that allows us to set any value less than thresh to 0 and any value greater than thresh to 1
:param sigmoid: Bool set to True by default
:returns: A value from 0 to 1 depending on wheter it passes the threshold value or not
"""
def accuracy_multi(inp, targ, thresh=0.5, sigmoid=True):
    if sigmoid:
        inp = inp.sigmoid()
    return ((inp>thresh) == targ.bool()).float().mean()

"""
Function that initialises the model object of the NeuralNetwork
which contains information of all of the layers of our NeuralNetwork
:param learner: CNN Learner
:returns: model
"""
def init_model(learner):
    model = learner.model
    model.to('cuda')
    return model

"""
Function that creates a DataLoader
which contains information of all of the layers of our NeuralNetwork
:param learner: DataFrame to be split up into a DataBlock and loaded onto a DataLoader
:param splitter: Any splitter function, if None use default Splitter Function
:param bs: int
:returns: DataBlock (dblock) and DataLoader (dls)
"""
def createDataLoader(df, splitter=None, bs=32):
    if splitter == None:
        splitter = RandomSplitter(0, seed=1)
    
    dblock = DataBlock(blocks=(ImageBlock, MultiCategoryBlock), splitter=splitter, get_x=get_x, get_y=get_y, item_tfms=RandomResizedCrop(128, min_scale=0.35))
    dls = dblock.dataloaders(df, bs=bs)

    return dblock, dls

"""
Hook Class which is able to hook into our NeuralNetwork and extract the 
feature vectors at a particular layer in our NeuralNetwork
"""
class Hook():
    "Create a hook on 'm' with 'hook_func' "
    def __init__(self, m:nn.Module, hook_func, is_forward:bool=True, detach:bool=True):
        self.hook_func,self.detach,self.stored = hook_func,detach,None
        f = m.register_forward_hook if is_forward else m.register_backward_hook
        self.hook = f(self.hook_fn)
        self.removed = False
    
    def hook_fn(self, module:nn.Module, input:torch.Tensor , output:torch.Tensor):
        "Applies 'hook_func' to 'module', 'input', 'output' "
        if self.detach:
            input  = (o.detach() for o in input ) if is_listy(input ) else input.detach()
            output = (o.detach() for o in output) if is_listy(output) else output.detach()
        self.stored = self.hook_func(module, input, output)
    
    def remove(self):
        "Remove the hook from the model."
        if not self.removed:
            self.hook.remove()
            self.removed=True

def get_output(module, input_value, output):
    return output.flatten(1)

def get_input(module, input_value, output):
    return list(input_value)[0]


def get_named_module_from_model(model, name):
    "Given a model, return the specified layer (name)"
    for n, m in model.named_modules():
        if n == name:
            return m
    return None

"""
Function that constructs our Annoy (Spotify's Approximate Nearest Neighbour algorithm) Tree given a DataFrame
:param df: DataFrame that contains the Feature Vectors
:returns: Annoy Tree
"""
def construct_annoy_tree(df):
    f = len(df['img_repr'][0])
    t = AnnoyIndex(f, metric='euclidean')

    for i, vector in enumerate(df['img_repr']):
        t.add(i, vector)
        t.build(23) # Number of unique genres we have in our dataset
    
    return t

# Given a specific Image Index, for the given DataFrame, get the similar images for that Base Image
def get_similar_images_annoy(df, tree, img_index, total_images=21):
    base_img_id, base_vector, base_label = df.iloc[img_index, [0, 1, 2]]
    similar_img_ids, similarity_distance = tree.get_nns_by_item(img_index, total_images, include_distances=True)
    return base_img_id, base_label, df.iloc[similar_img_ids[1:]], similarity_distance[1:]

"""
Function that constructs a mapping of Image -> Image similarities
:param df: DataFrame that contains the Feature Vectors
:param tree: Annoy Tree
:param total_img_ids: int, total amount of image_ids we will be creating mappings for
:returns: dict of Image -> Image similarities
"""
def build_image_sim_map(df, tree, total_img_ids):
    image_sim_map = {}

    for i in range(total_img_ids):
        base_image, _, similar_images_df, sim_distances = get_similar_images_annoy(df, tree, i)
        image_sim_map[base_image] = list(zip(similar_images_df['Game ID'], similar_images_df['Image IDs'], sim_distances))
    
    return image_sim_map

"""
Function that constructs a mapping of Game -> Game similarities
This is done by taking all of the Image IDs associated with each Game ID
and aggregating + sorting the scores
:param image_sim_map: dict, Map of Image -> Image similarities
:param game_ids: list of unique Game IDs
:returns: dict of Game -> Game similarities
"""
def construct_game_sim_map(image_sim_map, game_ids):
    d = {}
    for game_id in game_ids:
        img_ids = get_image_ids(game_id)

        temp_scores = []
        for img_id in img_ids:
            for game, _, score in image_sim_map[img_id]:
                temp_scores.append((game, score))

        reduced_scores = reduce_dupe(temp_scores)
        d[game_id] = reduced_scores

    return d

def main():

    # Path to Dataset containing information about each Image in the Dataset
    pickle_file_path = '../data/dataset.pkl'

    df = pd.read_pickle(pickle_file_path)

    # Init our NeuralNetwork
    nn = NeuralNetwork(df)

    # Train and Export our NeuralNetwork
    nn.train()
    nn.export_learner()

    # Constructing new datablock for feature extraction by getting 70% of images contained within whole dataset of images
    subset_df = df.loc[df['is_valid'] != True].reset_index(drop=True)
    subset_df = subset_df.drop(labels=['is_valid', 'Game ID'], axis=1)

    # Creating an Image Feature Vectors Map of each individual Image ID and their corresponding Feature Vectors
    dblock_inf, inf_dls = createDataLoader(subset_df)
    img_feature_map = nn.extract_feature_vectors(inf_dls, dblock_inf)
    
    # Storing this Image Feature Vectors Map inside a DataFrame
    temp_df = pd.DataFrame(img_feature_map.items(), columns=['Image IDs', 'img_repr'])
    img_feature_df = temp_df.merge(df.drop_duplicates(), on=['Image IDs'], how='left').drop(columns='is_valid')
    img_feature_df = img_feature_df.reindex(columns=['Image IDs', 'img_repr', 'Labels', 'Game ID'])

    # Pickling the Image Features DataFrame
    img_feature_df.to_pickle('../data/pc_vector_df.pkl')

    # Constructing the ANNOY Tree to be used for getting the similarity score between images
    annoy_t = construct_annoy_tree(img_feature_df)
    total_img_ids = img_feature_df.shape[0]
    image_sim_map = build_image_sim_map(img_feature_df, annoy_t, total_img_ids)

    # Pickling the Image Similarity Map
    serialize('../data/image_sim_map.pkl', image_sim_map)

    # Building the mapping of Game -> Game Similarities
    game_ids = img_feature_df['Game ID'].unique().tolist()
    game_id_sim_map = construct_game_sim_map(image_sim_map, game_ids)

    # Pickling the Game Similarity Map
    serialize('../data/game_sim_map.pkl', game_id_sim_map)

if __name__ == '__main__':
    main()