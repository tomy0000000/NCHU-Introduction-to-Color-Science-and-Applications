import csv
import os
from typing import Dict, Tuple

import numpy as np
from PIL import Image

DIR = "Origi_image"
DIR_EN = "Encry_image"
MODES = ["HD", "VD", "DD"]
CHANNELS = ["R", "G", "B"]


def process_img(img_path: str, img_name: str) -> Dict:
    results = []
    with Image.open(img_path) as img:
        img_arr = np.transpose(np.array(img), (2, 0, 1))
    for mode in MODES:
        for channel, img_mono_arr in zip(CHANNELS, img_arr):
            x_vector, y_vector = slice_array(img_mono_arr, mode)
            metrics = calculate_metrics(x_vector, y_vector)
            metrics.update(
                {
                    "Image Name": img_name,
                    "Mode": mode,
                    "Channel": f"{channel} Channel",
                }
            )
            results.append(metrics)
    return results


def slice_array(mono_arr: np.array, mode: str) -> Tuple[np.array, np.array]:
    if mode == "HD":
        return (mono_arr[:, :-1].flatten(), mono_arr[:, 1:].flatten())
    if mode == "VD":
        return (mono_arr[:-1, :].flatten(), mono_arr[1:, :].flatten())
    if mode == "DD":
        return (mono_arr[:-1, :-1].flatten(), mono_arr[1:, 1:].flatten())
    raise ValueError(f"Invalid mode: {mode}")


def calculate_metrics(x_vector: np.array, y_vector: np.array) -> Dict:
    return {
        "MEAN(X)": f"{round(x_vector.mean(), 2):.2f}",
        "MEAN(Y)": f"{round(y_vector.mean(), 2):.2f}",
        "VAR(X)": f"{round(x_vector.var(ddof=1), 2):.2f}",
        "VAR(Y)": f"{round(y_vector.var(ddof=1), 2):.2f}",
        "COV(X,Y)": f"{round(np.cov(x_vector, y_vector, rowvar=False, ddof=1)[0][1], 2):.2f}",
        "Correlation(X,Y)": f"{round(np.corrcoef(x_vector, y_vector, rowvar=False)[0][1], 6):.6f}",
    }


if __name__ == "__main__":

    # Read image names
    files = os.listdir(DIR)
    files.sort()

    # Calculation
    results = []
    for index, file in enumerate(files):
        # Process original image
        path = os.path.join(DIR, file)
        results.extend(process_img(path, file))

        # Process encrypted image
        file_en = file.replace(".bmp", "_en.bmp")
        path_en = os.path.join(DIR_EN, file_en)
        results.extend(process_img(path_en, file_en))

    # Export
    with open("Output13.csv", "w") as csvfile:
        fieldnames = [
            "Image Name",
            "Mode",
            "Channel",
            "MEAN(X)",
            "MEAN(Y)",
            "VAR(X)",
            "VAR(Y)",
            "COV(X,Y)",
            "Correlation(X,Y)",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for data in results:
            writer.writerow(data)
