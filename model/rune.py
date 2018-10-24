import random

class Rune:
    """
    A model class used to represent the rune.
    """
    def __init__(self):
        self.atk_plus = 2 #random.randrange(1,4)
        self.hp_plus = 2 #random.randrange(1,4)
        self.step_plus = 1 #random.randrange(1,2)
        self.x = None
        self.y = None

    def buff_pawn(self, pawn):
        """
        Get all the rune list.
        ...

        Parameters
        ----------
        pawn : Pawn
            Change the parameter of our pawn randomly
            get buff of one of the following attribute: atk, hp, step
        """
        rand_num = random.randrange(0,3)
        if rand_num == 0:
            pawn.atk += self.atk_plus
        elif rand_num == 1:
            pawn.hp += self.hp_plus
        else:
            pawn.step += self.step_plus

    def __repr__(self):
        return "a" + str(self.atk_plus) + "h" + str(self.hp_plus) + "s" + str(self.step_plus) + "+r"
