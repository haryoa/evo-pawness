from IPython.core.display import display

from controller.game_controller import GameController, AIElements
from pprint import pprint
import pandas as pd
class GameViewCLI():
    """
    A class used to show the view in CLI
    """

    def __init__(self):
        self.gc = GameController()
        self.board_size = 9
        self.board = [[None for i in range(self.board_size)] for j in range(self.board_size)]

    def start_game_2_players(self):
        """
        Start the game in 2 players mode (no AI)
        To play use these command:
        "exit" : exit the game
        action_key : input the action key stated in the command line.
        """
        state = self.gc.state
        while(not AIElements.is_over(state)):
            pprint(AIElements.get_state_dict(state))
            collected_action = AIElements.get_possible_action(state)
            print("List of Action : ")
            pprint(collected_action)
            self.gc.debug_print_board(state)
            print("Mana (White, Black) = " + str(AIElements.get_players_mana(state)))
            print("Rune List:")
            print(AIElements.get_rune_information(state))
            inp = input("command : ")
            if inp in collected_action.keys():
                state = AIElements.result_function(state,collected_action[inp])
            if inp == 'exit':
                break

    def start_game_2_experimental_(self):
        """
        Start the game in 2 players mode (no AI)
        To play use these command:
        "exit" : exit the game
        action_key : input the action key stated in the command line.
        """
        returned_params = self.gc.play_with_two_players_start()
        returned_task_controller = returned_params['task']

        while (not returned_task_controller == "END_GAME"):
            print(returned_task_controller)
            self.parse_returned_params_change_player(returned_params)
            pprint(pd.DataFrame(self.board))
            pprint(self.possible_action)
            pprint(self.rune_list)
            pprint(self.player_list)
            inp = input("command : ")
            if inp in self.possible_action_keys:
                self.gc.receive_input_action_play(inp, self.possible_action[inp])
                returned_params = self.gc.get_whattodo_view()
                returned_task_controller = returned_params['task']
            elif inp == 'exit':
                break
            else:
                print("Wrong Input")

    def start_game_ai_experimental_(self):
        """
        Start the game in 2 players mode (no AI)
        To play use these command:
        "exit" : exit the game
        action_key : input the action key stated in the command line.
        """
        # returned_params = self.gc.play_with_two_players_start()
        returned_params = self.gc.play_with_ai_white()

        returned_task_controller = returned_params['task']

        while (not returned_task_controller == "END_GAME"):
            print(returned_task_controller)
            if returned_task_controller == 'CHANGE_PLAYER':
                self.parse_returned_params_change_player(returned_params)
                pd.options.display.max_columns = 10
                display(pd.DataFrame(self.board))
                pprint(self.possible_action)
                pprint(self.rune_list)
                pprint(self.player_list)
            elif returned_task_controller == 'AI_MOVE':
                self.parse_returned_params_ai_move(returned_params)
                if 'end' in returned_params:
                    break

                print("AI MOVE")
                pprint(returned_params['ai_action'])
                pprint(pd.DataFrame(self.board))
                print("----")
                self.parse_returned_params_change_player(returned_params)
                pprint(pd.DataFrame(self.board))
                pprint(self.possible_action)
                pprint(self.rune_list)
                pprint(self.player_list)
            inp = input("command : ")
            if inp in self.possible_action_keys:
                self.gc.receive_input_action_play(inp, self.possible_action[inp])
                returned_params = self.gc.get_whattodo_view()
                returned_task_controller = returned_params['task']

            elif inp == 'exit':
                break
            else:
                print("Wrong Input")

    def parse_returned_params_ai_move(self,returned_params):
        self.board = [[None for i in range(self.board_size)] for j in range(self.board_size)]

        # Prev state
        self.black_king = returned_params['prev_state']['black_king']
        self._pawn_write_to_board(self.black_king)
        self.white_king = returned_params['prev_state']['white_king']
        self._pawn_write_to_board(self.white_king)

        self.black_pawn_list = returned_params['prev_state']['black_pawn_list']
        for black_pawn in self.black_pawn_list:
            self._pawn_write_to_board(black_pawn)

        self.white_pawn_list = returned_params['prev_state']['white_pawn_list']
        for white_pawn in self.white_pawn_list:
            self._pawn_write_to_board(white_pawn)

        self.player_list = returned_params['prev_state']['player_list']
        self.rune_list = returned_params['prev_state']['rune_list']
        for rune in self.rune_list:
            self._rune_write_to_board(rune)


    def parse_returned_params_change_player(self,returned_params):
        self.board = [[None for i in range(self.board_size)] for j in range(self.board_size)]
        self.black_king = returned_params['state']['black_king']
        self._pawn_write_to_board(self.black_king)
        self.white_king = returned_params['state']['white_king']
        self._pawn_write_to_board(self.white_king)

        self.black_pawn_list = returned_params['state']['black_pawn_list']
        for black_pawn in self.black_pawn_list:
            self._pawn_write_to_board(black_pawn)

        self.white_pawn_list = returned_params['state']['white_pawn_list']
        for white_pawn in self.white_pawn_list:
            self._pawn_write_to_board(white_pawn)

        self.player_list = returned_params['state']['player_list']
        self.rune_list = returned_params['state']['rune_list']
        for rune in self.rune_list:
            self._rune_write_to_board(rune)
        self.possible_action = returned_params['possible_action']
        self.possible_action_keys = returned_params['possible_action'].keys()

    def _rune_write_to_board(self, rune):
        self.board[rune['y']][rune['x']] = 'Runeeeeee'

    def _pawn_write_to_board(self, pawn):
        self.board[pawn['y']][pawn['x']] = pawn['pawn_type'][0:2] + 'i' \
                                                        + str(pawn['pawn_index']) \
                                                        + 'a' \
                                                        + str(pawn['atk']) \
                                                        + 'h' \
                                                        + str(pawn['hp']) \
                                                        + 'p' \
                                                        + str(pawn['step']) \
                                                        + 't' \
                                                        + str(pawn['status'])[0:2]

    def one_action(self, list_action):
        """
        Concatenate all list of actions to become one list

        ...

        Attributes
        ----------
        list_action : list
            a list of actions of Kings, Players, and Pawns

        Returns
        -------
        list
            a concatenated all list of actions.
        """
        action_list_completed = {}
        for act in list_action:
            if 'action' in act and len(act['action']) > 0:
                for key,value in act['action'].items():
                    action_list_completed[key] = value
        return action_list_completed
