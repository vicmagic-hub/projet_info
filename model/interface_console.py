from model.game import Game

class ConsoleInterface():
    """
    classe pour gérer l'interface console du jeu
    """
    def __init__(self):
        """
        initialisation de l'interface console : 
        sélection du type de partie et des paramètres via un menu à input
        Présentation de la partie et lancement
        """
        valid = False
        while not valid :
            type =  input ("choisissez une partie en JcJ sur ce PC (local) ou contre IA (IA) ")
            if type == "IA" or type == "local" : valid = True
            else : pro=int("tapez 'IA' ou 'local'")
        player_1 = input("tapez votre pseudonyme")
        if type == "IA" : 
            valid = False
            level = int(input("choisissez le niveau de l'IA : IAdifficelementpire, l'IA aléatoire(1) ou IAmoyendsefaireavoir, l'IA qui calcule un peu(2)"))
            if level == 1 or level == 2 : 
                valid = True
                opponent = None
            else : print("tapez 1 ou 2")
        else : 
            level = 0
            opponent = input("tapez le pseudonyme de votre adversaire")
        
        self.game = Game(player_1, "white", level, type, opponent)
        self.IA = self.game.IA if self.game.type == "IA" else None

        #affichage de début de partie 
        s="/////////////////////////////////////////////////////////////////////////////////// \n"
        s+="/////////////////////////////////////////////////////////////////////////////////// \n"
        s+= "\n"
        if self.game.side == 'white' : 
            s+= "Partie du " + self.game.date + " de " + self.game.player_1 + " contre " + self.game.opponent + '\n'
        else :
            s+= "Partie du " + self.game.date + " de " + self.game.opponent + " contre " + self.game.player_1 + '\n'
        print (s)
    
        self.run()
    
    def run(self) : 
        """
        Gestion de l'alternance des tours et affichage en fin de partie
        """
        #lancement des tours, jusqu'à ce que la partie prenne fin
        while not self.game.board.end :
            if self.game.type == 'local' : 
                m = self.get_human_move()
                self.game.play(m)
            else :
                if self.game.board.trait == self.game.side :
                    m = self.get_human_move()
                    self.game.play(m)
                else :
                    m = self.get_AI_move()
                    self.game.play(m)
        #affichage de la partie
        print(self.game)
        print(self.game.board)
    
    def get_human_move(self) : 
        """
        Système d'input pour demander les coups à un joueur humain, en proposant les coups disponibles par pièce sélectionnée
        Renvoie un coup valide
        """
        print(self.game.board)
        print(f"{self.game.board.trait}'s turn to play")
        valid = False
        while valid == False:
            s = input("Select the case of the piece you would like to move (e.g., e4 or d4) : ")
            #abandon
            if s == "resign":
                self.game.board.end = True
                if self.game.board.trait == 'white' : self.game.white_score = 0
                else : self.game.white_score = 1
                return None
            #annulation Ctrl-Z
            elif s== "z" :
                self.game.undo()
            #case non existante sur le plateau
            elif len(s) != 2 or ord('h')<ord(s[0]) or ord('a')>ord(s[0]) or 0>int(s[1]) or 8<int(s[1]) :
                print("invalid case : make sure to tap something like: h1")
                continue
            i, j = int(s[1])-1, ord(s[0])-ord('a')
            #pas de pièce jouable sur la case
            if self.game.board.squares[i][j] is None or self.game.board.squares[i][j].color != self.game.board.trait :
                print("Invalid piece, try again")
                continue
            #cas normal : affichage des coups possibles
            possible_moves = self.game.board.squares[i][j].possible_moves()
            if len (possible_moves) >0 :
                s = "Possible moves for " + str(self.game.board.squares[i][j])  + " :"
            else : 
                print("no possible move for", self.game.board.squares[i][j])
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
        return m
    
    def get_AI_move(self) : 
        """
        Demande des coups à une IA
        Renvoie un coup valide
        """
        return self.IA.select_move(self.game.board) 