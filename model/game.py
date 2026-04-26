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
        counter = 1
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
            to_play, counter = self.tour(to_play, type, counter)
    
    
    def tour (self, to_play, type, counter):
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
                s = "Possible moves for " + str(self.board.squares[i][j])  + " :"
                for i in range(len(possible_moves)):
                    s += "\nMove " + str(i) + ": " + str(possible_moves[i])
                print(s)
                move = input("select your move with its position (e.g 0 or 4)  in the list enter exit to cancel : ")
                if move == "exit":
                    continue 
                if move.isdigit() and int(move) < len(possible_moves):
                    m = possible_moves[int(move)]
                    valid = True
                else :
                    print("Invalid move, try again")
            #traitement du coup (a faire)
            if to_play == 'black':
                to_play = 'white'
                return to_play, counter +1
            else :
                to_play = 'black'
                return to_play, counter

#tests temporaires
if __name__ == "__main__":
    g = Game("test", "local", "none", "ongoing")
