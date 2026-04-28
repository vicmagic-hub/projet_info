class Move():
    """
    Classe pour les coups
    """
    def __init__(self,piece, depart, arrivee, type,captured_piece = None, promotion_piece = None):
        """
        initialisation d'un coup : 
        pièce, position de départ, position d'arrivée, 
        type de coup (normal, prise, enpassant, promotion, promoprise, castle),
        éventuelle pièce capturée, éventuelle pièce de promotion si besoin
        """""
        self.piece = piece
        self.depart = depart
        self.arrivee = arrivee
        self.type = type
        self.promotion_piece = promotion_piece
        self.captured_piece = captured_piece

    def __str__(self):
        """
        Affichage d'un coup en notation non ambiguë
        a4 -> a5, e4*d5 pour une prise, e7->e8=Q pour une promotion, e7*d8=Q pour une promoprise, O-O pour un petit roque
        """
        piece = self.piece
        i,j = self.depart
        l,k = self.arrivee
        s = ""
        if self.type == 'castle':
            if j == 6:
                s+= "O-O"
            else:
                s+= "O-O-O"
        elif self.type == 'promotion':
            assert self.promotion_piece in ['Q', 'R', 'B', 'N'], "Invalid promotion piece, must be one of Q, R, B, N"
            s+= str(piece) + "->" + chr(ord('a') + k) + str(l+1) + '=' + self.promotion_piece
        elif self.type == 'prise':
            s+= str(piece) + 'x' + chr(ord('a') + k) + str(l+1)
        elif self.type == 'promoprise':
            assert self.promotion_piece in ['Q', 'R', 'B', 'N'], "Invalid promotion piece, must be one of Q, R, B, N"
            s+= str(piece) + 'x' + chr(ord('a') + k) + str(l+1) + '=' + self.promotion_piece
        else:
            s+= str(piece) + "->" + chr(ord('a') + k) + str(l+1)
        return s