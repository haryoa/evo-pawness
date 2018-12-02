from ai_modules.ai_elements import AIElements
from copy import deepcopy
from collections import deque
import numpy as np

from config import StackedStateConfig
from model.pawn import KnightPawn, RookPawn, BishopPawn, SoldierPawn, QueenPawn, King
from model.state import State

class StackedState:
    """
    Class for stacking the state at desired time steps.
    It will be changed into the representation used for the input of neural network.
    It can be used to be input of an CNN layer.
    It will be used as an input of any Reinforcement Learning Algorithm
    """

    def __init__(self, state,
                 max_len=StackedStateConfig.MAX_TIME_STEPS,
                 max_features=28):
        """

        :param state: the initial state
        :param max_len: timesteps and the maximum length of the deque
        :param max_features: The number of plane for representating a state.
            Since there are max_len states. It will be multiplied by max_len
        """
        self.deque_collection = deque(maxlen=max_len)
        self.planes_total = max_features * max_len
        self.max_features = max_features
        self.deque_collection.append(state)
        self.head = state
        self.max_len = max_len

    def get_deep_representation_stack(self):
        """
        The representation of state to be input of the deep learning
        For more details, see my medium post (Part 3)
        :return: the state representation
        """
        input_network = np.zeros((9, 9, self.planes_total))
        counter_iter = self.max_len - len(self.deque_collection)
        for state in reversed(self.deque_collection):
            planes_index = counter_iter * self.max_features
            counter_iter += 1
            all_pawn_list = state.white_pawn_list + state.black_pawn_list + [state.white_king, state.black_king]
            possible_action = AIElements.get_possible_action(state)
            all_rune_list = state.rune_list
            input_network[0, 4, planes_index + 22] = state.turn % 5
            input_network[4, 4, planes_index + 23] = state.turn % 5
            input_network[8, 4, planes_index + 24] = state.turn % 5

            for rune in all_rune_list:
                input_network[rune.x,rune.y, planes_index + 25] = 1
            for i in possible_action:
                if i != 'skip':
                    possible_action_dict = possible_action[i]
                    # player_index = possible_action_dict['player_index']
                    x = possible_action_dict['pawn_x']
                    y = possible_action_dict['pawn_y']
                    if 'player' in possible_action_dict:
                        index_color = possible_action_dict['player']
                        input_network[x, y, planes_index + 26 + index_color] += 1
                    if 'player_index' in possible_action_dict:
                        index_color = possible_action_dict['player_index']
                        input_network[x, y, planes_index + 26 + index_color] += 1
            for pawn in all_pawn_list:
                x, y = pawn.x, pawn.y
                player_mana = pawn.player.mana
                if not pawn.dead:
                    index_color = 0 if pawn.player.color == 0 else 1

                    pawn_hp = pawn.hp
                    input_network[x, y, planes_index + index_color + 0] = pawn_hp

                    pawn_atk = pawn.atk
                    input_network[x, y, planes_index + index_color + 2] = pawn_atk

                    pawn_step = pawn.step
                    input_network[x, y, planes_index + index_color + 4] = pawn_step

                    input_network[x, y, planes_index + index_color + 6] = 1 # location pawn
                    if isinstance(pawn, KnightPawn):
                        input_network[x, y, planes_index + index_color + 8] = 1
                    elif isinstance(pawn, RookPawn):
                        input_network[x, y, planes_index + index_color + 10] = 1
                    elif isinstance(pawn, BishopPawn):
                        input_network[x, y, planes_index + index_color + 12] = 1
                    elif isinstance(pawn, SoldierPawn):
                        input_network[x, y, planes_index + index_color + 14] = 1
                    elif isinstance(pawn, QueenPawn):
                        input_network[x, y, planes_index + index_color + 16] = 1
                    elif isinstance(pawn, King):
                        input_network[x, y, planes_index + index_color + 18] = 1
                    input_network[x, y, planes_index + index_color + 20] = player_mana
        return input_network

    def append(self, state):
        """
        Append a new state into the data structure deque
        :param state: state that want to be appended
        :return:
        """
        self.deque_collection.append(deepcopy(state))
        self.head = deepcopy(state)

    def mirror_stacked_state(self):
        """
        Mirror all of the state in the deque
        :return:
        """
        from util.state_modifier_util import mirror_state
        copy_stacked = deepcopy(self)
        new_deque = deque(maxlen=self.max_len)
        for state in copy_stacked.deque_collection:
            new_deque.append(mirror_state(state))
            print(mirror_state(state).turn)
        copy_stacked.deque_collection = new_deque
        print(copy_stacked.deque_collection[0].turn)
        return copy_stacked


    def __repr__(self):
        returned_string = ""
        for state in self.deque_collection:
            returned_string += state.__repr__() + " then "
        return returned_string
