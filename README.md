# The feasting savages problem

### A fully functional project written in python to showcase a solution to the savages feasting problem using the mutex, signaling and barriers

This repository shows an implementation of mutex and singalization in a multiple thread problem. The feasting savages problem is as follows: there are NUM_SAVAGES number of savages in a village. The savages are relatively friendly and polite, and when they wish to feast, they will wait for all of them to queue up for the meal before they start feasting. The village has a cook, who will fill the pot with food. If the pot is empty, the savage who is next in turn to take their serving of the food will wake up the cook and then the cook will refill the pot. The pot will always have less portions than there are savages, so the savages will always need to wake up the chef at least once during the feast. Once a savage has finished their meal, they will wait for all the savages to finish eating, before repeating the cycle infinitely.

This obviously poses some synchonization obstacles; we needed to make sure that no savage eats before every savage has been gathered to the feast. The filling and emptying of the pot was also at risk to be accessed by multiple threads at the same time as well as signaling the cook to fill up the pot, while all the savages are waiting for the cook to fill up the pot, before eating from it. So how did implement a solution to this problem?

### The implementation

First we created variables to hold the numbers of savages and the capacity of the pot ```NUM_SAVAGES: int = 10 NUM_POT: int = 5```. This means, that the pot has enough capacity to feed 5 savages. We use the NUM_SAVAGES to create that many Threads to represent each savage, as well as an additional thread to represent the cook. Savages' behavior is represented in the function ```savage()``` and the cook's behavior is represented in the function ```cook()```.  The processes will run forever in while loops. 
Because all of the savages need to gather up before the feast can begin, we implemented a **reusable barrier**, that will only allow the savages to eat after they have all been gathered:
```python
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
```

Next, one savage after the other comes in to get a portion of the serving. If the pot is empty, they will wake up the cook and the cook will start to fill the pot. There are two mutexes here, one that locks the critical area when one savage enters it, to prevent others from entering until the savage has finished filling up his plate:
```python
shared.mutex2.lock()
print(f"Savage {i} is first in queue to take their portion. Remaining portions: {shared.servings} / {NUM_POT}")
if(shared.servings == 0):
    print(f"Savage {i} is waking up the cook")
    shared.empty_pot.signal()
    shared.full_pot.wait()
getServingFromPot(i, shared)
shared.mutex2.unlock()
```
The other mutex makes sure that the integrity of the number of servings in the pot is secure while the cook is filling up the pot:
```python
shared.mutex.lock()
print(f"The cook filling the pot with food")
shared.servings += NUM_POT
shared.mutex.unlock()
```
Lastly, we use signalization to allow the savage to signal the cook to cook the food and fill up the pot. The savage will meanwhile wait. Once the cook has finished filling up the pot, he will signal the savage that the food is ready and then he will go back to sleep: 
```python
shared.empty_pot.signal()
shared.full_pot.wait()

...

while True:
    shared.empty_pot.wait()
    putServingInPot(shared)
    sleep(5)
    shared.full_pot.signal()
```
The cycle will then repeat once more after all the savages have eaten.

### Console output

