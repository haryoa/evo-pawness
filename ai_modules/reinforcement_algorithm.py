from reinforcement_learning_train.alpha_zero.deep_net_architecture import PawnNetZero
from reinforcement_learning_train.alpha_zero.mcts import MCTreeSearch
from reinforcement_learning_train.util.action_encoder import ActionEncoder
from reinforcement_learning_train.util.stacked_state import StackedState
from keras.models import load_model
from reinforcement_learning_train.util.alphazero_util import action_spaces_new
from copy import deepcopy
from config import AlphaZeroConfig
class AlphaZeroAgent:
    """
        AlphaZero agent. The agent uses AlphaZero algorithm which uses Monte Carlo Tree Search
    """
    def __init__(self,
                 init_state,
                 max_simulation=AlphaZeroConfig.MAX_SIMULATION_AGENT,
                 MODEL_PATH=AlphaZeroConfig.DEFAULT_MODEL_AGENT):
        """
        Contructor of AlphaZero Agent
        :param init_state: the initial state of the game. It will be used continuously
        :param max_simulation: MCTS max simulation
        :param MODEL_PATH: Model Path used for AlphaZero Agent
        """
        self.max_simulation = max_simulation
        all_action_spaces = action_spaces_new()
        self.ae = ActionEncoder()
        self.ae.fit(list_all_action=all_action_spaces)
        self.stacked_state = StackedState(init_state)
        self.deepnet_model = PawnNetZero(len(all_action_spaces))
        self.deepnet_model.model = load_model(MODEL_PATH)
        self.mcts = MCTreeSearch(self.deepnet_model.model, 1, self.max_simulation, self.ae, self.stacked_state)

    def enemy_turn_action(self, action_key, new_state):
        """
        Must be used in the enemy's turn.
        It will update the root of the MCTS to match the state of the game.

        TODO: do result function in this method
        :param action_key: Action of the opponent
        :param new_state: The new state that is the result of enemy's action
        :return:
        """
        self.mcts.self_play()
        self.stacked_state.append(deepcopy(new_state))
        self.mcts.update_root(action_key)

    def choose_action(self, state):
        """
        Predict the move using AlphaZero algorithm

        Parameters
        ----------
        state : State
            unused. The purpose of this parameter is to match the other class.
        float, str:
            The evaluation or utility and the action key name
        """
        from ai_modules.ai_elements import AIElements
        import numpy as np
        self.mcts.self_play()
        action_proba = np.array(self.mcts.get_action_proba(temperature=0))
        action = np.random.choice(len(action_proba), p=action_proba)
        action_key = self.ae.inverse_transform([action])[0]
        possible_action = AIElements.get_possible_action(self.stacked_state.head)
        from ai_modules.ai_elements import AIElements
        new_state = AIElements.result_function(self.stacked_state.head, possible_action[action_key])
        self.stacked_state.append(new_state)
        self.mcts.update_root(action_key)
        return (action_key, possible_action[action_key])