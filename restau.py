import time
import random
import multiprocessing as mp
import curses

def client_process(server_queue, display_list):
    client_id = 1
    while True:
        time.sleep(random.randint(1, 4))
        menu_item = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        server_queue.put((client_id, menu_item))
        display_list.append(f"Commande du client {client_id} : Menu {menu_item}")
        client_id += 1

def server_process(server_id, server_queue, kitchen_queue, display_list):
    while True:
        client_id, menu_item = server_queue.get()
        display_list.append(f"Serveur {server_id} prend la commande du client {client_id} : Menu {menu_item}")
        time.sleep(random.randint(1, 3))  # Simulation de préparation de commande
        kitchen_queue.put((server_id, client_id, menu_item))

def kitchen_process(kitchen_queue, display_list):
    while True:
        server_id, client_id, menu_item = kitchen_queue.get()
        display_list.append(f"Serveur {server_id} délivre la commande du client {client_id} : Menu {menu_item}")

def display_process(display_list, screen):
    while True:
        screen.clear()
        for i, line in enumerate(display_list[-20:]):  # Afficher les 10 dernières lignes
            screen.addstr(i, 0, line)
        screen.refresh()
        time.sleep(1)  # Rafraîchir l'affichage toutes les secondes

def main(screen):
    server_count = 5
    server_queue = mp.Queue()
    kitchen_queue = mp.Queue()
    display_list = mp.Manager().list()

    processes = []

    # Processus clients
    client_proc = mp.Process(target=client_process, args=(server_queue, display_list))
    processes.append(client_proc)

    # Processus serveurs
    for i in range(server_count):
        server_proc = mp.Process(target=server_process, args=(i + 1, server_queue, kitchen_queue, display_list))
        processes.append(server_proc)

    # Processus cuisine
    kitchen_proc = mp.Process(target=kitchen_process, args=(kitchen_queue, display_list))
    processes.append(kitchen_proc)

    # Processus affichage
    display_proc = mp.Process(target=display_process, args=(display_list, screen))
    processes.append(display_proc)

    # Démarrage des processus
    for process in processes:
        process.start()

    # Attente de la terminaison des processus
    for process in processes:
        process.join()

if __name__ == "__main__":
    curses.wrapper(main)
