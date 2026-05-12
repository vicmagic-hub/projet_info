from random import randint, shuffle
from abc import ABC, abstractmethod

class AI() :
    """
    Classe abstraite des IA
    """

    @abstractmethod
    def __init__(self):
        """
        Initialisation de l'IA
        Dépend du modèle choisi
        """
        pass

    @abstractmethod
    def select_move(self, board, to_play):
        """
        choix du coup de l'IA dans une situation donnée
        entree : plateau, couleur du joueur qui doit jouer
        renvoie une instance de Move
        """
        pass

class DumbAI (AI) : 
    """
    Classe de l'IA stupide : 
    coups aléatoires
    """
    def __init__(self):
        """
        Initialisation de l'IA
        attribution du nom
        """
        self.name = "IAdifficilementpire"
    
    def select_move(self, board, to_play) :
        """
        choix du coup de l'IA dans une situation donnée
        entree : plateau, couleur du joueur qui doit jouer
        renvoie une instance de Move
        méthode de réflexion : 
            - génération d'une liste de coup possibles
            - sélection d'un indice de coup au hasard
        """
        move_list = board.move_list(to_play)
        n = len(move_list)
        k = randint(0, n-1)
        return move_list[k]
    
class MinmaxAI (AI) :
    """
    Classe de l'IA (un peu) réfléchie
    algo de min max à profondeur variable et heuristique douteuse
    En l'état, gère en temps raisonnable des profondeurs de 3, voire 4.
    """
    def __init__(self, depth):
        """
        Initialisation de l'IA
        entree : profondeur souhaitée
        attribution du nom et initialisation de la profondeur 
        """
        self.name = "IAmoyendsefaireavoir"
        self.depth = depth
    
    def select_move(self, board, to_play) :
        """
        choix du coup de l'IA dans une situation donnée
        entree : plateau, couleur du joueur qui doit jouer
        renvoie une instance de Move
        méthode de réflexion : 
            - génération d'une liste de coup possibles
            - évaluation des coups par min_max
            -sélection du coup le plus favorable
        """
        move_list = board.move_list(to_play)
        shuffle(move_list)
        if to_play == 'white' :
            best = -10000
            best_move = None
            for m in move_list :
                board.apply_move(m)
                eval = self.rec_minmax(board, "black", self.depth-1)
                board.unapply_move(m)
                if eval > best :
                    best_move, best = m, eval
        else :
            best = 10000
            best_move = None
            for m in move_list :
                board.apply_move(m)
                eval = self.rec_minmax(board, "white", self.depth-1)
                board.unapply_move(m)
                if eval < best :
                    best_move, best = m, eval
        return best_move
      
    def rec_minmax(self, board, to_play, depth,) :
        """
        Algo de minmax récursif !:
        entree : plateau, joueur profondeur
        renvoie l'évaluation d'une position 
        calcul l'évaluation en simulant tous les coups à une profondeur p, puis en utilsant une heuristique pour évaluer la position
        considère que chaque joueur tentera de jouer le meilleur coup possible (tentative d'alternativelent minimiser/maximiser le score blanc)
        donne des valeurs très fortes aux mats pour créer une aspiration
        """
        if depth == 0 : 
            return self.evaluate_board(board)
        else :
            move_list = board.move_list(to_play)
            if move_list == [] :
                if to_play =='white' and board.is_attacked_by(board.white_king, 'black') :
                    return -1000
                elif to_play =='black' and board.is_attacked_by(board.black_king, 'white') :
                    return 1000
                else :
                    return 0
            else :
                if to_play =='white' : 
                    best = -10000
                    for move in move_list : 
                        board.apply_move(move)
                        eval = self.rec_minmax(board,'black', depth-1)
                        board.unapply_move(move)
                        if eval > best : 
                            best = eval
                else :
                    best = 10000
                    for move in move_list : 
                        board.apply_move(move)
                        eval = self.rec_minmax(board, 'white', depth-1)
                        board.unapply_move(move)
                        if eval < best :
                            best = eval
                return best
        
    def evaluate_board(self, board) : 
        """
        évaluation naive d'une position
        entree : plateau
        renvoie le score des blancs dans la partie
        évalue le score via la différence de materiel
        """
        wscore = 0
        bscore = 0
        for piece in board.white_pieces() :
            wscore += piece.value
        for piece in board.black_pieces() :
            bscore += piece.value 
        return wscore - bscore
