import multiprocessing as mp
import os, time,math, random, sys, ctypes


# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
def frequence_de_hits_pour_n_essais(nb_iteration):
    count = 0
    for _ in range(nb_iteration):
        x = random.random()
        y = random.random()
    # si le point est dans l’unit circle
        if x**2 + y**2 <= 1: 
            count += 1
    
    return count


# Nombre d’essai pour l’estimation
start_time = time.time()
nb_total_iteration = 10000000

hits = frequence_de_hits_pour_n_essais(nb_total_iteration)
approx_pi = 4 *(hits/nb_total_iteration)
print(f"Valeur estimée de Pi par la méthode monoprocessus: {approx_pi} calculée en {round(time.time() - start_time, 2)} s")

# TRACE :
# Valeur estimée de Pi par la méthode monoprocessus: 3.1411388 calculée en 3.78 s