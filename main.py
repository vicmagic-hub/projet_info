from model.game import Game

#lancement du programme
if __name__ == "__main__":
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

    g = Game(player_1, "white", level, type, opponent)