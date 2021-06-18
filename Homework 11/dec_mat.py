import csv
import os

import numpy as np
from PIL import Image, ImageStat
from scipy.stats import entropy

DIR_MAPPING = {
    "Origi_image": "output11.csv",
    "Encry_image": "output11_en.csv",
    "Decry_image": "output11_de.csv",
}


def calculate_metrics(img: Image):
    stat = ImageStat.Stat(img)
    hist = img.histogram()
    rhist = np.array(hist[0:256])
    ghist = np.array(hist[256:512])
    bhist = np.array(hist[512:768])

    return {
        "MIR": f"{round(stat.mean[0], 2):.2f}",
        "MIG": f"{round(stat.mean[1], 2):.2f}",
        "MIB": f"{round(stat.mean[2], 2):.2f}",
        "VHR": f"{round(np.var(rhist), 2):.2f}",
        "VHG": f"{round(np.var(ghist), 2):.2f}",
        "VHB": f"{round(np.var(bhist), 2):.2f}",
        "SER": f"{round(entropy(rhist, base=2), 6):.6f}",
        "SEG": f"{round(entropy(ghist, base=2), 6):.6f}",
        "SEB": f"{round(entropy(bhist, base=2), 6):.6f}",
    }


def export_results(filename: str, results: dict):
    with open(filename, "w") as csvfile:
        fieldnames = [
            "No",
            "Images",
            "MIR",
            "MIG",
            "MIB",
            "VHR",
            "VHG",
            "VHB",
            "SER",
            "SEG",
            "SEB",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for data in results:
            writer.writerow(data)


if __name__ == "__main__":

    for dir, output_metrics_file in DIR_MAPPING.items():
        results = []
        files = os.listdir(dir)
        files.sort()
        for index, file in enumerate(files):
            path = os.path.join(dir, file)
            with Image.open(path) as img:
                metrics = calculate_metrics(img)
            metrics.update(
                {
                    "No": index + 1,
                    "Images": file,
                }
            )
            results.append(metrics)
        export_results(output_metrics_file, results)
