from abc import ABC, abstractmethod
from model.coup_encoder import Move

class Piece(ABC):
    """
    Classe abstraite pour les pièces d'échecs
    """
    def __init__(self,color, position, board):
        """
        initialisation d'un pièce : 
        entrées : Couleur, position, et échiquier
        Contrôle de la présence dans les limites de l'échiquier
        """
        self.color = color
        self.board = board
        self.position = position
        i,j = position
        assert 0 <= i < 8 and 0 <= j < 8, "Invalid position, out of bounds "
        self.board.squares[i][j] = self
        self.marque = 'PIECE'
        self.symbole = 'PIECE'
        self.first_move=None

    def __str__(self):
        """
        Affichage de la pièce
        renvoie "Nb5" ou "a3" par exemple
        """
        i,j = self.position
        col = chr(ord('a') + j)
        return self.marque + col + str(i+1)
    
    @abstractmethod
    def possible_moves(self):
        """
        méthode abstraite qui liste les coups légaux 
        renvoie une liste d'instanciation de Move contenenant les coups légaux de self
        """
        pass

    @abstractmethod
    def attacked_cases(self):
        """
        méthode abstraite qui liste les cases attaquées par une pièce
        renvoie une liste de coordonées de cases attaquées
        """
        pass

    def sliding_moves(self, vect_list) : 
        """
        Factorisation de possible_moves pour les pièces coulissantes (Dame, Fou, Tour)
        entrée : liste de vecteurs déplacements élémentaires à regarder, e.g (1,1) pour une diagonale
        renvoie une liste d'instanciation de Move contenenant les coups légaux de self
        """
        move_list = []
        i, j = self.position
        for di,dj in vect_list :
            occupied = False
            k = 0
            while not occupied and 0<= i+(k+1)*di <= 7 and  0 <= j+(k+1)*dj <= 7:
                targeted_color = self.board.test_color((i+(k+1)*di, j+(k+1)*dj))
                if targeted_color is None:
                    m = Move(self, self.position, (i+(k+1)*di, j+(k+1)*dj), 'classic')
                    if self.board.simulate(m):
                        move_list.append(m)
                else:
                    occupied = True
                    if targeted_color != self.color:
                        m = Move(self, self.position, (i+(k+1)*di, j+(k+1)*dj), 'prise', captured_piece = self.board.squares[i+(k+1)*di][j+(k+1)*dj])
                        if self.board.simulate(m):
                            move_list.append(m)
                k += 1
        return move_list
    
    def sliding_attack(self, vect_list) :
        """
        Factorisation de attacked_cases pour les pièces coulissantes (Dame, Fou, Tour)
        entrée : liste de vecteurs déplacements élémentaires à regarder, e.g (1,1) pour une diagonale
        renvoie une liste de coordonées de cases attaquées
        """
        attacked = []
        i, j = self.position
        for di,dj in vect_list : 
            occupied = False
            k = 0
            while not occupied and 0<= i+(k+1)*di <= 7 and  0 <= j+(k+1)*dj <= 7:
                targeted_color = self.board.test_color((i+(k+1)*di, j+(k+1)*dj))
                if targeted_color is None or (isinstance(self.board.squares[i+(k+1)*di][j+(k+1)*dj], King) and targeted_color != self.color):
                    attacked.append((i+(k+1)*di, j+(k+1)*dj))
                else :
                    occupied = True
                    attacked.append((i+(k+1)*di, j+(k+1)*dj))
                k += 1
        return attacked
    
    def listed_moves(self, vect_list) :
        """
        Factorisation de possible_moves pour les pièces à coups listés (Roi et Cavalier)
        entrée : liste de vecteurs déplacements à regarder, e.g (1,1)
        renvoie une liste d'instanciation de Move contenenant les coups légaux de self
        """
        move_list = []
        i, j = self.position
        for di,dj in vect_list :
            if 0<=(i+di)<=7 and 0<=(j+dj)<=7 :
                targeted_color = self.board.test_color((i+di, j+dj))
                if targeted_color is None:
                    m = Move(self, self.position, (i + di, j + dj), 'classic')
                    if self.board.simulate(m):
                        move_list.append(m)
                elif targeted_color != self.color:
                    m = Move(self, self.position, (i + di, j + dj), 'prise', captured_piece=self.board.squares[i + di][j + dj])
                    if self.board.simulate(m):
                        move_list.append(m)
        return move_list
    
    def listed_attack(self, vect_list):
        """
        Factorisation de attacked_cases pour les pièces à coups listés (Roi et Cavalier)
        entrée : liste de vecteurs déplacements à regarder, e.g (1,1)
        renvoie une liste de coordonées de cases attaquées
        """
        attacked = []
        i, j = self.position
        for di,dj in vect_list :
            if 0<= i+di <= 7 and  0 <= j+dj <= 7 :
                attacked.append((i+di,j+dj))
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
        méthode qui liste les coups légaux du pion
        renvoie une liste d'instanciation de Move contenenant les coups légaux du pion           
        """
        direction = 1
        if self.color == 'black': direction = -1
        move_list = []
        i, j = self.position
        #gestion de l'avancée
        if not self.board.test_case((i+direction, j)) :
            #gestion de l'avancée en promotion
            prom_row = 7 if self.color == 'white' else 0
            if i + direction == prom_row:
                m = Move(self, self.position, (i + direction, j), 'promotion')
                m.promotion_piece = 'Q'
                if self.board.simulate(m):
                    move_list.append(m)
                m = Move(self, self.position, (i + direction, j), 'promotion')
                m.promotion_piece = 'R'
                if self.board.simulate(m):
                    move_list.append(m)
                m = Move(self, self.position, (i + direction, j), 'promotion')
                m.promotion_piece = 'B'
                if self.board.simulate(m):
                    move_list.append(m)
                m = Move(self, self.position, (i + direction, j), 'promotion')
                m.promotion_piece = 'N'
                if self.board.simulate(m):
                    move_list.append(m)
            #avancée classique
            else:
                m = Move(self, self.position, (i + direction, j), 'classic')
                if self.board.simulate(m):
                    move_list.append(m)
            #avancée de deux cases
            start_row = 1 if self.color == 'white' else 6
            if (i == start_row) and not self.board.test_case((i + 2*direction, j)):
                m = Move(self, self.position, (i + 2*direction, j), 'doublepion')
                if self.board.simulate(m):
                    move_list.append(m)
        #gestion de la prise en passant
        en_passant_row = 4 if self.color == 'white' else 3
        if i == en_passant_row:
            #coté gauche pour les blancs, coté droit pour les noirs
            if 0 <= j-direction <= 7 :
                targeted_color = self.board.test_color((i,j-direction))
                if targeted_color is not None and isinstance(self.board.squares[i][j-direction], Pawn) and targeted_color != self.color and self.board.last_move.type == 'doublepion' and self.board.last_move.arrivee == (i, j-direction):
                    m = Move(self, self.position, (i+direction, j-direction), 'enpassant', captured_piece = self.board.squares[i][j-direction])
                    if self.board.simulate(m):
                        move_list.append(m)
            #coté droit pour les blancs, coté gauche pour les noirs
            if 0 <= j+ direction <= 7 :
                targeted_color = self.board.test_color((i,j+direction))
                if targeted_color is not None and isinstance(self.board.squares[i][j+direction], Pawn) and targeted_color != self.color and self.board.last_move.type == 'doublepion' and self.board.last_move.arrivee == (i, j+direction):
                    m = Move(self, self.position, (i+direction, j+direction), 'enpassant', captured_piece = self.board.squares[i][j+direction])
                    if self.board.simulate(m):
                        move_list.append(m) 
        #gestion de la prise classique du coté gauche pour les blancs, du coté droit pour les noirs
        if j > 0 :
            targeted_color = self.board.test_color((i+direction,j-1))
            if targeted_color is not None and targeted_color != self.color:
                #promoprise
                if (i + direction == 7*(self.color=='white')):
                    m = Move(self, self.position, (i + direction, j-1), 'promoprise', captured_piece = self.board.squares[i + direction][j-1])
                    m.promotion_piece = 'Q'
                    if self.board.simulate(m):
                        move_list.append(m)
                    m = Move(self, self.position, (i + direction, j-1), 'promoprise', captured_piece = self.board.squares[i + direction][j-1])
                    m.promotion_piece = 'R'
                    if self.board.simulate(m):
                        move_list.append(m)
                    m = Move(self, self.position, (i + direction, j-1), 'promoprise', captured_piece = self.board.squares[i + direction][j-1])
                    m.promotion_piece = 'B'
                    if self.board.simulate(m):
                        move_list.append(m)
                    m = Move(self, self.position, (i + direction, j-1), 'promoprise', captured_piece = self.board.squares[i + direction][j-1])
                    m.promotion_piece = 'N'
                    if self.board.simulate(m):
                        move_list.append(m)
                else:
                    m = Move(self, self.position, (i + direction, j-1), 'prise', captured_piece = self.board.squares[i + direction][j-1])
                    if self.board.simulate(m):
                        move_list.append(m)
        #gestion de la prise classique du coté droit pour les blancs, du coté gauche pour les noirs
        if j < 7 : 
            targeted_color = self.board.test_color((i+direction,j+1))
            if targeted_color is not None and targeted_color != self.color:
                #promoprise
                if (i + direction == 7*(self.color=='white')):
                    m = Move(self, self.position, (i + direction, j+1), 'promoprise', captured_piece = self.board.squares[i + direction][j+1])
                    m.promotion_piece = 'Q'
                    if self.board.simulate(m):
                        move_list.append(m)
                    m = Move(self, self.position, (i + direction, j+1), 'promoprise', captured_piece = self.board.squares[i + direction][j+1])
                    m.promotion_piece = 'R'
                    if self.board.simulate(m):
                        move_list.append(m)
                    m = Move(self, self.position, (i + direction, j+1), 'promoprise', captured_piece = self.board.squares[i + direction][j+1])
                    m.promotion_piece = 'B'
                    if self.board.simulate(m):
                        move_list.append(m)
                    m = Move(self, self.position, (i + direction, j+1), 'promoprise', captured_piece = self.board.squares[i + direction][j+1])
                    m.promotion_piece = 'N'
                    if self.board.simulate(m):
                        move_list.append(m)
                else:
                    m = Move(self, self.position, (i + direction, j+1), 'prise', captured_piece = self.board.squares[i + direction][j+1])
                    if self.board.simulate(m):
                        move_list.append(m)
        return move_list
    
    def attacked_cases(self):
        """
        méthode qui liste les cases attaquées par le pion
        renvoie une liste de coordonées de cases attaquées
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
        -une variable first_move différente de None pour marquer la possibilité de roquer
        """
        super().__init__(color, position, board)
        self.marque = 'R'
        if self.color == 'white':
            self.symbol = '+R'
        else:
            self.symbol = '-R'
        self.first_move = True


    def possible_moves(self):
        """
        méthode qui liste les coups légaux 
        renvoie une liste d'instanciation de Move contenenant les coups légaux de la tour
        la tour est une pièce coulissante donc s'appuie sur sliding_moves
        fournit à sliding_moves les vecteurs des déplacements horizontaux et verticaux
        """
        return self.sliding_moves([(1,0),(-1,0),(0,1),(0,-1)])   
    
    def attacked_cases(self):
        """
        méthode qui liste les cases attaquées par la tour
        renvoie une liste de coordonées de cases attaquées
        la tour est une pièce coulissante donc s'appuie sur sliding_attack
        fournit à sliding_attack les vecteurs des déplacements horizontaux et verticaux
        """
        return self.sliding_attack([(1,0),(-1,0),(0,1),(0,-1)])


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

    def possible_moves(self):
        """
        méthode qui liste les coups légaux 
        renvoie une liste d'instanciation de Move contenenant les coups légaux du cavalier
        le cavalier est une pièce à coups listés donc s'appuie sur listed_moves
        fournit à listed_moves les 8 déplacements possibles du cavalier
        """
        return self.listed_moves([(2, 1), (2, -1), (1,-2), (-1,-2), (-2,-1), (-2,1), (-1, 2), (1,2)])
    
    def attacked_cases(self):
        """
        méthode qui liste les cases attaquées par le cavalier
        renvoie une liste de coordonées de cases attaquées
        le cavalier est une pièce à coups listés donc s'appuie sur listed_attack
        fournit à listed_attack les 8 déplacements possibles du cavalier
        """
        return self.listed_attack([(2, 1), (2, -1), (1,-2), (-1,-2), (-2,-1), (-2,1), (-1, 2), (1,2)])


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

    def possible_moves(self):
        """
        méthode qui liste les coups légaux 
        renvoie une liste d'instanciation de Move contenenant les coups légaux du fou
        le fou est une pièce coulissante donc s'appuie sur sliding_moves
        fournit à sliding_moves les vecteurs des déplacements diagonaux
        """
        return self.sliding_moves([(1,1),(1,-1),(-1,-1),(-1,1)])
    
    def attacked_cases(self):
        """
        méthode qui liste les cases attaquées par le fou
        renvoie une liste de coordonées de cases attaquées
        le fou est une pièce coulissante donc s'appuie sur sliding_attack
        fournit à sliding_attack les vecteurs des déplacements diagonaux
        """
        return self.sliding_attack([(1,1),(1,-1),(-1,-1),(-1,1)])


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

    def possible_moves(self):
        """
        méthode qui liste les coups légaux 
        renvoie une liste d'instanciation de Move contenenant les coups légaux de la dame
        la dame est une pièce coulissante donc s'appuie sur sliding_moves
        fournit à sliding_moves les vecteurs des déplacements diagonaux, horizontaux et verticaux
        """
        return self.sliding_moves([(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)])

    def attacked_cases(self):
        """
        méthode qui liste les cases attaquées par la dame
        renvoie une liste de coordonées de cases attaquées
        la dame est une pièce coulissante donc s'appuie sur sliding_attack
        fournit à sliding_attack les vecteurs des déplacements diagonaux, horizontaux et verticaux
        """
        return self.sliding_attack([(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)])


class King(Piece):
    """
    Classe roi : hérite de la classe pièce
    """
    def __init__(self, color, position, board):
        """
        Un roi est une pièce, avec : 
        -marque 'K' pour King : son affichage renvoie "Ka4" par exemple
        -le symbole K (+ ou - suivant la couleur)
        -une variable first_move différente de None pour marquer la possibilité de roquer
        """
        super().__init__(color, position, board)
        self.marque = 'K'
        if self.color == 'white':
            self.symbol = '+K'
        else:
            self.symbol = '-K'
        self.first_move = True

    def possible_moves(self):
        """
        méthode qui liste les coups légaux 
        renvoie une liste d'instanciation de Move contenenant les coups légaux du Roi
        le Roi est une pièce à coups listés donc s'appuie sur listed_moves
        fournit à listed_moves les 8 déplacements possibles du Roi
        ajoute ensuite les deux roques, si disponibles
        """
        i, j = self.position
        #ajout des mouvements classique
        move_list = self.listed_moves([(1,1), (0,1), (-1,1),(-1,0), (-1,-1), (0,-1), (1,-1), (1,0)])
        #Petit roque sous conditions
        if self.first_move and isinstance(self.board.squares[i][j+3], Rook) and self.board.squares[i][j+3].first_move and not self.board.test_case((i,j+1)) and not self.board.test_case((i,j+2)) :
            if (not self.board.is_attacked_by((i,j+1), "white") and self.color=="black") or (not self.board.is_attacked_by((i,j+1), "black") and self.color=="white"):
                if (not self.board.is_attacked_by((i,j), "white") and self.color=="black") or (not self.board.is_attacked_by((i,j), "black") and self.color=="white"):
                    m=Move(self, self.position, (i, j+2), 'castle')
                    if self.board.simulate(m):
                        move_list.append(m)
        # grand roque sous conditions
        if self.first_move and isinstance(self.board.squares[i][j - 4], Rook) and self.board.squares[i][j - 4].first_move and not self.board.test_case((i,j - 1)) and not self.board.test_case((i,j - 2)) and not self.board.test_case((i,j - 3)):
                        if (not self.board.is_attacked_by((i, j - 1), "white") and self.color == "black") or (not self.board.is_attacked_by((i, j - 1), "black") and self.color == "white"):
                            if (not self.board.is_attacked_by((i, j), "white") and self.color == "black") or (not self.board.is_attacked_by((i, j), "black") and self.color == "white"):
                                m = Move(self, self.position, (i, j - 2), 'castle')
                                if self.board.simulate(m):
                                    move_list.append(m)
        return move_list

    def attacked_cases(self):
        """
        méthode qui liste les cases attaquées par le Roi
        renvoie une liste de coordonées de cases attaquées
        le Roi est une pièce à coups listés donc s'appuie sur listed_attack
        fournit à listed_attack les 8 déplacements possibles du Roi
        """
        return self.listed_attack([(1,1), (0,1), (-1,1),(-1,0), (-1,-1), (0,-1), (1,-1), (1,0)])
