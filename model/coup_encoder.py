class Move():
    """
    Classe pour les coups
    """
    def __init__(self,piece, depart, arrivee, type,captured_piece = None):
        """
        initialisation d'un coup : 
        entrées :   pièce concernée, position de départ, position d'arrivée, 
                    type de coup :str parmi('normal', 'prise', 'enpassant', 'promotion', 'promoprise', 'castle', 'doublepion'),
                    éventuelle pièce capturée
        garde aussi une marque pour la pièce de promotion, des flags échec/mat
        intègre les informations en self.prev_... pour revenir à l'état avant le coup
        """""
        self.piece = piece
        self.depart = depart
        self.arrivee = arrivee
        self.type = type
        self.captured_piece = captured_piece
        self.promotion_piece = None
        self.is_a_mat = False
        self.is_a_check = False
        #information pour annuler un coup
        self.prev_last_move = None
        self.prev_piece_first_move = None
        self.prev_tour_first_move = None
        self.prev_white_king = None
        self.prev_black_king = None

        
    
    def clone(self, new_board):
        """
        copie profonde d'un coup sur un nouvel échiquier
        entrée : nouvelle instance de board
        renvoie le clone de self sur le nouveau plateau
        """
        piece_copy = new_board.squares[self.depart[0]][self.depart[1]]
        if self.captured_piece is None :
            m = Move(piece_copy, self.depart, self.arrivee, self.type, None)
        else :
            captured_piece_copy = new_board.squares[self.captured_piece.position[0]][self.captured_piece.position[1]]
            m = Move(piece_copy, self.depart, self.arrivee, self.type, captured_piece_copy)
        if self.promotion_piece is not None :
            m.promotion_piece = self.promotion_piece
        return m

    def __str__(self):
        """
        Affichage d'un coup en notation non ambiguë
        renvoie "Na4->b6" pour un coup classique, "e4*d5" pour une prise, "e7->e8=Q" pour une promotion, "O-O" pour un petit roque, etc
        """
        piece = self.piece
        i,j = self.depart
        l,k = self.arrivee
        col = chr(ord('a') + j)
        p = piece.marque + col + str(i+1)
        s = ""
        if self.type == 'castle':
            if k == 6:
                s+= "O-O"
            else:
                s+= "O-O-O"
        elif self.type == 'promotion':
                s+= p + "->" + chr(ord('a') + k) + str(l+1) + '=' + self.promotion_piece
        elif self.type == 'prise' or self.type == 'enpassant':
            s+= p + 'x' + chr(ord('a') + k) + str(l+1)
        elif self.type == 'promoprise':
                s+= p + 'x' + chr(ord('a') + k) + str(l+1) + '=' + self.promotion_piece
        else:
            s+= p + "->" + chr(ord('a') + k) + str(l+1)
        if self.is_a_mat : 
            s+= "#"
        elif self.is_a_check : 
            s+= '+'
        n = len(s)
        if n < 9 :
             for _ in range(9-n):
                  s+=" "
        return s
