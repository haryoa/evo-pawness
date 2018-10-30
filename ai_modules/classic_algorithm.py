from random import shuffle
from model.state import State
from ai_modules.ai_elements import AIElements

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
        list_action = AIElements.get_possible_action(state)
        eval_score, selected_key_action = self._minimax(0,state,True)
        return (selected_key_action,list_action[selected_key_action])

    def _minimax(self, current_depth, state, is_max_turn):

        if current_depth == self.max_depth or state.is_terminal():
            return AIElements.evaluation_function(state, self.player_color), ""

        possible_action = AIElements.get_possible_action(state)
        key_of_actions = list(possible_action.keys())

        shuffle(key_of_actions) #randomness
        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = ""
        for action_key in key_of_actions:
            new_state = AIElements.result_function(state,possible_action[action_key])

            eval_child, action_child = self._minimax(current_depth+1,new_state,False)

            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_target = action_key

            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_target = action_key

        return best_value, action_target

class MinimaxABAgent:
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
        print("MINIMAX AB : Wait AI is choosing")
        list_action = AIElements.get_possible_action(state)
        eval_score, selected_key_action = self._minimax(0,state,True,float('-inf'),float('inf'))
        print("MINIMAX : Done, eval = %d" % (eval_score))
        return (selected_key_action,list_action[selected_key_action])

    def _minimax(self, current_depth, state, is_max_turn, alpha, beta):

        if current_depth == self.max_depth or state.is_terminal():
            return AIElements.evaluation_function(state, self.player_color), ""

        possible_action = AIElements.get_possible_action(state)
        key_of_actions = list(possible_action.keys())

        shuffle(key_of_actions) #randomness
        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = ""
        for action_key in key_of_actions:
            new_state = AIElements.result_function(state,possible_action[action_key])

            eval_child, action_child = self._minimax(current_depth+1,new_state,False, alpha, beta)

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
        list_action = AIElements.get_possible_action(state)
        key_list_action = list_action.keys()
        rand_int = random.randint(0,len(key_list_action)-1)
        selected_key_action = list(key_list_action)[rand_int]
        return (selected_key_action,list_action[selected_key_action])


# if __name__ == '__main__':
#     state = State()
#     state.initial_state()
#
#     ga = GameAI()
#     possible = AIElements.get_possible_action(state)
#     action_key, action_dict = ga.choose_action(state, possible)
#     state = AIElements.result_function(state, possible[action_key])
#
#     # [4]
#     minimax = MinimaxAgent(max_depth=5,player_color=0)
#     %timeit -n 1 -r 1 print(minimax.choose_action(state))
#
#     # []
#     print("aha")
#     minimaxab = MinimaxABAgent(max_depth=6,player_color=0)
#     %timeit -n 1 -r 1 print(minimaxab.choose_action(state))
