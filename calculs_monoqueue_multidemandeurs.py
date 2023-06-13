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
    fini.value -= 1
    
def calcule():
    while not queueCalculs.empty():
        try:
            calcul, identifiant = queueCalculs.get(timeout=1)
        except:
            if fini.value == 0:
                break
            continue
        res =  str(eval(calcul))
        print(f"Un serveur a calculé {calcul} = {res}")
        # time.sleep(1)
        les_queues[identifiant].put(res)
        


if __name__ == '__main__':

    nb_calculateurs = 2
    mes_esclaves = []
    mes_demandeurs = []
    queueCalculs = mp.Queue()
    nb_demandeurs = 3
    nb_expr = 1
    les_queues = []
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

    

    
