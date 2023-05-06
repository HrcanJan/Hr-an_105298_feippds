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
from math import ceil


def transform_to_grayscale_cpu(pixels):
    gray_img = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)
    return np.array(gray_img)


def cpu(path):
    start_time = time.time()
    for filename in os.listdir(path):
        img_name = filename.split(".")
        name = img_name[0]

        img = cv2.imread(f'./img/{name}.{img_name[1]}')
        new_pixel = transform_to_grayscale_cpu(img)
        cv2.imwrite(f'./gray_cpu/{name}.{img_name[1]}', new_pixel)

    end_time = time.time()
    timer = round(end_time - start_time, 2)
    print("CPU", timer)


# https://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale
@cuda.jit
def transform_to_grayscale(img, gray):
    row, col = cuda.grid(2)
    if row >= img.shape[0] or col >= img.shape[1]:
        return

    r = img[row, col, 0]
    g = img[row, col, 1]
    b = img[row, col, 2]
    img_gray = 0.299 * r + 0.587 * g + 0.114 * b
    gray[row, col] = img_gray


def gpu(path):
    start_time = time.time()
    for filename in os.listdir(path):
        img_name = filename.split(".")
        name = img_name[0]
        img = cv2.imread(f'./img/{name}.{img_name[1]}')
        height = img.shape[0]
        width = img.shape[1]

        # https://github.com/tj314/ppds-2023-cvicenia/blob/master/seminar5/03_mandelbrot.py
        tpb = (16, 16)
        bpg = (ceil(height / tpb[0]), ceil(width / tpb[1]))
        new_pixel = np.zeros((height, width))
        transform_to_grayscale[bpg, tpb](img, new_pixel)

        cv2.imwrite(f'./gray/{name}.{img_name[1]}', new_pixel)
    end_time = time.time()
    timer = round(end_time - start_time, 2)
    print("GPU", timer)


if __name__ == '__main__':
    directory = "./img"
    cpu(directory)
    gpu(directory)
