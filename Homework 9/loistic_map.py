import csv
import random
import statistics

if __name__ == "__main__":
    # Read input
    with open("input09.txt") as f:
        x0, r, n, seed = f.read().split()
    r = float(r)
    n = int(n)
    random.seed(int(seed))

    # Generate points
    log_map_pts = [float(x0)]
    seed_pts = [0]
    for i in range(n):
        log_map_pts.append(r * log_map_pts[-1] * (1 - log_map_pts[-1]))
        seed_pts.append(random.random())

    # Write output
    with open("output09.csv", "w") as f:
        writer = csv.writer(f)

        # Write input parameters
        writer.writerow(["x0", "r", "N", "seed"])
        writer.writerow([x0, r, n, seed])

        # Write generated output
        for i in range(n):
            writer.writerow(
                [i + 1, f"{log_map_pts[i + 1]:.6f}", f"{seed_pts[i + 1]:.6f}"]
            )

        # First element is placeholder, pop them out
        log_map_pts.pop(0)
        seed_pts.pop(0)

        # Write mean & std
        writer.writerow(
            [
                "mean",
                f"{statistics.mean(log_map_pts):.6f}",
                f"{statistics.mean(seed_pts):.6f}",
            ]
        )
        writer.writerow(
            [
                "std",
                f"{statistics.stdev(log_map_pts):.6f}",
                f"{statistics.stdev(seed_pts):.6f}",
            ]
        )
