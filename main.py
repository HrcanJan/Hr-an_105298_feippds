"""This module contains an implementation of CUDA.

In this application, we use CUDA to demonstrate a difference in transforming images to grayscale using CPU and GPU
separately."""

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
    """This function transforms an image to grayscale using opencv's function.

        parameters:
        pixels:     an image array
    """
    gray_img = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)
    return np.array(gray_img)


def cpu(path, save_path):
    """This function loads all images from a given directory and applies grayscale to all images using CPU.
        Then it saves the images in a given folder.

        parameters:
        path:       path to images folder
        save_path:  path to where the images should be saved
    """
    start_time = time.time()
    for filename in os.listdir(path):
        img_name = filename.split(".")
        name = img_name[0]

        img = cv2.imread(f'./img/{name}.{img_name[1]}')
        new_pixel = transform_to_grayscale_cpu(img)
        cv2.imwrite(f'./{save_path}/{name}.{img_name[1]}', new_pixel)

    end_time = time.time()
    timer = round(end_time - start_time, 2)
    print("CPU", timer)


# https://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale
@cuda.jit
def transform_to_grayscale(img, gray):
    """This function transforms an image to grayscale using CUDA and GPU.

        parameters:
        img:     an image array
        gray:    output variable of the grayscale image
    """
    row, col = cuda.grid(2)
    if row >= img.shape[0] or col >= img.shape[1]:
        return

    r = img[row, col, 0]
    g = img[row, col, 1]
    b = img[row, col, 2]
    img_gray = 0.299 * r + 0.587 * g + 0.114 * b
    gray[row, col] = img_gray


def gpu(path, save_path):
    """This function loads all images from a given directory and applies grayscale to all images using GPU.
        Then it saves the images in a given folder.

        parameters:
        path:       path to images folder
        save_path:  path to where the images should be saved
    """
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

        cv2.imwrite(f'./{save_path}/{name}.{img_name[1]}', new_pixel)
    end_time = time.time()
    timer = round(end_time - start_time, 2)
    print("GPU", timer)


if __name__ == '__main__':
    """Main"""
    directory = "./img"
    cpu(directory, 'gray_cpu')
    gpu(directory, 'gray')
