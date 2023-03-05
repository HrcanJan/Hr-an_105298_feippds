"""
Program represents different sequences of using mutex
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__author__ = "Jan Hrćan"
__email__ = "xhrcan@stuba.sk"
__license__ = "MIT"

from fei.ppds import Mutex, Thread, Semaphore, print
from time import sleep
from random import randint


# The template of the project inspired from: https://github.com/tj314/ppds-2023-cvicenia/blob/master/seminar3/barberShop.py
class Shared(object):
    """"Object Shared for multiple threads using demonstration"""

    def __init__(self):
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    """ 
    Simulate time and print info when customer gets haircut.

    :param i: customer id
    :return:
    """
    print(f"{i} got a haircut")
    sleep(1)


def cut_hair():
    """Simulate time and print info when barber cuts a customer's hair."""
    print("Barber is cutting a customer's hair")
    sleep(4)


def balk(i):
    """ 
    Represents a situation when waiting room is full and prints info.

    :param i: customer id
    :return:
    """
    print(f"Customer {i} can't enter, because the waiting room is full, so he leaves.")
    sleep(randint(10, 20))


# Mutex implementations inspired from: https://github.com/tj314/ppds-2023-cvicenia/blob/master/seminar3/mutex.py
def leave(i, shared):
    """
    Simulates the customer leaving the barbershop and freeing up the space in the waiting room.

    :param shared: object of class Shared
    :param i: customer id
    :return:
    """
    shared.mutex.lock()
    sleep(1 / 100)
    shared.waiting_room -= 1
    print(f"Customer {i} leaves the waiting room. The capacity is now: ", shared.waiting_room, "/", N)
    shared.mutex.unlock()


def growing_hair(i):
    """
    Represents situation when customer wait after getting haircut.
    So the hair is growing and customer is sleeping for some time.

    :param i: customer id
    :return:
    """
    print(f"Customer {i}'s hair is growing\n")
    sleep(randint(10, 20))


def customer_wait(i, shared):
    """
    Checks if the waiting room if full when a customer enters.
    If it is, then the customer leaves.
    If it isn't, then the customer enters the waiting room.

    :param shared: object of class Shared
    :param i: customer id
    :return:
    """
    shared.mutex.lock()
    sleep(1 / 100)
    if shared.waiting_room >= N:
        shared.mutex.unlock()
        balk(i)
        return False
    shared.waiting_room += 1
    print(f"Customer {i} enters the waiting room. The capacity is now: ", shared.waiting_room, "/", N)
    shared.mutex.unlock()
    return True


# Signalization implementation inspired from: https://github.com/tj314/ppds-2023-cvicenia/blob/master/seminar3/signalization.py
def customer(i, shared):
    """
    Function represents customers behaviour. Customer come to waiting if room is full sleep.
    Wake up barber and waits for invitation from barber. Then gets a new haircut.
    After both wait to complete their work, the customer waits to hair grow again before coming back.

    :param shared: object of class Shared
    :param i: customer id
    :return:
    """
    shared.barber.wait()
    sleep(randint(0, 3))

    while True:
        # Access to waiting room. Can the customer enter or must they wait?
        print(f"Customer {i} comes in to the waiting room")
        if not customer_wait(i, shared):
            continue

        # Signalization
        shared.customer.signal()
        shared.barber.wait()
        shared.customer_done.wait()
        get_haircut(i)

        # Leave the waiting room
        leave(i, shared)
        shared.barber_done.signal()
        growing_hair(i)


def barber(shared):
    """
    Function barber represents the barber.
    When a customer comes to get a new haircut, the barber soon wakes up.
    Barber cuts the customer's hair and they both wait to complete their tasks.

    :param shared: object of class Shared
    :return:
    """
    shared.barber.signal(C)
    print("Barber is sleeping")
    sleep(randint(3, 10))
    print("Barber woke up\n")

    while True:
        # Signalization
        shared.barber.signal()
        shared.customer.wait()
        cut_hair()
        
        # Signalization
        shared.customer_done.signal()
        shared.barber_done.wait()


def main():
    global C, N
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


C = 5
N = 3


if __name__ == "__main__":
    main()
