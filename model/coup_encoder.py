from board import Board

class Move():
    def __init__(self,board, depart, arrivee, type, promotion_piece = None):
        self.board = board
        self.depart = depart
        self.arrivee = arrivee
        self.type = type
        self.promotion_piece = promotion_piece
        i,j = self.depart
        l,k = self.arrivee
        assert 0 <= i < 8 and 0 <= j < 8, "Invalid move, departure position out of bounds "
        assert 0 <= l < 8 and 0 <= k < 8, "Invalid move, arrival position out of bounds "
        assert self.board.squares[i][j] is not None, "Invalid move, no piece at departure position "

    def __str__(self):
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