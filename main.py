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


class Shared(object):

    def __init__(self):

        # TODO : Initialize patterns we need and variables
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        # self.customer = Rendezvous is implemented as ?
        # self.barber = Rendezvous is implemented as ?
        # self.customer_done = Rendezvous is implemented as ?
        # self.barber_done = Rendezvous is implemented as ?


def get_haircut(i):
    # TODO: Simulate time and print info when customer gets haircut
    print(i, " got a haircut")
    sleep(1)


def cut_hair():
    # TODO: Simulate time and print info when barber cuts customer's hair
    print("Barber is cutting a customer's hair")
    sleep(4)


def balk(i):
    # TODO: Represents situation when waiting room is full and print info
    print(f"Customer {i} can't enter, because the waiting room is full, so he leaves.")
    sleep(randint(10, 20))

def leave(i, shared):
    shared.mutex.lock()
    sleep(1 / 100)
    shared.waiting_room -= 1
    print("Customer ", i, " leaves the waiting room. The capacity is now: ", shared.waiting_room, "/", N)
    shared.mutex.unlock()

def growing_hair(i):
    # TODO: Represents situation when customer wait after getting haircut. So hair is growing and customer is sleeping for some time
    print("Customer ", i, "'s hair is growing\n")
    sleep(randint(20, 30))


def customer_wait(i, shared):
    shared.mutex.lock()
    sleep(1 / 100)
    if shared.waiting_room >= N:
        shared.mutex.unlock()
        balk(i)
        return False
    shared.waiting_room += 1
    print("Customer ", i, " enters the waiting room. The capacity is now: ", shared.waiting_room, "/", N)
    shared.mutex.unlock()
    return True

def customer(i, shared):
    # TODO: Function represents customers behaviour. Customer come to waiting if room is full sleep.
    # TODO: Wake up barber and waits for invitation from barber. Then gets new haircut.
    # TODO: After it both wait to complete their work. At the end waits to hair grow again

    shared.barber.wait()
    sleep(randint(0, 3))

    while True:
        # TODO: Access to waiting room. Could customer enter or must wait? Be careful about counter integrity :)
        print(f"Customer {i} is comes in to the waiting room")
        if not customer_wait(i, shared):
            continue

        # TODO: Rendezvous 1
        shared.customer.signal()
        shared.barber.wait()
        get_haircut(i)
        shared.customer.wait()
        # TODO: Rendezvous 2

        # TODO: Leave waiting room. Integrity again
        leave(i, shared)
        growing_hair(i)

def barber(shared):
    # TODO: Function barber represents barber. Barber is sleeping.
    # TODO: When customer come to get new hair wakes up barber.
    # TODO: Barber cuts customer hair and both wait to complete their work.
  
    shared.barber.signal(C)
    print("Barber is sleeping")
    sleep(randint(3, 10))
    print("Barber woke up\n")

    while True:
        shared.barber.signal()
        shared.customer.wait()
        # TODO: Rendezvous 1
        cut_hair()
        shared.customer.signal()
        # TODO: Rendezvous 2


def main():
    global C, N
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


# TODO: Global variables C = 5 numOfCustomers N = 3 sizeOfWaitingRoom
C = 5
N = 3


if __name__ == "__main__":
    main()