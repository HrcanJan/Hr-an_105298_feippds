"""This module implements the solution to the savages problem """

__author__ = "Ján Hrćan"
__email__ = "xhrcan@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print, Semaphore
from time import sleep, time

NUM_SAVAGES: int = 10
NUM_POT: int = 5        # Number of portions in the pot
NUM_COOKS: int = 2


class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.mutex = Mutex()
        self.mutex2 = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        
        self.barrier1 = Semaphore(0)
        self.barrier2 = Semaphore(0)
        self.barrier_count = 0


def getServingFromPot(i, shared):
    """
    Savage is getting a serving of food.

    shared:   shared class between threads
    i:        savage_id
    """
    print(f"Savage {i} is getting a serving of food")
    shared.servings -= 1
    sleep(2)


def savage(i, shared):
    """
    Function represents savages behaviour.

    shared:   shared class between threads
    i:        savage_id
    """
    while True:
        shared.mutex.lock()
        shared.barrier_count += 1
        print(f"Savage {i} wants to eat. There's {shared.barrier_count} of them waiting.")
        if(shared.barrier_count == NUM_SAVAGES):
            shared.barrier1.signal(NUM_SAVAGES)
            print("All the savages have arrived to eat. The feast shall comence")
        shared.mutex.unlock()
        shared.barrier1.wait()

        shared.mutex.lock()
        shared.barrier_count -= 1
        if shared.barrier_count == 0:
            shared.barrier2.signal(NUM_SAVAGES)
        shared.mutex.unlock()
        shared.barrier2.wait()

        shared.mutex2.lock()
        print(f"Savage {i} is first in queue to take their portion. Remaining portions: {shared.servings} / {NUM_POT}")
        if(shared.servings == 0):
            print(f"Savage {i} is waking up the cook")
            shared.empty_pot.signal()
            shared.full_pot.wait()
        getServingFromPot(i, shared)
        shared.mutex2.unlock()

        print(f"Savage {i} is feasting")
        sleep(4)


def putServingInPot(shared):
    """
    The cook is filling the pot with food

    shared:   shared class between threads
    """
    shared.mutex.lock()
    print(f"The cook filling the pot with food")
    shared.servings += NUM_POT
    shared.mutex.unlock()


def cook(i, shared):
    """
    Function represents cook behaviour.

    i:        id of the cook
    shared:   shared class between threads
    """
    while True:
        shared.empty_pot.wait()
        putServingInPot(shared)
        sleep(5)
        shared.full_pot.signal()


def main():
    """Run main"""
    global NUM_SAVAGES, NUM_POT
    shared = Shared()
    savages = []
    cooks = []

    for i in range(NUM_SAVAGES):
        savages.append(Thread(savage, i, shared))
    for i in range(NUM_COOKS):
        cooks.append(Thread(cook, i, shared))

    for t in savages:
        t.join()
    for t in cooks:
        t.join()


if __name__ == "__main__":
    main()
