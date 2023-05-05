"""This module contains an implementation of CUDA.
"""

__author__ = "Jan Hrćan"
__email__ = "xhrcan@stuba.sk"
__license__ = "MIT"

from numba import cuda
import matplotlib.pyplot as plt


def transform_to_grayscale(pixels):
    return pixels


if __name__ == '__main__':
    pixel = plt.imread('./img/sivy.jpg')
    new_pixel = transform_to_grayscale(pixel)
    plt.imsave('./img/gray.sivy.jpg', new_pixel, format="jpg")

