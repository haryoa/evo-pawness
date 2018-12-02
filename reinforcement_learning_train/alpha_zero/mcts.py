from numpy.core.multiarray import ndarray

from ai_modules.ai_elements import AIElements
from copy import deepcopy
import random
import numpy as np

from config import AlphaZeroConfig
from reinforcement_learning_train.util.alphazero_util import mirror_stacked_state
from reinforcement_learning_train.util.stacked_state import StackedState


class NodeMCTS():
    """
        Node in the tree
    """
    def __init__(self, stacked_state, parent=None, root=False, maximizer=0):
        self.stacked_state:StackedState = stacked_state
        self.num_state = 0
        self.parent = parent
        self.q_state_action = {}  # action : q
        self.num_state_action = {}
        self.selected_action = None  # For backfill
        self.p_state = None  # Array that has len(all_list_possible_action)
        self.child = []
        self.edge_action = {}
        self.is_terminal = False
        self.v = 0  # Init
        self.root = root
        self.maximizer = maximizer

    def expand_node(self, model_deep_net, player_color, label_encoder,
                    epsilon=AlphaZeroConfig.MCTS_EPSILON,
                    alpha_diri=AlphaZeroConfig.MCTS_ALPHA_DIRICHLET,
                    cpuct=AlphaZeroConfig.MCTS_PUCT,
                    greed_attack = False):
        """
        This function contains 2 steps on the MCTS.
        Select and Expand & Evaluate
        :param model_deep_net: The neural network model
        :param player_color: why did I include this???
        :param label_encoder: The encoder used to encode the action key
        :param epsilon: hyperparameter for using the dirichlet random proba
        :param alpha_diri: hyperparameter of dirichlet
        :param cpuct: hyperparameter of the MCTS in alpha zero
        :param greed_attack: HACK! the agent will prioritize attacking and promoting
        :return:
        """
        terminal = AIElements.is_over(self.stacked_state.head)
        self.is_terminal = terminal
        if not terminal:
            possible_action = AIElements.get_possible_action(self.stacked_state.head)
            possible_action_keys = list(possible_action.keys())

            if self.p_state is None:
                """
                    Expand and Evaluate goes here!
                """
                if self.stacked_state.head.get_player_turn() == self.maximizer:
                    state_stack_representation = np.array([self.stacked_state.get_deep_representation_stack()])
                else:
                    state_stack_representation = mirror_stacked_state(self.stacked_state)
                    state_stack_representation = np.array([state_stack_representation.get_deep_representation_stack()])

                self.p_state, self.v = model_deep_net.predict(state_stack_representation)
                self.v_ = self.v[0][0]
                self.v = self.v[0][0]
                self.p_state = self.p_state[0]

                if self.stacked_state.head.get_player_turn() != self.maximizer:
                    self.p_state = label_encoder.array_mirrored(self.p_state)
                possible_action_ohe = label_encoder.transform(possible_action_keys).sum(axis=0)
                self.p_state *= possible_action_ohe
                sum_policy_state = np.sum(self.p_state)
                if sum_policy_state > 0:
                    ## normalize to sum 1
                    self.p_state /= sum_policy_state
                else:
                    print("All valid moves were masked, do workaround.")
                    self.p_state += possible_action_ohe
                    self.p_state /= np.sum(self.p_state)

                # Initialize num and q
                for action in possible_action_keys:
                    self.num_state_action[action] = 0
                    self.q_state_action[action] = 0
                    next_state = AIElements.result_function(self.stacked_state.head, possible_action[action])
                    new_stacked_state = deepcopy(self.stacked_state)
                    new_stacked_state.append(next_state)
                    if action not in self.edge_action:
                        self.edge_action[action] = NodeMCTS(new_stacked_state, parent=self, root=False)

            else:
                """
                    Select goes here
                """
                best_action = ""
                best_upper_confidence = -float('inf')

                dirchlet_prob = np.random.dirichlet([alpha_diri] * len(possible_action_keys))
                counter_loop = 0

                # Randomize possible_action_keys
                random.shuffle(possible_action_keys)
                for action in possible_action_keys:
                    # Get the index of the action
                    index_action = label_encoder.le.transform([action])[0]
                    q_state_action_val = 0
                    num_state_action_val = 0
                    if action in self.q_state_action and action in self.num_state_action:
                        q_state_action_val = self.q_state_action[action]
                        num_state_action_val = self.num_state_action[action]
                    if self.root:
                        upper_confidence = q_state_action_val + \
                                           cpuct * ((1 - epsilon) * self.p_state[index_action] + epsilon * dirchlet_prob[
                            counter_loop]) * \
                                           np.sqrt(self.num_state) / (1 + num_state_action_val)


                    else:
                        upper_confidence = q_state_action_val + \
                                           cpuct * self.p_state[index_action] * \
                                           np.sqrt(self.num_state) / (1 + num_state_action_val)
                    if greed_attack and possible_action[action]['action'] == 'attack':
                        upper_confidence += AlphaZeroConfig.Q_ATTACK_GREEDY # Higher Chance to Attack
                    if greed_attack and possible_action[action]['action'] == 'promote':
                        upper_confidence += AlphaZeroConfig.Q_PROMOTE_GREEDY # Higher Chance to promote
                    counter_loop += 1
                    if best_upper_confidence < upper_confidence:
                        best_upper_confidence = upper_confidence
                        best_action = action

                        # Expand the node and check if this node is terminal

                        next_state = AIElements.result_function(self.stacked_state.head, possible_action[action])
                        new_stacked_state = deepcopy(self.stacked_state)
                        new_stacked_state.append(next_state)
                        if action not in self.edge_action:
                            self.edge_action[action] = NodeMCTS(new_stacked_state, parent=self, root=False)

                self.selected_action = best_action

        else:
            self.v = self.stacked_state.head.sparse_eval(self.stacked_state.head.get_player_turn())

    def backfill(self):
        """
            Called if the terminal state is reached.
            Update all parents parameters.
            This is the Backup Step
        """
        current_node = self
        while current_node.parent is not None:
            parent_node = current_node.parent
            parent_selected_action = parent_node.selected_action
            if parent_selected_action in parent_node.q_state_action:
                parent_node.q_state_action[parent_selected_action] = (-current_node.v + parent_node.num_state_action[
                    parent_selected_action] * parent_node.q_state_action[
                                                                          parent_selected_action]) / \
                                                                     (parent_node.num_state_action[
                                                                          parent_selected_action] + 1)
                parent_node.num_state_action[parent_selected_action] += 1

            else:  # First Time
                parent_node.q_state_action[parent_selected_action] = -current_node.v
                parent_node.num_state_action[parent_selected_action] = 1
            parent_node.num_state += 1
            parent_node.v = -current_node.v
            current_node = parent_node


