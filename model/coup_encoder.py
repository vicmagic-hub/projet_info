class Move():
    """
    Classe pour les coups
    """
    def __init__(self,piece, depart, arrivee, type,captured_piece = None):
        """
        initialisation d'un coup : 
        entrées :   pièce concernée, position de départ, position d'arrivée, 
                    type de coup :str parmi('classic', 'prise', 'enpassant', 'promotion', 'promoprise', 'castle', 'doublepion'),
                    éventuelle pièce capturée
        garde aussi une marque pour la pièce de promotion, des flags échec/mat
        intègre les informations en self.prev_... pour revenir à l'état avant le coup
        """""
        self.piece = piece
        self.depart = depart
        self.arrivee = arrivee
        self.type = type
        self.captured_piece = captured_piece
        self.promotion_piece = None
        self.is_a_mat = False
        self.is_a_check = False
        #information pour annuler un coup
        self.prev_last_move = None
        self.prev_piece_first_move = None
        self.prev_tour_first_move = None
        self.prev_white_king = None
        self.prev_black_king = None

    @classmethod
    def from_str (cls, s, color, board) :
        """
        création de coup en "lecture" depuis une string au format alternatif
        entrée : string du coup, couleur du joueur
        renvoie une instance de move correspondante
        """
        n = len (s)
        captured_piece = None
        promotion_piece = None
        if s[:5] =="O-O-O" :
            print("gdr")
            #grand roque
            if color == 'white' : 
                piece = board.squares[0][4]
                depart = (0,4)
                arrivee = (0,2)
            else :
                piece = board.squares[7][4]
                depart = (7,4)
                arrivee = (7,2)
            type = 'castle'
            n_parcouru = 4
        elif s[:3] == "O-O" : 
            print("petitroque")
            #petit roque
            if color == 'white' : 
                piece = board.squares[0][4]
                depart = (0,4)
                arrivee = (0,6)
            else :
                piece = board.squares[7][4]
                depart = (7,4)
                arrivee = (7,6)
            type = 'castle'
            n_parcouru = 2
        else : 
            if s[0].isupper() : 
                #coup de pièce
                i,j = int(s[2]) - 1, ord(s[1])- ord('a')
                piece = board.squares[i][j]
                depart = i,j
                if s[3] ==  'x' : 
                    #prise
                    type = 'prise'
                    k,l = int(s[5]) - 1, ord(s[4])- ord('a')
                    captured_piece = board.squares[k][l]
                    n_parcouru = 5
                else :
                    type = 'classic'
                    k,l = int(s[6]) - 1, ord(s[5])- ord('a')
                    n_parcouru = 6
                arrivee = (k,l)
            else : 
                #coup de pion
                i,j = int(s[1]) - 1, ord(s[0])- ord('a')
                piece = board.squares[i][j]
                depart = i,j
                if s[2] == 'x' : 
                    #prise/promoprise/enpassant : 
                    k,l = int(s[4]) - 1, ord(s[3])- ord('a')
                    arrivee = k,l
                    if color == 'white' :  prom_row = 7 
                    else : prom_row = 0
                    if k == prom_row : 
                        #promoprise
                        type = 'promoprise'
                        promotion_piece = s[6]
                        n_parcouru = 6
                    elif not board.test_case((k,l)) :
                        #en passant
                        type = 'enpassant'
                        if color == 'white' : captured_piece = board.squares[k][l-1]
                        else : captured_piece = board.squares[k][l+1]
                        n_parcouru = 4
                    else : 
                        #prise classique
                        type = 'prise' 
                        captured_piece = board.squares[k][l]
                        n_parcouru = 4
                else : 
                    #promotion/classic/double-coup
                    k,l = int(s[5]) - 1, ord(s[4])- ord('a')
                    arrivee = k,l
                    if color == 'white' :  prom_row = 7 
                    else : prom_row = 0
                    if k == prom_row : 
                        #promoprise
                        type = 'promotion'
                        promotion_piece = s[7]
                        n_parcouru = 7
                    elif abs(k-i) == 2 :
                        #double coup
                        type = 'doublepion'
                        n_parcouru = 5
                    else : 
                        #coup normal
                        type = 'classic'
                        n_parcouru = 5
        #generation du coup
        m = cls (piece, depart, arrivee, type, captured_piece)
        m.promotion_piece = promotion_piece
        if n_parcouru + 1 < n :
            if s[-1] == '+' : 
                m.is_a_check = True
            else :
                m.is_a_mat = True
                m.is_a_check = True
        return m
             

    def __str__(self):
        """
        Affichage d'un coup en notation non ambiguë
        renvoie "Na4->b6" pour un coup classique, "e4xd5" pour une prise, "e7->e8=Q" pour une promotion, "O-O" pour un petit roque, etc
        """
        piece = self.piece
        i,j = self.depart
        l,k = self.arrivee
        col = chr(ord('a') + j)
        p = piece.marque + col + str(i+1)
        s = ""
        if self.type == 'castle':
            if k == 6:
                s+= "O-O"
            else:
                s+= "O-O-O"
        elif self.type == 'promotion':
                s+= p + "->" + chr(ord('a') + k) + str(l+1) + '=' + self.promotion_piece
        elif self.type == 'prise' or self.type == 'enpassant':
            s+= p + 'x' + chr(ord('a') + k) + str(l+1)
        elif self.type == 'promoprise':
                s+= p + 'x' + chr(ord('a') + k) + str(l+1) + '=' + self.promotion_piece
        else:
            s+= p + "->" + chr(ord('a') + k) + str(l+1)
        if self.is_a_mat : 
            s+= "#"
        elif self.is_a_check : 
            s+= '+'
        n = len(s)
        if n < 9 :
             for _ in range(9-n):
                  s+=" "
        return s
