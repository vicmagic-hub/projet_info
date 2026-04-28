from board import Board
from piece import Pawn, Rook, Knight, Bishop, Queen, King


class Game():
    """
    Classe pour les parties
    """
    def __init__(self, name, type,opponent, side):
        """
        initialisation d'une partie :
        création d'un historique des coups, d'un plateau, nom de la partie, 
        type de partie (local, online), adversaire (none si local), côté joué (white ou black)
        initialisation des pièces sur le plateau
        TEMPORAIREMENT, quelques tours implémentés
        """
        self.moves = []
        self.board = Board()
        self.name = name
        self.type = type
        self.opponent = opponent
        self.side = side
        to_play = 'white'
        counter = 1
        #initialisation des pions
        for j in range(8):
            pw = Pawn('white', (1, j), self.board)
            pb = Pawn('black', (6, j), self.board)
        #initialisation des Tours
        Rw1 = Rook('white', (0, 0), self.board)
        Rw2 = Rook('white', (0, 7), self.board)
        Rb1 = Rook('black', (7, 0), self.board)
        Rb2 = Rook('black', (7, 7), self.board)
        #initialisation des Cavaliers
        Nw1 = Knight('white', (0, 1), self.board)
        Nw2 = Knight('white', (0, 6), self.board)
        Nb1 = Knight('black', (7, 1), self.board)
        Nb2 = Knight('black', (7, 6), self.board)
        #initialisation des Fous
        Bw1 = Bishop('white', (0, 2), self.board)
        Bw2 = Bishop('white', (0, 5), self.board)
        Bb1 = Bishop('black', (7, 2), self.board)
        Bb2 = Bishop('black', (7, 5), self.board)
        #initialisation des Reines
        Qw = Queen('white', (0, 3), self.board)
        Qb = Queen('black', (7, 3), self.board)
        #initialisation des Rois
        Kw = King('white', (0, 4), self.board)
        Kb = King('black', (7, 4), self.board)
        while not self.board.end :
            to_play, counter = self.tour(to_play, type, counter)
    
    
    def tour (self, to_play, type, counter):
        """
        Méthode pour faire jouer un tour
        to_play : couleur du joueur qui doit jouer
        type : type de partie (local, online)
        counter : nombre de tours joués(1 tour = blanc + noirs)
        POUR LE MOMENT : 
            Sélection d'une pièce 
            Affichage des coups possibles pour cette pièce
            Sélection du coup à jouer
            Traitement du coup et mise à jour du plateau
            Passage au joueur suivant
        A faire :
            Gestion des échecs ? des mats, des nuls ? 
        """
        if type == "local":
            valid = False
            print(f"{to_play}'s turn to play")
            if self.name == "test":
                print(self.board)
            while valid == False:
                s = input("Select the case of the piece you would like to move (e.g., e4 or d4) : ")
                i, j = int(s[1])-1, ord(s[0])-ord('a')
                if self.board.squares[i][j] is None or self.board.squares[i][j].color != to_play :
                    print("Invalid piece, try again")
                    continue
                possible_moves = self.board.squares[i][j].possible_moves()
                s = "Possible moves for " + str(self.board.squares[i][j])  + " :"
                for k in range(len(possible_moves)):
                    s += "\nMove " + str(k) + ": " + str(possible_moves[k])
                print(s)
                coup = input("select your move with its position (e.g 0 or 4)  in the list enter exit to cancel : ")
                if coup == "exit":
                    continue 
                if coup.isdigit() and int(coup) < len(possible_moves):
                    m = possible_moves[int(coup)]
                    valid = True
                else :
                    print("Invalid move, try again")
            self.board.squares[i][j].move(m)
            if to_play == 'black':
                self.moves[-1].append(m)
                to_play = 'white'
                if self.name == "test":
                    print(self)
                return to_play, counter +1
            else :
                self.moves.append([m])
                to_play = 'black'
                if self.name == "test":
                    print(self)
                return to_play, counter
            
    def __str__(self):
        """
        Affichage de la partie dans la console
        """
        s = "String d'intro de la partie encore non complète\n"
        for i in range(len(self.moves)):
            s += str(i+1) + " : "
            for m in self.moves[i]:
                s += str(m) + " "
            s+= "\n"
        return s

#tests temporaires
if __name__ == "__main__":
    g = Game("test", "local", "none", "white")
