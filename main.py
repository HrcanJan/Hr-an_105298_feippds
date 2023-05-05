"""This module contains an implementation of CUDA.
"""

__author__ = "Jan Hrćan"
__email__ = "xhrcan@stuba.sk"
__license__ = "MIT"

from numba import cuda
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np


def transform_to_grayscale_cpu(pixels):
    gray_img = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)

    # Convert the grayscale image to a NumPy array
    img_array = np.array(gray_img)

    return img_array


def transform_to_grayscale(pixels):
    return pixels


if __name__ == '__main__':
    directory = "./img"
    for filename in os.listdir(directory):
        filepath = (os.path.join(directory, filename))
        img_name = filename.split(".")
        name = img_name[0]

        img = cv2.imread(f'./img/{name}.{img_name[1]}', cv2.IMREAD_GRAYSCALE)
        new_pixel = transform_to_grayscale(img)
        cv2.imwrite(f'./gray_cpu/{name}.{img_name[1]}', new_pixel)

        pixel = plt.imread(f'./img/{name}.{img_name[1]}')
        new_pixel = transform_to_grayscale(pixel)
        plt.imsave(f'./gray/{name}.{img_name[1]}', new_pixel, format="jpg")
