class Pawn:
    """
        A model class used to represent the pawn.
        Should be abstract class. But I don't know how to to define abstract
        class in python.
    """

    def __init__(self, pawn_index, hp, atk, x, y, status, player, step, pawn_type=""):
        """
        Parameters
        ----------
        pawn_index : int
            The pawn index in the list stated in the state
        hp : int
            The health points of the pawn. If 0, the pawn is removed from game
        atk : atk
            The attack points of the pawn.
        x : int
            Coordinate of the pawn
        y : int
            Coordinate of the pawn
        player : intz
            index or color of the player who has this pawn. 0 is white, 1 is black
        step : int
            steps can be taken by the pawn on using 'move' action
        pawn_type : str
            type of pawn
        """
        self.pawn_index = pawn_index
        self.hp = hp
        self.atk = atk
        self.x = x
        self.y = y
        self.status = status
        self.player = player
        self.step = step
        self.max_hp = hp
        self.dir = []
        self.dead = False
        self.pawn_type = self.__class__.__name__
        self.LIMIT_ATK = 8
        self.LIMIT_STEP = 3
        self.LIMIT_HP = 20

    def attack_enemy(self, enemy_pawn):
        """
        Attack enemy's pawn by reducing its health.
        If the enemy's hp is zero, change the dead status
        Parameters
        ----------
        enemy_pawn : Pawn
            enemy's pawn that want to be attacked.
            """
        enemy_pawn.hp -= self.atk
        if enemy_pawn.hp <= 0:
            enemy_pawn.dead = True
            enemy_pawn.x = -2
            enemy_pawn.y = -2
            enemy_pawn.hp = 0

    def add_step(self, added_step):
        """
            limit the added state max to 4

            Parameters
            ----------
            added_step : int
                added step to this pawn
        """
        self.step += added_step
        if self.step >= self.LIMIT_STEP:
            self.step = self.LIMIT_STEP

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def add_atk(self, added_atk):
        """
            Limit ATK Bonus
        :param added_atk: add the atk. The atk cannot be higher than 8
        :return:
        """
        self.atk += added_atk
        if self.atk >= self.LIMIT_ATK:
            self.atk = self.LIMIT_ATK

    def add_hp(self, added_hp):
        """
            Limit ATK Bonus
        :param added_atk: add the atk. The atk cannot be higher than 8
        :return:
        """
        self.hp += added_hp
        if self.hp >= self.LIMIT_HP:
            self.hp = self.LIMIT_HP

    def possible_move(self,x,y):
        """
            Possible move need to be overriden
        """
        pass

    def _possible_move_promoted_helper(self,x,y,direction_move):
        """
            If promoted, the class can use this function to help the function

            Parameters
            ----------
            x : int
                pawn's x coordinate
            y : int
                pawn's y coordinate
            direction_move : list
                list of direction vector. For example (0, 1) represent top/north
        """
        if self.status == 0:
            return {'possible' : []}
        possible_move_list = []
        possible_attack_list = []
        index_dir_counter = 0
        for i in range(self.step):
            for direction in direction_move:
                x_dir = direction[0] * (i+1)
                y_dir = direction[1] * (i+1)
                possible_move_list.append((x+x_dir,y+y_dir,index_dir_counter))
                possible_attack_list.append((x+x_dir,y+y_dir))
                index_dir_counter += 1
        return {'possible' : possible_move_list}

    def __repr__(self):
        active = 'a' if self.status == 1 else 'i'
        return self.__class__.__name__[0:2] + str(self.player.color) + active + str(self.pawn_index) + 'A' + str(self.atk) + 'H' + str(self.hp) +  'S' + str(self.step)

