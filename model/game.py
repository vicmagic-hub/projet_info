from board import Board
from piece import Pawn, Rook, Knight, Bishop, Queen, King


class Game():
    def __init__(self, name, type,opponent, status):
        self.board = Board()
        self.name = name
        self.type = type
        self.opponent = opponent
        self.status = status
    
    def initialize(self):
        #initialisation des pions
        for j in range(8):
            pw = Pawn('white', (1, j), self.board)
            pb = Pawn('black', (6, j), self.board)
        #initialisation des Tours
        Rw1 = Rook('white', (0, 0), self.board)
        Rw2 = Rook('white', (0, 7), self.board)
        Rb1 = Rook('black', (7, 0), self.board)
        Rb2 = Rook('black', (7, 7), self.board)
        #initialisation des Cavaliers
        Nw1 = Knight('white', (0, 1), self.board)
        Nw2 = Knight('white', (0, 6), self.board)
        Nb1 = Knight('black', (7, 1), self.board)
        Nb2 = Knight('black', (7, 6), self.board)
        #initialisation des Fous
        Bw1 = Bishop('white', (0, 2), self.board)
        Bw2 = Bishop('white', (0, 5), self.board)
        Bb1 = Bishop('black', (7, 2), self.board)
        Bb2 = Bishop('black', (7, 5), self.board)
        #initialisation des Reines
        Qw = Queen('white', (0, 3), self.board)
        Qb = Queen('black', (7, 3), self.board)
        #initialisation des Rois
        Kw = King('white', (0, 4), self.board)
        Kb = King('black', (7, 4), self.board)


#tests temporaires
if __name__ == "__main__":
    g = Game("test", "local", "none", "ongoing")
    g.initialize()
    print(g.board)