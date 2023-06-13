import multiprocessing as mp
import time, random


def donne_des_calculs(nb_expr, identifiant):

    caracteres=["*","/","+","-"]
    for _ in range(nb_expr):
        calcul = ""
        chiffre1 = random.randrange(0, 1000, 1)
        chiffre2 = random.randrange(0, 1000, 1)
        operateur = random.randrange(0, 4, 1)
        calcul = calcul + str(chiffre1)
        calcul = calcul + caracteres[operateur]
        calcul = calcul + str(chiffre2)
        queueCalculs.put((calcul, identifiant))
        print(f"Je suis le client {identifiant} et je demande {calcul}")

        res = les_queues[identifiant].get()
        print(f"j'ai mon resultat {res}")
    
    # Lorsqu'un demandeur a fini d'envoyer ses calculs il décrémente fini pour éviter le problème avec get dans une queue (queueCalculs) qui pourrait
    # etre vide
    fini.value -= 1
    
def calcule():
    keep_running = True
    while keep_running:     
        try:
            calcul, identifiant = queueCalculs.get(timeout=1) # leve le blocage de get au bout dune seconde si rien a get et passe dans except
        except:
            if fini.value == 0:
                keep_running = False
            continue
        res =  str(eval(calcul))
        print(f"Un serveur a calculé {calcul} = {res}")
        time.sleep(1)
        les_queues[identifiant].put(res)
        


if __name__ == '__main__':

    nb_calculateurs = 5
    mes_esclaves = []
    mes_demandeurs = []
    queueCalculs = mp.Queue()
    nb_demandeurs = 10
    nb_expr = 4
    les_queues = []
    
    # on initialise fini egale aux nb de demandeurs
    fini = mp.Value("i", nb_demandeurs) 
    
    
    for i in range(nb_demandeurs):
        queueRes = mp.Queue()
        les_queues.append(queueRes)

    for i in range(nb_demandeurs):
        demandeur = mp.Process(target=donne_des_calculs, args=(nb_expr,i))
        demandeur.start()
        mes_demandeurs.append(demandeur)

    
    for _ in range(nb_calculateurs):
        calculateurs = mp.Process(target=calcule)
        calculateurs.start()
        mes_esclaves.append(calculateurs)

    

    for p in mes_esclaves: p.join()
    for p in mes_demandeurs: p.join()

    

    
