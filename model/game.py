from datetime import date

from model.board import Board
from model.piece import Pawn, Rook, Knight, Bishop, Queen, King
from ai.ai_lab import DumbAI, MinmaxAI


class Game():
    """
    Classe pour les parties
    """
    def __init__(self, player_1, side, level = 0, type = "IA", opponent = None):
        """
        initialisation d'une partie 
        entrees :   date, type de partie (local ou IA), coté du joueur 1 (blanc, noir ou aléatoire)
                    nom du joueur 1 , de son adversaire si local (IANiveau si IA)            
        création d'un historique des coups, d'un plateau, du score des blancs
        initialisation des pièces sur le plateau
        initialisation des positions des rois dans la mémoire du plateau
        lancement de la partie
        """
        self.moves = []
        self.board = Board()
        self.board.place_piece()
        self.date = str(date.today())
        self.level = level
        self.type = type
        self.side = side
        self.opponent = opponent
        self.player_1 = player_1
        if self.type == "IA"  :
            if self.level == 1 :
                self.IA = DumbAI()
            elif self.level == 2 : 
                self.IA = MinmaxAI(3)
            self.opponent = self.IA.name                
        self.white_score = None
        to_play = self.board.trait
        #affichage de début de partie 
        s="/////////////////////////////////////////////////////////////////////////////////// \n"
        s+="/////////////////////////////////////////////////////////////////////////////////// \n"
        s+= "\n"
        if self.side == 'white' : 
            s+= "Partie du " + self.date + " de " + self.player_1 + " contre " + self.opponent + '\n'
        else :
            s+= "Partie du " + self.date + " de " + self.opponent + " contre " + self.player_1 + '\n'
        print (s)
        #lancement des tours, jusqu'à ce que la partie prenne fin
        while not self.board.end :
            if self.type == 'local' : 
                self.tour_human()
            else :
                if self.board.trait == self.side :
                    self.tour_human()
                else :
                    self.tour_IA()
        #affichage de la partie
        print(self)
        print(self.board)
    
    
    def tour_human (self):
        """
        Méthode pour faire jouer un tour à un joueur humain
        Déroulé : 
            Sélection d'une pièce 
            Affichage des coups possibles pour cette pièce
            Sélection du coup à jouer
            Traitement du coup et mise à jour du plateau
            Enregistrement du coup
            si fin de partie, actualisation du score
        """
        print(self.board)
        print(f"{self.board.trait}'s turn to play")
        valid = False
        while valid == False:
            s = input("Select the case of the piece you would like to move (e.g., e4 or d4) : ")
            #abandon
            if s == "resign":
                self.board.end = True
                if self.board.trait == 'white' : self.white_score = 0
                else : self.white_score = 1
                return None
            #annulation Ctrl-Z
            elif s== "z" :
                if len(self.moves) == 0 : continue
                #suppression du coup de l'adversaire
                m = self.moves.pop()
                self.board.unapply_move(m)
                if len(self.moves) == 0 : return None
                #suppression du coup du joueur
                m = self.moves.pop()
                self.board.unapply_move(m)
                return None
            #case non existante sur le plateau
            elif len(s) != 2 or ord('h')<ord(s[0]) or ord('a')>ord(s[0]) or 0>int(s[1]) or 8<int(s[1]) :
                print("invalid case : make sure to tap something like: h1")
                continue
            i, j = int(s[1])-1, ord(s[0])-ord('a')
            #pas de pièce jouable sur la case
            if self.board.squares[i][j] is None or self.board.squares[i][j].color != self.board.trait :
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
        #enregistrement du coup 
        self.board.update_move_flag(m)
        self.moves.append(m)
        #application des fins de partie
        if self.board.end :
            if m.is_a_mat : 
                if self.board.trait == 'black' : 
                    self.white_score = 1
                else :
                    self.white_score = 0
            else :
                self.white_score = 0.5
        return None
    
    def tour_IA(self) :
        """
        Méthode pour faire jouer un tour à une IA
        Déroulé :
            Appel de l'IA pour sélectionner le coup joué
            Traitement du coup et mise à jour du plateau
            Enregistrement du coup
            si fin de partie, actualisation du score
        """
        #SELECTION DU COUP
        m = self.IA.select_move(self.board)          
        #application du coup
        self.board.apply_move(m)
        print("\n", self.IA.name, " played ", m)
        #enregistrement du coup 
        self.board.update_move_flag(m)
        self.moves.append(m)
        #application des fins de parties
        if self.board.end :
            if m.is_a_mat : 
                if self.trait == 'black' : 
                    self.white_score = 1
                else :
                    self.white_score = 0
            else :
                self.white_score = 0.5
            
    def __str__(self):
        """
        Affichage de la partie dans la console
        renvoie la lsite des coups effectués, une description de la partie et le score
        """
        s="/////////////////////////////////////////////////////////////////////////////////// \n"
        s+="/////////////////////////////////////////////////////////////////////////////////// \n"
        s+= "\n"
        if self.side == 'white' : 
            s+= "Partie du " + self.date + " de " + self.player_1 + " contre " + self.opponent + '\n'
        else :
            s+= "Partie du " + self.date + " de " + self.opponent + " contre " + self.player_1 + '\n'
        s+= "Score : (" + str(self.white_score) + " - " + str(1- self.white_score) + ")\n"
        for i in range(0,len(self.moves),2):
            if (i+1)//2 < 10 :
                s += str((i+1)//2) + " "
            else :
                s += str(((i+1)//2))
            s += " : " + str(self.moves[i]) + " "
            if i+1 < len (self.moves) :
                s+= str(self.moves[i+1])
            s+= "\n"
        if self.board.end :
            s+= "(" + str(self.white_score) + " - " + str(1- self.white_score) + ")"
        return s
