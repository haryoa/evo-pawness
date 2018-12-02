from ai_modules.reinforcement_algorithm import AlphaZeroAgent
from util.state_modifier_util import mirror_state
from model.state import State
from copy import deepcopy
from ai_modules.classic_algorithm import MinimaxABAgent, RandomAgent
from ai_modules.ai_elements import AIElements
from config import ControllerConfig
class GameController():
    """
    A class used to connect the view and the model.
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
        self.state = State()
        self.state.initial_state()
        self.two_players = True
        state_dict = AIElements.get_state_dict(self.state)
        possible_action = AIElements.get_possible_action(self.state)
        self.possible_action_keys = possible_action.keys()
        return {"state": state_dict, "possible_action": possible_action, "task" : "CHANGE_PLAYER"}

    def play_with_ai_white(self, ai_agent=ControllerConfig.AI_AGENT):
        """
        Returns
        -------
        dict
            Dict of possible action and state
        """
        self.state = State()
        self.state.initial_state()
        self.player_vs_ai_white = True
        state_dict = AIElements.get_state_dict(self.state)
        possible_action = AIElements.get_possible_action(self.state)
        self.possible_action_keys = possible_action.keys()

        if ai_agent == 'random':
            self.ai_agent = RandomAgent()
        elif ai_agent == 'minimaxab':
            self.ai_agent = MinimaxABAgent(player_color=0)
        elif ai_agent == 'azero':
            self.ai_agent = AlphaZeroAgent()

        self.old_state_reward = deepcopy(self.state)

        return {"state": state_dict, "possible_action": possible_action, "task" : "CHANGE_PLAYER"}

    def receive_input_action_play(self, input_key, input_params):
        """
        Process the input from the user in the view
        :param input_key: str, the key of the action
        :param input_params: dict, the parameter of the action
        :return: bool, tell that the action is present in the possible action
        """
        if input_key in self.possible_action_keys:
            self.state = AIElements.result_function(self.state, input_params)

            ## Useful for alpha zero only
            self.ai_agent.enemy_turn_action(input_key, input_params)

            index_player = (AIElements.get_player(self.state)+1)%2
            print("TURN %d" % (self.state.turn))
            print("The Evaluation of Player %d is %.2f" % (index_player, AIElements.evaluation_function(self.state, index_player)))
            return True
        else:
            return False

    def get_whattodo_view(self):
        """
        Give the view the dict that tell the possible action on this turn and the task
        that the view should do
        :return: dict
        """
        params_view_action = {}

        self.state.print_board()
        if AIElements.is_over(self.state):
            params_view_action['task'] = 'END_GAME'
            print("test")
            return params_view_action
        if self.two_players:
            params_view_action['task'] = 'CHANGE_PLAYER'
            params_view_action['state'] = AIElements.get_state_dict(self.state)
            possible_action = AIElements.get_possible_action(self.state)
            params_view_action['possible_action'] = possible_action
            self.possible_action_keys = possible_action.keys()
        if self.player_vs_ai_white:
            self.possible_action_keys = AIElements.get_possible_action(self.state).keys()
            params_view_action['task'] = 'AI_MOVE'
            ai_key_action, ai_action_params = self.ai_agent.choose_action(self.state)
            previous_state = deepcopy(self.state)
            self.receive_input_action_play(ai_key_action, ai_action_params)
            if AIElements.is_over(self.state):
                params_view_action['end'] = True
                params_view_action['task'] = 'END_GAME'
                return params_view_action
            print("Reward Function is %.2f" % (AIElements.reward_function(self.old_state_reward, self.state, 1))) #Black
            self.old_state_reward = deepcopy(self.state)
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
