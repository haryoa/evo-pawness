from ai_modules.ai_elements import AIElements
from copy import deepcopy

from ai_modules.classic_algorithm import RandomAgent
from model.state import State
from reinforcement_learning_train.util.stacked_state import StackedState


def reinforce_one_helper(state, action, player_color, agent_enemy):
    """
    Parameters
    ----------
    agent_enemy: GameAI
        enemy
    Returns
    -------
    new_state, reward, dead, state_old
    """
    # TODO handle selfplay
    middle_state = AIElements.result_function(state, action)

    if middle_state.is_terminal():
        return middle_state, AIElements.evaluation_function(middle_state, player_color), True, state
    # Opponent's move
    possible_action_new_state = AIElements.get_possible_action(middle_state)
    enemy_move, enemy_dict = agent_enemy.choose_action(middle_state)
    new_state = AIElements.result_function(middle_state, enemy_dict)

    if new_state.is_terminal():
        return new_state, AIElements.evaluation_function(new_state, player_color), True, state
    # Get the reward function
    return new_state, AIElements.reward_function(state, new_state, player_color), False, state

def _one_action(list_action):
    """
    Concatenate all list of actions to become one list

    ...

    Attributes
    ----------
    list_action : list
        a list of actions of Kings, Players, and Pawns

    Returns
    -------
    dict
        a concatenated all list of actions.
    """
    action_list_completed = {}
    for act in list_action:
        if 'action' in act and len(act['action']) > 0:
            for key,value in act['action'].items():
                action_list_completed[key] = value
    return action_list_completed

# Collect all elements
def get_possible_action_player(state):
    """
    Get all possible action of a player from this state

    TODO: fix the mess of inputting the dict.
    """
    possible_action = []

    # get player possible action
    player_possible_action = {}
    player = state.player_list[state.turn%2]
    player_string = "White Player" if player.color == 0 else "Black Player"
    player_possible_action["actor"] = player_string
    ref_pawn = state.white_pawn_list if player.color == 0 else state.black_pawn_list
    dict_action = {}
    p_moves = player.possible_move(ref_pawn)
    for move in p_moves:
        key_name = 'p' + str(player.color)
        action_type = move[0]
        pawn_index = move[1]
        if action_type == 'promote':
            key_name += 'p'
        else:
            key_name += 'a'

        key_name += str(pawn_index)
        action_params = {}
        targetted_pawn = ref_pawn[pawn_index]
        if not targetted_pawn.dead:
            action_params['pawn_hp'] = targetted_pawn.hp
            action_params['pawn_atk'] = targetted_pawn.atk
            action_params['pawn_step'] = targetted_pawn.step
            action_params['pawn_x'] = targetted_pawn.x
            action_params['pawn_y'] = targetted_pawn.y
            action_params['action'] = action_type
            action_params['pawn_index'] = pawn_index
            action_params['player_index'] = player.color
            if action_type == 'promote':
                promoted_choice = move[2]
                action_params['promoted_choice'] = promoted_choice
                key_name += promoted_choice[0]

            dict_action[key_name] = action_params
    player_possible_action["action"] = dict_action
    possible_action.append(deepcopy(player_possible_action))
    return possible_action

def get_possible_action_pawn(state):
    """
    Get all possible action of all pawns from this state

    TODO: fix the mess of inputting the dict.
    """
    possible_action = []
    pawn_possible_action = {}
    player = state.player_list[state.turn%2]
    ref_pawn = state.white_pawn_list if player.color == 0 else state.black_pawn_list

    for pawn in ref_pawn:
        if not pawn.dead:
            dict_action = {}
            possible_action_iter = pawn.possible_move()['possible']
            key_name_move_start = 'mp' + str(state.turn%2) + 'w' + str(pawn.pawn_index)
            key_name_atk_start = 'ap' + str(state.turn%2) + 'w' + str(pawn.pawn_index)
            counter_loop_moves = 0
            x_start = pawn.x
            y_start = pawn.y
            step = pawn.step
            for possible_moves in possible_action_iter:
                action_params = {}
                x_end = possible_moves[0]
                y_end = possible_moves[1]
                dir_index = possible_moves[2]
                counter_loop_moves += 1

                action_params = {
                    'player_index' : player.color,
                    'pawn_x' : x_start,
                    'actor' : pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index),
                    'pawn_y' : y_start,
                    'pawn_hp' : pawn.hp,
                    'pawn_atk' : pawn.atk,
                    'pawn_step' : pawn.step,
                    'x_end' : x_end,
                    'y_end' : y_end,
                    'dir_index' : dir_index,
                    'step' : step,
                    'pawn_index' : pawn.pawn_index,
                    'action' : "attack",
                }
                key_name_atk = key_name_atk_start + 'd' + str(dir_index)
                dict_action[key_name_atk] = deepcopy(action_params)
                action_params = {
                    'player_index' : player.color,
                    'pawn_x' : x_start,
                    'actor' : pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index),
                    'pawn_hp' : pawn.hp,
                    'pawn_atk' : pawn.atk,
                    'pawn_step' : pawn.step,
                    'pawn_y' : y_start,
                    'pawn_index' : pawn.pawn_index,
                    'x_end' : x_end,
                    'y_end' : y_end,
                    'dir_index' : dir_index,
                    'step' : step,
                    'action' : 'move'
                }
                key_name_move = key_name_move_start + 'd' + str(dir_index)
                dict_action[key_name_move] = deepcopy(action_params)

            pawn_possible_action['actor'] = pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index)
            pawn_possible_action['action'] = deepcopy(dict_action)
        possible_action.append(deepcopy(pawn_possible_action))
    return possible_action

