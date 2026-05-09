from random import randint
from abc import ABC, abstractmethod

class AI() :
    """
    Classe des IA
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def select_move(self, l):
        pass

class DumbAI (AI) : 
    """
    Classe de l'IA stupide : 
    coups aléatoires
    """
    def __init__(self):
        self.name = "IAdifficilementpire"
    
    def select_move(self, l, board) :
        n = len(l)
        k = randint(0, n-1)
        return l[k]
    
class MinmaxAI (AI) :
    """
    Classe de l'IA réfléchie
    algo de min max à profondeur variable
    POUR LE MOMENT CEST UN CLONE DE DUMBAI
    """
    def __init__(self):
        self.name = "IAdifficilementpire"
    
    def select_move(self, l, board) :
        n = len(l)
        k = randint(0, n-1)
        return l[k]

