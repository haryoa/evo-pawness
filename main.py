# from view.game_view import GameViewCLI
import sys, getopt
import argparse

def main_CLI_GUI():
    """
    Currently unusable
    TODO : Fix CLI
    :return:
    """
    # GameViewCLI().start_game_2_experimental_()
    raise NotImplementedError

def main_alpha_zero_train():
    """
    Main option to train the alpha zero model from start
    :return:
    """
    import tensorflow as tf
    from keras.backend.tensorflow_backend import set_session
    from reinforcement_learning_train.alpha_zero.train_module import fit_train
    from reinforcement_learning_train.util.action_encoder import ActionEncoder
    from reinforcement_learning_train.alpha_zero.deep_net_architecture import PawnNet, PawnNetZero
    from reinforcement_learning_train.util.alphazero_util import action_spaces_new
    from collections import deque

    # config = tf.ConfigProto()
    # config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
    # config.log_device_placement = True  # to log device placement (on which device the operation ran)
    # # (nothing gets printed in Jupyter, only if you run it standalone)
    # sess = tf.Session(config=config)
    # set_session(sess)  # set this TensorFlow session as the default session for Keras
    all_action_spaces = action_spaces_new()

    deepnet_model = PawnNetZero(len(all_action_spaces))
    global_list_training = deque(maxlen=9000)
    ae = ActionEncoder()
    ae.fit(list_all_action=all_action_spaces)
    print(deepnet_model.model.summary())
    fit_train(global_list_training,ae, deepnet_model)
    deepnet_model.model.save("best_model.hdf5")

def main_alpha_zero_train_continue():
    """
    Main option to play to continue training the model of alpha zero
    :return:
    """
    from collections import deque

    from keras.models import load_model
    from reinforcement_learning_train.alpha_zero.train_module import fit_train
    from reinforcement_learning_train.util.action_encoder import ActionEncoder
    from reinforcement_learning_train.alpha_zero.deep_net_architecture import PawnNet, PawnNetZero
    from reinforcement_learning_train.util.alphazero_util import action_spaces_new
    import pickle

    # config = tf.ConfigProto()
    # config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
    # config.log_device_placement = True  # to log device placement (on which device the operation ran)
    # # (nothing gets printed in Jupyter, only if you run it standalone)
    # sess = tf.Session(config=config)
    # set_session(sess)  # set this TensorFlow session as the default session for Keras
    all_action_spaces = action_spaces_new()

    MODEL_PATH = "checkpoint.hdf5"
    BEST_MODEL = "best_model.hdf5"
    GLOBAL_LIST_TRAINING_PATH = "global_list_training.p"
    # Import Model
    deepnet_model = PawnNetZero(len(all_action_spaces))
    deepnet_model.model = load_model(MODEL_PATH)
    best_model = load_model(BEST_MODEL)
    global_list_training = pickle.load(open(GLOBAL_LIST_TRAINING_PATH, "rb"))
    print("GLOBAL LIST SHAPE : {}".format(len(global_list_training)))
    ae = ActionEncoder()
    ae.fit(list_all_action=all_action_spaces)
    fit_train(global_list_training, ae, deepnet_model, best_model=best_model)

def main_play_gui():
    """
    Option for playing the game with GUI
    :return:
    """
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    sys.exit(app.exec_())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evo Pawness (Temporary Name) command line usage.')

    parser.add_argument('command', help='{play, train} . If play, use optional args -p.'
                                        'if train, use -azt or -aztc')
    parser.add_argument('-azt', '--alpha_zero_train',
                        action='store_true',
                        help='Train the model of alpha zero from start')
    parser.add_argument('-aztc', '--alpha_zero_train_continue',
                        action='store_true',
                        help='Continue to train the model of alpha zero from checkpoint')
    parser.add_argument('-p', '--play', nargs=1,
                        help='Play with the interface with an option. '
                             'Currently, only {GUI} is supported.',
                        metavar=('interface'),
                        default=('GUI'))
    if len(sys.argv) < 2:
        print('See the usage below:')
        parser.print_help()
        sys.exit(2)
    else:
        namespace_arguments = parser.parse_args()
        if namespace_arguments.command == 'train':
            if namespace_arguments.alpha_zero_train:
                main_alpha_zero_train()
            elif namespace_arguments.alpha_zero_train_continue:
                main_alpha_zero_train_continue()
            else:
                print("Please use -azt or -aztc as the optional arguments")
                sys.exit(2)
        elif namespace_arguments.command == 'play':
            interface_game = namespace_arguments.play[0]
            main_play_gui()




