#!/usr/bin/env python
# coding: utf-8
import logging
import math
from typing import List

# logging.getLogger().setLevel(logging.DEBUG)  # Uncomment this for debugging


def comb(n: int, k: int) -> int:
    """Return the possible combination count of given n, and k"""
    if n < k:
        return 0
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def cobidic(n: int, k: int, m: int) -> List[int]:
    """Return the cobidic combination index of given n, k, and m"""
    # Check input value
    if not (1 <= n and n <= 81):
        raise ValueError(f"n should be range in 1 <= n <= 81, got {n}")
    if not (1 <= k and k <= n):
        raise ValueError(f"k should be range in 1 <= k <= n, got {k}")
    if not (0 <= m and m <= comb(n, k) - 1):
        raise ValueError(f"m should be range in 0 <= m <= C(n, k)-1, got {m}")

    # Algorithm
    sequence = []
    range_from = n - 1
    r = m
    for j in range(k, 0, -1):
        if sequence:
            range_from = sequence[-1] - 1
            r = r - comb(sequence[-1], j + 1)
        logging.debug(f"r={r}")
        closest = r  # The Maximum possible distance is r itself
        for i in range(range_from, j - 2, -1):
            cik = comb(i, j)
            r_i_dist = abs(r - cik)
            if cik <= r and r_i_dist <= closest:
                logging.debug(
                    f"i={i}\tC({i}, {j})={cik}\tdist={r_i_dist}, closest={closest}"
                )
                new_sequence_item = i
                closest = r_i_dist
                break
            else:
                logging.debug(f"i={i}\tC({i}, {j})={cik}")
        sequence.append(new_sequence_item)
        logging.debug(f"\t\t\ts_{j}={new_sequence_item}")
    return sequence


if __name__ == "__main__":
    nums = input("n, k, m: ").split()
    if len(nums) != 3:
        raise ValueError("Input exactly 3 number represent n, k, m, respectively")
    n, k, m = list(map(int, nums))
    print(" ".join(map(str, cobidic(n, k, m))))
