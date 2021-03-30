from color_transfer import color_transfer
import cv2

CONVERT_FILES = ["1", "2", "3", "4", "5-self", "6-self"]

if __name__ == "__main__":
    for index in CONVERT_FILES:
        # load the images
        source = cv2.imread(f"sou{index}.bmp")
        target = cv2.imread(f"tar{index}.bmp")

        # transfer the color distribution from the source image
        # to the target image
        transfer = color_transfer(source, target)

        # output image
        cv2.imwrite(f"ult{index}.bmp", transfer)