def get_possible_action_king(state):
    """
    Get all possible action of a king from this state

    TODO: fix the mess of inputting the dict.
    """
    possible_action = []
    pawn_possible_action = {}
    player = state.player_list[state.turn%2]
    pawn = state.white_king if player.color == 0 else state.black_king

    if not pawn.dead:
        dict_action = {}
        possible_action_iter = pawn.possible_move()['possible']
        key_name_move_start = 'mp' + str(state.turn%2) + 'w' + str(pawn.pawn_index)
        key_name_atk_start = 'ap' + str(state.turn%2) + 'w' + str(pawn.pawn_index)
        counter_loop_moves = 0
        x_start = pawn.x
        y_start = pawn.y
        step = pawn.step
        for possible_moves in possible_action_iter:
            action_params = {}
            x_end = possible_moves[0]
            y_end = possible_moves[1]
            dir_index = possible_moves[2]
            counter_loop_moves += 1
                #pprint((x_end, y_end))


            action_params = {
                'player_index' : player.color,
                'pawn_x' : x_start,
                'actor' : pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index),
                'pawn_y' : y_start,
                'pawn_hp' : pawn.hp,
                'pawn_atk' : pawn.atk,
                'pawn_step' : pawn.step,
                'x_end' : x_end,
                'y_end' : y_end,
                'dir_index' : dir_index,
                'step' : step,
                'pawn_index' : pawn.pawn_index,
                'action' : "attack",
            }
            key_name_atk = key_name_atk_start + 'd' + str(dir_index)
            dict_action[key_name_atk] = deepcopy(action_params)

        pawn_possible_action['actor'] = pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index)
        pawn_possible_action['action'] = deepcopy(dict_action)
        possible_action.append(deepcopy(pawn_possible_action))
    return possible_action

class HelperTrainingExample:
    def __init__(self, stacked_state, current_player, action_proba, reward=None):
        self.stacked_state = stacked_state
        self.current_player = current_player
        self.action_proba = action_proba
        self.reward = reward


def parse_global_list_training(global_list_training):
    deep_repr_state = []
    action_proba = []
    reward = []

    for i in global_list_training:
        deep_repr_state.append(i.stacked_state.get_deep_representation_stack())
        action_proba.append(i.action_proba)
        reward.append(i.reward)

    return deep_repr_state, action_proba, reward

def mirror_stacked_state(stacked_state_orig):
    from util.state_modifier_util import mirror_state
    copy_stacked:StackedState = deepcopy(stacked_state_orig)
    from collections import deque
    copy_stacked.deque_collection.clear()
    for state in stacked_state_orig.deque_collection:
        copy_stacked.append(mirror_state(state))
    return copy_stacked

def action_spaces():
    """
    Generator
    """
    ai_enemy = RandomAgent(1, 1)

    all_of_list = []

    for i in range(2):
        state = State()
        state.initial_state()
        state_pawn_list = state.black_pawn_list
        if i == 0:
            possible_action_new_state = AIElements.get_possible_action(state)
            enemy_move,enemy_dict = ai_enemy.choose_action(state)
            state = AIElements.result_function(state, enemy_dict)
            state_pawn_list = state.white_pawn_list
        state.player_list[0].mana = 10
        state.player_list[1].mana = 10

        for x in state_pawn_list:
            x.status = False
        all_of_list += list(_one_action(get_possible_action_player(state)).keys())
        for x in state_pawn_list:
            x.status = True
        all_of_list += list(_one_action(get_possible_action_player(state)).keys())
        for m in range(len(state_pawn_list)):
             state_pawn_list[m] = state_pawn_list[m].promote('Rook')
        all_of_list += list(_one_action(get_possible_action_player(state)).keys())

        for n in range(len(state_pawn_list)):
            state_pawn_list[n] = state_pawn_list[n].promote('Queen')
            state_pawn_list[n].add_step(10)
        all_of_list += list(_one_action(get_possible_action_pawn(state)).keys())
        all_of_list += list(_one_action(get_possible_action_king(state)).keys())
        if i == 0:
            all_of_list += ['skip']
    return all_of_list

def action_spaces_new(board_size=9,max_step = 3):
    """
    Generator all items
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



