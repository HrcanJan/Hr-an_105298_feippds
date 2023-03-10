"""This module implements dinning philosophers problem using the waiter solution. 

This is just a copy of the code from: https://github.com/tj314/ppds-2023-cvicenia/blob/master/seminar4/04_philosophers.py
This implementation is only for comparison purposes.
"""

__author__ = "Tomáš Vavro"
__email__ = "xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep, time

STARVATION: int = 9 # number of seconds philosophers can stay hungry for
NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 10  # number of repetitions of think-eat cycle of philosophers


class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]
        self.waiter: Semaphore = Semaphore(NUM_PHILOSOPHERS - 1)


def think(i: int):
    """Simulate thinking.
    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(1.5)


def eat(i: int):
    """Simulate eating.
    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is eating!\n")
    sleep(1.5)


def philosopher(i: int, shared: Shared):
    """Run philosopher's code.
    Args:
        i -- philosopher's id
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        think(i)
        print(f"{i} wants to eat")
        timeout = time() + STARVATION

        # get forks
        shared.waiter.wait()
        shared.forks[i].lock()
        sleep(0.5)
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()

        if time() > timeout:
            print(f"{i} has starved to death\n")
            shared.forks[i].unlock()
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
            break

        eat(i)
        shared.forks[i].unlock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
        shared.waiter.signal()


def main():
    """Run main."""
    timer = time()
    shared: Shared = Shared()
    philosophers: list[Thread] = [
        Thread(philosopher, i, shared) for i in range(NUM_PHILOSOPHERS)
    ]
    for p in philosophers:
        p.join()
    print("Completed in", round(time() - timer, 3), "seconds")


if __name__ == "__main__":
    main()
    