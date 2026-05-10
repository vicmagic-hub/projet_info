from random import randint, shuffle
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
    
    def select_move(self, board, to_play) :
        #établissement des coups possibles
        move_list = board.move_list(to_play)
        #choix éclairé du coup
        n = len(move_list)
        k = randint(0, n-1)
        return move_list[k]
    
class MinmaxAI (AI) :
    """
    Classe de l'IA réfléchie
    algo de min max à profondeur variable
    heuristique qui s'appuie uniquement sur la valeur des pièces (1 à 9 pts par pièce)
    """
    def __init__(self, depth):
        self.name = "IAmoyendsefaireavoir"
        self.depth = depth
    
    def select_move(self, board, to_play) :
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
        print (best)
        return best_move
      
    def rec_minmax(self, board, to_play, depth,) :
        if depth == 0 : 
            return self.evaluate_board(board)
        else :
            move_list = board.move_list(to_play)
            if move_list == [] :
                if to_play =='white' and board.is_attacked_by(board.white_king, 'black') :
                    print("mat contre les blancs repéré")
                    print(board.white_king)
                    return -1000
                elif to_play =='black' and board.is_attacked_by(board.black_king, 'white') :
                    print("mat contre les noirs repéré")
                    print(board.black_king)
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
        wscore = 0
        bscore = 0
        for piece in board.white_pieces() :
            wscore += piece.value
        for piece in board.black_pieces() :
            bscore += piece.value 
        return wscore - bscore
