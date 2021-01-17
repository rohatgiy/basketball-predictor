import tensorflow as tf
from tensorflow import keras
from model import get_odds_loaded
import h5py


def getResults(team1, team2):
    new_model = keras.models.load_model("probaball_model.h5")
    return get_odds_loaded(new_model, team1, team2)