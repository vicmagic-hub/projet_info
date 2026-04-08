"""
Creation de la classe pièce et des sous classes variées
"""

class Piece:
    """
    Classe de base pour les pièces d'échecs
    """
    def __init__(self,color, position):
        self.color = color
        self.position = position
    
    def move(self, new_position):
        """
        Méthode pour déplacer la pièce à une nouvelle position
        Pour le moment elle est très con
        Mais bientôt elle sera abstraite
        Chaque pièce aura sa méthode de déplacement spécifique
        """
        self.position = new_position
    
    def take(self, new_position):
        """
        Méthode pour prendre une pièce adverse
        Pour le moment elle est très con
        Mais bientôt elle sera abstraite
        Chaque pièce aura sa méthode de prise spécifique
        """
        self.position = new_position
    
    def possible_moves(self):
        """
        Méthode pour obtenir les mouvements possibles de la pièce
        Pour le moment elle est très con
        Mais bientôt elle sera abstraite
        Chaque pièce aura sa méthode de mouvements possibles spécifique
        """
        return []
    