def arc_tangente(n):
    pi = 0
    for i in range(n):
        pi += 4/(1+ ((i+0.5)/n)**2)
    return (1/n)*pi

print(arc_tangente(0))