class MCTreeSearch():
    """
        Class for simulating the MCTS
    """
    def __init__(self, model_deep_net, cpuct, number_of_simulation, label_encoder, init_state_stack):
        self.model_deep_net = model_deep_net
        self.root = NodeMCTS(init_state_stack, root=True)
        self.number_of_simulation = number_of_simulation
        self.cpuct = cpuct
        self.label_encoder = label_encoder

    def self_play(self, greed_attack = False):
        """
        Simulate the MCTS until the defined number of simulation
        :param greed_attack:
        :return:
        """
        for i in range(self.number_of_simulation):
            node_check = self.root
            current_player = node_check.stacked_state.head.get_player_turn()
            end_loop = False
            while not end_loop:
                if node_check.p_state is None:
                    # Select and backup
                    node_check.expand_node(self.model_deep_net, current_player, self.label_encoder, cpuct=self.cpuct, greed_attack=greed_attack)
                    node_check.backfill()
                    end_loop = True
                else:
                    # Expand and Evaluate
                    node_check.expand_node(self.model_deep_net, current_player, self.label_encoder, cpuct=self.cpuct, greed_attack=greed_attack)
                    node_check = node_check.edge_action[node_check.selected_action]
        print("Simulation End, num of simulation = %d" % (self.number_of_simulation))

    def get_action_proba(self, temperature=1):
        """
        Get the probability distribution of the action on the current root based on the
        temperature.
        :param temperature: used on controlling the probability of actions.
        :return:
        """
        counts = [self.root.num_state_action[action] if action
                in self.root.num_state_action else 0 for action in
                  self.label_encoder.le.classes_]
        if temperature == 0:
            best_action = np.argmax(counts)
            probability = [0] * len(counts)
            probability[best_action] = 1
            return probability

        if sum(counts) == 0:
            return [0] * len(counts)

        counts = [x ** (1. / temperature) for x in counts]
        probability = [x / float(sum(counts)) for x in counts]  # Normalize
        return probability

    def update_root(self, action_key):
        """
        Update the root based on the action key. The action key must be present
        in the edge of the current root.
        :param action_key:
        :return:
        """
        self.root:NodeMCTS = self.root.edge_action[action_key]
        self.root.root = True
        self.root.parent = None  # omitted

    def is_terminal(self):
        """
        Check whether the root is already terminal
        :return:
        """
        return self.root.is_terminal
