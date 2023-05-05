"""This module contains an implementation of CUDA.
"""

__author__ = "Jan Hrćan"
__email__ = "xhrcan@stuba.sk"
__license__ = "MIT"

from numba import cuda
import os
import cv2
import numpy as np
import time


def transform_to_grayscale_cpu(pixels):
    gray_img = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)
    return np.array(gray_img)


def cpu(path):
    start_time = time.time()
    for filename in os.listdir(path):
        (os.path.join(directory, filename))
        img_name = filename.split(".")
        name = img_name[0]

        img = cv2.imread(f'./img/{name}.{img_name[1]}', cv2.IMREAD_GRAYSCALE)
        new_pixel = transform_to_grayscale(img)
        cv2.imwrite(f'./gray_cpu/{name}.{img_name[1]}', new_pixel)

    end_time = time.time()
    timer = round(end_time - start_time, 2)
    print("CPU", timer)


def transform_to_grayscale(pixels):
    return pixels


@cuda.jit
def gpu(path):
    start_time = time.time()
    for filename in os.listdir(path):
        (os.path.join(path, filename))
        img_name = filename.split(".")
        name = img_name[0]

        img = cv2.imread(f'./img/{name}.{img_name[1]}', cv2.IMREAD_GRAYSCALE)
        new_pixel = transform_to_grayscale(img)
        cv2.imwrite(f'./gray_cpu/{name}.{img_name[1]}', new_pixel)
    end_time = time.time()
    timer = round(end_time - start_time, 2)
    print("GPU", timer)


if __name__ == '__main__':
    directory = "./img"
    cpu(directory)
    gpu(directory)
