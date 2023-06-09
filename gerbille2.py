import multiprocessing as mp
import time



def travailleur(num, k):
    for i in range(nb_iterations):
        demander(k)
        print("   "*num, num, f"- Travailleur {mp.current_process().name} utilise {k} billes")
        time.sleep(1)  # Simulation du travail
        rendre(k)
        print("   "*num, num, f"-Travailleur {mp.current_process().name} rend {k} billes")

def demander(k):
    
    with verrou:
        while nbr_disponible_billes.value < k:
            condition.wait()
        nbr_disponible_billes.value -= k

def rendre(k):
    
    with verrou:
        nbr_disponible_billes.value += k
        time.sleep(0.1)
        condition.notify_all()

def controleur():
    while True:
        time.sleep(0.1)  # Vérification périodique
        with verrou: # 0 < x < 10
            if nbr_disponible_billes.value < 0 or nbr_disponible_billes.value > nb_max_billes:
                print("Erreur : nombre de billes hors de la plage")
                raise
        # print("OK")

if __name__ == "__main__":
    processus_travailleurs = []
    nb_max_billes = 9
    nbr_disponible_billes = mp.Value('i', nb_max_billes)
    nb_iterations = 3
    k_bills = [4, 3, 5, 2]
    verrou = mp.Lock()
    condition = mp.Condition(verrou)

    for i in range(len(k_bills)):
        if k_bills[i] <= nbr_disponible_billes.value:
            
            p = mp.Process(target=travailleur, args=(i, k_bills[i],))
            processus_travailleurs.append(p)
        else:
            print(f"La demande de ressources du processus {i+1} ({k_bills[i]} billes) dépasse la limite.")

    controleur_processus = mp.Process(target=controleur)

    for p in processus_travailleurs:
        p.start()

    controleur_processus.start()

    for p in processus_travailleurs:
        p.join()

    controleur_processus.terminate()
