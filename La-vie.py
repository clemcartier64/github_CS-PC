import multiprocessing as mp
import time

# Quelques codes d'échappement (tous ne sont pas utilisés)
CLEARSCR="\x1B[2J\x1B[;H"          #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"             #  effacer après la position du curseur
CRLF  = "\r\n"                     #  Retour à la ligne

# Nov 2021
# Course Hippique (version élèves)
# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

# Taille de la grille
TAILLE_GRILLE = 10

# Codes d'échappement pour le graphique
CLEARSCR = "\x1B[2J\x1B[;H"  # Effacer l'écran
GOTOYX = "\x1B[%.2d;%.2dH"  # Déplacer le curseur

def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='') # Un exemple !

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
                ligne_str += "   "  # Cellule morte
        print(ligne_str)

def initialiser_grille():
    grille = [[0] * TAILLE_GRILLE[1] for _ in range(TAILLE_GRILLE[0])]
    for i in range(TAILLE_GRILLE[0]):
        for j in range(TAILLE_GRILLE[1]):
            grille[i][j] = random.randint(0, 1)  # Initialisation aléatoire des cellules
    return grille

def mise_a_jour_grille(grille):
    nouvelle_grille = [[0] * TAILLE_GRILLE[1] for _ in range(TAILLE_GRILLE[0])]

    for i in range(TAILLE_GRILLE[0]):
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

    return nouvelle_grille

def jeu_de_la_vie(grille, keep_running):
    while keep_running.value:
        afficher_grille(grille)
        grille = mise_a_jour_grille(grille)
        time.sleep(3)  # Attente d'une seconde entre chaque génération

# La partie principale
if __name__ == "__main__":
    grille = initialiser_grille()
    keep_running = mp.Value('i', 1)  # Valeur partagée pour contrôler l'exécution du jeu

    jeu_process = mp.Process(target=jeu_de_la_vie, args=(grille, keep_running))
    jeu_process.start()

    input("Appuyez sur Enter pour arrêter le jeu.")

    keep_running.value = 0
    jeu_process.join()
