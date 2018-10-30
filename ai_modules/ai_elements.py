from model.state import State
from copy import deepcopy
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

    def evaluation_function(state, player_color):
        """
        Attributes
        ----------
        state : State
            a state S.
        player_color : int
            a dict of an action A that want to be launched in the defined state
        """
        return state.total_eval(player_color)

    def get_player(state):
        """
        Attributes
        ----------
        state : State
            a state S.
        """
        return state.turn % 2

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

    ## state
    ## possible -> action
    ## result_fuction -> state'
    ## possible -> action
    ## get_opponent_action(state') -> state''
    ## reward_func(state, state', state'')
    ## state'' - state'
    ## 0.5, 0.8, 1
    def reward_function(old_state, new_state, player_color, middle_state = None):
        '''
        Current Formula : old_state_evaluation_function - new_state_evaluation_function
        Parameters
        ----------
        old_state: State
            the state
        new_state: State
            next state
        player_color: int
            player_color
        '''
        return new_state.total_eval(player_color) - old_state.total_eval(player_color)

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
