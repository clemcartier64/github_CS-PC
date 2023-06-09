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
        calcul = calcul + caracteres[operateur]
        calcul = calcul + str(chiffre2)
        queue.put(calcul)
        print("Le client a demandé ", calcul)
    
def calcule():

    calcul = queue.get()
    res =  str(eval(calcul))
    print(f"Un serveur a calculé {calcul} = {res}")
    time.sleep(1)
        


if __name__ == '__main__':

    queue = mp.Queue()
    queueRes = mp.Queue()


    nb_expr = 50
    expressions = []
    
    demandeur = mp.Process(target=donne_des_calculs, args=(nb_expr,))
    demandeur.start()
    expressions.append(demandeur)

    nb_calculateurs = 10
    mes_esclaves = []
    for _ in range(nb_calculateurs):
        calculateurs = mp.Process(target=calcule)
        calculateurs.start()
        expressions.append(calculateurs)

    for p in mes_esclaves: p.join()

    

    2+3

    5*6

    7/2

    (2+3)-(5*6)/(7/2)