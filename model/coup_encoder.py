class Move():
    """
    Classe pour les coups
    """
    def __init__(self,piece, depart, arrivee, type,captured_piece = None, promotion_piece = None):
        """
        initialisation d'un coup : 
        pièce, position de départ, position d'arrivée, 
        type de coup (normal, prise, enpassant, promotion, promoprise, castle, doublepion),
        éventuelle pièce capturée, éventuelle pièce de promotion
        """""
        self.piece = piece
        self.depart = depart
        self.arrivee = arrivee
        self.type = type
        self.promotion_piece = promotion_piece
        self.captured_piece = captured_piece
        self.is_a_mat = False
        self.is_a_check = False
    
    def clone(self, new_board):
        piece_copy = new_board.squares[self.depart[0]][self.depart[1]]
        if self.captured_piece is None :
            m = Move(piece_copy, self.depart, self.arrivee, self.type, None, self.promotion_piece)
        else :
            captured_piece_copy = new_board.squares[self.captured_piece.position[0]][self.captured_piece.position[1]]
            m = Move(piece_copy, self.depart, self.arrivee, self.type, captured_piece_copy, self.promotion_piece)
        return m

    def __str__(self):
        """
        Affichage d'un coup en notation non ambiguë
        a4 -> a5, e4*d5 pour une prise, e7->e8=Q pour une promotion, e7*d8=Q pour une promoprise, O-O pour un petit roque
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
            if self.promotion_piece in ['Q', 'R', 'B', 'N']:
                s+= + "->" + chr(ord('a') + k) + str(l+1) + '=' + self.promotion_piece
            else:
                s+= p + "->" + chr(ord('a') + k) + str(l+1) + '= ?'
        elif self.type == 'prise' or self.type == 'enpassant':
            s+= p + 'x' + chr(ord('a') + k) + str(l+1)
        elif self.type == 'promoprise':
            if self.promotion_piece in ['Q', 'R', 'B', 'N']:
                s+= p + 'x' + chr(ord('a') + k) + str(l+1) + '=' + self.promotion_piece
            else:
                s+= p + 'x' + chr(ord('a') + k) + str(l+1) + '= ?' 
        else:
            s+= p + "->" + chr(ord('a') + k) + str(l+1)
        if self.is_a_mat : 
            s+= "#"
        elif self.is_a_check : 
            s+= '+'
        return s