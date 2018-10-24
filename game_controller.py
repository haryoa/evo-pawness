from model.state import State
from copy import deepcopy
import random
class AIElements:
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

    def get_possible_action(state):
        """
        Get all possible action in the state
        ...

        Attributes
        ----------
        state : State
            A state that want to be searched about the possible action.

        Returns
        -------
        dict
            a concatenated all list of actions.
        """
        collected_action = state.get_possible_action_player() + state.get_possible_action_pawn() + state.get_possible_action_king()
        all_possible_action = AIElements._one_action(collected_action)
        if len(all_possible_action.keys()) == 0:
            return {'skip' : {'action': 'skip'}} # skip if no action is available
        return all_possible_action

    def result_function(state,action):
        """
        Get the result of action A in state S.

        ...

        Attributes
        ----------
        state : State
            a state S.
        action : dict
            a dict of an action A that want to be launched in the defined state

        Returns
        -------
        new_state : State
            a new state from the result of doing action A in state S.
        """
        new_state = deepcopy(state)
        if action['action'] == 'activate':
            pawn_index = action['pawn_index']
            player_color = action['player_index']
            new_state.activate_pawn(player_color,pawn_index)

        if action['action'] == 'promote':
            pawn_index = action['pawn_index']
            player_color = action['player_index']
            choice = action['promoted_choice']
            new_state.promote_pawn(player_color,pawn_index, choice)

        if action['action'] == 'move':
            pawn_index = action['pawn_index']
            player_color = action['player_index']
            x_end = action['x_end']
            y_end = action['y_end']
            new_state.move_pawn(pawn_index, player_color, x_end, y_end)

        if action['action'] == 'move':
            pawn_index = action['pawn_index']
            player_color = action['player_index']
            x_end = action['x_end']
            y_end = action['y_end']
            new_state.move_pawn(pawn_index, player_color, x_end, y_end)

        if action['action'] == 'attack':
            pawn_index = action['pawn_index']
            player_color = action['player_index']
            x_end = action['x_end']
            y_end = action['y_end']
            enemy_pawn_index = action['enemy_pawn_index']
            new_state.attack_pawn(pawn_index, enemy_pawn_index, player_color, x_end, y_end)
        new_state.change_turn()
        return new_state

    def get_state_dict(state):
        return state.get_dict_value_state()

    def get_players_mana(state):
        return state.get_players_mana()

    def debug_print_board(state):
        state.print_board()

    def get_rune_information(state):
        return state.get_rune_list()

    def is_over(state):
        """
        Terminal State.

        ...

        Attributes
        ----------
        state : State
            a state S.

        Returns
        -------
        end : bool
            Return true if the game has ended in the current state.
        """
        return state.is_terminal()

class GameController():
    """
    A class used to connect the view and the model. It will be used to be the
    input of our AI Algorithm
    """
    def __init__(self):
        self.state = State()
        self.state.initial_state()
        self.possible_action_keys = []
        self.two_players = False
        self.player_vs_ai_white = False

    def play_with_two_players_start(self):
        """
        Return the initial state

        Returns
        -------
        dict
            Dict of possible Action and state
        """
        returned_dict_info = {}
        self.state = State()
        self.state.initial_state()
        self.two_players = True
        state_dict = AIElements.get_state_dict(self.state)
        possible_action = AIElements.get_possible_action(self.state)
        self.possible_action_keys = possible_action.keys()
        return {"state": state_dict, "possible_action": possible_action, "task" : "CHANGE_PLAYER"}

    def play_with_ai_white(self, ai_agent='random'):
        """
        Returns
        -------
        dict
            Dict of possible action and state
        """
        returned_dict_info = {}
        self.state = State()
        self.state.initial_state()
        self.player_vs_ai_white = True
        state_dict = AIElements.get_state_dict(self.state)
        possible_action = AIElements.get_possible_action(self.state)
        self.possible_action_keys = possible_action.keys()
        self.ai_agent = GameAI(agent_type=ai_agent)
        return {"state": state_dict, "possible_action": possible_action, "task" : "CHANGE_PLAYER"}


    def receive_input_action_play(self, input_key, input_params):
        print(input_key)

        if input_key in self.possible_action_keys:
            self.state = AIElements.result_function(self.state, input_params)
            return True
        else:
            return False

    def get_whattodo_view(self):
        params_view_action = {}
        if AIElements.is_over(self.state):
            params_view_action['task'] = 'END_GAME'
            return params_view_action
        if self.two_players:
            params_view_action['task'] = 'CHANGE_PLAYER'
            params_view_action['state'] = AIElements.get_state_dict(self.state)
            possible_action = AIElements.get_possible_action(self.state)
            params_view_action['possible_action'] = possible_action
            self.possible_action_keys = possible_action.keys()
        if self.player_vs_ai_white:
            print("masuk")
            params_view_action['task'] = 'AI_MOVE'
            possible_action = AIElements.get_possible_action(self.state)
            ai_key_action, ai_action_params = self.ai_agent.choose_action(self.state, possible_action)
            previous_state = deepcopy(self.state)
            self.possible_action_keys = possible_action.keys()
            self.receive_input_action_play(ai_key_action, ai_action_params)
            if AIElements.is_over(self.state):
                params_view_action['end'] = True
                return

            state_dict = AIElements.get_state_dict(self.state)
            previous_state_dict = AIElements.get_state_dict(previous_state)
            possible_action = AIElements.get_possible_action(self.state)
            previous_mana = AIElements.get_players_mana(previous_state)
            params_view_action['state'] = state_dict
            params_view_action["prev_state"] = previous_state_dict
            params_view_action["ai_action"] = ai_action_params
            params_view_action["prev_mana"] = previous_mana
            params_view_action["possible_action"] = possible_action
            self.possible_action_keys = possible_action.keys()

        return params_view_action



class GameAI:
    def __init__(self, agent_type="random"):
        self.agent_type = agent_type

    def choose_action(self, state, list_action):
        """
        Parameters
        ----------
        list_action : dict
            List of action
        Returns
        --------
        (str,dict)
            return
        """
        if self.agent_type == "random":
            key_list_action = list_action.keys()
            print(key_list_action)
            rand_int = random.randint(0,len(key_list_action)-1)
            selected_key_action = list(key_list_action)[rand_int]
            return (selected_key_action,list_action[selected_key_action])
