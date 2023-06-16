import multiprocessing as mp
import time, random


def donne_des_calculs(nb_expr):

    caracteres=["*","/","+","-"]
    for _ in range(nb_expr):
        calcul = ""
        chiffre1 = random.randrange(0, 1000, 1)
        chiffre2 = random.randrange(0, 1000, 1)
        operateur = random.randrange(0, 4, 1)
        calcul = calcul + str(chiffre1)
        calcul = calcul + " " + caracteres[operateur] + " "
        calcul = calcul + str(chiffre2)
        queueCalculs.put(calcul)
        print(f"Je demande {calcul}")
    fini.value = True
    
def calcule():
    keep_running = True
    while keep_running:
        try:
            calcul = queueCalculs.get(timeout=1)
        except:
            if fini.value == True:
                keep_running = False
            continue
        res =  str(eval(calcul))
        print(f"Le calculateur {mp.current_process().name} a calculé {calcul} = {res}")
        time.sleep(0.5)
        UniqueQueueRes.put(res)
        


if __name__ == '__main__':

    nb_calculateurs = mp.cpu_count()//2
    mes_calculateurs = []
    
    nb_demandeurs = mp.cpu_count() - nb_calculateurs
    nb_expr = 5
    
    queueCalculs = mp.Queue()
    UniqueQueueRes = mp.Queue()
    
    fini = mp.Value("b", False) 
    
    
    demandeur = mp.Process(target=donne_des_calculs, args=(nb_expr,))
    demandeur.start()
    
    
    for _ in range(nb_calculateurs):
        calculateurs = mp.Process(target=calcule, name=f"{_}")
        calculateurs.start()
        mes_calculateurs.append(calculateurs)

    for p in mes_calculateurs: p.join()
    demandeur.join()