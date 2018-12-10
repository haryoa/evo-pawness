class AlphaZeroConfig:
    """
    A static class that contains most of the configuration for AlphaZero Algorithm.
    You can edit the configuration here.
    """

    """
    Config for AlphaZero Agent in the ai_modules.reinforcement_algorithm module
    """
    # The default model used in the Evo Pawness Game. It can contains absolute path
    DEFAULT_MODEL_AGENT = 'best_model.hdf5'

    # Maximum of MCTS simulation
    MAX_SIMULATION_AGENT = 20

    """
    Config for training the model of AlphaZero
    """
    # Path of the best model. Can contain absolute path.
    BEST_MODEL_PATH = "best_model.hdf5"

    # Path of the current model or the checkpoint. Can contain absolute path.
    CURRENT_MODEL_PATH = "checkpoint.hdf5"

    # Number of episodes to train the model
    EPISODE = 100

    # Number of simulations of the MCTS
    MCTS_SIMULATION = 25

    # Maximum of the number of episodes used to do "greedy" mode. 0 If you
    # do not want it.
    GREEDY_EPISODE = 0.125 * EPISODE

    # Batch size on fitting the neural network model
    BATCH_SIZE_FIT = 32

    # Number of epochs to fit the neural network model
    EPOCHS_FIT = 11

    # Below is the configuration of the hyperparameter of the neuralnetwork
    FILTERS_CNN_RESIDUAL = 199
    KERNEL_SIZE_RESIDUAL = (4,4)
    NUMBER_OF_RESIDUAL = 4
    LEARNING_RATE = 0.001

    VALUE_HEAD_FILTER_CNN = 1
    VALUE_HEAD_KERNEL_SIZE = (1,1)
    VALUE_HEAD_DENSE_UNITS = 180

    POLICY_HEAD_FILTER_CNN = 2
    POLICY_HEAD_KERNEL_SIZE = (1,1)
    # end of the hyperparameter of the neural network

    # Number of round in the arena
    ROUND_ARENA = 3

    # Max turn of the arena. It will be concluded as draw if the turn has reached it.
    MAX_TURN_ARENA = 200

    # The MCTS simulation in the arena
    MAX_SIMULATION_ARENA = 25

    # The difference of the win of the current model must be higher than WIN_DIFFERENCE_ARENA * best_model win
    WIN_DIFFERENCE_ARENA = 1.5

    # The maximum turn to make the temperature to 1
    TEMPERATURE_END_STEP = 31

    # The number of minimum turn in each episode to do the greedy mode.
    GREEDY_TURN_MIN = 50

    # The maximum of simulation of MCTS on training the model
    MAX_TURN_SIMULATION = 250

    # Hyperparameter of MCTS
    MCTS_EPSILON = 0.25
    MCTS_ALPHA_DIRICHLET = 0.3
    MCTS_PUCT = 1

    # Increase the Q of action attack when in 'greedy' mode
    Q_ATTACK_GREEDY = 0.6

    # Increase the Q of action attack when in 'promote' mode
    Q_PROMOTE_GREEDY = 0.5

class StackedStateConfig:
    """
    A static class that contains most of the configuration for the Stacked State.
    You can edit the configuration here
    """

    # Maximum of time steps of the stacked state
    MAX_TIME_STEPS = 5

class MinimaxABConfig:
    """
        A static class that contains most of the configuration for Minimax AB Prunning Algorithm.
        You can edit the configuration here.
    """
    MAX_DEPTH = 3

class ControllerConfig:
    """
        A static class that contains most of the configuration for the controller
        You can edit the configuration here.
    """

    # The default agent as the white player.
    # The viable option : {'minimaxab','azero','random'}
    # Note if you use 'azero', it's untested.  Of course, you need the model
    AI_AGENT = 'minimaxab'
