import multiprocessing as mp
import os
import random
import time

# Taille de la grille
TAILLE_GRILLE = (15, 15)

def afficher_grille(grille):
    os.system("clear")  # Effacer l'écran (pour Linux/Mac)
    # os.system("cls")  # Effacer l'écran (pour Windows)

    for ligne in grille:
        ligne_str = ""
        for cellule in ligne:
            if cellule:
                ligne_str += "■"  # Cellule vivante
            else:
                ligne_str += "□"  # Cellule morte
        print(ligne_str)

def initialiser_grille_partagee():
    grille = mp.Array('i', [0] * (TAILLE_GRILLE[0] * TAILLE_GRILLE[1]))
    for i in range(TAILLE_GRILLE[0]):
        for j in range(TAILLE_GRILLE[1]):
            grille[i * TAILLE_GRILLE[1] + j] = random.randint(0, 1)  # Initialisation aléatoire des cellules
    return grille


def mise_a_jour_grille(grille, sous_grille):
    nouvelle_grille = [[0] * TAILLE_GRILLE[1] for _ in range(TAILLE_GRILLE[0])]

    for i in range(sous_grille[0], sous_grille[1]):
        for j in range(TAILLE_GRILLE[1]):
            voisins = 0

            # Compter le nombre de voisins vivants
            for x in range(max(0, i - 1), min(TAILLE_GRILLE[0], i + 2)):
                for y in range(max(0, j - 1), min(TAILLE_GRILLE[1], j + 2)):
                    if (x, y) != (i, j) and grille[x][y]:
                        voisins += 1

            # Appliquer les règles du jeu de la vie
            if grille[i][j]:
                if voisins == 2 or voisins == 3:
                    nouvelle_grille[i][j] = 1  # Cellule vivante
                else:
                    nouvelle_grille[i][j] = 0  # Cellule morte
            else:
                if voisins == 3:
                    nouvelle_grille[i][j] = 1  # Cellule vivante

    for i in range(sous_grille[0], sous_grille[1]):
        for j in range(TAILLE_GRILLE[1]):
            grille[i][j] = nouvelle_grille[i][j]

def jeu_de_la_vie(grille, sous_grille, keep_running):
    while keep_running.value:
        afficher_grille(grille)
        mise_a_jour_grille(grille, sous_grille)
        time.sleep(1)  # Attente d'une seconde entre chaque génération

# La partie principale
if __name__ == "__main__":
    grille = initialiser_grille_partagee()
    keep_running = mp.Value('i', 1)  # Valeur partagée pour contrôler l'exécution du jeu

    # Division de la grille en 4 sous-grilles
    quart_taille = TAILLE_GRILLE[0] // 4
    sous_grilles = [
        mp.Array('i', [i * quart_taille, (i + 1) * quart_taille]) for i in range(4)
    ]

    processes = []
    for i in range(4):
        process = mp.Process(target=jeu_de_la_vie, args=(grille, sous_grilles[i], keep_running))
        process.start()
        processes.append(process)

    input("Appuyez sur Enter pour arrêter le jeu.")

    keep_running.value = 0

    for process in processes:
        process.join()
