import csv
import os

import numpy as np
from PIL import Image, ImageStat
from scipy.stats import entropy


def calculate_metrics(img: Image, img_en: Image):

    ar_img = np.transpose(np.array(img), (2, 0, 1))
    r_org, g_org, b_org = ar_img

    ar_img_en = np.transpose(np.array(img_en), (2, 0, 1))
    r_enc, g_enc, b_enc = ar_img_en

    npcr_r = round((r_org != r_enc).sum() / (img.width * img.height) * 100, 4)
    npcr_g = round((g_org != g_enc).sum() / (img.width * img.height) * 100, 4)
    npcr_b = round((b_org != b_enc).sum() / (img.width * img.height) * 100, 4)

    uaci_r = round(
        np.abs(r_org - r_enc).sum() / (img.width * img.height * 255) * 100, 4
    )
    uaci_g = round(
        np.abs(g_org - g_enc).sum() / (img.width * img.height * 255) * 100, 4
    )
    uaci_b = round(
        np.abs(b_org - b_enc).sum() / (img.width * img.height * 255) * 100, 4
    )

    return {
        "NPCR(R)": f"{npcr_r:.4f}",
        "NPCR(G)": f"{npcr_g:.4f}",
        "NPCR(B)": f"{npcr_b:.4f}",
        "UACI(R)": f"{uaci_r:.4f}",
        "UACI(G)": f"{uaci_g:.4f}",
        "UACI(B)": f"{uaci_b:.4f}",
    }


if __name__ == "__main__":

    # Read image names
    DIR = "Origi_image"
    DIR_EN = "Encry_image"
    files = os.listdir(DIR)
    files.sort()

    # Calculation
    results = []
    for index, file in enumerate(files):
        file_en = file.replace(".bmp", "_en.bmp")
        path = os.path.join(DIR, file)
        path_en = os.path.join(DIR_EN, file_en)
        with Image.open(path) as img, Image.open(path_en) as img_en:
            metrics = calculate_metrics(img, img_en)
        metrics.update(
            {
                "No": index + 1,
                "ORI Images": file,
                "ENC Image": file_en,
            }
        )
        results.append(metrics)

    # Export
    with open("Output12.csv", "w") as csvfile:
        fieldnames = [
            "No",
            "ORI Images",
            "ENC Image",
            "NPCR(R)",
            "NPCR(G)",
            "NPCR(B)",
            "UACI(R)",
            "UACI(G)",
            "UACI(B)",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for data in results:
            writer.writerow(data)
