import math
import random
from decimal import getcontext, Decimal

if __name__ == "__main__":

    # Setting decimal precision
    getcontext().prec = 22

    # Read input
    with open("Input10.txt") as f:
        x0, rx = map(Decimal, f.readline().split())
        y0, ry = map(Decimal, f.readline().split())
        seed, n = map(int, f.readline().split())
        length_raw = f.readline()
        length = Decimal(length_raw)

    # Compute
    random.seed(seed)
    rand_ints = random.sample(range(n), 3)

    log_map_x = x0
    for i in range(rand_ints[0]):
        log_map_x = rx * log_map_x * (1 - log_map_x)
    log_map_y = y0
    for i in range(rand_ints[1]):
        log_map_y = ry * log_map_y * (1 - log_map_y)

    a = math.ceil(log_map_x / length)
    b = math.ceil(log_map_y / length)

    # Write output
    with open("Output10.txt", "w") as f:
        # Write input parameters
        f.write(f"{x0} {rx}\n")
        f.write(f"{y0} {ry}\n")
        f.write(f"{seed} {n}\n")
        f.write(length_raw)

        # Write generated output
        f.write(f"{rand_ints[0]} {rand_ints[1]} {rand_ints[2]}\n")
        f.write(f"{log_map_x} {log_map_y}\n")
        f.write(f"{a} {b}\n")
