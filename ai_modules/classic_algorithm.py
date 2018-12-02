from random import shuffle
from model.state import State
from ai_modules.ai_elements import AIElements
import time
import random
from config import MinimaxABConfig
class MinimaxAgent:
    """
        Minimax agent
    """
    def __init__(self, max_depth, player_color):
        """
        Initiation

        Parameters
        ----------
        max_depth : int
            The max depth of the tree

        player_color : int
            The player's index as MAX in minimax algorithm
        """
        self.max_depth = max_depth
        self.player_color = player_color
        self.node_expanded = 0

    def enemy_turn_action(self, action_key, new_state):
        """
        Nothing to do here
        """
        pass

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
        self.node_expanded = 0
        print("MINIMAX : Wait AI is choosing")
        start_time = time.time()
        list_action = AIElements.get_possible_action(state)
        eval_score, selected_key_action = self._minimax(0,state,True)
        print("MINIMAX : Done, eval = %d, expanded %d" % (eval_score, self.node_expanded))
        print("--- %s seconds ---" % (time.time() - start_time))
        return (selected_key_action,list_action[selected_key_action])

    def _minimax(self, current_depth, state, is_max_turn):
        """
        Minimax Helper
        :param current_depth: the current tree depth in the recursion
        :param state: the current state in the tree node
        :param is_max_turn: bool check the current's node maximizer or not?
        :return:
        """
        if current_depth == self.max_depth or state.is_terminal():
            return AIElements.evaluation_function(state, self.player_color), ""

        self.node_expanded += 1
        possible_action = AIElements.get_possible_action(state)
        key_of_actions = list(possible_action.keys())

        shuffle(key_of_actions) #randomness
        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = ""
        for action_key in key_of_actions:
            new_state = AIElements.result_function(state,possible_action[action_key])

            eval_child, action_child = self._minimax(current_depth+1,new_state,not is_max_turn)

            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_target = action_key

            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_target = action_key

        return best_value, action_target

class MinimaxABAgent:
    """
        Minimax agent with Alpha Beta Pruning
    """
    def __init__(self, max_depth=MinimaxABConfig.MAX_DEPTH, player_color=0):
        """
        Initiation

        Parameters
        ----------
        max_depth : int
            The max depth of the tree

        player_color : int
            The player's index as MAX in minimax algorithm
        """
        self.max_depth = max_depth
        self.player_color = player_color
        self.node_expanded = 0

    def enemy_turn_action(self, action_key, new_state):
        """
        Nothing to do here
        """
        pass

    def choose_action(self, state):
        """
        Predict the move using minimax alpha beta pruning algorithm

        Parameters
        ----------
        state : State

        Returns
        -------
        float, str:
            The evaluation or utility and the action key name
        """
        self.node_expanded = 0

        start_time = time.time()

        print("MINIMAX AB : Wait AI is choosing")
        list_action = AIElements.get_possible_action(state)
        eval_score, selected_key_action = self._minimax(0,state,True,float('-inf'),float('inf'))
        print("MINIMAX : Done, eval = %d, expanded %d" % (eval_score, self.node_expanded))
        print("--- %s seconds ---" % (time.time() - start_time))

        return (selected_key_action,list_action[selected_key_action])

    def _minimax(self, current_depth, state, is_max_turn, alpha, beta):
        """
        Helper function of minimax
        :param current_depth: The current depth on the tree in recursive
        :param state: State of the current node in recursive
        :param is_max_turn: Check if the current node is the max turn in recursive
        :param alpha: parameter of AB Prunning, save the current maximizer best value
        :param beta: parameter of AB Prunning, save the current minimizer best value
        :return: int , str The value of the best action and the name of the action
        """
        if current_depth == self.max_depth or state.is_terminal():
            return AIElements.evaluation_function(state, self.player_color), ""

        self.node_expanded += 1

        possible_action = AIElements.get_possible_action(state)
        key_of_actions = list(possible_action.keys())

        shuffle(key_of_actions) # add randomness here
        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = ""
        for action_key in key_of_actions:
            new_state = AIElements.result_function(state,possible_action[action_key])

            eval_child, action_child = self._minimax(current_depth+1,new_state,not is_max_turn, alpha, beta)

            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_target = action_key
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_target = action_key
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        return best_value, action_target

class RandomAgent:
    """
        Random Random
    """
    def __init__(self, max_depth=2, player_color=1):
        """
        Initiation

        Parameters
        ----------
        max_depth : int
            The max depth of the tree

        player_color : int
            The player's index as MAX in minimax algorithm
        """
        self.max_depth = max_depth
        self.player_color = player_color

    def enemy_turn_action(self, action_key, new_state):
        """
        Nothing to do here
        """
        pass

    def choose_action(self, state):
        """
        Predict the move with uniform proba random.

        Parameters
        ----------
        state : State

        Returns
        -------
        float, str:
            The evaluation or utility and the action key name
        """
        import random
        list_action = AIElements.get_possible_action(state)
        key_list_action = list_action.keys()
        rand_int = random.randint(0,len(key_list_action)-1)
        selected_key_action = list(key_list_action)[rand_int]
        return (selected_key_action,list_action[selected_key_action])
