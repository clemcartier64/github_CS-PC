import time
import random
import multiprocessing as mp
import curses

def travail_client(queue_serveur, liste_dAffichage):
    client_id = 1
    while True:
        time.sleep(random.randint(1, 2))                                                 # un client arrive aléatoirement 
        menu_item = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')                          # il choisit un menu
        queue_serveur.put((client_id, menu_item))                                        # il envoie son id et son menu dans la queue pour les serveurs et
        liste_dAffichage.append(f"Commande du client {client_id} : Menu {menu_item}")    # il envoie le message correspondant pour l'affichage donc dans la liste
        client_id += 1                                                                   # change d'identifiant pour le prochain client

def commande_serveur(server_id, queue_serveur, queue_cuisine, liste_dAffichage):
    while True:
        client_id, menu_item = queue_serveur.get()                                                                   # récupere une commande d'un client dans la queue
        liste_dAffichage.append(f"  Serveur {server_id} prend la commande du client {client_id} : Menu {menu_item}") # Dis ce qu'il fait sur l'écran
        time.sleep(random.randint(1, 3))                                                                             # Simulation de préparation de commande
        queue_cuisine.put((server_id, client_id, menu_item))                                                         # Envoie la commande à la queue cuisine avec notement un serveur_id

def cuisto(queue_cuisine, liste_dAffichage):
    while True: 
        server_id, client_id, menu_item = queue_cuisine.get()                                                                                     # récupere la commande prise par le bien connu serveur
        liste_dAffichage.append(f"      Le cuisto prepare la commande du client {client_id} : Menu {menu_item} prise par le serveur {server_id}") # affiche 
        liste_dAffichage.append(f"          Serveur {server_id} délivre la commande du client {client_id} : Menu {menu_item}")

def majordHomme(liste_dAffichage, screen):
    while True:
        screen.clear()
        for i, line in enumerate(liste_dAffichage[-20:]):  # Garde afficher à l'ecran les 20 dernier messages
            screen.addstr(i, 0, line)
        screen.refresh()                                   # Rafraîchir l'affichage
        time.sleep(1)                                      # toutes les secondes

def main(screen):
    
    nb_serveur = 5
    queue_serveur = mp.Queue()
    queue_cuisine = mp.Queue()
    liste_dAffichage = mp.Manager().list() # liste partagée qui gère l'affichage

    mes_process = [] # Tous dans le même tab

    # Processus clients
    process_client = mp.Process(target=travail_client, args=(queue_serveur, liste_dAffichage))
    mes_process.append(process_client)

    # Processus serveurs
    for i in range(nb_serveur):
        process_serveur = mp.Process(target=commande_serveur, args=(i + 1, queue_serveur, queue_cuisine, liste_dAffichage))
        mes_process.append(process_serveur)

    # Processus cuisine
    process_cuisine = mp.Process(target=cuisto, args=(queue_cuisine, liste_dAffichage))
    mes_process.append(process_cuisine)

    # Processus affichage
    process_affichage = mp.Process(target=majordHomme, args=(liste_dAffichage, screen))
    mes_process.append(process_affichage)

    # Démarrage des processus
    for process in mes_process:
        process.start()

    # Attente de la terminaison des processus
    for process in mes_process:
        process.join()

if __name__ == "__main__":
    curses.wrapper(main) # Utilisation du module curse pour l'affichage
