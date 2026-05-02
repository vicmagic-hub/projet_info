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
    def possible_moves(self, moves):
        """
        méthode abstraite
        dépend du type de pièce
        construit une liste d'instanciation de Move possibles
        """
        pass

    @abstractmethod
    def attacked_cases(self):
        """
        méthode pour afficher les cases attaquées par la pièce
        renvoie une liste de position attaquées
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
        """
        super().__init__(color, position, board)
        self.marque = ''
        if self.color == 'white':
            self.symbol = '+p'
        else:
            self.symbol = '-p'
    
    def possible_moves(self, moves):
        """
        construit une liste d'instanciation de Move possibles
        Actuellement traité : 
            -Déplacement initial de deux cases
            -Déplacement d'une case
            -Collision avec une autre pièce
            -Prise
            -Promotion
            -Prise en passant
            -Mise en échec 
        COMPLET            
        """
        direction = 1
        if self.color == 'black': direction = -1
        move_list = []
        i, j = self.position
        #avancée classique d'une case
        if self.board.squares[i + direction][j] is None:
            #promotion
            if (i + direction == 7*(self.color=='white')):
                m = Move(self, self.position, (i + direction, j), 'promotion')
            #normal
            else:
                m = Move(self, self.position, (i + direction, j), 'classic')
            if self.board.simulate(m, moves):
                move_list.append(m)
            start_row = 1 if self.color == 'white' else 6
            if (i== start_row) and self.board.squares[i + 2 * direction][j] is None:
                #ajouter l'avancée de deux cases
                m = Move(self, self.position, (i + 2 * direction, j), 'doublepion')
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #gestion du EN-PASSANT
        row = 4 if self.color == 'white' else 3
        if i == row:
            #coté gauche pour les blancs, coté droit pour les noirs
            if j > 0 and self.board.squares[i][j-direction] is not None and isinstance(self.board.squares[i][j-direction], Pawn) and self.board.squares[i][j-direction].color != self.color and self.board.last_move.type == 'doublepion' and self.board.last_move.arrivee == (i, j-direction):
                m = Move(self, self.position, (i+direction, j-direction), 'enpassant', captured_piece = self.board.squares[i][j-direction])
                if self.board.simulate(m, moves):
                    move_list.append(m)
            #coté droit pour les blancs, coté gauche pour les noirs
            if j < 7 and self.board.squares[i][j+direction] is not None and isinstance(self.board.squares[i][j+direction], Pawn) and self.board.squares[i][j+direction].color != self.color and self.board.last_move.type == 'doublepion' and self.board.last_move.arrivee == (i, j+direction):
                m = Move(self, self.position, (i+direction, j+direction), 'enpassant', captured_piece = self.board.squares[i][j+direction])
                if self.board.simulate(m, moves):
                    move_list.append(m) 
        #gestion de la prise du coté gauche pour les blancs, du coté droit pour les noirs
        if j > 0 and self.board.squares[i + direction][j-1] is not None and self.board.test_color((i + direction, j-1)) != self.color:
            if (i + direction == 7*(self.color=='white')):
                m = Move(self, self.position, (i + direction, j-1), 'promoprise', captured_piece = self.board.squares[i + direction][j-1])
            else:
                m = Move(self, self.position, (i + direction, j-1), 'prise', captured_piece = self.board.squares[i + direction][j-1])
            if self.board.simulate(m, moves):
                move_list.append(m)
        #gestion de la prise du coté droit pour les blancs, du coté gauche pour les noirs
        if j < 7 and self.board.squares[i + direction][j+1] is not None and self.board.test_color((i + direction, j+1)) != self.color:
            if (i + direction == 7*(self.color=='white')):
                m = Move(self, self.position, (i + direction, j+1), 'promoprise', captured_piece = self.board.squares[i + direction][j+1])
            else:
                m = Move(self, self.position, (i + direction, j+1), 'prise', captured_piece = self.board.squares[i + direction][j+1])
            if self.board.simulate(m, moves):
                move_list.append(m)
        return move_list
    
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
    
    def attacked_cases(self):
        """
        renvoie la liste des cases attaquées
        """
        direction = 1
        if self.color == 'black' : direction = -1
        attacked = []
        i,j = self.position
        if j>0 : attacked.append((i+direction, j-1))
        if j<7 : attacked.append((i+direction, j+1))
        return attacked


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

    def possible_moves(self, moves):
        """
        construit une liste d'instanciation de Move possibles
        Actuellement traité : 
            -Déplacement classique
            -Prise
            -Mise en échec 
        COMPLET
        """
        move_list = []
        i, j = self.position
        #déplacement vertical vers dans l'ordre des ligne croissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7:
            if self.board.squares[i+k+1][j] is None:
                m = Move(self, self.position, (i+k+1, j), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i+k+1, j)) != self.color:
                    m = Move(self, self.position, (i+k+1, j), 'prise', captured_piece = self.board.squares[i+k+1][j])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        #déplacement vertical vers dans l'ordre des ligne décroissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0:
            if self.board.squares[i-k-1][j] is None:
                m = Move(self, self.position, (i-k-1, j), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i-k-1, j)) != self.color:
                    m = Move(self, self.position, (i-k-1, j), 'prise', captured_piece = self.board.squares[i-k-1][j])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        #déplacement horizontal vers dans l'ordre des ligne croissantes
        occupied = False
        k = 0
        while not occupied and j+k < 7:
            if self.board.squares[i][j+k+1] is None:
                m = Move(self, self.position, (i, j+k+1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i, j+k+1)) != self.color:
                    m = Move(self, self.position, (i, j+k+1), 'prise', captured_piece = self.board.squares[i][j+k+1])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        #déplacement horizontal vers dans l'ordre des ligne décroissantes
        occupied = False
        k = 0
        while not occupied and j-k > 0:
            if self.board.squares[i][j-k-1] is None:
                m = Move(self, self.position, (i, j-k-1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i, j-k-1)) != self.color:
                    m = Move(self, self.position, (i, j-k-1), 'prise', captured_piece = self.board.squares[i][j-k-1])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        return move_list
    
    def attacked_cases(self):
        """
        renvoie la liste des cases attaquées
        """
        attacked = []
        i, j = self.position
        #déplacement vertical vers dans l'ordre des ligne croissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7:
            if self.board.squares[i+k+1][j] is None or (isinstance(self.board.squares[i+k+1][j], King) and self.board.test_color((i+k+1, j)) != self.color):
                attacked.append((i+k+1, j))
            else :
                occupied = True
                attacked.append((i+k+1, j))
            k += 1
        #déplacement vertical vers dans l'ordre des ligne décroissantes
        occupied = False
        k = 0
        while not occupied and i-k >0 :
            if self.board.squares[i-k-1][j] is None or (isinstance(self.board.squares[i-k-1][j], King) and self.board.test_color((i-k-1, j)) != self.color):
                attacked.append((i-k-1, j))
            else :
                occupied = True
                attacked.append((i-k-1, j))
            k += 1
        #déplacement horizontal vers dans l'ordre des ligne croissantes
        occupied = False
        k = 0
        while not occupied and j+k < 7:
            if self.board.squares[i][j+k+1] is None or (isinstance(self.board.squares[i][j+k+1], King) and self.board.test_color((i, j+k+1)) != self.color):
                attacked.append((i, j+k+1))
            else :
                occupied = True
                attacked.append((i, j+k+1))
            k += 1
        #déplacement horizontal vers dans l'ordre des ligne décroissantes
        occupied = False
        k = 0
        while not occupied and j-k >0:
            if self.board.squares[i][j-k-1] is None or (isinstance(self.board.squares[i][j-k-1], King) and self.board.test_color((i, j-k-1)) != self.color):
                attacked.append((i, j-k-1))
            else :
                occupied = True
                attacked.append((i, j-k-1))
            k += 1
        return attacked

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

    def possible_moves(self,moves):
        move_list = []
        i, j = self.position
        # 8 déplacements possibles
        #1
        if (i+2)<=7 and (j+1)<=7 :
            if self.board.squares[i + 2][j + 1] is None:
                m = Move(self, self.position, (i + 2, j + 1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i + 2, j + 1)) != self.color:
                m = Move(self, self.position, (i + 2, j + 1), 'prise', captured_piece=self.board.squares[i + 2][j + 1])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #2
        if (i+2)<=7 and 0<=(j-1)<=7 :
            if self.board.squares[i + 2][j - 1] is None:
                m = Move(self, self.position, (i + 2, j - 1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i + 2, j - 1)) != self.color:
                m = Move(self, self.position, (i + 2, j - 1), 'prise', captured_piece=self.board.squares[i + 2][j - 1])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #3
        if (i+1)<=7 and 0<=(j-2)<=7 :
            if self.board.squares[i + 1][j - 2] is None:
                m = Move(self, self.position, (i + 1, j - 2), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i + 1, j - 2)) != self.color:
                m = Move(self, self.position, (i + 1, j - 2), 'prise', captured_piece=self.board.squares[i + 1][j - 2])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #4
        if 0<=(i-1)<=7 and 0<=(j-2)<=7 :
            if self.board.squares[i - 1][j - 2] is None:
                m = Move(self, self.position, (i - 1, j - 2), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i - 1, j - 2)) != self.color:
                m = Move(self, self.position, (i - 1, j - 2), 'prise', captured_piece=self.board.squares[i - 1][j - 2])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #5
        if 0<=(i-2)<=7 and 0<=(j-1)<=7 :
            if self.board.squares[i - 2][j - 1] is None:
                m = Move(self, self.position, (i - 2, j - 1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i - 2, j - 1)) != self.color:
                m = Move(self, self.position, (i - 2, j - 1), 'prise', captured_piece=self.board.squares[i - 2][j - 1])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #6
        if 0<=(i-2)<=7 and (j+1)<=7 :
            if self.board.squares[i - 2][j + 1] is None:
                m = Move(self, self.position, (i - 2, j + 1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i - 2, j + 1)) != self.color:
                m = Move(self, self.position, (i - 2, j + 1), 'prise', captured_piece=self.board.squares[i - 2][j + 1])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #7
        if 0<=(i-1)<=7 and (j+2)<=7 :
            if self.board.squares[i - 1][j + 2] is None:
                m = Move(self, self.position, (i - 1, j + 2), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i - 1, j + 2)) != self.color:
                m = Move(self, self.position, (i - 1, j + 2), 'prise', captured_piece=self.board.squares[i - 1][j + 2])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #8
        if (i+1)<=7 and (j+2)<=7 :
            if self.board.squares[i + 1][j + 2] is None:
                m = Move(self, self.position, (i + 1, j + 2), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i + 1, j + 2)) != self.color:
                m = Move(self, self.position, (i + 1, j + 2), 'prise', captured_piece=self.board.squares[i + 1][j + 2])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        return move_list
    
    def attacked_cases(self):
        """
        renvoie la liste des cases attaquées
        """
        attacked = []
        i, j = self.position
        # 8 déplacements possibles
        #1
        if (i+2)<=7 and (j+1)<=7 :
            attacked.append((i+2,j+1))
        #2
        if (i+2)<=7 and 0<=(j-1)<=7 :
            attacked.append((i+2,j-1))
        #3
        if (i+1)<=7 and 0<=(j-2)<=7 :
            attacked.append((i+1,j-2))
        #4
        if 0<=(i-1)<=7 and 0<=(j-2)<=7 :
            attacked.append((i-1,j-2))
        #5
        if 0<=(i-2)<=7 and 0<=(j-1)<=7 :
            attacked.append((i-2,j-1))
        #6
        if 0<=(i-2)<=7 and (j+1)<=7 :
            attacked.append((i-2,j+1))
        #7
        if 0<=(i-1)<=7 and (j+2)<=7 :
            attacked.append((i-1,j+2))
        #8
        if (i+1)<=7 and (j+2)<=7 :
            attacked.append((i+1,j+2))
        return attacked

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

    def possible_moves(self, moves):
        """
        construit une liste d'instanciation de Move possibles
        Actuellement traité : 
            -Déplacement classique
            -Prise
            -Mise en échec 
            COMPLET            
        """
        move_list = []
        i, j = self.position
        #déplacement diagonal vers dans l'ordre des ligne croissantes, colonnes croissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7 and j+k < 7:
            if self.board.squares[i+k+1][j+k+1] is None:
                m = Move(self, self.position, (i+k+1, j+k+1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i+k+1, j+k+1)) != self.color:
                    m = Move(self, self.position, (i+k+1, j+k+1), 'prise', captured_piece = self.board.squares[i+k+1][j+k+1])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        #déplacement diagonal vers dans l'ordre des ligne croissantes, colonnes décroissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7 and j-k > 0:
            if self.board.squares[i+k+1][j-k-1] is None:
                m = Move(self, self.position, (i+k+1, j-k-1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i+k+1, j-k-1)) != self.color:
                    m = Move(self, self.position, (i+k+1, j-k-1), 'prise', captured_piece = self.board.squares[i+k+1][j-k-1])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        #déplacement diagonal dans l'ordre des lignes décroissantes, colonnes croissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0 and j+k < 7:
            if self.board.squares[i-k-1][j+k+1] is None:
                m = Move(self, self.position, (i-k-1, j+k+1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i-k-1, j+k+1)) != self.color:
                    m = Move(self, self.position, (i-k-1, j+k+1), 'prise', captured_piece = self.board.squares[i-k-1][j+k+1])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        #déplacement diagonal dans l'ordre des lignes décroissantes, colonnes décroissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0 and j-k > 0:
            if self.board.squares[i-k-1][j-k-1] is None:
                m = Move(self, self.position, (i-k-1, j-k-1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i-k-1, j-k-1)) != self.color:
                    m = Move(self, self.position, (i-k-1, j-k-1), 'prise', captured_piece = self.board.squares[i-k-1][j-k-1])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        return move_list
    
    def attacked_cases(self):
        """
        renvoie la liste des cases attaquées
        """
        attacked = []
        i, j = self.position
        #déplacement diagonal vers dans l'ordre des ligne croissantes, colonnes croissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7 and j+k <7:
            if self.board.squares[i+k+1][j+k+1] is None or (isinstance(self.board.squares[i+k+1][j+k+1], King) and self.board.test_color((i+k+1, j+k+1)) != self.color):
                attacked.append((i+k+1, j+k+1))
            else :
                occupied = True
                attacked.append((i+k+1, j+k+1))
            k += 1
        #déplacement diagonal vers dans l'ordre des ligne croissantes, colonnes décroissantes
        occupied = False
        k = 0
        while not occupied and j-k >0 and i+k <7 :
            if self.board.squares[i+k+1][j-k-1] is None or (isinstance(self.board.squares[i+k+1][j-k-1], King) and self.board.test_color((i+k+1, j-k-1)) != self.color):
                attacked.append((i+k+1, j-k-1))
            else :
                occupied = True
                attacked.append((i+k+1, j-k-1))
            k += 1
        #déplacement diagonal dans l'ordre des lignes décroissantes, colonnes croissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0 and j+k < 7:
            if self.board.squares[i-k-1][j+k+1] is None or (isinstance(self.board.squares[i-k-1][j+k+1], King) and self.board.test_color((i-k-1, j+k+1)) != self.color):
                attacked.append((i-k-1, j+k+1))
            else :
                occupied = True
                attacked.append((i-k-1, j+k+1))
            k += 1
        #déplacement diagonal dans l'ordre des lignes décroissantes, colonnes décroissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0 and j-k > 0:
            if self.board.squares[i-k-1][j-k-1] is None or (isinstance(self.board.squares[i-k-1][j-k-1], King) and self.board.test_color((i-k-1, j-k-1)) != self.color):
                attacked.append((i-k-1, j-k-1))
            else :
                occupied = True
                attacked.append((i-k-1, j-k-1))
            k += 1
        return attacked

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


    def possible_moves(self, moves):
        """
        construit une liste d'instanciation de Move possibles
        Actuellement traité : 
            -Déplacement classique
            -Prise
            -Mise en échec 
        COMPLET
            
        """
        move_list = []
        i, j = self.position
        #déplacement vertical vers dans l'ordre des ligne croissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7:
            if self.board.squares[i+k+1][j] is None:
                m = Move(self, self.position, (i+k+1, j), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i+k+1, j)) != self.color:
                    m = Move(self, self.position, (i+k+1, j), 'prise', captured_piece = self.board.squares[i+k+1][j])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        #déplacement vertical vers dans l'ordre des ligne décroissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0:
            if self.board.squares[i-k-1][j] is None:
                m = Move(self, self.position, (i-k-1, j), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i-k-1, j)) != self.color:
                    m = Move(self, self.position, (i-k-1, j), 'prise', captured_piece = self.board.squares[i-k-1][j])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        #déplacement horizontal vers dans l'ordre des ligne croissantes
        occupied = False
        k = 0
        while not occupied and j+k < 7:
            if self.board.squares[i][j+k+1] is None:
                m = Move(self, self.position, (i, j+k+1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i, j+k+1)) != self.color:
                    m = Move(self, self.position, (i, j+k+1), 'prise', captured_piece = self.board.squares[i][j+k+1])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        #déplacement horizontal vers dans l'ordre des ligne décroissantes
        occupied = False
        k = 0
        while not occupied and j-k > 0:
            if self.board.squares[i][j-k-1] is None:
                m = Move(self, self.position, (i, j-k-1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i, j-k-1)) != self.color:
                    m = Move(self, self.position, (i, j-k-1), 'prise', captured_piece = self.board.squares[i][j-k-1])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        occupied = False
        k = 0
        while not occupied and i+k < 7 and j+k < 7:
            if self.board.squares[i+k+1][j+k+1] is None:
                m = Move(self, self.position, (i+k+1, j+k+1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i+k+1, j+k+1)) != self.color:
                    m = Move(self, self.position, (i+k+1, j+k+1), 'prise', captured_piece = self.board.squares[i+k+1][j+k+1])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        #déplacement diagonal vers dans l'ordre des ligne croissantes, colonnes décroissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7 and j-k > 0:
            if self.board.squares[i+k+1][j-k-1] is None:
                m = Move(self, self.position, (i+k+1, j-k-1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i+k+1, j-k-1)) != self.color:
                    m = Move(self, self.position, (i+k+1, j-k-1), 'prise', captured_piece = self.board.squares[i+k+1][j-k-1])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        #déplacement diagonal dans l'ordre des lignes décroissantes, colonnes croissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0 and j+k < 7:
            if self.board.squares[i-k-1][j+k+1] is None:
                m = Move(self, self.position, (i-k-1, j+k+1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i-k-1, j+k+1)) != self.color:
                    m = Move(self, self.position, (i-k-1, j+k+1), 'prise', captured_piece = self.board.squares[i-k-1][j+k+1])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        #déplacement diagonal dans l'ordre des lignes décroissantes, colonnes décroissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0 and j-k > 0:
            if self.board.squares[i-k-1][j-k-1] is None:
                m = Move(self, self.position, (i-k-1, j-k-1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            else:
                occupied = True
                if self.board.test_color((i-k-1, j-k-1)) != self.color:
                    m = Move(self, self.position, (i-k-1, j-k-1), 'prise', captured_piece = self.board.squares[i-k-1][j-k-1])
                    if self.board.simulate(m, moves):
                        move_list.append(m)
            k += 1
        return move_list

    def attacked_cases(self):
        """
        renvoie la liste des cases attaquées
        """
        attacked = []
        i, j = self.position
        #déplacement vertical vers dans l'ordre des ligne croissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7:
            if self.board.squares[i+k+1][j] is None or (isinstance(self.board.squares[i+k+1][j], King) and self.board.test_color((i+k+1, j)) != self.color):
                attacked.append((i+k+1, j))
            else :
                occupied = True
                attacked.append((i+k+1, j))
            k += 1
        #déplacement vertical vers dans l'ordre des ligne décroissantes
        occupied = False
        k = 0
        while not occupied and i-k >0 :
            if self.board.squares[i-k-1][j] is None or (isinstance(self.board.squares[i-k-1][j], King) and self.board.test_color((i-k-1, j)) != self.color):
                attacked.append((i-k-1, j))
            else :
                occupied = True
                attacked.append((i-k-1, j))
            k += 1
        #déplacement horizontal vers dans l'ordre des ligne croissantes
        occupied = False
        k = 0
        while not occupied and j+k < 7:
            if self.board.squares[i][j+k+1] is None or (isinstance(self.board.squares[i][j+k+1], King) and self.board.test_color((i, j+k+1)) != self.color):
                attacked.append((i, j+k+1))
            else :
                occupied = True
                attacked.append((i, j+k+1))
            k += 1
        #déplacement horizontal vers dans l'ordre des ligne décroissantes
        occupied = False
        k = 0
        while not occupied and j-k >0:
            if self.board.squares[i][j-k-1] is None or (isinstance(self.board.squares[i][j-k-1], King) and self.board.test_color((i, j-k-1)) != self.color):
                attacked.append((i, j-k-1))
            else :
                occupied = True
                attacked.append((i, j-k-1))
            k += 1
        #déplacement diagonal vers dans l'ordre des ligne croissantes, colonnes croissantes
        occupied = False
        k = 0
        while not occupied and i+k < 7 and j+k <7:
            if self.board.squares[i+k+1][j+k+1] is None or (isinstance(self.board.squares[i+k+1][j+k+1], King) and self.board.test_color((i+k+1, j+k+1)) != self.color):
                attacked.append((i+k+1, j+k+1))
            else :
                occupied = True
                attacked.append((i+k+1, j+k+1))
            k += 1
        #déplacement diagonal vers dans l'ordre des ligne croissantes, colonnes décroissantes
        occupied = False
        k = 0
        while not occupied and j-k >0 and i+k <7 :
            if self.board.squares[i+k+1][j-k-1] is None or (isinstance(self.board.squares[i+k+1][j-k-1], King) and self.board.test_color((i+k+1, j-k-1)) != self.color):
                attacked.append((i+k+1, j-k-1))
            else :
                occupied = True
                attacked.append((i+k+1, j-k-1))
            k += 1
        #déplacement diagonal dans l'ordre des lignes décroissantes, colonnes croissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0 and j+k < 7:
            if self.board.squares[i-k-1][j+k+1] is None or (isinstance(self.board.squares[i-k-1][j+k+1], King) and self.board.test_color((i-k-1, j+k+1)) != self.color):
                attacked.append((i-k-1, j+k+1))
            else :
                occupied = True
                attacked.append((i-k-1, j+k+1))
            k += 1
        #déplacement diagonal dans l'ordre des lignes décroissantes, colonnes décroissantes
        occupied = False
        k = 0
        while not occupied and i-k > 0 and j-k > 0:
            if self.board.squares[i-k-1][j-k-1] is None or (isinstance(self.board.squares[i-k-1][j-k-1], King) and self.board.test_color((i-k-1, j-k-1)) != self.color):
                attacked.append((i-k-1, j-k-1))
            else :
                occupied = True
                attacked.append((i-k-1, j-k-1))
            k += 1
        return attacked


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

        Regarder si le roi a bougé/si y'a une tour/si elle a bougé/si c'est vide entre les deux/Si les cases traversée par le roi sont attaquées/
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

    def possible_moves(self, moves):
        """
        construit une liste d'instanciation de Move possibles
        Actuellement traité : 
            -Déplacement
            -Prise
            -Mise en échec
            -Roque (gère aussi le mouvement de la tour concernée)
        COMPLET
            
        """
        move_list = []
        i, j = self.position
        # 8 déplacements possibles
        #1
        if (i+1)<=7 and (j)<=7 :
            if self.board.squares[i + 1][j] is None:
                m = Move(self, self.position, (i + 1, j), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i + 1, j)) != self.color:
                m = Move(self, self.position, (i + 1, j), 'prise', captured_piece=self.board.squares[i + 1][j])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #2
        if 0<=(i-1)<=7 and (j)<=7 :
            if self.board.squares[i - 1][j] is None:
                m = Move(self, self.position, (i - 1, j), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i - 1, j)) != self.color:
                m = Move(self, self.position, (i - 1, j), 'prise', captured_piece=self.board.squares[i - 1][j])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #3
        if (i)<=7 and 0<=(j+1)<=7 :
            if self.board.squares[i][j + 1] is None:
                m = Move(self, self.position, (i, j + 1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i, j + 1)) != self.color:
                m = Move(self, self.position, (i, j + 1), 'prise', captured_piece=self.board.squares[i][j + 1])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #4
        if 0<=(i)<=7 and 0<=(j-1)<=7 :
            if self.board.squares[i][j - 1] is None:
                m = Move(self, self.position, (i, j - 1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i, j - 1)) != self.color:
                m = Move(self, self.position, (i, j - 1), 'prise', captured_piece=self.board.squares[i][j - 1])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #5
        if 0<=(i+1)<=7 and 0<=(j+1)<=7 :
            if self.board.squares[i + 1][j + 1] is None:
                m = Move(self, self.position, (i + 1, j + 1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i + 1, j + 1)) != self.color:
                m = Move(self, self.position, (i + 1, j + 1), 'prise', captured_piece=self.board.squares[i + 1][j + 1])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #6
        if 0<=(i+1)<=7 and 0<=(j-1)<=7 :
            if self.board.squares[i + 1][j - 1] is None:
                m = Move(self, self.position, (i + 1, j - 1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i + 1, j - 1)) != self.color:
                m = Move(self, self.position, (i + 1, j - 1), 'prise', captured_piece=self.board.squares[i + 1][j - 1])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #7
        if 0<=(i-1)<=7 and (j+1)<=7 :
            if self.board.squares[i - 1][j + 1] is None:
                m = Move(self, self.position, (i - 1, j + 1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i - 1, j + 1)) != self.color:
                m = Move(self, self.position, (i - 1, j + 1), 'prise', captured_piece=self.board.squares[i - 1][j + 1])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #8
        if 0<=(i-1)<=7 and 0<=(j-1)<=7 :
            if self.board.squares[i - 1][j - 1] is None:
                m = Move(self, self.position, (i - 1, j - 1), 'classic')
                if self.board.simulate(m, moves):
                    move_list.append(m)
            elif self.board.test_color((i - 1, j - 1)) != self.color:
                m = Move(self, self.position, (i - 1, j - 2), 'prise', captured_piece=self.board.squares[i - 1][j - 1])
                if self.board.simulate(m, moves):
                    move_list.append(m)
        #Petit roque : Regarder si le roi a bougé/si y'a une tour/si elle a bougé/si c'est vide entre les deux/Si les cases traversée par le roi sont attaquées/
        if self.first_move :
            if isinstance(self.board.squares[i][j+3], Rook) :
                if self.board.squares[i][j+3].first_move :
                    if self.board.squares[i][j+1] is None and self.board.squares[i][j+2] is None :
                        if (not self.board.is_attacked_by((i,j+1), "white") and self.color=="black") or (not self.board.is_attacked_by((i,j+1), "black") and self.color=="white"):
                            if (not self.board.is_attacked_by((i,j), "white") and self.color=="black") or (not self.board.is_attacked_by((i,j), "black") and self.color=="white"):
                                m=Move(self, self.position, (i, j+2), 'castle')
                                if self.board.simulate(m, moves):
                                    move_list.append(m)
        # grand roque : Regarder si le roi a bougé/si y'a une tour/si elle a bougé/si c'est vide entre les deux/Si les cases traversée par le roi sont attaquées/
        if self.first_move:
            if isinstance(self.board.squares[i][j - 4], Rook):
                if self.board.squares[i][j - 4].first_move:
                    if self.board.squares[i][j - 1] is None and self.board.squares[i][j - 2] is None and self.board.squares[i][j - 3] is None:
                        if (not self.board.is_attacked_by((i, j - 1), "white") and self.color == "black") or (not self.board.is_attacked_by((i, j - 1), "black") and self.color == "white"):
                            if (not self.board.is_attacked_by((i, j), "white") and self.color == "black") or (not self.board.is_attacked_by((i, j), "black") and self.color == "white"):
                                m = Move(self, self.position, (i, j - 2), 'castle')
                                if self.board.simulate(m, moves):
                                    move_list.append(m)
        return move_list

    def attacked_cases(self):
        """
        renvoie la liste des cases attaquées
        """
        attacked = []
        i, j = self.position
        # 8 déplacements possibles
        #1
        if (i+1)<=7 and 0<=(j-1) :
            attacked.append((i+1,j-1))
        #2
        if (i+1)<=7 :
            attacked.append((i+1,j))
        #3
        if (i+1)<=7 and (j+1)<=7 :
            attacked.append((i+1,j+1))
        #4
        if 0<=(i-1) and 0<=(j-1) :
            attacked.append((i-1,j-1))
        #5
        if 0<=(i-1) :
            attacked.append((i-1,j))
        #6
        if 0<=(i-1) and (j+1)<=7 :
            attacked.append((i-1,j+1))
        #7
        if (j-1)>=0 :
            attacked.append((i,j-1))
        #8
        if (j+1)<=7 :
            attacked.append((i,j+1))
        return attacked