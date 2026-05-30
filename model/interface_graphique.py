import sys
import pygame
from model.game import Game

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

# correspondance marque → unicode
UNICODE = {
    ('white', ''):  '♙', ('black', ''):  '♟',
    ('white', 'R'): '♖', ('black', 'R'): '♜',
    ('white', 'N'): '♘', ('black', 'N'): '♞',
    ('white', 'B'): '♗', ('black', 'B'): '♝',
    ('white', 'Q'): '♕', ('black', 'Q'): '♛',
    ('white', 'K'): '♔', ('black', 'K'): '♚',
}


# Mémoïsation : on échange de la mémoire contre du temps de calcul
_piece_cache: dict = {}

def piece_surface(piece, size: int) -> pygame.Surface:
    key = (piece.marque, piece.color, size)

    if key in _piece_cache:
        return _piece_cache[key]

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

    ch   = UNICODE.get((piece.color, piece.marque), '?') #récupère le bon symbole dans le dic
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


class TextInput:
    def __init__(self, rect, placeholder=""):
        self.rect = pygame.Rect(rect)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.font = pygame.font.SysFont("georgia", 18)

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(ev.pos)

        if ev.type == pygame.KEYDOWN and self.active:
            if ev.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif ev.key == pygame.K_RETURN:
                self.active = False
            else:
                if ev.unicode.isprintable():
                    self.text += ev.unicode

    def draw(self, screen):
        color = (120, 200, 120) if self.active else (90, 90, 90)
        pygame.draw.rect(screen, color, self.rect, 2)

        display = self.text if self.text else self.placeholder
        surf = self.font.render(display, True, (220, 220, 220))
        screen.blit(surf, (self.rect.x + 8, self.rect.y + 6))

