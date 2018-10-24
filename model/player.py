from model.pawn import RookPawn, BishopPawn, SoldierPawn, QueenPawn

class Player():
    """
        A model class used to represent the player.
        Color 0 for white and 1 for black
    """
    def __init__(self, mana, color):
        """
        Parameters
        ----------
        mana : int
            Initial mana
        color : int
            Player index. 0 = white, 1 = black
        """
        self.mana = mana
        self.color = color

    def special_activate_pawn(self, pawn):
        """
        Special skill that player can use. "Activate pawn"
        ...

        Parameters
        ----------
        pawn : Pawn
        """
        pawn.status = True
        self.mana -= 3

    def gain_mana(self, count_mana):
        """
        Function to gain the mana. Limit the mana by 10
        ...

        Parameters
        ----------
        count_mana : int
            amount of mana gained.
        """
        total = self.mana + count_mana
        if total <= 10:
            self.mana = total

    def possible_move(self,list_pawn):
        """
        Get possible move of the players.
        ...

        Parameters
        ----------
        list_pawn : list
            list of possible moves
        """
        list_possible_move = []
        for pawn in list_pawn:
            if self.mana == 10:
                if pawn.status == 1 and (isinstance(pawn,RookPawn) or isinstance(pawn,BishopPawn)):
                     list_possible_move.append(("promote", pawn.pawn_index, "Queen"))
            if self.mana >= 3:
                if pawn.status == 0:
                    list_possible_move.append(("activate",pawn.pawn_index))
            if self.mana >= 5:
                if isinstance(pawn,SoldierPawn) and pawn.status:
                    list_possible_move.append(("promote", pawn.pawn_index ,"Rook"))
                    list_possible_move.append(("promote", pawn.pawn_index ,"Bishop"))
                    list_possible_move.append(("promote", pawn.pawn_index ,"Knight"))

        return list_possible_move

    def special_promote_pawn(self, pawn, choice):
        """
        Special skill that player can use. "promote pawn"
        ...

        Parameters
        ----------
        pawn : Pawn

        choice: string
            Player's choose a choice to evolve the pawn.
        """
        pawn = pawn.promote(choice)
        self.mana = (self.mana - 10) if isinstance(pawn,QueenPawn) else (self.mana - 5)
        return pawn

    def __repr__(self):
        return str(self.color)
