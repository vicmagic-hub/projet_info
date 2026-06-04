from datetime import date
from pathlib import Path

from model.board import Board
from model.piece import Pawn, Rook, Knight, Bishop, Queen, King
from model.coup_encoder import Move
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
        Méthode pour appliquer un coup
        entrée : coup à appliquer
        applique le coup sur le plateau, l'enregistre dans l'historique et traite les fins de partie
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
            #effacement de la partie dans la sauvegarde
            folder = Path("game")
            folder.mkdir(exist_ok=True)
            for file in folder.iterdir():
                if file.is_file():
                    file.unlink()
        else : 
            self.save()
    
    def undo(self):
        """
        Méthode pour faire un Ctrl Z : annulation du dernier coup de l'adversaire, et du dernier coup du joueur
        """
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
        renvoie la liste des coups effectués, une description de la partie et le score
        """
        #description de la partie
        s = "[Date \"" + self.date + "\"]\n"

        if self.side == 'white':
            s += "[White \"" + self.player_1 + "\"]\n"
            s += "[Black \"" + self.opponent + "\"]\n"
        else:
            s += "[White \"" + self.opponent + "\"]\n"
            s += "[Black \"" + self.player_1 + "\"]\n"

        s += "[Side \"" + self.side + "\"]\n"
        s += "[Type \"" + self.type + "\"]\n"
        if self.white_score is not None:
            s += "[Result \"" + str(self.white_score) + "-" + str(1 - self.white_score) + "\"]\n\n"

        #Passage à l'affichage des coups
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

    def save(self):
        """
        sauvegarde de la partie dans un fichier txt
        écrasement des autres parties sauvegardées
        """
        game_path = Path("game")
        has_game = game_path.exists()
        if not has_game : 
            Path("game").mkdir()
            game_path = Path("game")
        path = game_path / "save.txt"
        s = str(self)
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
        
    @classmethod
    def load_game(cls):
        """
        création de partie en "lecture" depuis partie stockée en local en txt
        renvoie la partie correspondante
        """
        path = "game/save.txt"

        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f]

        #description de la partie
        i = 0
        while i < len(lines) and lines[i].startswith("["):
            line = lines[i]

            if line.startswith("[Date"):
                date = line.split('"')[1]

            elif line.startswith("[White"):
                white = line.split('"')[1]

            elif line.startswith("[Black"):
                black = line.split('"')[1]

            elif line.startswith("[Side"):
                side = line.split('"')[1]

            elif line.startswith("[Type"):
                type = line.split('"')[1]

            i += 1
        #création de la partie
        if side == 'white' :
            player_1 = white
            opponent = black
        else :
            player_1 = black
            opponent = white
        level = 0
        if type == 'IA' :
            if opponent == "IAdifficilementpire" :
                level = 1
            elif opponent == "IAmoyendsefaireavoir" :
                level = 2 
        game = cls(player_1, side, level, type, opponent)

        # saut lignes vides
        while i < len(lines) and lines[i] == "":
            i += 1

        #Passage aux coups
        color = 'white'
        while i < len(lines) :
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            if ":" in line :
                _, moves_part = line.split(":", 1)
                moves_str = moves_part.strip().split()

                for m in moves_str :
                    move = Move.from_str(m, color, game.board)
                    game.play(move)
                    if color == 'white' : color = 'black'
                    else : color = 'white'
            i += 1

        return game