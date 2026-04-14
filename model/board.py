class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
    
    def test_case(self, position):
        """
        Méthode pour tester si une case est occupée ou non
        """
        i, j = position
        return self.board[i][j] != None
    
