import random, time
import multiprocessing as mp

def monte_carlo_pi(nb_total_iteration, queue):
    count = 0
    
    for _ in range(nb_total_iteration):
        x = random.random()
        y = random.random()
        
        if x**2 + y**2 <= 1:
            count += 1
    
    queue.put(count)
    
if __name__ == '__main__':
    
    start_time = time.time() # Lance un chrono
    
    nb_total_iteration = 1000000
    nb_process = mp.cpu_count()
    
    iteration_par_process = nb_total_iteration // nb_process
    
    mes_process = []
    queue = mp.Queue()
    
    for _ in range(nb_process):
        process = mp.Process(target=monte_carlo_pi, args=(iteration_par_process, queue))
        process.start()
        mes_process.append(process)
    
    total_hits = 0
    
    for _ in range(nb_process): 
        result = queue.get() # on récupère dans la queue les contributions des processus
        total_hits += result # on somme ces contributions
    
    for process in mes_process:
        process.join()
    
    # Résultat
    approx_pi = 4 * (total_hits / nb_total_iteration)
    
    print(f"Approximation de PI: {approx_pi} calculée en {round((time.time() - start_time)*1000, 2)} ms")
    
    # TRACE : 
    # Approximation de PI: 3.140504 calculée en 83.56 ms
