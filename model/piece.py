import board

class Piece:
    """
    Classe de base pour les pièces d'échecs
    """
    def __init__(self,color, position):
        self.color = color
        self.position = position 
        self.marque = ''

    def __str__(self):
        i,j = self.position
        col = chr(ord('a') + j)
        return self.marque + col + str(i+1)
    
    def move(self, new_position):
        """
        Méthode pour déplacer la pièce à une nouvelle position
        Pour le moment elle est très con
        Mais bientôt elle sera abstraite
        Chaque pièce aura sa méthode de déplacement spécifique
        """
        self.position = new_position
    
    def take(self, new_position):
        """
        Méthode pour prendre une pièce adverse
        Pour le moment elle est très con
        Mais bientôt elle sera abstraite
        Chaque pièce aura sa méthode de prise spécifique
        """
        self.position = new_position
    
    def possible_moves(self):
        """
        Méthode pour obtenir les mouvements possibles de la pièce
        Pour le moment elle est très con
        Mais bientôt elle sera abstraite
        Chaque pièce aura sa méthode de mouvements possibles spécifique
        """
        return []
    
class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.marque = 'p'
        self.first_move = True
    
    def possible_moves(self):
        #ne gère pas les colisions/sorties de plateau pour le moment
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


a=board.Board()
p = Pawn('white', (1,0))
a.board[1][0] = p
print(p.possible_moves())
print(p, p.position)
p.move((3,0))
print(p, p.position)