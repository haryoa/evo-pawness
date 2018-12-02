from copy import deepcopy

from reinforcement_learning_train.util.stacked_state import StackedState


class HelperTrainingExample:
    """
    Class that is used to collect the data from the MCTS simulation
    """
    def __init__(self, stacked_state, current_player, action_proba, reward=None):

        self.stacked_state = stacked_state
        self.current_player = current_player
        self.action_proba = action_proba
        self.reward = reward


def parse_global_list_training(global_list_training):
    """
    Parse the list of the object HelperTrainingExample that is ready
    to be input of the neural network ( as the targetted output )
    :param global_list_training: list object of HelperTrainingExample
    :return: list of state representation, list of action probability, reward
    """
    deep_repr_state = []
    action_proba = []
    reward = []

    for i in global_list_training:
        deep_repr_state.append(i.stacked_state.get_deep_representation_stack())
        action_proba.append(i.action_proba)
        reward.append(i.reward)

    return deep_repr_state, action_proba, reward

def mirror_stacked_state(stacked_state_orig):
    """
    Mirror all state in the stacked state
    :param stacked_state_orig: The Stacked State
    :return: the mirror of the Stacked State
    """
    from util.state_modifier_util import mirror_state
    copy_stacked:StackedState = deepcopy(stacked_state_orig)
    copy_stacked.deque_collection.clear()
    for state in stacked_state_orig.deque_collection:
        copy_stacked.append(mirror_state(state))
    return copy_stacked


def action_spaces_new(board_size = 9 ,max_step = 3):
    """
    Generator all possible actions in the game
    :return:
    """
    all_list_action = []

    for i in range(board_size):
        for j in range(board_size):
            # case of activate action
            # format activate input : a*<y coor>,<x coor>
            all_list_action.append("a*" + str(i) + ',' + str(j))

            # case of promote action
            # format activate input : p*<y coor>,<x coor>

            list_promote = ['K','R','B','Q']
            for promote in list_promote:
                promote_coor = "p*" + str(i) + ',' + str(j) + "*"
                promote_coor += promote
                all_list_action.append(promote_coor)


            # case of move and attack
            # Queen Move
            direction_move = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
            for dir_move in direction_move:
                for r in range(1,max_step+1):
                    dir_i = dir_move[0]*r
                    dir_j = dir_move[1]*r
                    move_coor = "mp*{},{}*{},{}".format(i,j,dir_i,dir_j)
                    all_list_action.append(move_coor)

            # Knight move
            direction_move = [(1,-2),(1,2),(-2,1),(2,1),(-1,-2),(-1,2), (-2,-1), (2,-1)]
            for dir_move in direction_move:
                dir_i = dir_move[0]
                dir_j = dir_move[1]
                move_coor = "mp*{},{}*{},{}".format(i,j,dir_i,dir_j)
                all_list_action.append(move_coor)

    all_list_action.append('skip')
    return all_list_action



