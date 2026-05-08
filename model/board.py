from copy import deepcopy

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
        creation des variables white_king et black_king, pour accéder plus rapidement aux positions des rois
        """
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.end = False
        self.last_move = None
        self.white_king = None
        self.black_king = None
    
    def apply_move(self, m):
        """
        méthode qui reçoit une instanciation de Move et traite le coup
        entrée : instance de la classe Move
        délègue la gestion du coup à la pièce concernée
        """
        m.piece.move(m)
        self.last_move = m
    
    def undo_last_move(self,moves):
        """
        méthode d'annulation du dernier coup (demi Ctrl-Z)
        entrée : historique des coups joués dans la partie
        Remet le plateau dans son état précédent
        Renvoie l'historique des coups, ajusté
        """
        m = self.last_move
        #traitement du déplacement simple ou de la promotion
        if m.type == 'classic' or m.type == 'doublepion' or m.type == 'promotion':
            m.piece.position = m.depart
            self.squares[m.depart[0]][m.depart[1]] = m.piece
            self.squares[m.arrivee[0]][m.arrivee[1]] = None
        #traitement des prises et promotion sur prise
        if m.type == 'prise' or m.type == 'promoprise' :
            m.piece.position = m.depart
            self.squares[m.depart[0]][m.depart[1]] = m.piece
            self.squares[m.arrivee[0]][m.arrivee[1]] = m.captured_piece
        #traitement de la prise en passant
        if m.type == 'enpassant' :
            if m.piece.color == 'white':
                self.squares[m.arrivee[0]-1][m.arrivee[1]] = m.captured_piece
            else:
                self.squares[m.arrivee[0]+1][m.arrivee[1]] = m.captured_piece
            m.piece.position = m.depart
            self.squares[m.depart[0]][m.depart[1]] = m.piece
            self.squares[m.arrivee[0]][m.arrivee[1]] = None
        #traitement du roque
        if m.type == 'castle' : 
            m.piece.position = m.depart
            #petit roque
            if m.arrivee[1] == 6:
                #gestion du roi
                m.piece.position = m.depart
                self.squares[m.depart[0]][m.depart[1]] = m.piece
                self.squares[m.arrivee[0]][m.arrivee[1]] = None
                #gestion de la tour
                tour=self.squares[m.arrivee[0]][5]
                tour.position = (m.arrivee[0],7)
                self.squares[m.arrivee[0]][7] = tour
                self.squares[m.arrivee[0]][5] = None
            #grand roque
            else:
                #gestion du roi
                m.piece.position = m.depart
                self.squares[m.depart[0]][m.depart[1]] = m.piece
                self.squares[m.arrivee[0]][m.arrivee[1]] = None
                #gestion de la tour
                tour=self.squares[m.arrivee[0]][3]
                tour.position = (m.arrivee[0],0)
                self.squares[m.arrivee[0]][0] = tour
                self.squares[m.arrivee[0]][3] = None
        #actualisation de la position des rois dans la mémoire du plateau
        if m.arrivee==self.white_king : 
            self.white_king = m.depart
        if m.arrivee==self.black_king : 
            self.black_king = m.depart
        #adaptation de l'historique de coups
        if m.piece.color == 'black':
            moves[-1].pop()
            self.last_move = moves[-1][0] 
        else :
            moves.pop()
            if len(moves) == 0 : self.last_move = None  
            else : self.last_move = moves[-1][1]
        #gestion des contraintes sur le premier coup
        if m.piece.first_move is not None : 
            m.piece.first_move = not self.already_moved(m.piece, moves)
        return moves   
    
    def already_moved(self, piece, moves):
        """
        Méthode pour vérifier si une pièce à déjà bougé dans une historique de partie.
        entrées : piece concernée, historique de la partie
        renvoie True si la pièce a déjà bougé, False sinon
        """
        for two_moves in moves:
            for move in two_moves:
                if move.piece == piece:
                    return True
        return False

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
    
    def simulate(self,move):
        """
        Methode de vérification d'un coup (pas d'auto_échec)
        entrée : coup à vérifier
        renvoie False si le roi du joueur est attaqué à la suite de son propre coup, True sinon
        POUR LE MOMENT fonctionne par copie profonde et simulation sur un plateau parallèle
        """
        board_copy = deepcopy(self)
        move_copy = move.clone(board_copy)
        board_copy.apply_move(move_copy)
        if move.piece.color == 'white' :
            return not board_copy.is_attacked_by(board_copy.white_king, 'black')
        else :
            return not board_copy.is_attacked_by(board_copy.black_king, 'white') 
                
    def test_case(self, position):
        """
        Méthode pour tester l'occupation d'une case 
        entrée : position au format (i,j)
        renvoie True si une pièce se trouve sur la case, False sinon
        """
        i, j = position
        return self.squares[i][j] != None
    
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
            