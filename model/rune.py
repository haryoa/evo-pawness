import random

class Rune:
    """
    A model class used to represent the rune.
    """
    def __init__(self,atk_plus=2,hp_plus=2,step_plus=2):
        self.atk_plus = atk_plus #random.randrange(1,4)
        self.hp_plus = hp_plus #random.randrange(1,4)
        self.step_plus = step_plus #random.randrange(1,2)
        self.x = None
        self.y = None

    def buff_pawn(self, pawn, randoming=True):
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
        if randoming:
            if rand_num == 0:
                pawn.add_atk(self.atk_plus)
            elif rand_num == 1:
                pawn.add_hp(self.hp_plus)
            else:
                pawn.add_step(self.step_plus)
        else:
            pawn.add_atk(self.atk_plus)
            pawn.add_hp(self.hp_plus)
            pawn.add_step(self.step_plus)


    def __repr__(self):
        return "a" + str(self.atk_plus) + "h" + str(self.hp_plus) + "s" + str(self.step_plus) + "+r"
