# Projet Info : Modélisation d'un jeu d'échec

Chess.com n'a qu'à bien se tenir 

Moteur d’échecs orienté objet développé sous Python, intégrant :
- un système de gestion des règles des échecs(complet sauf nulles hors pat),
- un mode joueur contre joueur local,
- plusieurs intelligences artificielles,
- un algorithme MinMax avec profondeur configurable,
- un système de simulation et d’annulation de coups.

---

# Présentation

Ce projet informatique est un moteur d’échecs entièrement codé sous Python dans une approche orientée objet.
Le moteur fonctionne pour l'instant intégralement dans le terminal.
Version de python recommandée : 3.12 / Devrait fonctionner pour 3.10+ / Pas au-delà de 3.12 (compatibilité pygame)
Les seules bibliothèques utilisées sont : 
- random
- unitest
- abc
- datetime
- pygame (2.6.1)
---

# Fonctionnalités

## Jeu
- Partie locale joueur contre joueur
- Partie contre IA
- Affichage ASCII du plateau ou IHM
- Sauvegarde et chargement de parties non terminées

## Règles des échecs
- Déplacements légaux
- Échecs
- Échecs et mats
- Pats
- Promotions
- Promotions avec prise
- Roque petit et grand
- Prise en passant
- WARNING : ne gère pas les nulles en 50 coups où les répétitions de positions

## IA
### Niveau 1 — DumbAI
IA aléatoire jouant un coup légal au hasard.

### Niveau 2 — MinmaxAI
IA utilisant :
- l’algorithme MinMax récursif,
- une profondeur configurable,
- une fonction d’évaluation matérielle simpliste.

---
# Lancement du programme

Pour lancer une partie, il suffit d'éxécuter main.py et de se laisser guider
Pour passer en mode dégradé, lancer la version console

---

# Architecture du projet

```text
projet_info/
│
├── main.py
│
├── ai/
│   └── ai_lab.py
│
├── game/
│   └── save.txt (eventuelle partie en cours sauvegardée)
│
├── model/
│   ├── board.py
│   ├── game.py
│   ├── piece.py
│   └── coup_encodeur.py
│
├── ui/
│   ├── interface_console.py
│   └── interface_graphique.py
│
├── tests/
│   └── test_chess.py
│
└── README.md
... et autres fichiers plus ou moins utile (compatibilté OS, ...)
---

