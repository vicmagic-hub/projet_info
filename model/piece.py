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
        self.first_move=None

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

    def attacked_cases(self):
        """
        méthode pour afficher les cases attaquées par la pièce
        """
        moves = self.possible_moves()
        attacked = []
        for m in moves:
            if m.type == 'prise' or m.type == 'enpassant' or m.type == 'promoprise':
                attacked.append(m.captured_piece.position)
            elif isinstance (m.piece, Pawn) == True : 
                pass
            else :
                attacked.append(m.arrivee)
        return attacked
    
class Pawn(Piece):
    """
    Classe pion : hérite de la classe pièce
    """
    def __init__(self, color, position, board):
        """
        Un pion est une pièce, avec : 
        -marque vide : son affichage renvoie simplement "a4" par exemple
        -le symbole p (+ ou - suivant la couleur)
        """
        super().__init__(color, position, board)
        self.marque = ''
        if self.color == 'white':
            self.symbol = '+p'
        else:
            self.symbol = '-p'
    
    def possible_moves(self):
        """
        construit une liste d'instanciation de Move possibles
        Actuellement traité : 
            -Déplacement initial de deux cases
            -Déplacement d'une case
            -Collision avec une autre pièce
            -Prise
            -Promotion
            -Prise en passant
        Non géré pour le moment : 
            -Mise en échec 
        """
        direction = 1
        if self.color == 'black': direction = -1
        moves = []
        i, j = self.position
        #avancée classique d'une case
        if self.board.squares[i + direction][j] is None:
            #promotion
            if (i + direction == 7*(self.color=='white')):
                m = Move(self, self.position, (i + direction, j), 'promotion')
            #normal
            else:
                m = Move(self, self.position, (i + direction, j), 'classic')
            moves.append(m)
            start_row = 1 if self.color == 'white' else 6
            if (i== start_row) and self.board.squares[i + 2 * direction][j] is None:
                #ajouter l'avancée de deux cases
                m = Move(self, self.position, (i + 2 * direction, j), 'doublepion')
                moves.append(m)
        #gestion du EN-PASSANT
        row = 4 if self.color == 'white' else 3
        if i == row:
            #coté gauche pour les blancs, coté droit pour les noirs
            if j > 0 and self.board.squares[i][j-direction] is not None and isinstance(self.board.squares[i][j-direction], Pawn) and self.board.squares[i][j-direction].color != self.color and self.board.last_move.type == 'doublepion' and self.board.last_move.arrivee == (i, j-direction):
                m = Move(self, self.position, (i+direction, j-direction), 'enpassant', captured_piece = self.board.squares[i][j-direction])
                moves.append(m)
            #coté droit pour les blancs, coté gauche pour les noirs
            print("on y est")
            if j < 7 and self.board.squares[i][j+direction] is not None and isinstance(self.board.squares[i][j+direction], Pawn) and self.board.squares[i][j+direction].color != self.color and self.board.last_move.type == 'doublepion' and self.board.last_move.arrivee == (i, j+direction):
                print("in")
                m = Move(self, self.position, (i+direction, j+direction), 'enpassant', captured_piece = self.board.squares[i][j+direction])
                moves.append(m)  
        #gestion de la prise du coté gauche pour les blancs, du coté droit pour les noirs
        if j > 0 and self.board.squares[i + direction][j-1] is not None and self.board.test_color((i + direction, j-1)) != self.color:
            if (i + direction == 7*(self.color=='white')):
                m = Move(self, self.position, (i + direction, j-1), 'promoprise', captured_piece = self.board.squares[i + direction][j-1])
            else:
                m = Move(self, self.position, (i + direction, j-1), 'prise', captured_piece = self.board.squares[i + direction][j-1])
            moves.append(m)
        #gestion de la prise du coté droit pour les blancs, du coté gauche pour les noirs
        if j < 7 and self.board.squares[i + direction][j+1] is not None and self.board.test_color((i + direction, j+1)) != self.color:
            if (i + direction == 7*(self.color=='white')):
                m = Move(self, self.position, (i + direction, j+1), 'promoprise', captured_piece = self.board.squares[i + direction][j+1])
            else:
                m = Move(self, self.position, (i + direction, j+1), 'prise', captured_piece = self.board.squares[i + direction][j+1])
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
        self.first_move = False

    def possible_moves(self):
        """
        construit une liste d'instanciation de Move possibles
        Actuellement traité : 
            -Déplacement classique
            -Prise
        Non géré pour le moment : 
            -Mise en échec 
        """
        moves = []
        i, j = self.position
        #déplacement vertical vers dans l'ordre des ligne croissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7:
            if self.board.squares[i+k+1][j] is None:
                m = Move(self, self.position, (i+k+1, j), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i+k+1, j)) != self.color:
                    m = Move(self, self.position, (i+k+1, j), 'prise', captured_piece = self.board.squares[i+k+1][j])
                    moves.append(m)
            k += 1
        #déplacement vertical vers dans l'ordre des ligne décroissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0:
            if self.board.squares[i-k-1][j] is None:
                m = Move(self, self.position, (i-k-1, j), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i-k-1, j)) != self.color:
                    m = Move(self, self.position, (i-k-1, j), 'prise', captured_piece = self.board.squares[i-k-1][j])
                    moves.append(m)
            k += 1
        #déplacement horizontal vers dans l'ordre des ligne croissantes
        occupied = False
        k = 0
        while not occupied and j+k < 7:
            if self.board.squares[i][j+k+1] is None:
                m = Move(self, self.position, (i, j+k+1), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i, j+k+1)) != self.color:
                    m = Move(self, self.position, (i, j+k+1), 'prise', captured_piece = self.board.squares[i][j+k+1])
                    moves.append(m)
            k += 1
        #déplacement horizontal vers dans l'ordre des ligne décroissantes
        occupied = False
        k = 0
        while not occupied and j-k > 0:
            if self.board.squares[i][j-k-1] is None:
                m = Move(self, self.position, (i, j-k-1), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i, j-k-1)) != self.color:
                    m = Move(self, self.position, (i, j-k-1), 'prise', captured_piece = self.board.squares[i][j-k-1])
                    moves.append(m)
            k += 1
        return moves

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

    def possible_moves(self):
        """
        construit une liste d'instanciation de Move possibles
        Actuellement traité : 
            -Déplacement classique
            -Prise
        Non géré pour le moment : 
            -Mise en échec 
        """
        moves = []
        i, j = self.position
        #déplacement diagonal vers dans l'ordre des ligne croissantes, colonnes croissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7 and j+k < 7:
            if self.board.squares[i+k+1][j+k+1] is None:
                m = Move(self, self.position, (i+k+1, j+k+1), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i+k+1, j+k+1)) != self.color:
                    m = Move(self, self.position, (i+k+1, j+k+1), 'prise', captured_piece = self.board.squares[i+k+1][j+k+1])
                    moves.append(m)
            k += 1
        #déplacement diagonal vers dans l'ordre des ligne croissantes, colonnes décroissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7 and j-k > 0:
            if self.board.squares[i+k+1][j-k-1] is None:
                m = Move(self, self.position, (i+k+1, j-k-1), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i+k+1, j-k-1)) != self.color:
                    m = Move(self, self.position, (i+k+1, j-k-1), 'prise', captured_piece = self.board.squares[i+k+1][j-k-1])
                    moves.append(m)
            k += 1
        #déplacement diagonal dans l'ordre des lignes décroissantes, colonnes croissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0 and j+k < 7:
            if self.board.squares[i-k-1][j+k+1] is None:
                m = Move(self, self.position, (i-k-1, j+k+1), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i-k-1, j+k+1)) != self.color:
                    m = Move(self, self.position, (i-k-1, j+k+1), 'prise', captured_piece = self.board.squares[i-k-1][j+k+1])
                    moves.append(m)
            k += 1
        #déplacement diagonal dans l'ordre des lignes décroissantes, colonnes décroissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0 and j-k > 0:
            if self.board.squares[i-k-1][j-k-1] is None:
                m = Move(self, self.position, (i-k-1, j-k-1), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i-k-1, j-k-1)) != self.color:
                    m = Move(self, self.position, (i-k-1, j-k-1), 'prise', captured_piece = self.board.squares[i-k-1][j-k-1])
                    moves.append(m)
            k += 1
        return moves

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


    def possible_moves(self):
        """
        construit une liste d'instanciation de Move possibles
        Actuellement traité : 
            -Déplacement classique
            -Prise
        Non géré pour le moment : 
            -Mise en échec 
        """
        moves = []
        i, j = self.position
        #déplacement vertical vers dans l'ordre des ligne croissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7:
            if self.board.squares[i+k+1][j] is None:
                m = Move(self, self.position, (i+k+1, j), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i+k+1, j)) != self.color:
                    m = Move(self, self.position, (i+k+1, j), 'prise', captured_piece = self.board.squares[i+k+1][j])
                    moves.append(m)
            k += 1
        #déplacement vertical vers dans l'ordre des ligne décroissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0:
            if self.board.squares[i-k-1][j] is None:
                m = Move(self, self.position, (i-k-1, j), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i-k-1, j)) != self.color:
                    m = Move(self, self.position, (i-k-1, j), 'prise', captured_piece = self.board.squares[i-k-1][j])
                    moves.append(m)
            k += 1
        #déplacement horizontal vers dans l'ordre des ligne croissantes
        occupied = False
        k = 0
        while not occupied and j+k < 7:
            if self.board.squares[i][j+k+1] is None:
                m = Move(self, self.position, (i, j+k+1), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i, j+k+1)) != self.color:
                    m = Move(self, self.position, (i, j+k+1), 'prise', captured_piece = self.board.squares[i][j+k+1])
                    moves.append(m)
            k += 1
        #déplacement horizontal vers dans l'ordre des ligne décroissantes
        occupied = False
        k = 0
        while not occupied and j-k > 0:
            if self.board.squares[i][j-k-1] is None:
                m = Move(self, self.position, (i, j-k-1), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i, j-k-1)) != self.color:
                    m = Move(self, self.position, (i, j-k-1), 'prise', captured_piece = self.board.squares[i][j-k-1])
                    moves.append(m)
            k += 1
        occupied = False
        k = 0
        while not occupied and i+k < 7 and j+k < 7:
            if self.board.squares[i+k+1][j+k+1] is None:
                m = Move(self, self.position, (i+k+1, j+k+1), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i+k+1, j+k+1)) != self.color:
                    m = Move(self, self.position, (i+k+1, j+k+1), 'prise', captured_piece = self.board.squares[i+k+1][j+k+1])
                    moves.append(m)
            k += 1
        #déplacement diagonal vers dans l'ordre des ligne croissantes, colonnes décroissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7 and j-k > 0:
            if self.board.squares[i+k+1][j-k-1] is None:
                m = Move(self, self.position, (i+k+1, j-k-1), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i+k+1, j-k-1)) != self.color:
                    m = Move(self, self.position, (i+k+1, j-k-1), 'prise', captured_piece = self.board.squares[i+k+1][j-k-1])
                    moves.append(m)
            k += 1
        #déplacement diagonal dans l'ordre des lignes décroissantes, colonnes croissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0 and j+k < 7:
            if self.board.squares[i-k-1][j+k+1] is None:
                m = Move(self, self.position, (i-k-1, j+k+1), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i-k-1, j+k+1)) != self.color:
                    m = Move(self, self.position, (i-k-1, j+k+1), 'prise', captured_piece = self.board.squares[i-k-1][j+k+1])
                    moves.append(m)
            k += 1
        #déplacement diagonal dans l'ordre des lignes décroissantes, colonnes décroissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0 and j-k > 0:
            if self.board.squares[i-k-1][j-k-1] is None:
                m = Move(self, self.position, (i-k-1, j-k-1), 'classic')
                moves.append(m)
            else:
                occupied = True
                if self.board.test_color((i-k-1, j-k-1)) != self.color:
                    m = Move(self, self.position, (i-k-1, j-k-1), 'prise', captured_piece = self.board.squares[i-k-1][j-k-1])
                    moves.append(m)
            k += 1
        return moves


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
        self.first_move = False
        i,j = m.arrivee
        if self.color == 'white':
            self.board.white_king = (i,j)
        else :
            self.board.black_king = (i,j)
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
