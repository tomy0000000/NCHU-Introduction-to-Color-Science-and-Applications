import numpy as np
from PIL import Image

if __name__ == "__main__":

    # Read input operations
    tasks = []
    with open("ART-ENC-input08.txt") as f:
        for line in f:
            tasks.append(line)

    # Run each operations
    with open("ART-ENC-output08.txt", "w") as f:
        for task in tasks:
            filename, operation, store_iteration = task.split()
            source_file = filename.split("_")[1]
            store_iteration = int(store_iteration)

            # Read image
            im_array = np.array(Image.open(source_file))
            if im_array.shape[0] != im_array.shape[1]:
                raise ValueError(f"{source_file} is not a square image")
            original = np.array(im_array)  # create a backup for comparison

            # Construct mapping
            dim = im_array.shape[0]
            x, y = np.meshgrid(range(dim), range(dim), indexing="ij")
            if operation == "+":  # ART
                xmap = (2 * x + y) % dim
                ymap = (x + y) % dim
            elif operation == "-":  # IART
                xmap = (x - y) % dim
                ymap = (2 * y - x) % dim
            else:
                raise ValueError(f"Invalid operation: {operation}")

            # Iterate
            stored = period_found = False
            for iteration in range(1, dim + 1):
                im_array = im_array[xmap, ymap]

                # Store image
                if iteration == store_iteration:
                    out_image = Image.fromarray(im_array)
                    out_image.save(filename)
                    stored = True

                # Check for period
                if np.array_equal(im_array, original):
                    period = iteration
                    period_found = True

                if stored and period_found:
                    break

            # Write results
            task = task.strip("\n")
            f.write(f"{task} {period}\n")
