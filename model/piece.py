from abc import abstractmethod

from board import Board
from coup_encoder import Move

class Piece:
    """
    Classe de base pour les pièces d'échecs
    """
    def __init__(self,color, position, board):
        self.color = color
        self.board = board
        self.position = position
        i,j = position
        assert 0 <= i < 8 and 0 <= j < 8, "Invalid position, out of bounds "
        self.board.squares[i][j] = self
        self.marque = 'PIECE'

    def __str__(self):
        i,j = self.position
        col = chr(ord('a') + j)
        return self.marque + col + str(i+1)
    
    @abstractmethod
    def move(self, m):
        pass
    
    @abstractmethod
    def possible_moves(self):
        pass
    
class Pawn(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.marque = ''
        if self.color == 'white':
            self.symbol = '+p'
        else:
            self.symbol = '-p'
        self.first_move = True
    
    def possible_moves(self):
        #proto methode
        #ne gère pas les prises pour le moment
        #ne gère pas la promotion pour le moment
        """
        Méthode pour obtenir les mouvements possibles du pion
        Renvoie une liste de futures positions possibles pour le pion
        """
        direction = 1
        if self.color == 'black': direction = -1
        moves = []
        i, j = self.position
        if self.first_move:
            m = Move(self.board, self.position, (i + 2 * direction, j), 'classic')
            moves.append(m)
        m = Move(self.board, self.position, (i + direction, j), 'classic')
        moves.append(m)
        return moves
    
    def move(self, m):
        i,j = m.arrivee
        self.board.squares[self.position[0]][self.position[1]] = None
        if m.type == 'promotion' or m.type == 'promoprise':
            #gestion de la promotion
            new_piece = input("Enter the piece you want to promote to (Q, R, B, N) : ")
            m.promotion_piece = new_piece
            if new_piece == 'Q':
                self.board.squares[i][j] = Queen(self.color, (i,j), self.board)
            elif new_piece == 'R':
                self.board.squares[i][j] = Rook(self.color, (i,j), self.board)  
            elif new_piece == 'B':
                self.board.squares[i][j] = Bishop(self.color, (i,j), self.board)
            elif new_piece == 'N':
                self.board.squares[i][j] = Knight(self.color, (i,j), self.board)
        elif m.type == 'enpassant' :
            self.board.squares[i][j] = self
            self.position = (i,j)
            if self.color == 'white':
                self.board.squares[i-1][j] = None
        else:
            self.board.squares[i][j] = self
            self.position = (i,j)
            self.first_move = False

class Rook(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.marque = 'R'
        if self.color == 'white':
            self.symbol = '+R'
        else:
            self.symbol = '-R'
        self.first_move = True
    
    def move(self, m):
        i,j = m.arrivee
        self.board.squares[self.position[0]][self.position[1]] = None
        self.board.squares[i][j] = self
        self.position = (i,j)

class Knight(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.marque = 'N'
        if self.color == 'white':
            self.symbol = '+N'
        else:
            self.symbol = '-N'
    
    def move(self, m):
        i,j = m.arrivee
        self.board.squares[self.position[0]][self.position[1]] = None
        self.board.squares[i][j] = self
        self.position = (i,j)

class Bishop(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.marque = 'B'
        if self.color == 'white':
            self.symbol = '+B'
        else:
            self.symbol = '-B'
    
    def move(self, m):
        i,j = m.arrivee
        self.board.squares[self.position[0]][self.position[1]] = None
        self.board.squares[i][j] = self
        self.position = (i,j)

class Queen(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.marque = 'Q'
        if self.color == 'white':
            self.symbol = '+Q'
        else:
            self.symbol = '-Q'
    
    def move(self, m):
        i,j = m.arrivee
        self.board.squares[self.position[0]][self.position[1]] = None
        self.board.squares[i][j] = self
        self.position = (i,j)

class King(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.marque = 'K'
        if self.color == 'white':
            self.symbol = '+K'
        else:
            self.symbol = '-K'
        self.first_move = True
    
    def move(self, m):
        i,j = m.arrivee
        self.board.squares[self.position[0]][self.position[1]] = None
        if m.type == 'castle':
            #gestion du roque
            if j == 6:
                #petit roque 
                self.board.squares[i][j] = self
                self.board.squares[i][5] = self.board.squares[i][7]
                self.board.squares[i][5].position = (i,5)
                self.board.squares[i][7] = None
                
            else:
                #grand roque
                self.board.squares[i][j] = self
                self.board.squares[i][3] = self.board.squares[i][0]
                self.board.squares[i][3].position = (i,3)
                self.board.squares[i][0] = None
        else:
            self.board.squares[i][j] = self
            self.position = (i,j)