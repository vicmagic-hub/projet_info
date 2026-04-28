class Board:
    """
    Classe pour le plateaux
    """
    def __init__(self):
        """
        initialisation d'un plateau : 
        création de squares pour stocker les pièces
        création de white & black_attacked pour stocker les cases attaquées pa les blancs où noirs
        création de la variable mat (fin de partie)
        """
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.white_attacked = [[False for _ in range(8)] for _ in range(8)]
        self.black_attacked = [[False for _ in range(8)] for _ in range(8)]
        self.mat = False
    
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
            