class Board:
    """
    Classe pour le plateaux
    """
    def __init__(self):
        """
        initialisation d'un plateau : 
        création de squares pour stocker les pièces
        création de la variable mat (fin de partie)
        création de la variable last_move pour stocker le dernier coup joué (pour la gestion du en passant)
        """
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.end = False
        self.last_move = None
        self.white_king = None
        self.black_king = None
    
    def apply_move(self, m):
        m.piece.move(m)
        self.last_move = m
    
    def undo_last_move(self,moves):
        m = self.last_move
        if m.type == 'classic' or m.type == 'doublepion' :
            m.piece.position = m.depart
            self.squares[m.depart[0]][m.depart[1]] = m.piece
            self.squares[m.arrivee[0]][m.arrivee[1]] = None
        if m.type == 'prise' or m.type == 'promoprise' :
            m.piece.position = m.depart
            self.squares[m.depart[0]][m.depart[1]] = m.piece
            self.squares[m.arrivee[0]][m.arrivee[1]] = m.captured_piece
        if m.type == 'promotion':
            m.piece.position = m.depart
            self.squares[m.depart[0]][m.depart[1]] = m.piece
            self.squares[m.arrivee[0]][m.arrivee[1]] = None
        if m.type == 'enpassant' :
            if m.piece.color == 'white':
                self.squares[m.arrivee[0]-1][m.arrivee[1]] = m.captured_piece
            else:
                self.squares[m.arrivee[0]+1][m.arrivee[1]] = m.captured_piece
            m.piece.position = m.depart
            self.squares[m.depart[0]][m.depart[1]] = m.piece
            self.squares[m.arrivee[0]][m.arrivee[1]] = None
        if m.type == 'castle' : 
            m.piece.position = m.depart
            if m.arrivee[1] == 6:
                #gestion du roi
                m.piece.position = m.depart
                self.squares[m.depart[0]][m.depart[1]] = m.piece
                self.squares[m.arrivee[0]][m.arrivee[1]] = None
                #gestion de la tour
                tour=self.squares[m.arrivee[0]][5]
                tour.position = (m.arrivee[0],7)
                self.squares[m.arrivee[0][7]] = tour
                self.squares[m.arrivee[0][5]] = None
            else:
                #gestion du roi
                m.piece.position = m.depart
                self.squares[m.depart[0]][m.depart[1]] = m.piece
                self.squares[m.arrivee[0]][m.arrivee[1]] = None
                #gestion de la tour
                tour=self.squares[m.arrivee[0]][3]
                tour.position = (m.arrivee[0],0)
                self.squares[m.arrivee[0][0]] = tour
                self.squares[m.arrivee[0][3]] = None
        if m.arrivee==self.white_king : 
            self.white_king = m.depart
        if m.arrivee==self.black_king : 
            self.black_king = m.depart
        if m.piece.color == 'black':
            moves[-1].pop()
            self.last_move = moves[-1][0] 
        else :
            moves.pop()
            if len(moves) == 0 : self.last_move = None  
            else : self.last_move = moves[-1][1]
        if m.piece.first_move is not None : 
            m.piece.first_move = not self.already_moved(m.piece, moves)
        return moves   
    
    def already_moved(self, piece, moves):
        for two_moves in moves:
            for move in two_moves:
                if move.piece == piece:
                    return True
        return False

    def is_attacked_by(self, case, color) :    
        """
        Méthode pour tester si une case est attaquée par une pièce de la couleur
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
    
    def simulate_move(self,move, moves):
        """
        Methode pour simuler un coup, et renvoyer True si il est valide (ne met pas le roi en échec), False sinon
        annulation du coup ensuite
        """
        self.apply_move(move)
        if move.piece.color == 'white' :
            if self.is_attacked_by(self.white_king, 'black'):
                self.undo_last_move(moves)
                return False
            else :
                self.undo_last_move(moves)
                return True
        else :
            if self.is_attacked_by(self.black_king, 'white'):
                self.undo_last_move(moves)
                return False
            else :
                self.undo_last_move(moves)
                return True
                
    def test_case(self, position):
        """
        Méthode pour tester l'occupation d'une case de position (i,j) sur le plateau
        """
        i, j = position
        return self.squares[i][j] != None
    
    def test_color(self, position):
        """
        Méthode pour tester la couleur d'une pièce sur une case de position (i,j) sur le plateau
        """
        i, j = position
        if self.squares[i][j] is None:
            return None
        return self.squares[i][j].color
    
    def white_pieces(self):
        """
        Méthode qui récupère la liste des pièces blanches sur le plateau
        """
        return [self.squares[i][j] for i in range(8) for j in range(8) if self.test_color((i,j)) == 'white']
    
    def black_pieces(self):
        """
        Méthode qui récupère la liste des pièces black sur le plateau
        """
        return [self.squares[i][j] for i in range(8) for j in range(8) if self.test_color((i,j)) == 'black']
    
    def __str__(self):
        """
        Affichage du plateau dans la console
        Proposer une variation pour faire jouer les noirs ? 
        """
        board_str = ""
        board_str += "    a   b   c   d   e   f   g   h\n"
        board_str += "  +---+---+---+---+---+---+---+---+\n"
        for i in range(8):
            board_str += f"{8 - i} |"
            for j in range(8):
                if self.squares[7-i][j] is None:
                    board_str += "   |"
                else:
                    board_str += (self.squares[7-i][j].symbol + " |")
            board_str += f" {8 - i}"
            board_str += "\n"
            board_str += "  +---+---+---+---+---+---+---+---+\n"
        board_str += "    a   b   c   d   e   f   g   h\n"
        return board_str
            