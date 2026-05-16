from model.piece import Pawn, Queen, Rook, Bishop, Knight, King

class Board:
    """
    Classe pour l'échiquier
    """
    def __init__(self):
        """
        initialisation d'un échiquier : 
        création de squares pour stocker les pièces
        création de la variable end (fin de partie)
        création de la variable last_move pour stocker le dernier coup joué, pour la gestion d'en passant
        """
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.end = False
        self.last_move = None
        self.trait = 'white'      
    
    def place_piece(self) :
        """
        initialisation des pièces sur l'échiquier : format standard
        creation des variables white_king et black_king, pour accéder plus rapidement aux positions des rois
        """
        #initialisation des pions
        for j in range(8):
            pw = Pawn('white', (1, j), self)
            pb = Pawn('black', (6, j), self)
        #initialisation des Tours
        Rw1 = Rook('white', (0, 0), self)
        Rw2 = Rook('white', (0, 7), self)
        Rb1 = Rook('black', (7, 0), self)
        Rb2 = Rook('black', (7, 7), self)
        #initialisation des Cavaliers
        Nw1 = Knight('white', (0, 1), self)
        Nw2 = Knight('white', (0, 6), self)
        Nb1 = Knight('black', (7, 1), self)
        Nb2 = Knight('black', (7, 6), self)
        #initialisation des Fous
        Bw1 = Bishop('white', (0, 2), self)
        Bw2 = Bishop('white', (0, 5), self)
        Bb1 = Bishop('black', (7, 2), self)
        Bb2 = Bishop('black', (7, 5), self)
        #initialisation des Reines
        Qw = Queen('white', (0, 3), self)
        Qb = Queen('black', (7, 3), self)
        #initialisation des Rois
        Kw = King('white', (0, 4), self)
        self.white_king = (0,4)
        Kb = King('black', (7, 4), self)
        self.black_king = (7,4)
    
    def apply_move(self, m):
        """
        méthode qui reçoit une instanciation de Move, lui rentre les données nécessaire à l'annulation, et traite le coup
        entrée : instance de la classe Move
        !! ATENTION !! : self.apply_move(m)  se contente de réaliser un coup, sans vérifier qu'il soit légal.
        """
        #import de variables
        piece = m.piece
        i,j = m.arrivee
        k,l = m.piece.position
        #sauvegarde des variables actuelles
        m.prev_last_move = self.last_move
        m.prev_piece_first_move = piece.first_move
        m.prev_white_king = self.white_king
        m.prev_black_king = self.black_king
        #traitement classique
        self.squares[k][l] = None
        self.squares[i][j] = piece
        piece.position = (i,j)
        if piece.first_move is not None :
            piece.first_move = False
        #traitements particuliers :
            #gestion de la promotion
        if m.type == 'promotion' or m.type == 'promoprise':
            if m.promotion_piece == 'Q':
                self.squares[i][j] = Queen(piece.color, (i,j), self)
            elif m.promotion_piece == 'R':
                self.squares[i][j] = Rook(piece.color, (i,j), self)  
            elif m.promotion_piece == 'B':
                self.squares[i][j] = Bishop(piece.color, (i,j), self)
            elif m.promotion_piece == 'N':
                self.squares[i][j] = Knight(piece.color, (i,j), self)
        else : 
            #gestion de la prise en passant
            if m.type == 'enpassant' :
                if piece.color == 'white':
                    self.squares[i-1][j] = None
                else:
                    self.squares[i+1][j] = None
            #enregistrement de la position du roi
        if isinstance(piece, King) :
            if piece.color == 'white':
                self.white_king = (i,j)
            else :
                self.black_king = (i,j)
            #gestion du roque
        if m.type == 'castle':
            #si l'on roque, c'était forcément le premier coup de la tour
            m.prev_tour_first_move = True
            if j == 6:
                #petit roque
                #mouvement de la tour
                self.squares[i][5] = self.squares[i][7]
                self.squares[i][5].position = (i,5)
                self.squares[i][5].first_move = False
                self.squares[i][7] = None   
            else:
                #grand roque
                #mouvement de la tour
                self.squares[i][3] = self.squares[i][0]
                self.squares[i][3].position = (i,3)
                self.squares[i][3].first_move = False
                self.squares[i][0] = None
        self.last_move = m
        if m.piece.color == 'white' : 
            self.trait = 'black'
        else : 
            self.trait = 'white'

    def unapply_move(self, m): 
        """
        méthode qui reçoit le dernier coup joué, et restaure l'état du board avant ce dernier
        entrée : instance de la classe Move
        """
        #import de variables
        piece = m.piece
        i,j = m.arrivee
        k,l = m.depart
        #retour de la pièce dans les cas classiques
        self.squares[k][l] = m.piece
        m.piece.position = m.depart
        self.squares[i][j] = None
        if m.piece.first_move is not None :
            m.piece.first_move = m.prev_piece_first_move
        #traitement complémentaire des prises et promotion sur prise
        if m.type == 'prise' or m.type == 'promoprise' :
            self.squares[i][j] = m.captured_piece
        #traitement complémentaire de la prise en passant
        if m.type == 'enpassant' :
            if m.piece.color == 'white':
                self.squares[i-1][j] = m.captured_piece
            else:
                self.squares[i+1][j] = m.captured_piece
        #gestion complémentaire de la tour dans le roque
        if m.type == 'castle' : 
            #petit roque
            if m.arrivee[1] == 6:
                tour=self.squares[i][5]
                tour.position = (i,7)
                tour.first_move = m.prev_tour_first_move
                self.squares[i][7] = tour
                self.squares[i][5] = None
            #grand roque
            else:
                tour=self.squares[i][3]
                tour.position = (i,0)
                tour.first_move = m.prev_tour_first_move
                self.squares[i][0] = tour
                self.squares[i][3] = None
        #retour des états du board
        self.trait = m.piece.color    
        self.last_move = m.prev_last_move
        self.white_king = m.prev_white_king
        self.black_king = m.prev_black_king
        self.end = False  

    def update_move_flag(self, m) :
        """
        mise à jour des flags d'un coup après qu'il soit joué
        entree : move
        met à jour les flags du move : is_a_mat/ is_a_check
        met à jour le flag du board : end
        """
        #contrôle de l'existence d'un coup possible pour le prochain joueur
        self.end = self.check_end()
        #si aucun coup, vérification de mat ou pat et fin de partie: 
        if self.end :
            if self.trait =='white' and self.is_attacked_by(self.white_king, 'black') :
                m.is_a_mat = True
                m.is_a_check = True
                return self.trait
            elif self.trait =='black' and self.is_attacked_by(self.black_king, 'white') :
                m.is_a_mat = True
                m.is_a_check = True
                return self.trait
            else :
                return self.trait
        #si un coup est disponible, marquage de l'échec éventuel, enregistrement et passage au joueur suivant
        elif self.trait == 'white':
            if self.is_attacked_by(self.white_king, 'black') :
                m.is_a_check = True
        else :
            if self.is_attacked_by(self.black_king, 'white') :
                m.is_a_check = True

    def is_attacked_by(self, case, color) :    
        """
        Méthode pour vérifier si une case est attaquée par une couleur
        entrées : case concernée, couleur concernée
        renvoie True si un des pièces de color attaque case, False sinon
        """
        if color == 'white' : 
            for piece in self.white_pieces() :
                if case in piece.attacked_cases() :
                    return True
        else : 
            for piece in self.black_pieces() :
                if case in piece.attacked_cases() :
                    return True
        return False
    
    def simulate(self, m):
        """
        Methode de vérification d'un coup (pas d'auto_échec)
        entrée : coup à vérifier
        renvoie False si le roi du joueur est attaqué à la suite de son propre coup, True sinon
        simule le coup, regarde le résultat, et annule le coup
        """
        self.apply_move(m)
        if self.trait == 'black' :
            legal = not self.is_attacked_by(self.white_king, 'black')
        else :
            legal = not self.is_attacked_by(self.black_king, 'white') 
        self.unapply_move(m)
        return legal

    def check_end(self) :
        """
        Vérifie la présence de coup possible pour le joueur qui doit jouer
        renvoie False si au moins un coup est disponible, False sinon
        """
        if self.trait == 'white' : 
            for piece in self.white_pieces() :
                l = piece.possible_moves()
                if len (l) > 0 :
                    return False
        else : 
            for piece in self.black_pieces() :
                l = piece.possible_moves()
                if len (l) > 0 :
                    return False
        return True
                
    def test_case(self, position):
        """
        Méthode pour tester l'occupation d'une case 
        entrée : position au format (i,j)
        renvoie True si une pièce se trouve sur la case, False sinon
        """
        i, j = position
        return self.squares[i][j] is not None
    
    def test_color(self, position):
        """
        Méthode pour tester la couleur d'une pièce sur une case
        entrée : position au format (i,j)
        renvoie None la case est vide, la couleur ('white' ou 'black') de la pièce sinon
        """
        i, j = position
        if self.squares[i][j] is None:
            return None
        return self.squares[i][j].color
    
    def white_pieces(self):
        """
        Méthode qui récupère la liste des pièces blanches sur le plateau
        renvoie la liste des pièces blanches sur le plateau
        """
        return [self.squares[i][j] for i in range(8) for j in range(8) if self.test_color((i,j)) == 'white']
    
    def black_pieces(self):
        """
        Méthode qui récupère la liste des pièces noires sur le plateau
        renvoie la liste des pièces noires sur le plateau
        """
        return [self.squares[i][j] for i in range(8) for j in range(8) if self.test_color((i,j)) == 'black']

    def move_list(self) :
        """
        coups disponibles
        renvoie la liste des coups disponibles pour le joueur avec le trait
        """
        move_list = []
        if self.trait == 'white' : 
            for piece in self.white_pieces() :
                l = piece.possible_moves()
                if len (l) > 0 :
                    for move in l :
                        move_list.append(move)
        else : 
            for piece in self.black_pieces() :
                l = piece.possible_moves()
                if len (l) > 0 :
                    for move in l :
                        move_list.append(move)
        return move_list
    
    def __str__(self):
        """
        Affichage du plateau dans la console
        renvoie une string en plusieurs lignes
        Pour le moment, côté blanc, mais inversible à terme 
        """
        board_str = ""
        board_str += "    a    b    c    d    e    f    g    h\n"
        board_str += "  +----+----+----+----+----+----+----+----+\n"
        for i in range(8):
            board_str += f"{8 - i} | "
            for j in range(8):
                if self.squares[7-i][j] is None:
                    board_str += "   | "
                else:
                    board_str += (self.squares[7-i][j].symbol + " | ")
            board_str += f" {8 - i}"
            board_str += "\n"
            board_str += "  +----+----+----+----+----+----+----+----+\n"
        board_str += "    a    b    c    d    e    f    g    h\n"
        return board_str
            