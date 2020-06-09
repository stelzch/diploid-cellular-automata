#==============================================================================
# DIPLOID STOCHASTIC CELLULAR AUTOMATA
#==============================================================================
# Author: Christoph Stelz
# Creation Date: June 9th, 2020
# Purpose: Prints a diploid cellular automata on the console
#
# For more info, read the paper by Nazim Fatès: DOI 10.1007/978-3-319-58631-1_8

from time import sleep
from random import random
from math import inf
from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='Print diploid cellular automata')
parser.add_argument('-f1_rule', '-F1', type=int, required=True,
        help='Rule number of the first ECA')
parser.add_argument('-f2_rule', '-F2', type=int, required=True,
        help='Rule number of the second ECA')
parser.add_argument('-λ', '-lambda', type=float, default=0.5,
        help='Mixing rate. Must be between 0 and 1. Default value is 0.5')
parser.add_argument('-n_cells', '-N', type=int, default=80,
        help='Number of cells to simulate.')
parser.add_argument('-freq', '-f', type=float, default=23,
        help='Speed in Hz at which to update the cells')
parser.add_argument('-initial_p', '-p', type=float, default=0.1,
        help='Probability a cell is ON at t=0')
parser.add_argument('--output', '-o', type=str,
        help='Output an image instead of writing to the command line')
parser.add_argument('--timesteps', '-t', type=int, default=inf,
        help='Number of timesteps to simulate. Default value is infinite')

args = parser.parse_args()

SYMBOLS = {
    0: " ",
    1: "█"
}
ON_COLOR = (0, 0, 255)
OFF_COLOR = (255, 255, 255)

def local_f(rule, x, y, z):
    return (rule >> (x * 4 + y * 2 + z) & 1)

def f(state, oldstate):
    for cell_num in range(args.n_cells):
        x = oldstate[(cell_num - 1) % args.n_cells]
        y = oldstate[cell_num % args.n_cells]
        z = oldstate[(cell_num + 1) % args.n_cells]

        if random() > args.λ:
            state[cell_num] = local_f(args.f1_rule, x, y, z)
        else:
            state[cell_num] = local_f(args.f2_rule, x, y, z)


def state2string(arr):
    return "".join(map(lambda cell: SYMBOLS[cell], arr))

def print_to_console(initial_state):
    t = 0
    state_b = state.copy()
    while t < args.timesteps:
        t += 1
        print(state2string(state))
        try:
            sleep(1.0 / args.freq)
        except KeyboardInterrupt:
            break
        f(state_b, state)
        state, state_b = state_b, state

def print_to_image(initial_state, path):
    width = args.n_cells
    try:
        height = int(args.timesteps)
    except:
        print("[ERROR] Height must be finite when outputting image")
        return
    
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    state = initial_state
    state_b = state.copy()

    for t in range (height):
        for x in range(width):
            pixels[x, t] = ON_COLOR if state[x] == 1 else OFF_COLOR
        f(state_b, state)
        state, state_b = state_b, state

    img.save(path)
    

if __name__ == '__main__':
    state = list(map(lambda _: random() < args.initial_p, range(args.n_cells)))

    if args.output:
        print_to_image(state, args.output)
    else:
        print_to_console(state)

    