```
Savage 0 wants to eat. There's 1 of them waiting.
Savage 1 wants to eat. There's 2 of them waiting.
Savage 2 wants to eat. There's 3 of them waiting.
Savage 3 wants to eat. There's 4 of them waiting.
Savage 4 wants to eat. There's 5 of them waiting.
Savage 5 wants to eat. There's 6 of them waiting.
Savage 6 wants to eat. There's 7 of them waiting.
Savage 7 wants to eat. There's 8 of them waiting.
Savage 8 wants to eat. There's 9 of them waiting.
Savage 9 wants to eat. There's 10 of them waiting.
All the savages have arrived to eat. The feast shall comence
Savage 7 is first in queue to take their portion. Remaining portions: 0 / 5
Savage 7 is waking up the cook
The cook filling the pot with food
Savage 7 is getting a serving of food
Savage 7 is feasting
Savage 3 is first in queue to take their portion. Remaining portions: 4 / 5
Savage 3 is getting a serving of food
Savage 3 is feasting
Savage 6 is first in queue to take their portion. Remaining portions: 3 / 5
Savage 6 is getting a serving of food
Savage 7 wants to eat. There's 1 of them waiting.
Savage 6 is feasting
Savage 2 is first in queue to take their portion. Remaining portions: 2 / 5
Savage 2 is getting a serving of food
Savage 3 wants to eat. There's 2 of them waiting.
Savage 2 is feasting
Savage 0 is first in queue to take their portion. Remaining portions: 1 / 5
Savage 0 is getting a serving of food
Savage 6 wants to eat. There's 3 of them waiting.
Savage 0 is feasting
Savage 4 is first in queue to take their portion. Remaining portions: 0 / 5
Savage 4 is waking up the cook
The cook filling the pot with food
Savage 2 wants to eat. There's 4 of them waiting.
Savage 0 wants to eat. There's 5 of them waiting.
Savage 4 is getting a serving of food
Savage 4 is feasting
Savage 5 is first in queue to take their portion. Remaining portions: 4 / 5
Savage 5 is getting a serving of food
Savage 5 is feasting
Savage 1 is first in queue to take their portion. Remaining portions: 3 / 5
Savage 1 is getting a serving of food
Savage 4 wants to eat. There's 6 of them waiting.
Savage 1 is feasting
Savage 9 is first in queue to take their portion. Remaining portions: 2 / 5
Savage 9 is getting a serving of food
Savage 5 wants to eat. There's 7 of them waiting.
Savage 9 is feasting
Savage 8 is first in queue to take their portion. Remaining portions: 1 / 5
Savage 8 is getting a serving of food
Savage 1 wants to eat. There's 8 of them waiting.
Savage 8 is feasting
Savage 9 wants to eat. There's 9 of them waiting.
Savage 8 wants to eat. There's 10 of them waiting.
All the savages have arrived to eat. The feast shall comence
Savage 8 is first in queue to take their portion. Remaining portions: 0 / 5
Savage 8 is waking up the cook
The cook filling the pot with food
Savage 8 is getting a serving of food
Savage 8 is feasting
Savage 6 is first in queue to take their portion. Remaining portions: 4 / 5
Savage 6 is getting a serving of food
Savage 6 is feasting
Savage 5 is first in queue to take their portion. Remaining portions: 3 / 5
Savage 5 is getting a serving of food
Savage 8 wants to eat. There's 1 of them waiting.
Savage 5 is feasting
Savage 7 is first in queue to take their portion. Remaining portions: 2 / 5
Savage 7 is getting a serving of food
Savage 6 wants to eat. There's 2 of them waiting.
Savage 7 is feasting
Savage 3 is first in queue to take their portion. Remaining portions: 1 / 5
Savage 3 is getting a serving of food
Savage 5 wants to eat. There's 3 of them waiting.
Savage 3 is feasting
Savage 9 is first in queue to take their portion. Remaining portions: 0 / 5
Savage 9 is waking up the cook
The cook filling the pot with food
Savage 7 wants to eat. There's 4 of them waiting.
Savage 3 wants to eat. There's 5 of them waiting.
Savage 9 is getting a serving of food
Savage 9 is feasting
Savage 1 is first in queue to take their portion. Remaining portions: 4 / 5
Savage 1 is getting a serving of food
Savage 1 is feasting
Savage 4 is first in queue to take their portion. Remaining portions: 3 / 5
Savage 4 is getting a serving of food
Savage 9 wants to eat. There's 6 of them waiting.
Savage 4 is feasting
Savage 0 is first in queue to take their portion. Remaining portions: 2 / 5
Savage 0 is getting a serving of food
Savage 1 wants to eat. There's 7 of them waiting.
Savage 0 is feasting
Savage 2 is first in queue to take their portion. Remaining portions: 1 / 5
Savage 2 is getting a serving of food
Savage 4 wants to eat. There's 8 of them waiting.
Savage 2 is feasting
Savage 0 wants to eat. There's 9 of them waiting.
Savage 2 wants to eat. There's 10 of them waiting.
All the savages have arrived to eat. The feast shall comence
Savage 2 is first in queue to take their portion. Remaining portions: 0 / 5
Savage 2 is waking up the cook
The cook filling the pot with food
Savage 2 is getting a serving of food
Savage 2 is feasting
Savage 9 is first in queue to take their portion. Remaining portions: 4 / 5
Savage 9 is getting a serving of food
Savage 9 is feasting
Savage 0 is first in queue to take their portion. Remaining portions: 3 / 5
Savage 0 is getting a serving of food
Savage 2 wants to eat. There's 1 of them waiting.
Savage 0 is feasting
Savage 3 is first in queue to take their portion. Remaining portions: 2 / 5
Savage 3 is getting a serving of food
Savage 9 wants to eat. There's 2 of them waiting.
Savage 3 is feasting
Savage 6 is first in queue to take their portion. Remaining portions: 1 / 5
Savage 6 is getting a serving of food
Savage 0 wants to eat. There's 3 of them waiting.
Savage 6 is feasting
Savage 1 is first in queue to take their portion. Remaining portions: 0 / 5
Savage 1 is waking up the cook
The cook filling the pot with food
Savage 3 wants to eat. There's 4 of them waiting.
Savage 6 wants to eat. There's 5 of them waiting.
Savage 1 is getting a serving of food
Savage 1 is feasting
Savage 8 is first in queue to take their portion. Remaining portions: 4 / 5
Savage 8 is getting a serving of food
Savage 8 is feasting
Savage 4 is first in queue to take their portion. Remaining portions: 3 / 5
Savage 4 is getting a serving of food
Savage 1 wants to eat. There's 6 of them waiting.
Savage 4 is feasting
Savage 7 is first in queue to take their portion. Remaining portions: 2 / 5
Savage 7 is getting a serving of food
Savage 7 is feasting
Savage 8 wants to eat. There's 7 of them waiting.
Savage 5 is first in queue to take their portion. Remaining portions: 1 / 5
Savage 5 is getting a serving of food
Savage 5 is feasting
Savage 4 wants to eat. There's 8 of them waiting.
Savage 7 wants to eat. There's 9 of them waiting.
Savage 5 wants to eat. There's 10 of them waiting.
```