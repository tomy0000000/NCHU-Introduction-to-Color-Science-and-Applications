import numpy as np
from PIL import Image

if __name__ == "__main__":

    # Read input operations
    tasks = []
    with open("ART-DEC-input08.txt") as f:
        for line in f:
            tasks.append(line)

    # Run each operations
    with open("ART-DEC-output08.txt", "w") as f:
        for task in tasks:
            filename, operation, restore_iteration, _ = task.split()
            source_file = filename.split("_")[1]
            restore_iteration = int(restore_iteration)

            # Read image
            im_array = np.array(Image.open(filename))
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
            for iteration in range(restore_iteration):
                im_array = im_array[xmap, ymap]

            # Store image
            out_image = Image.fromarray(im_array)
            out_image.save(source_file)

            # Write results
            f.write(f"{source_file}\n")
