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
    
    
    def play(self, m):
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
    

    def undo(self):
        if len(self.moves) != 0 : 
            #suppression du coup de l'adversaire
            m = self.moves.pop()
            self.board.unapply_move(m)
            if len(self.moves) != 0 : 
                #suppression du coup du joueur
                m = self.moves.pop()
                self.board.unapply_move(m)


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