class SoldierPawn(Pawn):
    def __init__(self, pawn_index, hp, atk, x, y, status, player, step):

        super().__init__(pawn_index,hp,atk,x,y, status, player, step)
        if player.color == 0:
            self.dir = [(0,-1)]
        else:
            self.dir = [(0,1)]

    def promote(self, promote_choice):
        """
            Promote into bishop, knight, and rook

            Parameters
            ----------
                promote_choice : string
                    choice
        """
        if promote_choice == 'Bishop': #Bishop
            self.add_step(1)
            self.add_atk(1)
            self.hp = self.max_hp
            self.add_hp(2)
            return BishopPawn(self.pawn_index,self.hp,self.atk,self.x,self.y, self.status, self.player, self.step)
        if promote_choice == 'Knight': #Knight
            self.hp = self.max_hp
            self.add_atk(3)
            return KnightPawn(self.pawn_index,self.hp,self.atk,self.x,self.y, self.status, self.player, self.step)
        if promote_choice == 'Rook': #Rook
            self.hp = self.max_hp
            self.add_atk(2)
            self.add_hp(2)
            return RookPawn(self.pawn_index,self.hp+2,self.atk+2,self.x,self.y, self.status, self.player, self.step)

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def possible_move(self):
        """
            Possible move of the SoldierPawn. Can only move forward
        """
        if self.status == 0:
            return {'possible' : []}
        possible_move_list = []
        possible_attack_list = []
        index_dir_counter = 0

        for i in range(self.step):
            if self.player.color == 0:
                possible_move_list.append((self.x,self.y-1-i, index_dir_counter)) # Move Up if White
                possible_attack_list.append((self.x,self.y-1-i))

            else: #Move bot if Black
                possible_move_list.append((self.x,self.y+1+i, index_dir_counter)) # Move Down if white
                possible_attack_list.append((self.x,self.y+1+i))
            index_dir_counter += 1
        return {'possible' : possible_move_list}

class BishopPawn(Pawn):
    def __init__(self, pawn_index,hp, atk, x, y,status, player, step):
        super().__init__(pawn_index,hp,atk,x,y, status, player, step)
        self.dir = [(1,1),(-1,-1),(1,-1),(-1,1)]

    def promote(self, promote_choice):
        self.hp = self.max_hp
        self.add_atk(2)
        self.add_hp(2)
        if promote_choice == 'Queen': #Queen
            return QueenPawn(self.pawn_index,self.hp,self.atk,self.x,self.y, self.status, self.player, self.step)

    def possible_move(self):
        direction_move = self.dir
        return super()._possible_move_promoted_helper(self.x,self.y,direction_move)


class RookPawn(Pawn):
    def __init__(self, pawn_index,hp, atk, x, y,status, player, step):
        super().__init__(pawn_index,hp,atk,x,y, status, player, step)
        self.dir = [(1,0),(0,1),(0,-1),(-1,0)]

    def promote(self, promote_choice):
        self.hp = self.max_hp
        self.add_atk(2)
        self.add_hp(2)
        if promote_choice == 'Queen': #Queen
            return QueenPawn(self.pawn_index,self.hp,self.atk,self.x,self.y, self.status, self.player, self.step)

    def possible_move(self):
        direction_move = self.dir
        return super()._possible_move_promoted_helper(self.x,self.y,direction_move)

class QueenPawn(Pawn):
    def __init__(self, pawn_index,hp, atk, x, y,status, player, step):
        super().__init__(pawn_index,hp,atk,x,y, status, player, step)
        self.dir = [(1,0),(0,1),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]

    def possible_move(self):
        direction_move = self.dir
        return super()._possible_move_promoted_helper(self.x,self.y,direction_move)

class KnightPawn(Pawn):
    def __init__(self, pawn_index,hp, atk, x, y, status, player, step):
        super().__init__(pawn_index,hp,atk,x,y, status, player, step)
        self.dir = [(1,-2),(1,2),(-2,1),(2,1),(-1,-2),(-1,2), (-2,-1), (2,-1)]

    def possible_move(self):
        possible_move_list = []
        direction_move = self.dir
        index_dir_counter = 0

        for direction in direction_move:
            possible_move_list.append((self.x + direction[0],self.y + direction[1],index_dir_counter))
            index_dir_counter += 1
        return {'possible' : possible_move_list}

class King(Pawn):
    def __init__(self, hp, atk, x, y, player):
        self.hp = hp
        self.atk = atk
        self.x = x
        self.y = y
        self.player = player
        self.step = 3
        self.status = True
        self.dir = [(1,0),(0,1),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
        self.dead = False
        self.pawn_index = -1
        self.pawn_type = self.__class__.__name__


    def attack_enemy(self, enemy_pawn):
        """
            Return true if enemy_pawn dead, false otherwise
        """
        enemy_pawn.hp -= self.atk
        if enemy_pawn.hp <= 0:
            enemy_pawn.dead = True
            enemy_pawn.x = -2
            enemy_pawn.y = -2

    def possible_move(self):
        possible_move_list = []
        direction_move = self.dir
        counter_dir_moves = 0
        for direction in direction_move:
            possible_move_list.append((self.x + direction[0],self.y + direction[1], counter_dir_moves))
            counter_dir_moves += 1
        return super()._possible_move_promoted_helper(self.x,self.y,direction_move)
