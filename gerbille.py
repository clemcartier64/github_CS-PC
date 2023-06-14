import multiprocessing as mp
import time


# Fonction exécutée par les travailleurs
def travailleur(num, k):
    for i in range(nb_iterations):
        demander(k)
        print("   "*num, num, f"- Travailleur {mp.current_process().name} utilise {k} billes")
        time.sleep(1)  # Simulation du travail
        rendre(k)
        print("   "*num, num, f"-Travailleur {mp.current_process().name} rend {k} billes")

# Fonction pour demander des billes
def demander(k):
    
    with verrou:
        while nbr_disponible_billes.value < k:
            condition.wait() # Attente jusqu'à ce que suffisamment de billes soient disponibles
        nbr_disponible_billes.value -= k

# Fonction pour rendre des billes
def rendre(k):
    
    with verrou:
        nbr_disponible_billes.value += k
        time.sleep(0.1)
        condition.notify_all()  # Notification pour indiquer que des billes ont été rendues

def controleur():
    while True:
        time.sleep(0.1)  # Vérification périodique
        with verrou:
            if nbr_disponible_billes.value < 0 or nbr_disponible_billes.value > nb_max_billes:
                print("Erreur : nombre de billes hors de la plage")
                raise
        

if __name__ == "__main__":
    
    nb_max_billes = 9
    nbr_disponible_billes = mp.Value('i', nb_max_billes)
    nb_iterations = 3
    k_bills = [4, 3, 5, 2]  # Liste des demandes de billes pour chaque travailleur
    verrou = mp.Lock()
    condition = mp.Condition(verrou)
    
    processus_travailleurs = []
    
    # Création des processus travailleurs en fonction des demandes de billes
    for i in range(len(k_bills)):
        if k_bills[i] <= nbr_disponible_billes.value:
            p = mp.Process(target=travailleur, args=(i, k_bills[i],))
            processus_travailleurs.append(p)
        else:
            print(f"La demande de ressources du processus {i+1} ({k_bills[i]} billes) dépasse la limite.")
        
    # Démarrage du processus controleur
    controleur_processus = mp.Process(target=controleur)
    
    # Démarrage des processus travailleurs
    for p in processus_travailleurs:
        p.start()
        
    # Démarrage du processus contrôleur
    controleur_processus.start()
    
    # Attente de la fin des processus travailleurs
    for p in processus_travailleurs:
        p.join()
        
    # Arrêt du processus contrôleur
    controleur_processus.terminate()
