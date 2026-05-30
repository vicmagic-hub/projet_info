"""
chess_ui.py  —  IHM pygame pour le jeu d'échecs
S'appuie sur : board.py, piece.py, coup_encoder.py
Remplace uniquement la méthode tour() de Game (entrée console → clics souris) #dans l'absolu pk pas, mais, alors on peut garder les fonctions
"""
#peut_etre faire les fonctions tour avec des paramètres IHM = True si IHLM, false si console ? 

#Une partie demandé à l'IA pour ne pas avoir à changer d'interpréteur (pas Anaconda)
#import subprocess
import sys
#subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])

import pygame
from model.board import Board
from model.piece import Pawn, Rook, Knight, Bishop, Queen, King
from model.coup_encoder import Move
#bizarre qu'il y ait pas game... Tu refais tout à la main ????

# ── Constantes visuelles ─────────────────────────────────────────────────────
SIZE    = 720           # taille du plateau en pixels
CASE    = SIZE // 8     #une case
SIDEBAR = 240
WIN_W   = SIZE + SIDEBAR
WIN_H   = SIZE

# L'ensemble des couleurs utilisées
C_LIGHT     = (240, 217, 181)
C_DARK      = (181, 136,  99)
C_BG        = ( 30,  28,  26)
C_SIDEBAR   = ( 38,  36,  33)
C_BORDER    = ( 60,  57,  52)
C_TEXT      = (220, 210, 195)
C_TEXT_DIM  = (140, 130, 115)
C_BTN       = ( 55,  52,  48)
C_BTN_H     = ( 80,  76,  70)
C_BTN_ACT   = ( 70, 130,  55)

#LE 4ème indice donne la transparence : 0 c'est invisible et 255 opaque
C_SEL       = (100, 190,  70, 150) #Vert sur la pièce sélectionnée
C_DOT       = ( 80, 160,  60, 100) #Point vert discret sur les cases ou on peut jouer
C_LAST      = (200, 200,  50,  90) #jaune sur les deux cases su dernier coup joué
C_CHECK_H   = (210,  45,  45, 140) #Rouge quand échec au roi

# correspondance piece → unicode
UNICODE = {
    ('white', Pawn):   '♙', ('black', Pawn):   '♟',
    ('white', Rook):   '♖', ('black', Rook):   '♜',
    ('white', Knight): '♘', ('black', Knight): '♞',
    ('white', Bishop): '♗', ('black', Bishop): '♝',
    ('white', Queen):  '♕', ('black', Queen):  '♛',
    ('white', King):   '♔', ('black', King):   '♚',
}

# noms de fichiers assets (j'ai changé d'avis)
ASSET_NAME = {Pawn:   'pawn',   Rook:   'rook', Knight: 'knight', Bishop: 'bishop', Queen:  'queen', King:  'king',}


# Mémoïsation : on échange de la mémoire contre du temps de calcul
_piece_cache: dict = {}

