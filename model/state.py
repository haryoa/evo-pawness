from model.player import Player
from model.pawn import King, BishopPawn, Pawn, KnightPawn, QueenPawn, RookPawn ,SoldierPawn
from copy import deepcopy
from pprint import pprint
from model.rune import Rune
import random
from IPython.display import display, HTML
import pandas as pd


class State:
    """
    A model class used to represent our state.
    """
    def __init__(self):
        self.board_size = 9 # The board size row = 9, column = 9
        self.white_pawn_list = [] # list of white pawn
        self.black_pawn_list = [] # list of black pawn
        self.white_king = None
        self.black_king = None
        self.rune_list = [] # list of rune
        self.turn = 1
        self.player_list = []
        self.board = [[None for i in range(self.board_size)] for j in range(self.board_size)] # board to show the position of our pawns
        self.PAWN_HP_DEFAULT = 5
        self.PAWN_ATK_DEFAULT = 1
        self.PAWN_STEP_DEFAULT = 1
        self.KING_HP_DEFAULT = 15
        self.KING_ATK_DEFAULT = 3

    def is_terminal(self):
        """
        Check if the state is in the terminal state.
        ...

        Returns
        -------
        bool
            true if the game has ended, false otherwise
        """
        # check if the king is dead
        if self.white_king.dead or self.black_king.dead:
            return True

        boolean_white = True
        boolean_black = True
        # check if all of the pawns of white are dead
        for pawnw, pawnb in zip(self.white_pawn_list,self.black_pawn_list):
            if not pawnw.dead:
                boolean_white = False
            if not pawnb.dead:
                boolean_black = False
        return boolean_white or boolean_black

    def total_eval(self, player_color):
        """
            Evaluation Function
            The formula is:
            0.5(total_player_pawn_hp - total_enemy_pawn_hp) +
            0.1(total_player_pawn_atk - total_enemy_pawn_atk) +
            0.1(total_player_pawn_step - total_enemy_pawn_step) +
            5(total_enemy_dead_pawn - total_player_dead_pawn) +
            1(player_king_hp - enemy_king_hp)
            Parameters
            ----------
            player_color : the player_index

            Returns
            -------
            int
                how far is the advantage of a player
        """
        (player_king, enemy_king) = (self.white_king, self.black_king) if player_color == 0 else (self.black_king, self.white_king)
        (current_player_pawn_list, enemy_pawn_list) = (self.white_pawn_list, self.black_pawn_list) if player_color == 0 else (self.black_pawn_list, self.white_pawn_list)

        if self.is_terminal():
            if player_king.dead:
                return -120
            elif enemy_king.dead:
                return 120
            else:
                util_value = 0
                for player_pawn, enemy_pawn in zip(current_player_pawn_list,enemy_pawn_list):
                    util_value += (int(enemy_pawn.dead) - int(player_pawn.dead))
                if util_value < 0:
                    util_value = -120
                else:
                    util_value = 120
                return util_value

        eval_value = 0
        for player_pawn, enemy_pawn in zip(current_player_pawn_list,enemy_pawn_list):

            if not player_pawn.dead:
                eval_value += 0.3 * player_pawn.hp
            if not enemy_pawn.dead:
                eval_value -= 0.3 * enemy_pawn.hp
            if player_pawn.status and not player_pawn.dead:
                eval_value += 0.1 * player_pawn.atk + 0.1 * player_pawn.step
            if enemy_pawn.status and not enemy_pawn.dead:
                eval_value -= 0.1 * enemy_pawn.atk - 0.1 * enemy_pawn.step
            eval_value += (int(enemy_pawn.dead) - int(player_pawn.dead)) * 10

        eval_value += player_king.hp - enemy_king.hp

        return eval_value

    def sparse_eval(self, player_color):
        """
            Evaluation Function
            The formula is:
            1 is for the player to win
            Parameters
            ----------
            player_color : the player_index

            Returns
            -------
            int
                how far is the advantage of a player
        """
        (player_king, enemy_king) = (self.white_king, self.black_king) if player_color == 0 else (self.black_king, self.white_king)
        (current_player_pawn_list, enemy_pawn_list) = (self.white_pawn_list, self.black_pawn_list) if player_color == 0 else (self.black_pawn_list, self.white_pawn_list)

        if self.is_terminal():
            if player_king.dead:
                return -1
            elif enemy_king.dead:
                return 1
            else:
                util_value = 0
                for player_pawn, enemy_pawn in zip(current_player_pawn_list,enemy_pawn_list):
                    util_value += (int(enemy_pawn.dead) - int(player_pawn.dead))
                if util_value < 0:
                    util_value = -1
                else:
                    util_value = 1
                return util_value

        return 0

    def get_rune_list(self):
        """
        Get all the rune list.
        ...

        Returns
        -------
        list of dict
            dictionary of runes on the board.
        """
        returned_dict = {}
        counter_loop = 1
        for rune in self.rune_list:
            params = {
            'rune_atk_plus' : rune.atk_plus,
            'rune_hp_plus' : rune.hp_plus,
            'rune_step_plus' : rune.step_plus
            }
            returned_dict['rune-' + str(counter_loop)] = params
        return returned_dict

    def initial_state(self):
        """
        Change the state into initial state
        """
        # init player
        self.player_list.append(Player(5,0))
        self.player_list.append(Player(5,1))

        # init King
        self.white_king = King(self.KING_HP_DEFAULT,self.KING_ATK_DEFAULT,4,8, self.player_list[0])
        self.board[4][8] = self.white_king
        self.black_king = King(self.KING_HP_DEFAULT,self.KING_ATK_DEFAULT,4,0, self.player_list[1])
        self.board[4][0] = self.black_king

        init_pawn_spawn = int(9/2) + 1
        for i in range(init_pawn_spawn):
            self.white_pawn_list.append(SoldierPawn(i,self.PAWN_HP_DEFAULT,self.PAWN_ATK_DEFAULT,i*2,7,False,self.player_list[0],self.PAWN_STEP_DEFAULT))
            self.board[i*2][7] = self.white_pawn_list[i]
            self.black_pawn_list.append(SoldierPawn(i,self.PAWN_HP_DEFAULT,self.PAWN_ATK_DEFAULT,i*2,1,False,self.player_list[1],self.PAWN_STEP_DEFAULT))
            self.board[i*2][1] = self.black_pawn_list[i]

    def refresh_board(self):
        """
        Refresh the board array with the current situation
        :return:
        """
        self.board = [[None for i in range(self.board_size)] for j in range(self.board_size)] # board to show the position of our pawns
        self.board[4][8] = self.white_king
        self.board[4][0] = self.black_king

        for pawn in self.white_pawn_list:
            if not pawn.dead:
                self.board[pawn.x][pawn.y] = pawn

        for pawn in self.black_pawn_list:
            if not pawn.dead:
                self.board[pawn.x][pawn.y] = pawn

        # for rune in self.rune_list:
        #     self.board[rune.x][rune.y] = rune

    def print_board(self):
        """
        Print the board with the help of pandas DataFrame..
        Well it sounds stupid.. anyway, it has a nice display, right?
        :return:
        """
        df_pr = [[None for i in range(self.board_size)] for j in range(self.board_size)]
        pd.options.display.max_columns = 10
        pd.options.display.max_rows = 1000
        pd.options.display.width = 1000
        for i in range(self.board_size):
            for j in range(self.board_size):
                need_to_pass = False
                for rune in self.rune_list: # Print the rune if present
                    if j == rune.x and i == rune.y:
                        # print(rune, end=' ')
                        df_pr[i][j] = "Rune"
                        need_to_pass = True
                        pass
                if not need_to_pass:
                    if self.board[j][i] is not None and self.board[j][i].dead == False:
                        df_pr[i][j] = self.board[j][i].__repr__()
                    else:
                        df_pr[i][j] = "Nones"
        display(pd.DataFrame(df_pr))

    def get_possible_action_player(self):
        """
        Get all possible action of a player from this state

        TODO: fix the mess of inputting the dict.
        """
        possible_action = []

        # get player possible action
        player_possible_action = {}
        player = self.player_list[self.turn%2]
        # print(player.__dict__)
        player_string = "White Player" if player.color == 0 else "Black Player"
        player_possible_action["actor"] = player_string
        ref_pawn = self.white_pawn_list if player.color == 0 else self.black_pawn_list
        # print(ref_pawn[0].__dict__)
        dict_action = {}
        p_moves = player.possible_move(ref_pawn)
        for move in p_moves:
            key_name = ""
            action_type = move[0]
            pawn_index = move[1]
            if action_type == 'promote':
                key_name += 'p'
            else:
                key_name += 'a'

            action_params = {}
            targetted_pawn = ref_pawn[pawn_index]
            key_name += "*" + str(targetted_pawn.y) + "," +  str(targetted_pawn.x)

            if not targetted_pawn.dead:
                action_params['pawn_hp'] = targetted_pawn.hp
                action_params['pawn_atk'] = targetted_pawn.atk
                action_params['pawn_step'] = targetted_pawn.step
                action_params['pawn_x'] = targetted_pawn.x
                action_params['pawn_y'] = targetted_pawn.y
                action_params['action'] = action_type
                action_params['pawn_index'] = pawn_index
                action_params['player_index'] = player.color
                if action_type == 'promote':
                    promoted_choice = move[2]
                    action_params['promoted_choice'] = promoted_choice
                    key_name += "*" + promoted_choice[0]

                dict_action[key_name] = action_params
        player_possible_action["action"] = dict_action
        possible_action.append(deepcopy(player_possible_action))
        return possible_action

    def get_possible_action_pawn(self):
        """
        Get all possible action of all pawns from this state

        TODO: fix the mess of inputting the dict.
        """
        possible_action = []
        pawn_possible_action = {}
        player = self.player_list[self.turn%2]
        ref_pawn = self.white_pawn_list if player.color == 0 else self.black_pawn_list
        # print(player)
        # print(ref_pawn[0].__dict__)
        for pawn in ref_pawn:
            if not pawn.dead:
                dict_action = {}
                possible_action_iter = pawn.possible_move()['possible']
                key_name_move_start = 'mp*'
                key_name_atk_start = 'mp*'
                counter_loop_moves = 0
                x_start = pawn.x
                y_start = pawn.y
                step = pawn.step
                for possible_moves in possible_action_iter:
                    action_params = {}
                    x_end = possible_moves[0]
                    y_end = possible_moves[1]
                    dir_index = possible_moves[2]
                    counter_loop_moves += 1
                    if self._is_valid_moves(x_end, y_end):

                        if self._is_occupied_by_enemy(x_end, y_end): #attack
                            pawn_target = self.board[x_end][y_end]

                            action_params = {
                                'player_index' : player.color,
                                'pawn_x' : x_start,
                                'actor' : pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index),
                                'pawn_y' : y_start,
                                'pawn_hp' : pawn.hp,
                                'pawn_atk' : pawn.atk,
                                'pawn_step' : pawn.step,
                                'x_end' : x_end,
                                'y_end' : y_end,
                                'dir_index' : dir_index,
                                'step' : step,
                                'isKing' : pawn_target.__class__.__name__ == "King",
                                'enemy_pawn_index' : pawn_target.pawn_index,
                                'enemy_hp' : pawn_target.hp,
                                'enemy_step' : pawn_target.step,
                                'pawn_index' : pawn.pawn_index,
                                'action' : "attack",
                                'enemy_hp_after_attack' : pawn_target.hp - pawn.atk,
                                'enemy_name' : pawn_target.__class__.__name__ + ' ' + ("White" if pawn_target.player.color == 0 else "Black") + " No. " + str(pawn_target.pawn_index)
                            }
                            y_dir = y_end - y_start
                            x_dir = x_end - x_start
                            key_name_atk = key_name_atk_start + str(y_start) + ',' + str(x_start) + "*"
                            key_name_atk += str(y_dir) + "," + str(x_dir)
                            dict_action[key_name_atk] = deepcopy(action_params)
                        elif not self._is_occupied_by_ally(x_end, y_end):
                            action_params = {
                                'player_index' : player.color,
                                'pawn_x' : x_start,
                                'actor' : pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index),
                                'pawn_hp' : pawn.hp,
                                'pawn_atk' : pawn.atk,
                                'pawn_step' : pawn.step,
                                'pawn_y' : y_start,
                                'pawn_index' : pawn.pawn_index,
                                'x_end' : x_end,
                                'y_end' : y_end,
                                'dir_index' : dir_index,
                                'step' : step,
                                'action' : 'move'
                            }
                            y_dir = y_end - y_start
                            x_dir = x_end - x_start
                            key_name_move = key_name_move_start + str(y_start) + ',' + str(x_start) + "*"
                            key_name_move += str(y_dir) + "," + str(x_dir)
                            dict_action[key_name_move] = deepcopy(action_params)

                pawn_possible_action['actor'] = pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index)
                pawn_possible_action['action'] = deepcopy(dict_action)
            possible_action.append(deepcopy(pawn_possible_action))
        return possible_action

    def get_dict_value_state(self):
        """
        Return the dict contains the information on the current state
        :return: dict
        """
        returned_dict = {}

        # Return all of white pawns
        white_pawn_list_dict = []
        for pawn in self.white_pawn_list:
            white_pawn_list_dict.append(pawn.__dict__)
        returned_dict['white_pawn_list'] = white_pawn_list_dict

        # Return all of black pawns
        black_pawn_list_dict = []
        for pawn in self.black_pawn_list:
            black_pawn_list_dict.append(pawn.__dict__)
        returned_dict['black_pawn_list'] = black_pawn_list_dict

        player_list_dict = []
        for player in self.player_list:
            player_list_dict.append(player.__dict__)
        returned_dict['player_list'] = player_list_dict

        rune_list_dict = []
        for rune in self.rune_list:
            rune_list_dict.append(rune.__dict__)
        returned_dict['rune_list'] = rune_list_dict

        returned_dict['white_king'] = self.white_king.__dict__
        returned_dict['black_king'] = self.black_king.__dict__

        return returned_dict

    def get_possible_action_king(self):
        """
        Get all possible action of a king from this state

        TODO: fix the mess of inputting the dict.
        """
        possible_action = []
        pawn_possible_action = {}
        player = self.player_list[self.turn%2]
        pawn = self.white_king if player.color == 0 else self.black_king

        if not pawn.dead:
            dict_action = {}
            possible_action_iter = pawn.possible_move()['possible']
            key_name_move_start = 'mp*'
            key_name_atk_start = 'mp*'
            counter_loop_moves = 0
            x_start = pawn.x
            y_start = pawn.y
            step = pawn.step
            for possible_moves in possible_action_iter:
                action_params = {}
                x_end = possible_moves[0]
                y_end = possible_moves[1]
                dir_index = possible_moves[2]
                counter_loop_moves += 1
                if self._is_valid_moves(x_end, y_end):

                    if self._is_occupied_by_enemy(x_end, y_end): #attack
                        pawn_target = self.board[x_end][y_end]

                        action_params = {
                            'player_index' : player.color,
                            'pawn_x' : x_start,
                            'actor' : pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index),
                            'pawn_y' : y_start,
                            'pawn_hp' : pawn.hp,
                            'pawn_atk' : pawn.atk,
                            'pawn_step' : pawn.step,
                            'x_end' : x_end,
                            'y_end' : y_end,
                            'dir_index' : dir_index,
                            'step' : step,
                            'isKing' : pawn_target.__class__.__name__ == "King",
                            'enemy_pawn_index' : pawn_target.pawn_index,
                            'enemy_hp' : pawn_target.hp,
                            'enemy_step' : pawn_target.step,
                            'pawn_index' : pawn.pawn_index,
                            'action' : "attack",
                            'enemy_hp_after_attack' : pawn_target.hp - pawn.atk,
                            'enemy_name' : pawn_target.__class__.__name__ + ' ' + ("White" if pawn_target.player.color == 0 else "Black") + " No. " + str(pawn_target.pawn_index)
                        }
                        y_dir = y_end - y_start
                        x_dir = x_end - x_start
                        key_name_atk = key_name_atk_start + str(y_start) + ',' + str(x_start) + "*"
                        key_name_atk += str(y_dir) + "," + str(x_dir)
                        dict_action[key_name_atk] = deepcopy(action_params)

            pawn_possible_action['actor'] = pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index)
            pawn_possible_action['action'] = deepcopy(dict_action)
            possible_action.append(deepcopy(pawn_possible_action))
        return possible_action

    def _is_valid_moves(self, x_new, y_new):
        """
        Check if x_new and y_new is not out of bound in board

        Parameters
        ----------
        x_new : coordinate x
        y_new : coordinate y

        Return
        ------
        bool
            Valid move
        """
        if x_new >= 0 and x_new < self.board_size and y_new >= 0 and y_new < self.board_size:
            return True
        return False

    def change_turn(self):
        """
        Add effect on changing the turn
        """
        self.turn += 1
        self.player_list[self.turn % 2].gain_mana(1)

        if self.turn % 5 == 0:
            self.rune_list = []
            rune_list = [Rune(1,0,0), Rune(0,1,0), Rune(0,0,1)]
            #coor_random = random.sample([(i,j) for i in range(9) for j in range(9) if self.board[i][j] is None],2)
            coor_random = [(0, 4), (4, 4),  (8, 4)]
            counter_loop = 0
            for coor in coor_random:
                pawn_target = self.board[coor[0]][coor[1]]
                if pawn_target is not None:
                    pass # Too OP for now
                    #rune_list[counter_loop].buff_pawn(pawn_target)
                else:
                    rune_list[counter_loop].x = coor[0]
                    rune_list[counter_loop].y = coor[1]
                    self.rune_list.append(rune_list[counter_loop])

                counter_loop += 1

    def get_players_mana(self):
        """
        Get the players mana in tuple
        :return: tuple
        """
        return (self.player_list[0].mana,self.player_list[1].mana)

    def get_player_turn(self):
        """
        Get the players turn
        :return: int
        """
        return self.turn % 2

    def _is_occupied_by_enemy(self, x_new, y_new):
        """
        Check if the coordinates is occupied by an enemy's pawn

        Parameters
        ----------
        x_new : x coordinate
        y_new : y coordinate
        """
        target_spot = self.board[x_new][y_new]
        if target_spot is not None and target_spot.player.color == (self.turn + 1) % 2:
                return True
        return False

    def _is_occupied_by_ally(self, x_new, y_new):
        """
        Check if the coordinates is occupied by an ally's pawn

        Parameters
        ----------
        x_new : x coordinate
        y_new : y coordinate
        """
        target_spot = self.board[x_new][y_new]
        if target_spot is not None and target_spot.player.color == self.turn % 2:
                return True
        return False

    def attack_pawn(self,ally_pawn_index, enemy_pawn_index,player_color, x,y):
        """
        Function of action "attack"

        Parameters
        ----------
        ally_pawn_index : int
            the pawn index of the attacker in the list
        enemy_pawn_index : int
            the pawn index of the enemy's pawn in the list
        player_color : int
            player's color or index
        x : int
        y : int
        """
        if player_color == 0:
            ally_pawn = self.white_king if ally_pawn_index == -1 else self.white_pawn_list[ally_pawn_index]
            enemy_pawn = self.black_king if enemy_pawn_index == -1 else self.black_pawn_list[enemy_pawn_index]
        else:
            ally_pawn = self.black_king if ally_pawn_index == -1 else self.black_pawn_list[ally_pawn_index]
            enemy_pawn = self.white_king if enemy_pawn_index == -1 else self.white_pawn_list[enemy_pawn_index]
        old_x_enemy = enemy_pawn.x
        old_y_enemy = enemy_pawn.y
        ally_pawn.attack_enemy(enemy_pawn)

        if enemy_pawn.dead:
            self.board[old_x_enemy][old_y_enemy] = None

    def move_pawn(self, pawn_index, player_color, new_x, new_y):
        """
        Function of action "move"

        Parameters
        ----------
        pawn_index : int
            the pawn index in the list
        player_color : int
            player's color or index in the list
        new_x : x coordinate destination
        new_y : y coordinate destination
        """
        pawn = self.white_pawn_list[pawn_index] if player_color == 0 else self.black_pawn_list[pawn_index]
        self.board[pawn.x][pawn.y] = None
        self.board[new_x][new_y] = pawn
        pawn.move(new_x, new_y)

        for rune in self.rune_list:
            if new_x == rune.x and new_y == rune.y:
                rune.buff_pawn(pawn,randoming=False)
                self.rune_list.remove(rune)

    def activate_pawn(self, player_color, pawn_index):
        """
        Function of action "activate"

        Parameters
        ----------
        pawn_index : int
            the pawn index in the list
        player_color : int
            player's color or index in the list
        """
        self.player_list[player_color].special_activate_pawn(self.white_pawn_list[pawn_index] if player_color == 0 else self.black_pawn_list[pawn_index])

    def promote_pawn(self, player_color, pawn_index, choice):
        """
        Function of action "promote"

        Parameters
        ----------
        pawn_index : int
            the pawn index in the list
        player_color : int
            player's color or index in the list
        choce : string
            the choice of the unit promotion
        """
        targetted_pawn_list = self.white_pawn_list if player_color == 0 else self.black_pawn_list
        promoted_pawn = self.player_list[player_color].special_promote_pawn(targetted_pawn_list[pawn_index], choice)
        # update list
        targetted_pawn_list[pawn_index] = promoted_pawn
        self.board[promoted_pawn.x][promoted_pawn.y] = promoted_pawn

    def __repr__(self):
        returned_string = "p"
        for i in range(self.board_size):
            for j in range(self.board_size):
                need_to_pass = False
                for rune in self.rune_list: # Print the rune if present
                    if j == rune.x and i == rune.y:
                        returned_string += "rn"
                        need_to_pass = True
                        pass
                if not need_to_pass:
                    if self.board[j][i] is not None and self.board[j][i].dead == False:
                        returned_string += self.board[j][i].__repr__() + str(self.board[j][i].x) + str(self.board[j][i].y)
                    else:
                        pass
            returned_string += str(self.player_list[0].mana) + str(self.player_list[1].mana)
            returned_string += str(self.turn % 5)
        return returned_string
