import random, time
import multiprocessing as mp

def monte_carlo_pi(nb_total_iteration):
    count = 0

    for _ in range(nb_total_iteration):
        x = random.random()
        y = random.random()
        
        if x**2 + y**2 <= 1:
            count += 1

    return count

def travail_des_process(nb_total_iteration, queue):
    result = monte_carlo_pi(nb_total_iteration)
    queue.put(result)
    

def calculate_pi(nb_total_iteration, nb_process):
    iteration_par_process = nb_total_iteration // nb_process

    mes_process = []
    queue = mp.Queue()

    for _ in range(nb_process):
        process = mp.Process(target=travail_des_process, args=(iteration_par_process, queue))
        process.start()
        mes_process.append(process)

    total_hits = 0

    for _ in range(nb_process):
        result = queue.get()
        total_hits += result

    for process in mes_process:
        process.join()

    approx_pi = 4 * (total_hits / nb_total_iteration)
    return approx_pi

if __name__ == '__main__':
    start_time = time.time()
    nb_total_iteration = 1000000
    nb_process =  mp.cpu_count()
    
    

    approx_pi = calculate_pi(nb_total_iteration, nb_process)
    print(time.time() - start_time)
    print(f"Approximation de PI: {approx_pi}")
