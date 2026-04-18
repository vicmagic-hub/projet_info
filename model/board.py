class Board:
    def __init__(self):
        self.squares = [[None for _ in range(8)] for _ in range(8)]
    
    def test_case(self, position):
        """
        Méthode pour tester si une case est occupée ou non
        """
        i, j = position
        return self.squares[i][j] != None
    
    def __str__(self):
        board_str = ""
        board_str += "     a   b   c   d   e   f   g   h\n"
        board_str += "  +-------------------------------+\n"
        for i in range(8):
            board_str += f"{8 - i} |"
            for j in range(8):
                if self.squares[7-i][j] is None:
                    board_str += "   |"
                else:
                    board_str += (self.squares[7-i][j].symbol + " |")
            board_str += f" {8 - i}"
            board_str += "\n"
            board_str += "  +-------------------------------+\n"
        board_str += "     a   b   c   d   e   f   g   h\n"
        return board_str
            