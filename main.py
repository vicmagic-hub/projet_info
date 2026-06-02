from model.interface_console import ConsoleInterface
from model.interface_graphique import ChessUI

#lancement en IHM
if __name__ == "__main__" :
    ChessUI()

#lancement en console
if __name__ == "__degrade__":
    ConsoleInterface()