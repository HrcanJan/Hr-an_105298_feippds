"""This module implements dinning philosophers problem.

 Lefties/righties solution is implemented.
 """

__author__ = "Ján Hrćan"
__email__ = "xhrcan@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print
from time import sleep, time

STARVATION: int = 9 # number of seconds philosophers can stay hungry for
NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 10  # number of repetitions of think-eat cycle of philosophers


# The backbone of the entire application inspired from: https://github.com/tj314/ppds-2023-cvicenia/blob/master/seminar4/04_philosophers.py
class Shared:
    """Represent shared data for all threads."""
    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]


def think(i: int):
    """
    Simulate thinking.
    
    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(1.5)


def eat(i: int):
    """
    Simulate eating.

    Args: 
        i -- philosopher's id
    """
    print(f"Philosopher {i} is eating!\n")
    sleep(1.5)


# The idea inspired of the implementation from: https://www.geeksforgeeks.org/dining-philosophers-problem/
def philosopher(i: int, shared: Shared):
    """
    Run philosopher's code.
    Lefties/righties method: the philosopher with the lowest id is a lefty.

    Args:
        i      -- philosopher's id
        shared -- shared data
    """
    left_fork = i
    right_fork = (i + 1) % NUM_PHILOSOPHERS
    if(i == 0):
        right_fork = i
        left_fork = (i + 1) % NUM_PHILOSOPHERS

    for _ in range(NUM_RUNS):
        think(i)
        print(f"{i} wants to eat")
        timeout = time() + STARVATION

        # get forks
        shared.forks[left_fork].lock()
        sleep(0.5)
        shared.forks[right_fork].lock()

        if time() > timeout:
            print(f"{i} has starved to death\n")
            shared.forks[left_fork].unlock()
            shared.forks[right_fork].unlock()
            break

        eat(i)
        shared.forks[left_fork].unlock()
        shared.forks[right_fork].unlock()


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
