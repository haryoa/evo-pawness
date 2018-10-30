import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QGridLayout, QLabel,
    QMainWindow, QInputDialog, QMessageBox)
from controller.game_controller import GameController
from ai_modules.ai_elements import AIElements

from copy import deepcopy
from pprint import pprint
import gc
class ViewGUI(QWidget):
    # TODO Add AI handle
    def __init__(self):
        self.counter_debug = 0
        super().__init__()
        self.gc = GameController()
        self.initUI()
        self.activate_coor = [] # tuple x,y
        self.move_coor = []
        self.atk_coor = []
        self.INACTIVE_PAWN_CSS = "background-color: #9AAC41;"
        self.ACTIVE_PAWN_CSS = "background-color: #E1FE57"
        self.ACTIVATE_PAWN_CSS = "background-color: green; color: white; font-weight: 500;"
        self.TILE_MOVE_CSS = "background-color: #53F399;"
        self.TILE_ATK_CSS = "background-color: #FF3500;"
        self.PROMOTE_PAWN_CSS = "background-color: #2e00ff; color: white;"

    def button_two_players_clicked(self):
        sender = self.sender()
        returned_params = self.gc.play_with_two_players_start()
        returned_task_controller = returned_params['task']
        if returned_task_controller == "END_GAME":
            self.task = "END GAME"
        else:
            self.clear_all_button_board()
            self.reset_board_two_players(returned_params)
            self.parse_possible_action()

    def button_ai_white_vs_players_clicked(self):
        sender = self.sender()
        returned_params = self.gc.play_with_ai_white()
        returned_task_controller = returned_params['task']
        if returned_task_controller == "END_GAME":
            self.task = "END GAME"
        else:
            self.clear_all_button_board()
            self.reset_board_two_players(returned_params)
            self.parse_possible_action()

    def decide_status_board_css(self,y,x):
        return self.ACTIVE_PAWN_CSS if self.list_btn_board[y][x].active_status_pawn  else self.INACTIVE_PAWN_CSS

    def parse_possible_action(self):

        self.counter_debug += 1
        self.activate_coor = []
        self.promote_coor = []
        self.move_coor = []
        self.atk_coor = []
        # pprint(self.possible_action)
        for key, value in self.possible_action.items():
            if value['action'] == 'activate':
                self.btn_activate.setEnabled(True)
                self.list_btn_board[value['pawn_y']][value['pawn_x']].set_activate_key(key)
                self.btn_activate.clicked.connect(lambda: self.enable_activate_possible_action_button())
                self.activate_coor.append((value['pawn_x'],value['pawn_y']))
            if value['action'] == 'move':
                self.move_coor.append({"pawn_x" : value['pawn_x'],\
                                        "pawn_y" : value['pawn_y'],\
                                        "end_x" : value['x_end'],\
                                        "end_y" : value['y_end'],
                                        "move_key" : key})
                pawn_x = value['pawn_x']
                pawn_y = value['pawn_y']
                end_x = value['x_end']
                end_y = value['y_end']
                move_key = key
                self.list_btn_board[pawn_y][pawn_x].setEnabled(True)
                self.list_btn_board[pawn_y][pawn_x].add_move_list(end_y, end_x , key)
                self.list_btn_board[pawn_y][pawn_x].clicked.connect(lambda: self.enable_move())
            if value['action'] == 'attack':
                pawn_x = value['pawn_x']
                pawn_y = value['pawn_y']
                end_x = value['x_end']
                end_y = value['y_end']
                move_key = key
                self.list_btn_board[pawn_y][pawn_x].setEnabled(True)
                self.atk_coor.append({"pawn_x" : pawn_x,\
                                        "pawn_y" : pawn_y,\
                                        "end_x" : end_x,\
                                        "end_y" : end_y,\
                                        "move_key" : key})
                self.list_btn_board[pawn_y][pawn_x].add_attack_list(end_y, end_x , key)
                # print(self.list_btn_board[pawn_y][pawn_x].attack_list)
                self.list_btn_board[pawn_y][pawn_x].clicked.connect(lambda: self.enable_attack())

            if value['action'] == 'promote':
                pawn_x = value['pawn_x']
                pawn_y = value['pawn_y']
                move_key = key
                choice = value['promoted_choice']
                self.list_btn_board[pawn_y][pawn_x].add_promote_list(move_key,choice)
                self.promote_coor.append((pawn_x,pawn_y))
                self.btn_evolve.clicked.connect(lambda: self.enable_promote_possible_action_button())
                self.btn_evolve.setEnabled(True)

            if value['action'] == 'skip':
                self.gc.receive_input_action_play("skip", self.possible_action["skip"])
                returned_params = self.gc.get_whattodo_view()
                self.returned_params = returned_params
                returned_task_controller = returned_params['task']
                self.clear_all_button_board()
                self.reset_board_two_players(returned_params)
                self.btn_activate.setEnabled(False)
                self.btn_evolve.setEnabled(False)

                self.parse_possible_action()

    def enable_promote_possible_action_button(self):
        if len(self.promote_coor) > 0:
            self.btn_activate.setEnabled(False)
            self.disable_all_pawn_button()
            for coor in self.promote_coor:
                try: self.list_btn_board[coor[1]][coor[0]].clicked.disconnect()
                except Exception: pass
                self.list_btn_board[coor[1]][coor[0]].setEnabled(True)
                self.list_btn_board[coor[1]][coor[0]].setStyleSheet(self.PROMOTE_PAWN_CSS)
                self.list_btn_board[coor[1]][coor[0]].clicked.connect(self.button_promote_pawn)
            self.btn_evolve.setText("Cancel Evolve")
            try: self.btn_evolve.clicked.disconnect()
            except Exception: pass
            self.btn_evolve.clicked.connect(lambda: self.disable_promote_possible_action_button())

    def disable_promote_possible_action_button(self):
        for coor in self.promote_coor:
            self.list_btn_board[coor[1]][coor[0]].setEnabled(False)
            self.list_btn_board[coor[1]][coor[0]].setStyleSheet(self.decide_status_board_css(coor[1],coor[0]))
            try: self.list_btn_board[coor[1]][coor[0]].clicked.disconnect()
            except Exception: pass
        self.btn_evolve.setText("Evolve")
        self.parse_possible_action()

    def button_promote_pawn(self):
        # print(self.sender().promote_dict.keys())
        items = self.sender().promote_dict.keys()
        item, okPressed = QInputDialog.getItem(self, "Select Promote","Promote To:", items, 0, False)
        if item and okPressed:
            choice = self.sender().promote_dict[item]
            self.gc.receive_input_action_play(choice, self.possible_action[choice])
            returned_params = self.gc.get_whattodo_view()
            self.returned_params = returned_params
            returned_task_controller = returned_params['task']
            self.clear_all_button_board()
            self.reset_board_two_players(returned_params)
            self.btn_activate.setEnabled(False)
            self.btn_evolve.setEnabled(False)

            self.parse_possible_action()

    def enable_attack(self):
        sender = self.sender()

        self.disable_all_pawn_button()
        sender.setEnabled(True)
        self.btn_activate.setEnabled(False)
        self.btn_evolve.setEnabled(False)

        for tuple_range in sender.attack_list:
            self.list_btn_board[tuple_range[1]][tuple_range[0]].setEnabled(True)
            self.list_btn_board[tuple_range[1]][tuple_range[0]].setStyleSheet(self.TILE_ATK_CSS)
            self.list_btn_board[tuple_range[1]][tuple_range[0]].set_attack_key(tuple_range[2])
            self.list_btn_board[tuple_range[1]][tuple_range[0]].clicked.connect(lambda : self.button_attack_pawn())
        sender.clicked.connect(lambda : self.disable_attack())

    def disable_attack(self):
        sender = self.sender()
        for tuple_range in sender.attack_list:
            try: self.list_btn_board[tuple_range[1]][tuple_range[0]].disconnect()
            except Exception: pass
            self.list_btn_board[tuple_range[1]][tuple_range[0]].setEnabled(False)
        try: sender.clicked.disconnect()
        except Exception: pass
        for tuple_range in sender.attack_list:
            self.list_btn_board[tuple_range[1]][tuple_range[0]].setStyleSheet("")
        sender.clear_attack_list()
        for tuple_range in sender.move_list:
            try: self.list_btn_board[tuple_range[1]][tuple_range[0]].disconnect()
            except Exception: pass
            self.list_btn_board[tuple_range[1]][tuple_range[0]].setEnabled(False)
        try: sender.clicked.disconnect()
        except Exception: pass
        for tuple_range in sender.move_list:
            self.list_btn_board[tuple_range[1]][tuple_range[0]].setStyleSheet("")
        sender.clear_move_list()
        self.parse_possible_action()

    def button_attack_pawn(self):
        sender = self.sender()
        self.gc.receive_input_action_play(sender.attack_key, self.possible_action[sender.attack_key])
        returned_params = self.gc.get_whattodo_view()
        self.returned_params = returned_params
        returned_task_controller = returned_params['task']
        self.clear_all_button_board()
        self.reset_board_two_players(returned_params)
        self.btn_activate.setEnabled(False)
        self.btn_evolve.setEnabled(False)
        self.parse_possible_action()

    def disable_all_pawn_button(self):
        for move in self.move_coor:
            self.list_btn_board[move['pawn_y']][move['pawn_x']].setEnabled(False)
        for move in self.atk_coor:
            self.list_btn_board[move['pawn_y']][move['pawn_x']].setEnabled(False)

    def enable_move(self):
        sender = self.sender()
        # try: sender.clicked.disconnect()
        # except Exception: pass
        self.disable_all_pawn_button()
        sender.setEnabled(True)
        self.btn_activate.setEnabled(False)
        self.btn_evolve.setEnabled(False)

        for tuple_range in sender.move_list:
            self.list_btn_board[tuple_range[1]][tuple_range[0]].setEnabled(True)
            self.list_btn_board[tuple_range[1]][tuple_range[0]].setStyleSheet(self.TILE_MOVE_CSS)
            self.list_btn_board[tuple_range[1]][tuple_range[0]].set_move_key(tuple_range[2])
            self.list_btn_board[tuple_range[1]][tuple_range[0]].clicked.connect(lambda : self.button_move_pawn())
        sender.clicked.connect(lambda : self.disable_attack())

    def button_move_pawn(self):
        sender = self.sender()
        self.gc.receive_input_action_play(sender.move_key, self.possible_action[sender.move_key])
        returned_params = self.gc.get_whattodo_view()
        print(type(returned_params))

        self.returned_params = returned_params
        returned_task_controller = returned_params['task']
        self.clear_all_button_board()
        self.reset_board_two_players(returned_params)
        self.btn_activate.setEnabled(False)
        self.btn_evolve.setEnabled(False)
        self.parse_possible_action()

    def disable_move(self):
        sender = self.sender()
        for tuple_range in sender.move_list:
            try: self.list_btn_board[tuple_range[1]][tuple_range[0]].disconnect()
            except Exception: pass
            self.list_btn_board[tuple_range[1]][tuple_range[0]].setEnabled(False)
        try: sender.clicked.disconnect()
        except Exception: pass
        for tuple_range in sender.move_list:
            self.list_btn_board[tuple_range[1]][tuple_range[0]].setStyleSheet("")
        sender.clear_move_list()
        self.parse_possible_action()

    def enable_activate_possible_action_button(self):
        self.btn_evolve.setEnabled(False)

        if len(self.activate_coor) > 0:
            for coor in self.activate_coor:
                self.list_btn_board[coor[1]][coor[0]].setEnabled(True)
                self.list_btn_board[coor[1]][coor[0]].setStyleSheet(self.ACTIVATE_PAWN_CSS)
                self.list_btn_board[coor[1]][coor[0]].clicked.connect(self.button_activate_pawn)
            self.btn_activate.setText("Cancel Activate")
            self.disable_all_pawn_button()
            try: self.btn_activate.clicked.disconnect()
            except Exception: pass
            self.btn_activate.clicked.connect(lambda: self.disable_activate_possible_action_button())

    def disable_activate_possible_action_button(self):
        for coor in self.activate_coor:
            self.list_btn_board[coor[1]][coor[0]].setEnabled(False)
            self.list_btn_board[coor[1]][coor[0]].setStyleSheet(self.decide_status_board_css(coor[1],coor[0]))
            try: self.list_btn_board[coor[1]][coor[0]].clicked.disconnect()
            except Exception: pass
        self.btn_activate.setText("Activate")
        self.parse_possible_action()

    def button_activate_pawn(self):
        for coor in self.activate_coor:
            try: self.list_btn_board[coor[1]][coor[0]].clicked.disconnect()
            except Exception: pass
        key_action = self.sender().activate_key
        self.gc.receive_input_action_play(key_action, self.possible_action[key_action])
        returned_params = self.gc.get_whattodo_view()
        self.returned_params = returned_params
        returned_task_controller = returned_params['task']
        self.reset_board_two_players(returned_params)
        self.btn_activate.setEnabled(False)
        self.btn_evolve.setEnabled(False)
        self.parse_possible_action()


    def clear_all_button_board(self):
        self.btn_activate.setText("Activate")
        self.btn_evolve.setText("Evolve")
        for board_rows in self.list_btn_board:
            for board in board_rows:
                try: board.clicked.disconnect()
                except Exception: pass
                board.clear_move_list()
                board.clear_attack_list()
                board.clear_promote_list()
                board.setEnabled(False)
                board.move_key = None
                board.setText("")
                board.setStyleSheet("")

    def color_check_mana(self,mana,label):
        if mana == 10:
            label.setStyleSheet("background-color: #fe0081;" )
        elif mana > 4:
            label.setStyleSheet("background-color: #07fe00;")
        elif mana > 2:
            label.setStyleSheet("background-color: #e0e728;")
        else:
            label.setStyleSheet("")

    def check_task(self, returned_params):
        pass

    def reset_board_two_players(self, returned_params):
        self.clear_all_button_board()
        # pprint(returned_params)

        # TODO put to check task function
        if returned_params['task'] == 'END_GAME':
            QMessageBox.about(self, "Title", "Game has ended")
            sys.exit()


        self.mana_0 = returned_params['state']['player_list'][0]['mana']
        self.mana_1 = returned_params['state']['player_list'][1]['mana']
        self.mn0.setText(str(self.mana_0))
        self.mn1.setText(str(self.mana_1))
        self.color_check_mana(self.mana_0,self.mn0)
        self.color_check_mana(self.mana_1,self.mn1)

        self.black_king = returned_params['state']['black_king']
        if not self.black_king['dead']:
            self._pawn_write_to_board(self.black_king)
        self.white_king = returned_params['state']['white_king']
        if not self.white_king['dead']:
            self._pawn_write_to_board(self.white_king)

        self.black_pawn_list = returned_params['state']['black_pawn_list']
        for black_pawn in self.black_pawn_list:
            if not black_pawn['dead']:
                self._pawn_write_to_board(black_pawn)

        self.white_pawn_list = returned_params['state']['white_pawn_list']
        for white_pawn in self.white_pawn_list:
            if not white_pawn['dead']:
                self._pawn_write_to_board(white_pawn)

        self.player_list = returned_params['state']['player_list']
        self.rune_list = returned_params['state']['rune_list']
        for rune in self.rune_list:
            self._rune_write_to_board(rune)
        self.possible_action = returned_params['possible_action']
        self.possible_action_keys = returned_params['possible_action'].keys()

    def _rune_write_to_board(self, rune):
        self.list_btn_board[rune['y']][rune['x']].set_text_with_params(rune,"rune")

    def _pawn_write_to_board(self, pawn):
        self.list_btn_board[pawn['y']][pawn['x']].set_text_with_params(pawn,"pawn")
        self.list_btn_board[pawn['y']][pawn['x']].set_active_status_pawn(pawn['status'])
        self.list_btn_board[pawn['y']][pawn['x']].setStyleSheet(self.decide_status_board_css(pawn['y'], pawn['x']))

    def initUI(self):
        main_layout = QHBoxLayout()
        board_layout = self.ui_board()
        mana_info = self.ui_info_mana()
        special_ui_button = self.ui_button_special()
        info_game = self.ui_info_static()
        info_layout = QVBoxLayout()
        info_layout.addLayout(mana_info)
        info_layout.addLayout(special_ui_button)
        info_layout.addLayout(info_game)

        self.button_two_players = QPushButton("Play Two Players")
        self.button_two_players.clicked.connect(self.button_two_players_clicked)
        self.button_ai_white_player = QPushButton("AI White vs Human")
        self.button_ai_white_player.clicked.connect(self.button_ai_white_vs_players_clicked)

        main_layout.addWidget(self.button_two_players)
        main_layout.addWidget(self.button_ai_white_player)

        main_layout.addLayout(board_layout)
        main_layout.addLayout(info_layout)

        self.setLayout(main_layout)
        self.move(50,50)
        self.show()

    def ui_info_mana(self):
        lbl1 = QLabel('Player White',self)
        lbl2 = QLabel('Player Black', self)
        self.mn0 = QLabel('5',self)
        self.mn1 = QLabel('5', self)
        self.label_task = QLabel("STATUS", self)
        self.task = QLabel('WAIT',self)
        grid = QGridLayout()
        grid.addWidget(lbl1,0,0)
        grid.addWidget(lbl2,0,1)
        grid.addWidget(self.mn0,1,0)
        grid.addWidget(self.mn1,1,1)
        grid.addWidget(self.label_task,2,0)
        grid.addWidget(self.task,2,1)
        return grid

    def ui_button_special(self):
        hbox = QVBoxLayout()
        self.btn_evolve = QPushButton("Evolve")
        self.btn_evolve.setEnabled(False)
        self.btn_activate = QPushButton("Activate")
        self.btn_activate.setEnabled(False)

        hbox.addWidget(self.btn_evolve)
        hbox.addWidget(self.btn_activate)
        return hbox

    def ui_info_static(self):
        grid = QVBoxLayout()
        lbl1 = QLabel('3 = Activate',self)
        lbl2 = QLabel('5 = Promote 2nd tier',self)
        lbl3 = QLabel('10 = Promote to Queen',self)
        grid.addWidget(QLabel("Information"))
        grid.addWidget(lbl1)
        grid.addWidget(lbl2)
        grid.addWidget(lbl3)
        return grid


    def ui_board(self, size=9):
        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)

        i,j = 0,0
        self.list_btn_board = [[None for i in range(9)] for  j in range(9)]
        for k in range(size):
            for l in range(size):
                btn_board = BoardButton()
                btn_board.setEnabled(False)
                btn_board.setFixedSize(100,90)
                self.list_btn_board[k][l] = btn_board
                grid.addWidget(btn_board,k,l)
        return grid

