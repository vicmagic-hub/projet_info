from board import Board
from piece import Pawn, Rook, Knight, Bishop, Queen, King
from random import randint


class Game():
    """
    Classe pour les parties
    """
    def __init__(self, date, type, side,  player_1, opponent):
        """
        initialisation d'une partie 
        entrees :   date, type de partie (local ou IA), coté du joueur 1 (blanc, noir ou aléatoire)
                    nom du joueur 1 , de son adversaire si local (None si IA)            
        création d'un historique des coups, d'un plateau, du score des blancs et d'un compteur de tours
        initialisation des pièces sur le plateau
        initialisation des positions des rois dans la mémoire du plateau
        lancement de la partie
        """

        self.moves = []
        self.board = Board()
        self.date = date
        self.type = type
        self.side = side
        self.player_1 = player_1
        if opponent is None :
            self.opponent = "IA'pasmoyen"
        else :
            self.opponent = opponent
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
        #lancement des tours, jusqu'à ce que la partie prenne fin
        while not self.board.end :
            to_play, counter = self.tour(to_play, type, counter)
        #affichage de la partie
        print(self)
        print(self.board)
    
    
    def tour (self, to_play, type, counter):
        """
        Méthode pour faire jouer un tour
        entrées : couleur du joueur qui doit jouer, type de partie (local ou IA), numér du tour en cours (1 tour = blanc + noirs)
        renvoie la couleur du nouveau joueur qui doit jouer et le compteur actualisé
        Déroulé : 
            Sélection d'une pièce 
            Affichage des coups possibles pour cette pièce
            Sélection du coup à jouer
            Traitement du coup et mise à jour du plateau
            Contrôle de l'existence d'un coup possible
                si pas de coups, vérification de l'état (pat ou mat)
                enregistrement du coup et fin de partie
            Si coup possible, enregistrement du coup, marquage des échecs éventuels et 
        """
        if type == "local":
            if self.type == "local":
                print(self.board)
            print(f"{to_play}'s turn to play")
            valid = False
            while valid == False:
                s = input("Select the case of the piece you would like to move (e.g., e4 or d4) : ")
                #abandon
                if s == "resign":
                    self.board.end = True
                    if to_play == 'white' : self.white_score = 0
                    else : self.white_score = 1
                    return to_play, counter
                #demie-annulation
                elif s == "z" :
                    if len(self.moves) == 0 : 
                        continue
                    erased_color = self.board.last_move.piece.color
                    self.moves = self.board.undo_last_move(self.moves)
                    if erased_color == 'black' :
                        return 'black', counter
                    else :
                        return 'white', counter -1
                #annulation Ctrl-Z
                elif s== "Z" :
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
                #case non existante sur le plateau
                elif len(s) != 2 or ord('h')<ord(s[0]) or ord('a')>ord(s[0]) or 0>int(s[1]) or 8<int(s[1]) :
                    print("invalid case : make sure to tap something like: h1")
                    continue
                i, j = int(s[1])-1, ord(s[0])-ord('a')
                #pas de pièce jouable sur la case
                if self.board.squares[i][j] is None or self.board.squares[i][j].color != to_play :
                    print("Invalid piece, try again")
                    continue
                #cas normal : affichage des coups possibles
                possible_moves = self.board.squares[i][j].possible_moves()
                if len (possible_moves) >0 :
                    s = "Possible moves for " + str(self.board.squares[i][j])  + " :"
                else : 
                    print("no possible move for", self.board.squares[i][j])
                    continue
                for k in range(len(possible_moves)):
                    s += "\nMove " + str(k) + ": " + str(possible_moves[k])
                print(s)
                #sélection du coup joué
                coup = input("select your move with its position (e.g 0 or 4)  in the list enter exit to cancel : ")
                #choix d'une autre pièce
                if coup == "exit":
                    continue 
                #cas classique : sélection d'un coup valide
                if coup.isdigit() and int(coup) < len(possible_moves):
                    m = possible_moves[int(coup)]
                    valid = True
                #coup hors liste
                else :
                    print("Invalid move, try again")
            #application du coup
            self.board.apply_move(m)
            #contrôle de l'existence d'un coup possible pour le prochain joueur
            if to_play == 'black' : 
                self.board.end = self.check_end('white')
            else :
                self.board.end = self.check_end('black')
            #si aucun coup, vérification de mat ou pat et fin de partie: 
            if self.board.end :
                if to_play =='black' and self.board.is_attacked_by(self.board.white_king, 'black') :
                    m.is_a_mat = True
                    self.white_score = 0
                    self.moves.append(m)
                    return to_play, counter
                elif to_play =='white' and self.board.is_attacked_by(self.board.black_king, 'white') :
                    m.is_a_mat = True
                    self.white_score = 1
                    self.moves.append(m)
                    return to_play, counter
                elif to_play == 'white' : 
                    self.white_score = 0.5
                    self.moves.append(m)
                    return to_play, counter
                else :
                    self.white_score = 0.5
                    self.moves.append(m)
                    return to_play, counter
            #si un coup est disponible, marquage de l'échec éventuel, enregistrement et passage au joueur suivant
            if to_play == 'black':
                if self.board.is_attacked_by(self.board.white_king, 'black') :
                    m.is_a_check = True
                self.moves.append(m)
                to_play = 'white'
                return to_play, counter +1
            else :
                if self.board.is_attacked_by(self.board.black_king, 'white') :
                    m.is_a_check = True
                self.moves.append(m)
                to_play = 'black'
                return to_play, counter
    
    def check_end(self, trait) :
        """
        Vérifie la présence de coup possible pour le joueur avec le trait
        entrée : couleur du joueur qui devra jouer
        renvoie False si au moins un coup est disponible, False sinon
        """
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
        renvoie la lsite des coups effectués, une description de la partie et le score
        """
        s="/////////////////////////////////////////////////////////////////////////////////// \n"
        s+="/////////////////////////////////////////////////////////////////////////////////// \n"
        s+= "\n"
        s+= "Partie du " + self.date + " de " + self.player_1 + " contre " + self.opponent + '\n'
        s+= "Score : (" + str(self.white_score) + " - " + str(1- self.white_score) + ")\n"
        for i in range(0,len(self.moves),2):
            s += str((i+1)//2) + " : " + str(self.moves[i]) + " "
            if i+1 < len (self.moves) :
                s+= str(self.moves[i+1])
            s+= "\n"
        if self.board.end :
            s+= "(" + str(self.white_score) + " - " + str(1- self.white_score) + ")"
        return s

#test temporaire pour lancer 
if __name__ == "__main__":
    g = Game("aujourd'hui", "local", "white", "Victor FUZCO", " Oczuf ROTCIV")