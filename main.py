"""This module contains an implementation of the bakery algorithm.
"""

__author__ = "Jan Hrćan"
__email__ = "xhrcan@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread
from time import sleep

# inspired from https://github.com/tj314/ppds-2023-cvicenia/blob/master/seminar2/04_ticket.py
if __name__ == '__main__':
    DEFAULT_NUM_RUNS = 10
    NUM_THREADS = 5
    