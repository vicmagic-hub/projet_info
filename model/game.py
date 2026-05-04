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
        """
        self.moves = []
        self.board = Board()
        self.name = name
        self.type = type
        self.opponent = opponent
        self.side = side
        self.white_score = None
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
        self.board.white_king = (0,4)
        Kb = King('black', (7, 4), self.board)
        self.board.black_king = (7,4)
        while not self.board.end :
            to_play, counter = self.tour(to_play, type, counter)
        print(self)
    
    
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
            if self.name == "test":
                print(self.board)
            #enregistrement des coups possibles et contôle de l'existence d'un coup
            self.board.end = self.check_end(to_play)
            #si aucun coup, vérification de mat ou pat : 
            if self.board.end :
                if to_play =='white' and self.board.is_attacked_by(self.board.white_king, 'black') :
                    self.moves[-1][1].is_a_mat = True
                    self.white_score = 0
                    return to_play, counter
                elif to_play =='black' and self.board.is_attacked_by(self.board.black_king, 'white') :
                    self.moves[-1][0].is_a_mat = True
                    self.white_score = 1
                    return to_play, counter
                else : 
                    self.white_score = 0.5
                    return to_play, counter
            #tour classique autrement
            print(f"{to_play}'s turn to play")
            valid = False
            while valid == False:
                s = input("Select the case of the piece you would like to move (e.g., e4 or d4) : ")
                if s == "resign":
                    print (to_play + " resigns")
                    self.board.end = True
                    if to_play == 'white' : self.white_score = 0
                    else : self.white_score = 1
                    return to_play, counter
                if s == "z" :
                    if len(self.moves) == 0 : 
                        continue
                    erased_color = self.board.last_move.piece.color
                    self.moves = self.board.undo_last_move(self.moves)
                    if erased_color == 'black' :
                        return 'black', counter
                    else :
                        return 'white', counter -1
                if s== "Z" :
                    if len(self.moves) == 0 : 
                        continue
                    erased_color = self.board.last_move.piece.color
                    self.moves = self.board.undo_last_move(self.moves)
                    if len(self.moves) == 0 : 
                        continue
                    erased_color = self.board.last_move.piece.color
                    self.moves = self.board.undo_last_move(self.moves)
                    if erased_color == 'black' :
                        return 'black', counter
                    else :
                        return 'white', counter -1
                if len(s) != 2 or ord('h')<ord(s[0]) or ord('a')>ord(s[0]) or 0>int(s[1]) or 8<int(s[1]) :
                    print("invalid case : make sure to tap something like: h1")
                    continue
                i, j = int(s[1])-1, ord(s[0])-ord('a')
                if self.board.squares[i][j] is None or self.board.squares[i][j].color != to_play :
                    print("Invalid piece, try again")
                    continue
                possible_moves = self.board.squares[i][j].possible_moves()
                if len (possible_moves) >0 :
                    s = "Possible moves for " + str(self.board.squares[i][j])  + " :"
                else : 
                    print("no possible move for", self.board.squares[i][j])
                    continue
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
            self.board.apply_move(m)
            if to_play == 'black':
                if self.board.is_attacked_by(self.board.white_king, 'black') :
                    m.is_a_check = True
                self.moves[-1].append(m)
                to_play = 'white'
                return to_play, counter +1
            else :
                if self.board.is_attacked_by(self.board.black_king, 'white') :
                    m.is_a_check = True
                self.moves.append([m])
                to_play = 'black'
                return to_play, counter
    
    def check_end(self, trait) :
        if trait == 'white' : 
            for piece in self.board.white_pieces() :
                l = piece.possible_moves()
                if len (l) > 0 :
                    return False
        else : 
            for piece in self.board.black_pieces() :
                l = piece.possible_moves()
                if len (l) > 0 :
                    return False
        return True
            
    def __str__(self):
        """
        Affichage de la partie dans la console
        """
        s = "String d'intro de la partie (encore non complète)\n"
        for i in range(len(self.moves)):
            s += str(i+1) + " : "
            for m in self.moves[i]:
                s += str(m) + " "
            s+= "\n"
        if self.board.end :
            s+= "(" + str(self.white_score) + " - " + str(1- self.white_score) + ")"
        return s

#tests temporaires
if __name__ == "__main__":
    g = Game("test", "local", "none", "white")