# Mai 2023
# Calcul de PI par Arc tg
# Avec Process et Value

import multiprocessing as mp
import random, time, platform

from math import *

def calculer_une_part_de_PI_arc_tangente(my_num, nb_iter, nb_processus, integrale):
    print(" "*my_num*2, f"{my_num}- Je suis le fils Num {my_num}")
    pi = 0.0
    for i in range(0, nb_iter, nb_processus):
        pi += 4/(1+ ((i+0.5)/nb_iter)**2)
    integrale.value += (1/nb_iter)*pi
    print(" "*my_num*2, f"{my_num}- Je suis le fils Num {my_num} et ma part = {(1/nb_iter)*pi}")

if __name__ == "__main__" :
    #Pour tenir compte du MacOS
    import os, platform
    if platform.system() == 'Windows':
        mp.set_start_method('spawn')
    else:
        mp.set_start_method('fork')
        
    nb_processus = 16
    # Nombre d’essai pour l’estimation
    nb_total_iteration = 1000000
    integrale = mp.Value('f', 0.0)
    
    start_time = time.time()    
    tab_pid=[0 for i in range(nb_processus)]
    for i in range(nb_processus) :
        tab_pid[i]=mp.Process(target=calculer_une_part_de_PI_arc_tangente, args=(i+1, nb_total_iteration // nb_processus,nb_processus,integrale))
        tab_pid[i].start()
        
    for i in range(nb_processus) :
        tab_pid[i].join() 
    
    print("Valeur estimée Pi par la méthode Tangente : ", integrale.value)
    print("Temps d'execution : ", time.time() - start_time)
    
"""
Trace : comparer les temps entre 1, 4 et 8 processus

Avec Un seule processus :
--------------------------
1- Je suis le fils Num 1
1- Je suis le fils Num 1 et ma part = 3.141592653589764
Valeur estimée Pi par la méthode Tangente :  3.1415927410125732
Temps d'execution :  0.09533095359802246

Avec 4 Processus : 
---------------------
1- Je suis le fils Num 1
  2- Je suis le fils Num 2
    3- Je suis le fils Num 3
      4- Je suis le fils Num 4
1- Je suis le fils Num 1 et ma part = 0.7854011633937813
  2- Je suis le fils Num 2 et ma part = 0.7854011633937813
    3- Je suis le fils Num 3 et ma part = 0.7854011633937813
      4- Je suis le fils Num 4 et ma part = 0.7854011633937813
Valeur estimée Pi par la méthode Tangente :  3.1416046619415283
Temps d'execution :  0.011185884475708008

...

Avec 8 Processus : 
--------------------
1- Je suis le fils Num 1
  2- Je suis le fils Num 2
    3- Je suis le fils Num 3
1- Je suis le fils Num 1 et ma part = 0.3927060816433928
      4- Je suis le fils Num 4
  2- Je suis le fils Num 2 et ma part = 0.3927060816433928
        5- Je suis le fils Num 5
          6- Je suis le fils Num 6
    3- Je suis le fils Num 3 et ma part = 0.3927060816433928
            7- Je suis le fils Num 7
      4- Je suis le fils Num 4 et ma part = 0.3927060816433928
              8- Je suis le fils Num 8
        5- Je suis le fils Num 5 et ma part = 0.3927060816433928
          6- Je suis le fils Num 6 et ma part = 0.3927060816433928
            7- Je suis le fils Num 7 et ma part = 0.3927060816433928
              8- Je suis le fils Num 8 et ma part = 0.3927060816433928
Valeur estimée Pi par la méthode Tangente :  3.141648769378662
Temps d'execution :  0.00885772705078125

# Autre chose : 
>>> import psutil
>>> try:
...     print(psutil.cpu_count()) 
... except :
...     pass
... 
8

On peut faire la même chose avec "os" au lieu de "psutil"
"""