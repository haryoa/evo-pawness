from collections import deque

from keras.models import load_model
from reinforcement_learning_train.alpha_zero.train_module import fit_train
from reinforcement_learning_train.util.action_encoder import ActionEncoder
from reinforcement_learning_train.alpha_zero.deep_net_architecture import PawnNet, PawnNetZero
from reinforcement_learning_train.util.alphazero_util import action_spaces, action_spaces_new
import pickle

def main():
    all_action_spaces = action_spaces_new()

    MODEL_PATH = "checkpoint.hdf5"
    BEST_MODEL = "checkpoint.hdf5"
    GLOBAL_LIST_TRAINING_PATH = "global_list_training.p"
    # Import Model
    deepnet_model = PawnNetZero(len(all_action_spaces))
    deepnet_model.model = load_model(MODEL_PATH)
    global_list_training = pickle.load( open(GLOBAL_LIST_TRAINING_PATH, "rb" ) )
    ae = ActionEncoder()
    ae.fit(list_all_action=all_action_spaces)
    fit_train(global_list_training, ae, deepnet_model, 91, 20)


if __name__ == '__main__':
    main()