import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from model.game import Game


class TestChess(unittest.TestCase):

    # ─────────────────────────────────────────
    # 1. Tests des coups légaux
    # ─────────────────────────────────────────
    def test_legal_moves_pawn(self):
        game = Game("J1", "white", 0, "local", "J2")

        # pion blanc initial e2
        pawn = game.board.squares[6][4]  # e2

        moves = pawn.possible_moves()

        destinations = [m.arrivee for m in moves]

        # cas 1 : avance 1 case
        self.assertIn((5, 4), destinations)

        # cas 2 : avance 2 cases
        self.assertIn((4, 4), destinations)

    # ─────────────────────────────────────────
    # 2. Tests de Game.play()
    # ─────────────────────────────────────────
    def test_play_move(self):

        game = Game("J1", "white", 0, "local", "J2")
        pawn = game.board.squares[1][4]
        move = pawn.possible_moves()[0]

        game.play(move)

        # cas 1 : pion a bougé
        self.assertIsNone(game.board.squares[1][4])

        # cas 2 : tour changé
        self.assertEqual(game.board.trait, "black")

    # ─────────────────────────────────────────
    # 3. Tests de undo
    # ─────────────────────────────────────────
    def test_undo(self):
        game = Game("J1", "white", 0, "local", "J2")

        pawn = game.board.squares[6][4]
        move = pawn.possible_moves()[0]

        game.play(move)
        game.undo()

        # cas 1 : pièce revenue à sa place
        self.assertIsNotNone(game.board.squares[6][4])

        # cas 2 : historique vide ou restauré
        self.assertEqual(len(game.moves), 0)

    # ─────────────────────────────────────────
    # 4. Tests save / load
    # ─────────────────────────────────────────
    def test_save_load(self):
        game = Game("J1", "white", 0, "local", "J2")

        pawn = game.board.squares[6][4]
        move = pawn.possible_moves()[0]

        game.play(move)
        game.save()

        loaded = Game.load_game()

        # cas 1 : même nombre de coups
        self.assertEqual(len(game.moves), len(loaded.moves))

        # cas 2 : même tour
        self.assertEqual(game.board.trait, loaded.board.trait)


if __name__ == "__main__":
    unittest.main()