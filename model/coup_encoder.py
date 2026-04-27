from board import Board

class Move():
    """
    Classe pour les coups
    """
    def __init__(self,board, depart, arrivee, type, promotion_piece = None):
        """
        initialisation d'un coup : 
        échiquier, position de départ, position d'arrivée, type de coup (normal, prise, enpassant, promotion, promoprise, castle), éventuelle pièce de promotion si besoin
        """""
        self.board = board
        self.depart = depart
        self.arrivee = arrivee
        self.type = type
        self.promotion_piece = promotion_piece

    def __str__(self):
        """
        Affichage d'un coup en notation algébrique
        """
        i,j = self.depart
        l,k = self.arrivee
        piece = self.board.squares[i][j]
        if self.type == 'castle':
            if j == 6:
                return "O-O"
            else:
                return "O-O-O"
        if self.type == 'promotion':
            assert self.promotion_piece in ['Q', 'R', 'B', 'N'], "Invalid promotion piece, must be one of Q, R, B, N"
            return piece.marque + chr(ord('a') + k) + str(l+1) + '=' + self.promotion_piece
        if self.type == 'prise':
            return piece.marque + 'x' + chr(ord('a') + k) + str(l+1)
        if self.type == 'promoprise':
            assert self.promotion_piece in ['Q', 'R', 'B', 'N'], "Invalid promotion piece, must be one of Q, R, B, N"
            return piece.marque + 'x' + chr(ord('a') + k) + str(l+1) + '=' + self.promotion_piece
        return piece.marque + chr(ord('a') + k) + str(l+1)