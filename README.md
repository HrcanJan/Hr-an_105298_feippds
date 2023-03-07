# Barbershop problem with overtaking

### A fully functional EXAMPLE project written in python to showcase different sequences of using mutex and signalization

This repository shows an implementation of mutex and singalization in a multiple thread problem. The barbershop problem is as follows:
A barbershop has a waiting room, which has a capacity of 3 (N). There are 5 customers (C) and only 1 barber, which are represented as threads. When a customer comes into the waiting room, if the capacity isn't full, the customer will sit down in the waiting room, waiting for a haircut. This will increment the current occupants in the waiting room. If that counter is 3 (maximum number), another customer won't be able to enter the waiting room, and will instead leave and return after some time. After the barber wakes up, he will start cutting hair of a customer that is currently in the waiting room. After cutting their hair, that customer will leave the barbershop, a spot in the waiting room will be freed and the customer's hair will grow back up after some time. After customers' hair has grown, they will try to enter the barbershop again.

The example is written in Python (version 3.10) using ```fei.ppds``` module (```pip install --user fei.ppds```). Run the code in terminal to automatically test the program. There are five threads that will try to access the critical area at the same time, but they will all be forced to wait to access the critical area, to ensure that multiple processes can't access the critical area at the same time. ```shared.waiting_room``` also run a risk; multiple threads wanted to access it at the same time, but we made sure that only one thread can access it at once using mutex.

### Why this is an optimal solution

Let's look at all the conditions of mutual exclusion that must be fulfilled: [[2]](#2)

1. Mutual exclusion should be ensured in the middle of different processes when accessing shared resources. There must not be two processes within their critical sections at any time: 
* There are two critical sections: when a customer is getting a haircut and the access of ```shared.waiting_room``` and it's incrementation/decrementation. Signalizations sent by the barber ensure that only one customer can access the critical section in the customer() function at once. Mutex() ensures that only one process can access ```shared.waiting_room``` at once. The ```shared.waiting_room``` will be locked until one process is finished, and then it will unlock the critical area for other processes.
2. Assumptions should not be made as to the respective speed of the unstable processes: 
* A process may fail at any time. We assume that when it fails, it immediately goes to its noncritical section and halts. [[1]](#1)
3. The process that is outside the critical section must not interfere with another for access to the critical section: 
* The process can't access one critical area until the barber sends a signal. A barber can't send the signal until a customer sends a signal that they are done getting a haircut. The barber sends one signal after finishing cutting hair of one customer, ensuring that only one process will enter the critical area. The other critical area is protected by a mutex, which will lock that critical area until the process using it had finished using it.
4. When multiple processes access its critical section, they must be allowed access in a finite time: 
* After a customer has left the barbershop, they will send a signal to the barber, as well as decrementing the waiting room counter. The barber will then send a signal to one customer (who is currently in the waiting room), who will enter the critical area and start the same process over again. This process will loop forever and everyone will have the access to the critical area, eventually.

Because all conditions are met, that proves that our code work as intended.

### References
<a id="1">[1](wikipedia (https://en.wikipedia.org/wiki/Lamport%27s_bakery_algorithm#Implementation_of_the_algorithm))
<a id="2">[2](scaler, [2022](https://www.scaler.com/topics/mutual-exclusion-in-os/))