class PromoDialog:
    """Demande au joueur quelle pièce choisir lors d'une promotion."""
    PROMO_PIECES = ['Q', 'R', 'B', 'N']
    PROMO_LABELS = {'Q': '♕/♛', 'R': '♖/♜', 'B': '♗/♝', 'N': '♘/♞'}
    W, H = 320, 90 #Dimension de la boîte

    def __init__(self, screen_size):
        sw, sh = screen_size
        self.rect = pygame.Rect((sw - self.W) // 2, (sh - self.H) // 2, self.W, self.H)
        #On centre la fenêtre au milieu de l'écran
        self._font = pygame.font.SysFont('georgia,serif', 15, bold=True)
        self._big = pygame.font.SysFont("segoeuisymbol", 32)
        bw = self.W // 4
        #création des 4 boutons côte à côte :
        self.btns = {
            p: pygame.Rect(self.rect.x + i * bw, self.rect.y + 32, bw, self.H - 32)
            for i, p in enumerate(self.PROMO_PIECES)
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
            t2 = self._big.render(self.PROMO_LABELS[p], True, C_TEXT)
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
        self.selected = None
        self.legal = []
        self.flipped  = False
        self._promo_dialog = None
        self._pending_promo_moves = []

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

        self.show_menu()

        self.run()


    def show_menu(self):
        self.game = None

        font = pygame.font.SysFont("georgia", 24, bold=True)

        # inputs IA
        ia_name = TextInput((200, 150, 300, 35), "Pseudo joueur")
        ia_level = 1

        # inputs PvP
        p1 = TextInput((200, 320, 300, 35), "Blanc")
        p2 = TextInput((200, 370, 300, 35), "Noir")

        clock = pygame.time.Clock()

        while self.game is None:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                ia_name.handle_event(ev)
                p1.handle_event(ev)
                p2.handle_event(ev)

                if ev.type == pygame.MOUSEBUTTONDOWN:

                    # bouton IA
                    if pygame.Rect(200, 200, 300, 50).collidepoint(ev.pos):
                        self.game = Game(
                            ia_name.text or "Joueur",
                            "white",
                            ia_level,
                            "IA",
                            None
                        )
                        self.IA = self.game.IA

                    # bouton PvP
                    if pygame.Rect(200, 400, 300, 50).collidepoint(ev.pos):
                        self.game = Game(
                            p1.text or "Blanc",
                            "white",
                            0,
                            "local",
                            p2.text or "Noir"
                        )

                    # bouton reprendre (grisé)
                    if pygame.Rect(200, 500, 300, 50).collidepoint(ev.pos):
                        pass

            # draw
            self.screen.fill((30,30,30))

            # IA block
            pygame.draw.rect(self.screen, (60,60,60), (180, 120, 360, 160))
            ia_name.draw(self.screen)

            txt = font.render(f"Niveau IA: {ia_level}", True, (200,200,200))
            self.screen.blit(txt, (200, 260))

            pygame.draw.rect(self.screen, (100,180,100), (200, 200, 300, 50))
            self.screen.blit(font.render("Jouer vs IA", True, (0,0,0)), (260, 215))

            # PvP block
            pygame.draw.rect(self.screen, (60,60,60), (180, 290, 360, 180))
            p1.draw(self.screen)
            p2.draw(self.screen)

            pygame.draw.rect(self.screen, (100,180,100), (200, 400, 300, 50))
            self.screen.blit(font.render("Jouer local", True, (0,0,0)), (260, 415))

            # disabled
            pygame.draw.rect(self.screen, (80,80,80), (200, 500, 300, 50))
            self.screen.blit(font.render("Reprendre (bientôt)", True, (150,150,150)), (220, 515))

            pygame.display.flip()
            clock.tick(60)


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
        self.selected = None         # case (i,j) sélectionnée
        self.legal = []
        self.flipped  = False
        self._promo_dialog = None
        self._pending_promo_moves = []

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


    # gestion clic plateau
    def _board_click(self, i, j):
        """Traite un clic sur la case (i,j) du plateau."""

        # dialogue promo ouvert
        if self._promo_dialog:
            return   # géré dans handle_event

        piece = self.game.board.squares[i][j]

        # une pièce déjà sélectionnée
        if self.selected:
            fi, fj = self.selected
            # cherche un coup légal qui arrive en (i,j)
            moves = [m for m in self.legal if m.arrivee == (i, j)]

            if moves:
                promo_types = {'promotion', 'promoprise'}
                promo_moves = [m for m in moves if m.type in promo_types]

                if promo_moves:
                    # plusieurs choix de pièce → ouvre le dialogue
                    self._pending_promo_moves = promo_moves
                    self._promo_dialog = PromoDialog(self.screen.get_size())
                else:
                    self.chosen_move = moves[0]

                self.selected = None
                self.legal = []
                return

            # clique sur une autre pièce alliée → change la sélection
            if piece and piece.color == self.game.board.trait:
                self.selected = (i, j)
                self.legal = piece.possible_moves()
                return

            # clique ailleurs → désélectionne
            self.selected = None
            self.legal = []
            return

        #Pas encore de sélection
        if piece and piece.color == self.game.board.trait:
            self.selected = (i, j)
            self.legal = piece.possible_moves()

    # gestion événements
    def handle_event(self, ev):
        #si fin de partie, ne pas traiter
        if self.game.board.end:
            return
        # dialogue promotion
        if self._promo_dialog:
            choice = self._promo_dialog.clicked(ev)
            if choice:
                m = next((x for x in self._pending_promo_moves
                          if x.promotion_piece == choice), self._pending_promo_moves[0])
                self._promo_dialog        = None
                self._pending_promo_moves = []
                self.chosen_move = m
            return

        if self.btn_new.clicked(ev):
            #self.reset(); return
            pass #à définir : réinitialiser la partie
        if self.btn_flip.clicked(ev):
            self.flipped = not self.flipped; return
        if self.btn_undo.clicked(ev):
            self.game.undo(); return

        if (ev.type == pygame.MOUSEBUTTONDOWN
                and ev.button == 1
                and not self.game.board.end):
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
        board = self.game.board
        trait = board.trait
        last_move = self.game.moves[-1] if self.game.moves else None
        # cases
        for i in range(8):
            for j in range(8):
                x, y   = self.to_screen(i, j)
                color  = C_LIGHT if (i + j) % 2 == 0 else C_DARK
                pygame.draw.rect(self.screen, color, (x, y, CASE, CASE))

        # dernier coup joué
        if last_move:
            for pos in (last_move.depart, last_move.arrivee):
                x, y = self.to_screen(*pos)
                self.screen.blit(self._ov_last, (x, y))

        # roi en échec
        if last_move and not board.end and last_move.is_a_check:
            kp = board.white_king if self.game.board.trait == 'white' else board.black_king
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
                p = board.squares[i][j]
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

        # joueurs
        t_players = self.fn_md.render(f"{self.game.player_1} vs {self.game.opponent}", True, C_TEXT)
        self.screen.blit(t_players, (sx + 12, 90))

        # tour
        if not self.game.board.end:
            who  = 'Blancs' if self.game.board.trait == 'white' else 'Noirs'
            tcol = (235, 235, 225) if self.game.board.trait == 'white' else (90, 90, 80)
            t2   = self.fn_md.render(f'● Tour des {who}', True, tcol)
            self.screen.blit(t2, (sx + 12, 46))

        # séparateur
        pygame.draw.line(self.screen, C_BORDER, (sx + 10, 96), (sx + SIDEBAR - 10, 96), 1)

        # historique
        self.screen.blit(self.fn_md.render('Historique', True, C_TEXT_DIM), (sx + 12, 102))
        y    = 200
        rows = (WIN_H - 200) // 16
        log  = self.game.moves[-(rows * 2):]   # garde les derniers coups
        i    = 0
        num  = max(1, len(self.game.moves) - len(log)) // 2 + 1
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
            if hasattr(self, 'chosen_move') and self.chosen_move:
                self.game.play(self.chosen_move)
                self.chosen_move = None

            if (self.game.type == 'IA' and self.game.board.trait != self.game.side and not self.game.board.end):
                m = self.IA.select_move(self.game.board) 
                self.game.play(m)

            self.draw()
            self.clock.tick(60)
