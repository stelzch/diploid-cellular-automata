from time import sleep
from random import random

RULE_NUMBER = 30
N = 240
ON_PERCENTAGE = 0.01
LINES_PER_SECOND = 25
SYMBOLS = {
    0: " ",
    1: "█"
}

def local_f(x, y, z):
    return (RULE_NUMBER >> (x * 4 + y * 2 + z) & 1)

def f(state):
    new_state = [0] * N
    for cell_num in range(N):
        x = state[(cell_num - 1) % N]
        y = state[cell_num % N]
        z = state[(cell_num + 1) % N]

        new_state[cell_num] = local_f(x, y, z)
    return new_state


def state2string(arr):
    return "".join(map(lambda cell: SYMBOLS[cell], arr))

if __name__ == '__main__':
    state = list(map(lambda _: random() < ON_PERCENTAGE, range(N)))

    
    while True:
        print(state2string(state))
        sleep(1.0 / LINES_PER_SECOND)
        state = f(state)
