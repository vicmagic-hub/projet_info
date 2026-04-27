from abc import abstractmethod

from board import Board
from coup_encoder import Move

class Piece:
    """
    Classe abstraite pour les pièces d'échecs
    """
    def __init__(self,color, position, board):
        """
        initialisation d'un pièce : 
        Couleur, position, et échiquier
        Contrôle de la présence dans les limites de l'échiquier
        """
        self.color = color
        self.board = board
        self.position = position
        i,j = position
        assert 0 <= i < 8 and 0 <= j < 8, "Invalid position, out of bounds "
        self.board.squares[i][j] = self
        self.marque = 'PIECE'

    def __str__(self):
        """
        Fonction d'affichage de la pièce
        renvoie "Nb5" ou "a3" par exemple
        """
        i,j = self.position
        col = chr(ord('a') + j)
        return self.marque + col + str(i+1)
    
    def move(self, m):
        """
        méthode générale, évolue pour certaines pièces (ex : promotion du pion, roque du roi)
        reçoit une instanciation de Move
        traite le coup
        ATENTION : move ne connaît pas les règles du jeu, il se contente de réaliser un coup.
        C'est possible_moves qui fera le tri des coups possibles ou non
        """
        i,j = m.arrivee
        k,l = m.piece.position
        self.board.squares[k][l] = None
        self.board.squares[i][j] = self
        self.position = (i,j)
    
    @abstractmethod
    def possible_moves(self):
        """
        méthode abstraite
        dépend du type de pièce
        construit une liste d'instanciation de Move possibles
        """
        pass
    
class Pawn(Piece):
    """
    Classe pion : hérite de la classe pièce
    """
    def __init__(self, color, position, board):
        """
        Un pion est une pièce, avec : 
        -marque vide : son affichage renvoie simplement "a4" par exemple
        -le symbole p (+ ou - suivant la couleur)
        -une variable first_move pour la possibilité d'avancer de deux cases
        """
        super().__init__(color, position, board)
        self.marque = ''
        if self.color == 'white':
            self.symbol = '+p'
        else:
            self.symbol = '-p'
        self.first_move = True
    
    def possible_moves(self):
        """
        construit une liste d'instanciation de Move possibles
        Actuellement traité : 
            -Déplacement initial de deux cases
            -Déplacement d'une case
        Non géré pour le moment : 
            -Promotion
            -Collision avec une autre pièce
            -Prise
            -Prise en passant
            -Mise en échec 
        """
        direction = 1
        if self.color == 'black': direction = -1
        moves = []
        i, j = self.position
        if self.first_move:
            #ajouter l'avancée de deux cases
            m = Move(self.board, self.position, (i + 2 * direction, j), 'classic')
            moves.append(m)
        m = Move(self.board, self.position, (i + direction, j), 'classic')
        moves.append(m)
        return moves
    
    def move(self, m):
        """
        reçoit une instanciation de Move
        traite le mouvement
        Actuellement traité : 
            -Déplacement simple d'une ou deux cases
            -Prise
            -Prise en passant
            -Promotion
        Complet (en théorie)
        """
        super().move(m)
        i,j = m.arrivee
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
        else : 
            if m.type == 'enpassant' :
                if self.color == 'white':
                    self.board.squares[i-1][j] = None
                else:
                    self.board.squares[i+1][j] = None


class Rook(Piece):
    """
    Classe tour : hérite de la classe pièce
    """
    def __init__(self, color, position, board):
        """
        Une tour est une pièce, avec : 
        -marque 'R' pour Rook : son affichage renvoie "Ra4" par exemple
        -le symbole R (+ ou - suivant la couleur)
        -une variable first_move pour la possibilité de roquer
        """
        super().__init__(color, position, board)
        self.marque = 'R'
        if self.color == 'white':
            self.symbol = '+R'
        else:
            self.symbol = '-R'
        self.first_move = True
    
    def move(self, m):
        """
        reçoit une instanciation de Move
        traite le mouvement
        Actuellement traité : 
            -Déplacement
            -Prise
            -Roque(traité par le Roi)
        Complet (en théorie)
        """
        super().move(m)

class Knight(Piece):
    """
    Classe cavalier : hérite de la classe pièce
    """
    def __init__(self, color, position, board):
        """
        Un cavalier est une pièce, avec : 
        -marque 'N' pour Knight : son affichage renvoie "Na4" par exemple
        -le symbole N (+ ou - suivant la couleur)
        """
        super().__init__(color, position, board)
        self.marque = 'N'
        if self.color == 'white':
            self.symbol = '+N'
        else:
            self.symbol = '-N'
    
    def move(self, m):
        """
        reçoit une instanciation de Move
        traite le mouvement
        Actuellement traité : 
            -Déplacement
            -Prise
        Complet (en théorie)
        """
        super().move(m)

class Bishop(Piece):
    """
    Classe fou : hérite de la classe pièce
    """
    def __init__(self, color, position, board):
        """
        Un fou est une pièce, avec : 
        -marque 'B' pour Bishop : son affichage renvoie "Ba4" par exemple
        -le symbole B (+ ou - suivant la couleur)
        """
        super().__init__(color, position, board)
        self.marque = 'B'
        if self.color == 'white':
            self.symbol = '+B'
        else:
            self.symbol = '-B'
    
    def move(self, m):
        """
        reçoit une instanciation de Move
        traite le mouvement
        Actuellement traité : 
            -Déplacement
            -Prise
        Complet (en théorie)
        """
        super().move(m)

class Queen(Piece):
    """
    Classe dame : hérite de la classe pièce
    """
    def __init__(self, color, position, board):
        """
        Une dame est une pièce, avec : 
        -marque 'Q' pour Queen : son affichage renvoie "Qa4" par exemple
        -le symbole Q (+ ou - suivant la couleur)
        """
        super().__init__(color, position, board)
        self.marque = 'Q'
        if self.color == 'white':
            self.symbol = '+Q'
        else:
            self.symbol = '-Q'
    
    def move(self, m):
        """
        reçoit une instanciation de Move
        traite le mouvement
        Actuellement traité : 
            -Déplacement
            -Prise
        Complet (en théorie)
        """
        super().move(m)

class King(Piece):
    """
    Classe roi : hérite de la classe pièce
    """
    def __init__(self, color, position, board):
        """
        Un roi est une pièce, avec : 
        -marque 'K' pour King : son affichage renvoie "Ka4" par exemple
        -le symbole K (+ ou - suivant la couleur)
        -une variable first_move pour la possibilité de roquer
        """
        super().__init__(color, position, board)
        self.marque = 'K'
        if self.color == 'white':
            self.symbol = '+K'
        else:
            self.symbol = '-K'
        self.first_move = True
    
    def move(self, m):
        """
        reçoit une instanciation de Move
        traite le mouvement
        Actuellement traité : 
            -Déplacement
            -Prise
            -Roque (gère aussi le mouvement de la tour concernée)
        Complet (en théorie)
        """
        super().move(m)
        i,j = m.arrivee
        if m.type == 'castle':
            #gestion du roque
            if j == 6:
                #petit roque
                #mouvement de la tour
                self.board.squares[i][5] = self.board.squares[i][7]
                self.board.squares[i][5].position = (i,5)
                self.board.squares[i][7] = None
                
            else:
                #grand roque
                #mouvement de la tour
                self.board.squares[i][3] = self.board.squares[i][0]
                self.board.squares[i][3].position = (i,3)
                self.board.squares[i][0] = None