def piece_surface(piece, size: int) -> pygame.Surface:
    key = (type(piece), piece.color, size)
    if key in _piece_cache:
        return _piece_cache[key]

    # Essai image PNG
    #try:
    #    col  = 'white' if piece.color == 'white' else 'black'
    #    name = ASSET_NAME[type(piece)]
        img  = pygame.image.load(f"assets/{col}_{name}.png").convert_alpha()
        img  = pygame.transform.smoothscale(img, (size, size))
        _piece_cache[key] = img
        return img
    #except Exception:
        pass

    # la solution parce que les images c'est relou
    font_size = int(size * 0.75)
    #import des polices temporaires à décommenter suivant windows/Mac
    ############windows
    #try:
    #    font = pygame.font.SysFont('segoeuisymbol,symbola,unifont', font_size)
    #except Exception:
    #    font = pygame.font.Font(None, font_size)
    ########## pour Mac :
    #font = pygame.font.Font("/System/Library/Fonts/Apple Symbols.ttf", font_size)
    # la version en théorie robuste : 
    font = pygame.font.SysFont("segoeuisymbol", font_size)
    if font is None:
        font = pygame.font.SysFont("arial", font_size)
    if font is None:
        font = pygame.font.Font(None, font_size)

    ch   = UNICODE.get((piece.color, type(piece)), '?') #récupère le bon symbole dans le dic
    fg   = (255, 255, 255) if piece.color == 'white' else (15, 15, 15) #blanc pour les pièces blanches et quasi noir pour les autres
    surf = pygame.Surface((size, size), pygame.SRCALPHA) #surface transparente de la taille d'une case

    shadow = font.render(ch, True, (0, 0, 0, 200))
    sr     = shadow.get_rect(center=(size // 2 + 2, size // 2 + 2)) #pour faire l'ombre des pièces
    surf.blit(shadow, sr)

    txt = font.render(ch, True, fg)
    tr  = txt.get_rect(center=(size // 2, size // 2))
    surf.blit(txt, tr)

    _piece_cache[key] = surf #on mémorise le résultat dans le cache
    return surf


# Les boutons
class Bouton:
    def __init__(self, rect, label): #rect est un tuple (x, y, largeur, hauteur) qui définit la position et la taille du bouton
        self.rect  = pygame.Rect(rect) #on en fait un objet rectangle
        self.label = label #le texte affiché
        self._font = pygame.font.SysFont('georgia,serif', 14) #la police

    def draw(self, surf):
        hov = self.rect.collidepoint(pygame.mouse.get_pos()) #on récupère la position de la souris
        col = C_BTN_H if hov else C_BTN
        #on change la couleur du bouton quand la souris passe dessus
        pygame.draw.rect(surf, col,      self.rect, border_radius=6)
        pygame.draw.rect(surf, C_BORDER, self.rect, 1, border_radius=6)
        t = self._font.render(self.label, True, C_TEXT)
        surf.blit(t, t.get_rect(center=self.rect.center))

    def clicked(self, ev):
        return (ev.type == pygame.MOUSEBUTTONDOWN
                and ev.button == 1
                and self.rect.collidepoint(ev.pos))
#Renvoie True si trois conditions sont réunies simultanément : un événement clic souris a eu lieu, c'est le bouton gauche (button == 1), et le clic est à l'intérieur du rectangle.

# Test pour la promotion
PROMO_PIECES = ['Q', 'R', 'B', 'N']
PROMO_LABELS = {'Q': '♕/♛', 'R': '♖/♜', 'B': '♗/♝', 'N': '♘/♞'}

class PromoDialog:
    """Demande au joueur quelle pièce choisir lors d'une promotion."""
    W, H = 320, 90 #Dimension de la boîte

    def __init__(self, screen_size):
        sw, sh = screen_size
        self.rect = pygame.Rect((sw - self.W) // 2, (sh - self.H) // 2, self.W, self.H)
        #On centre la fenêtre au milieu de l'écran
        self._font = pygame.font.SysFont('georgia,serif', 15, bold=True)
        self._big  = pygame.font.SysFont('segoeuisymbol,symbola,unifont', 32)
        bw = self.W // 4
        #création des 4 boutons côte à côte :
        self.btns = {
            p: pygame.Rect(self.rect.x + i * bw, self.rect.y + 32, bw, self.H - 32)
            for i, p in enumerate(PROMO_PIECES)
        }

#Fonction de l'enfer : dessine ma boite (fond/bord/titre/les 4 boutons)
    def draw(self, surf):
        pygame.draw.rect(surf, C_SIDEBAR, self.rect, border_radius=8)
        pygame.draw.rect(surf, C_BORDER,  self.rect, 2, border_radius=8)
        t = self._font.render('Choisissez la pièce de promotion', True, C_TEXT)
        surf.blit(t, t.get_rect(midtop=(self.rect.centerx, self.rect.y + 6)))
        for p, r in self.btns.items():
            hov = r.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(surf, C_BTN_H if hov else C_BTN, r, border_radius=4)
            pygame.draw.rect(surf, C_BORDER, r, 1, border_radius=4)
            t2 = self._big.render(PROMO_LABELS[p], True, C_TEXT)
            surf.blit(t2, t2.get_rect(center=r.center))

#Vérifie si le joueur a cliqué sur un des 4 boutons. Renvoie la lettre correspondante ('Q', 'R', 'B' ou 'N') ou None si le clic est ailleurs.
    def clicked(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            for p, r in self.btns.items():
                if r.collidepoint(ev.pos):
                    return p
        return None


#Ca c'est l'IHM
class ChessUI:
    """
    Interface graphique.
    Utilise Board, les classes Piece et Move.
    """
    #Création de fenêtre+horloge gérant les 60 images/s et charge police/boutons/couleurs etc
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption('Chess')
        self.clock  = pygame.time.Clock()

        self.fn_sm = pygame.font.SysFont('georgia,serif', 12)
        self.fn_md = pygame.font.SysFont('georgia,serif', 15, bold=True)
        self.fn_lg = pygame.font.SysFont('georgia,serif', 22, bold=True)
        self.fn_mo = pygame.font.SysFont('couriernew,monospace', 12)

        SX = SIZE + 10
        self.btn_new    = Bouton((SX, WIN_H - 88, SIDEBAR - 20, 34), 'Nouvelle partie')
        self.btn_flip   = Bouton((SX, WIN_H - 48, SIDEBAR - 20, 34), 'Retourner le plateau')
        self.btn_undo   = Bouton((SX, WIN_H - 130, SIDEBAR - 20, 34), 'Annuler (z)')

        # overlays (surfaces SRCALPHA réutilisables)
        self._ov_sel   = self._flat(C_SEL)
        self._ov_last  = self._flat(C_LAST)
        self._ov_check = self._flat(C_CHECK_H)
        self._ov_dot   = self._dot()

        self._promo_dialog: PromoDialog | None = None
        self._pending_promo_moves: list = []   # coups de même arrivée, type promo*

        self.reset()

    def _flat(self, rgba):
        s = pygame.Surface((CASE, CASE), pygame.SRCALPHA)
        s.fill(rgba)
        return s

    def _dot(self):
        s = pygame.Surface((CASE, CASE), pygame.SRCALPHA)
        pygame.draw.circle(s, C_DOT, (CASE // 2, CASE // 2), CASE // 7)
        return s

    # état de jeu
    def reset(self):
        # là import de la partie
        self.board    = Board()
        self.moves_log: list[Move] = [] ###############REDONDANCE ?
        self.to_play  = 'white' ###############REDONDANCE ?
        self.selected = None         # case (i,j) sélectionnée
        self.legal    : list[Move] = []
        self.last_move: Move | None = None
        self.status   = ''
        self.game_over= False
        self.flipped  = False
        self._promo_dialog = None
        self._pending_promo_moves = []

        # placement initial des pièces
        for j in range(8):
            Pawn('white', (1, j), self.board)
            Pawn('black', (6, j), self.board)
        Rook('white',   (0, 0), self.board);  Rook('white',   (0, 7), self.board)
        Rook('black',   (7, 0), self.board);  Rook('black',   (7, 7), self.board)
        Knight('white', (0, 1), self.board);  Knight('white', (0, 6), self.board)
        Knight('black', (7, 1), self.board);  Knight('black', (7, 6), self.board)
        Bishop('white', (0, 2), self.board);  Bishop('white', (0, 5), self.board)
        Bishop('black', (7, 2), self.board);  Bishop('black', (7, 5), self.board)
        Queen('white',  (0, 3), self.board);  Queen('black',  (7, 3), self.board)
        kw = King('white', (0, 4), self.board)
        kb = King('black', (7, 4), self.board)
        self.board.white_king = (0, 4)
        self.board.black_king = (7, 4)

    # ── coordonnées ──────────────────────────────────────────────────────────
    def to_screen(self, i, j):
        """(ligne, colonne) plateau → (x, y) pixel (coin haut-gauche de la case)."""
        if self.flipped: #soucis d'affichage : inversion gauche droite mais pas haut bas
            return (7 - j) * CASE, (7 - i) * CASE
        return j * CASE, (7 - i) * CASE

    def from_screen(self, x, y):
        """Pixel → (ligne, colonne) plateau, ou None si hors plateau."""
        if x >= SIZE or x < 0 or y < 0 or y >= WIN_H:
            return None
        c = x // CASE
        r = y // CASE
        if self.flipped:
            return 7 - r, 7 - c
        return 7 - r, c

    # ── undo ─────────────────────────────────────────────────────────────────
    def undo(self):
    ##############REDONDANCE + VERSION PAS A JOUR 
        if not self.moves_log:
            return
        # annule le dernier coup du joueur courant + le coup adverse
        for _ in range(2):
            if not self.moves_log:
                break
            self.moves_log = self.board.undo_last_move(self.moves_log)
        self.last_move  = self.moves_log[-1] if self.moves_log else None
        self.selected   = None
        self.legal      = []
        self.status     = ''
        self.game_over  = False

    # logique fin de partie
    def _has_moves(self, color):
    ###############REDONDANCE
        pieces = self.board.white_pieces() if color == 'white' else self.board.black_pieces()
        return any(p.possible_moves() for p in pieces)

    def _is_in_check(self, color):
    ###############REDONDANCE
        king_pos = self.board.white_king if color == 'white' else self.board.black_king
        enemy    = 'black' if color == 'white' else 'white'
        return self.board.is_attacked_by(king_pos, enemy)

    def _after_move(self, m: Move):
    ###############REDONDANCE
        """Applique le coup, met à jour le statut, passe la main."""
        self.board.apply_move(m)
        m_color   = m.piece.color
        next_color = 'black' if m_color == 'white' else 'white'

        self.last_move = m
        self.moves_log.append(m)
        self.selected  = None
        self.legal     = []

        if not self._has_moves(next_color):
            if self._is_in_check(next_color):
                m.is_a_mat = True
                winner = 'Blancs' if next_color == 'black' else 'Noirs'
                self.status    = f'Échec et mat — {winner} gagnent !'
            else:
                self.status = 'Pat — nulle !'
            self.game_over = True
            return

        if self._is_in_check(next_color):
            m.is_a_check = True
            self.status  = 'Échec !'
        else:
            self.status = ''

        self.to_play = next_color

    # gestion clic plateau
    def _board_click(self, i, j):
        """Traite un clic sur la case (i,j) du plateau."""

        # dialogue promo ouvert
        if self._promo_dialog:
            return   # géré dans handle_event

        piece = self.board.squares[i][j]

        # une pièce déjà sélectionnée
        if self.selected:
            fi, fj = self.selected
            # cherche un coup légal qui arrive en (i,j)
            matching = [m for m in self.legal if m.arrivee == (i, j)]

            if matching:
                promo_types = {'promotion', 'promoprise'}
                promo_moves = [m for m in matching if m.type in promo_types]

                if promo_moves:
                    # plusieurs choix de pièce → ouvre le dialogue
                    self._pending_promo_moves = promo_moves
                    self._promo_dialog = PromoDialog(self.screen.get_size())
                else:
                    self._after_move(matching[0])
                return

            # clique sur une autre pièce alliée → change la sélection
            if piece and piece.color == self.to_play:
                self.selected = (i, j)
                self.legal    = piece.possible_moves()
                return

            # clique ailleurs → désélectionne
            self.selected = None
            self.legal    = []
            return

        # aucune sélection : choisir une pièce alliée
        if piece and piece.color == self.to_play:
            self.selected = (i, j)
            self.legal    = piece.possible_moves()

    # gestion événements
    def handle_event(self, ev):
        # dialogue promotion
        if self._promo_dialog:
            choice = self._promo_dialog.clicked(ev)
            if choice:
                m = next((x for x in self._pending_promo_moves
                          if x.promotion_piece == choice), self._pending_promo_moves[0])
                self._promo_dialog        = None
                self._pending_promo_moves = []
                self._after_move(m)
            return

        if self.btn_new.clicked(ev):
            self.reset(); return
        if self.btn_flip.clicked(ev):
            self.flipped = not self.flipped; return
        if self.btn_undo.clicked(ev):
            self.undo(); return

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_n:
                self.reset()
            elif ev.key == pygame.K_z:
                self.undo()
            elif ev.key == pygame.K_f:
                self.flipped = not self.flipped

        if (ev.type == pygame.MOUSEBUTTONDOWN
                and ev.button == 1
                and not self.game_over):
            pos = self.from_screen(*ev.pos)
            if pos:
                self._board_click(*pos)

    # rendu
    def draw(self):
        self.screen.fill(C_BG)
        self._draw_board()
        self._draw_sidebar()
        if self._promo_dialog:
            self._promo_dialog.draw(self.screen)
        pygame.display.flip()

    def _draw_board(self):
        # cases
        for i in range(8):
            for j in range(8):
                x, y   = self.to_screen(i, j)
                color  = C_LIGHT if (i + j) % 2 == 0 else C_DARK
                pygame.draw.rect(self.screen, color, (x, y, CASE, CASE))

        # dernier coup joué
        if self.last_move:
            for pos in (self.last_move.depart, self.last_move.arrivee):
                x, y = self.to_screen(*pos)
                self.screen.blit(self._ov_last, (x, y))

        # roi en échec
        if not self.game_over and self._is_in_check(self.to_play):
            kp = self.board.white_king if self.to_play == 'white' else self.board.black_king
            x, y = self.to_screen(*kp)
            self.screen.blit(self._ov_check, (x, y))

        # case sélectionnée + coups possibles
        if self.selected:
            x, y = self.to_screen(*self.selected)
            self.screen.blit(self._ov_sel, (x, y))
            seen = set()
            for m in self.legal:
                if m.arrivee not in seen:
                    seen.add(m.arrivee)
                    mx, my = self.to_screen(*m.arrivee)
                    self.screen.blit(self._ov_dot, (mx, my))

        # pièces
        for i in range(8):
            for j in range(8):
                p = self.board.squares[i][j]
                if p:
                    x, y = self.to_screen(i, j)
                    self.screen.blit(piece_surface(p, CASE), (x, y))

        # coordonnées
        for i in range(8):
            fi, fj = (i, 7 - i) if self.flipped else (i, i)
            # lettres colonnes (bas)
            col_ch = chr(ord('a') + fj)
            bg = C_DARK if (0 + fj) % 2 == 0 else C_LIGHT
            t  = self.fn_sm.render(col_ch, True, bg)
            self.screen.blit(t, (fj * CASE + CASE - 12, WIN_H - 14))
            # chiffres lignes (gauche)
            row_ch = str(fi + 1) if not self.flipped else str(8 - fi)
            bg2 = C_LIGHT if (fi + 0) % 2 == 0 else C_DARK
            t2  = self.fn_sm.render(str(i + 1), True, bg2)
            self.screen.blit(t2, (3, (7 - i) * CASE + 3))

    def _draw_sidebar(self):
        sx = SIZE
        pygame.draw.rect(self.screen, C_SIDEBAR, (sx, 0, SIDEBAR, WIN_H))
        pygame.draw.line(self.screen, C_BORDER, (sx, 0), (sx, WIN_H), 2)

        # titre
        t = self.fn_lg.render('♟  Chess', True, C_TEXT)
        self.screen.blit(t, (sx + 14, 14))

        # tour
        if not self.game_over:
            who  = 'Blancs' if self.to_play == 'white' else 'Noirs'
            tcol = (235, 235, 225) if self.to_play == 'white' else (90, 90, 80)
            t2   = self.fn_md.render(f'● Tour des {who}', True, tcol)
            self.screen.blit(t2, (sx + 12, 46))

        # statut
        if self.status:
            scol = (215, 70, 70) if 'mat' in self.status or 'Pat' in self.status else (220, 200, 70)
            t3   = self.fn_md.render(self.status, True, scol)
            self.screen.blit(t3, (sx + 12, 70))

        # séparateur
        pygame.draw.line(self.screen, C_BORDER, (sx + 10, 96), (sx + SIDEBAR - 10, 96), 1)

        # historique
        self.screen.blit(self.fn_md.render('Historique', True, C_TEXT_DIM), (sx + 12, 102))
        y    = 124
        rows = (WIN_H - 200) // 16
        log  = self.moves_log[-(rows * 2):]   # garde les derniers coups
        i    = 0
        num  = max(1, len(self.moves_log) - len(log)) // 2 + 1
        while i < len(log):
            w_str = str(log[i]).strip()
            b_str = str(log[i + 1]).strip() if i + 1 < len(log) else ''
            line  = f'{num:>3}. {w_str:<9} {b_str}'
            t4    = self.fn_mo.render(line, True, C_TEXT)
            self.screen.blit(t4, (sx + 10, y))
            y    += 16
            i    += 2
            num  += 1

        # boutons
        self.btn_undo.draw(self.screen)
        self.btn_new.draw(self.screen)
        self.btn_flip.draw(self.screen)

    # boucle principale
    def run(self):
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(ev)
            self.draw()
            self.clock.tick(60)


if __name__ == '__main__':
    ChessUI().run()