class BoardButton(QPushButton):


    def add_promote_list(self, promote_key, choice):
        if hasattr(self, 'promote_dict'):
            self.promote_dict[choice] = promote_key
        else:
            self.promote_dict = {choice : promote_key}

    def clear_promote_list(self):
        self.promote_dict = {}

    def set_activate_key(self, activate_key):
        self.activate_key = activate_key

    def set_active_status_pawn(self,active_status_pawn = False):
        self.active_status_pawn = active_status_pawn

    def add_move_list(self,y,x,key):
        if hasattr(self, 'move_list'):
            self.move_list.append((x,y,key))
        else:
            self.move_list = [(x,y,key)]

    def clear_move_list(self):
        self.move_list = []

    def set_move_key(self, key):
        self.move_key = key

    def add_attack_list(self,y,x,key):
        if hasattr(self, 'attack_list'):
            self.attack_list.append((x,y,key))
        else:
            self.attack_list = [(x,y,key)]

    def clear_attack_list(self):
        self.attack_list = []

    def set_attack_key(self, key):
        self.attack_key = key

    def set_text_with_params(self, params, object_type):
        if object_type == "rune":
            self.setText("Rune")
        else: # pawn
            # pprint(params)
            player_index = params['player'].color
            color = 'Black' if player_index == 1 else 'White'
            text_button = color + "\n " + params['pawn_type'] + str(params['pawn_index']) + "\n HP : " + str(params['hp']) + \
                    "\n ATK : " + str(params['atk']) + "\n STEP : " + str(params['step'])
            self.setText(text_button)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ViewGUI()
    sys.exit(app.exec_())
