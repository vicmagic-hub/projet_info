from board import Board
from piece import Pawn, Rook, Knight, Bishop, Queen, King


class Game():
    def __init__(self, name, type,opponent, side):
        self.board = Board()
        self.name = name
        self.type = type
        self.opponent = opponent
        self.side = side
        to_play = 'white'
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
        for i in range(8): #pour la démo, en vrai ce sera "while not self.board.mate : "
            self.tour(to_play, type)
    
    def tour (self, to_play, type, counter = 0):
        if type == "local":
            valid = False
            print(f"{to_play}'s turn to play")
            while valid == False:
                s = input("Select the case of the piece you would like to move (e.g., e4 or d4) : ")
                i, j = int(s[1])-1, ord(s[0])-ord('a')
                if self.board.squares[i][j] is None or self.board.squares[i][j].color != to_play :
                    print("Invalid piece, try again")
                    continue
                possible_moves = self.board.squares[i][j].possible_moves()
                print(f"Possible moves for place {i, j}, piece {self.board.squares[i][j]}: ", possible_moves)
                move = input("select your move, enter 0  to cancel : ")
                if move == "0":
                    continue 
                if move in possible_moves :
                    valid = True
                    self.board.squares[i][j].move(move)
                else :
                    print("Invalid move, try again")
            #traitement du coup (a faire)
            if to_play == 'black':
                to_play = 'white'
            else :
                to_play = 'black'

#tests temporaires
if __name__ == "__main__":
    g = Game("test", "test", "none", "ongoing")
    print(g.board)
    g = Game("test", "local", "none", "ongoing")
