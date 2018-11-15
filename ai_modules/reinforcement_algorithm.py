from reinforcement_learning_train.alpha_zero.deep_net_architecture import PawnNetZero
from reinforcement_learning_train.alpha_zero.mcts import MCTreeSearch
from reinforcement_learning_train.util.action_encoder import ActionEncoder
from reinforcement_learning_train.util.stacked_state import StackedState
from keras.models import load_model
from reinforcement_learning_train.util.alphazero_util import action_spaces, action_spaces_new
from copy import deepcopy

class AlphaZeroAgent:
    """
        Minimax agent
    """
    def __init__(self,init_state, player_color, max_simulation=20):
        """
        Initiation

        Parameters
        ----------
        max_depth : int
            The max depth of the tree

        player_color : int
            The player's index as MAX in minimax algorithm
        """
        MODEL_PATH = "checkpoint.hdf5"
        self.max_simulation = max_simulation
        self.player_color = player_color
        all_action_spaces = action_spaces_new()
        self.ae = ActionEncoder()
        self.ae.fit(list_all_action=all_action_spaces)
        self.stacked_state = StackedState(init_state)
        self.deepnet_model = PawnNetZero(len(all_action_spaces))
        self.deepnet_model.model = load_model(MODEL_PATH)
        self.mcts = MCTreeSearch(self.deepnet_model.model, 1, self.max_simulation, self.ae, self.stacked_state)

    def enemy_turn_action(self, action_key, new_state):
        self.mcts.self_play_till_leaf()
        self.stacked_state.append(deepcopy(new_state))
        self.mcts.update_root(action_key)

    def choose_action(self, state):
        """
        Predict the move using minimax algorithm

        Parameters
        ----------
        state : State

        Returns
        -------
        float, str:
            The evaluation or utility and the action key name
        """
        from ai_modules.ai_elements import AIElements
        import numpy as np
        self.mcts.self_play_till_leaf()
        action_proba = np.array(self.mcts.get_action_proba())
        action = np.random.choice(len(action_proba), p=action_proba)
        action_key = self.ae.inverse_transform([action])[0]
        possible_action = AIElements.get_possible_action(self.stacked_state.head)
        from ai_modules.ai_elements import AIElements
        new_state = AIElements.result_function(self.stacked_state.head, possible_action[action_key])
        self.stacked_state.append(new_state)
        self.mcts.update_root(action_key)
        return (action_key, possible_action[action_key])