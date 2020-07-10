from time import sleep
from random import random,seed
from math import inf
from time import time

f1 = 22
f2 = 110
n_cells = 10_000
timesteps = 5_000
initial_prob = 0.5
mlambda = 0.2

def local_f(rule, x, y, z):
    return (rule >> (x * 4 + y * 2 + z) & 1)

def f(state, oldstate):
    for cell_num in range(n_cells):
        x = oldstate[(cell_num - 1) % n_cells]
        y = oldstate[cell_num % n_cells]
        z = oldstate[(cell_num + 1) % n_cells]

        if random() > mlambda:
            state[cell_num] = local_f(f1, x, y, z)
        else:
            state[cell_num] = local_f(f2, x, y, z)

def state_density(state):
    return sum(state) / n_cells

def state_kink_density(state):
    return sum(
        map(lambda neighbours: 1 if neighbours[0] != neighbours[1] else 0,
            zip(state, state[1::] + [state[0]]))) / n_cells
    
def simulate():
    state = list(map(lambda x: random() < initial_prob, range(n_cells)))
    state_old = state.copy()
    for i in range(timesteps):
        f(state, state_old)
        state, state_old = state_old, state
    
    return state_old
    
def calc_densities():
    λ = 0 # in percent
    
    densities = []
    while λ <= 100:
        global mlambda
        mlambda = λ / 100.0
        state = simulate()
        densities.append((mlambda, state_density(state), state_kink_density(state)))
        
        if (λ < 5) or (λ >= 95):
            λ += 1
        else:
            λ += 5
    return densities

t1 = time()
md = calc_densities()
t2 = time()

print(md)
print(f"Took {(t2 -t1):.2}s")
