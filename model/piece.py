from board import Board

class Piece:
    """
    Classe de base pour les pièces d'échecs
    """
    def __init__(self,color, position, board):
        self.color = color
        self.board = board
        self.position = position
        self.board.squares[position[0]][position[1]] = self
        self.marque = ''

    def __str__(self):
        i,j = self.position
        col = chr(ord('a') + j)
        return self.marque + col + str(i+1)
    
    def move(self, new_position):
        self.board.squares[self.position[0]][self.position[1]] = None
        self.board.squares[new_position[0]][new_position[1]] = self
        self.position = new_position
    
    def take(self, new_position):
        self.board.squares[self.position[0]][self.position[1]] = None
        self.board.squares[new_position[0]][new_position[1]] = self
        self.position = new_position
    
    def possible_moves(self):
        #future classe abstraite, à implémenter pour chaque type de pièce
        return []
    
class Pawn(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.marque = ''
        self.first_move = True
    
    def possible_moves(self):
        #ne gère pas les colisions/sorties de plateau pour le moment
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
            moves.append((i+ 2 * direction, j ))
        moves.append((i + direction, j ))
        return moves
    
    def move(self, new_position):
        super().move(new_position)
        self.first_move = False

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.marque = 'R'
        self.first_move = True

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.marque = 'N'

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.marque = 'B'

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.marque = 'Q'

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.marque = 'K'
        self.first_move = True


#tests temporaires
if __name__ == "__main__":
    a=Board()
    p = Pawn('white', (1,0), a)
    print(p.possible_moves())
    print(p, p.position)
    print(a.test_case((1,0)))
    p.move((3,0))
    print(p, p.position)
    print(a.test_case((3,0)))
    print(p.possible_moves())