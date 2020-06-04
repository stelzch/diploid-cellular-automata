from time import sleep
from PIL import Image

IMAGE_WIDTH, IMAGE_HEIGHT = (40, 80)
OUTPUT_PATH = "eca-overview/"
ON_COLOR = (0, 0, 255)
OFF_COLOR = (255, 255, 255)

def local_f(rule, x, y, z):
    return (rule >> (x * 4 + y * 2 + z) & 1)

def f(rule, state):
    N = len(state)
    new_state = [0] * N
    for cell_num in range(N):
        x = state[(cell_num - 1) % N]
        y = state[cell_num % N]
        z = state[(cell_num + 1) % N]

        new_state[cell_num] = local_f(rule, x, y, z)
    return new_state


def state2string(arr):
    return "".join(map(lambda cell: SYMBOLS[cell], arr))

if __name__ == '__main__':
    for ruleno in range(256):
        img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))
        state = [0] * IMAGE_WIDTH
        state[IMAGE_WIDTH // 2] = 1
        pixels = img.load()

        for t in range(IMAGE_HEIGHT):
            for x in range(IMAGE_WIDTH):
                pixels[x, t] = ON_COLOR if state[x] == 1 else OFF_COLOR
            state = f(ruleno, state)
        
        file_path = OUTPUT_PATH + "rule_" + str(ruleno) + ".png"
        img.save(file_path)
        print(f'Generated {file_path}')

