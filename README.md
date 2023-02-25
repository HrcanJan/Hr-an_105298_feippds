# An implementation of the Bakery algorithm


## A fully functional EXAMPLE project written in python to showcases the Bakery algorithm in action

This repository showcases the how Bakery algorithm works. This algorithm solves the critical section problem for n processes in software. The basic idea is that of a bakery; customers take numbers, and whoever has the lowest number gets service next. Here, of course, "service" means entry to the critical section. 
All process threads must take a number and wait their turn to use a shared computing resource or to enter their critical section. The number can be any of the global variables, and processes with the lowest number will be processed first. If there is a tie or similar number shared by both processes, it is managed through their process ID. If a process terminates before its turn, it has to start over again in the process queue. [[1]](#1)

The examples are written in Python (version 3.10) using ```fei.ppds``` module (```pip install --user fei.ppds```). Run the code in terminal to automatically test the program. There are five threads that will try to access the critical area at the same time, but they will all be forced to wait for their turn to access the critical area, to ensure that multiple processes can't access the critical area at the same time.


### Why Bakery algorithm is an optimal solution

Let's look at all the conditions of mutual exclusion that must be fulfilled: 

* Mutual exclusion should be ensured in the middle of different processes when accessing shared resources. There must not be two processes within their critical sections at any time: **The two while loops in our for statement ensure that the process is not at the doorway and to favor one process when there is a conflict. If there are processes, with the same num value, favor the process with the smaller id.** 
* Assumptions should not be made as to the respective speed of the unstable processes: **A process may fail at any time. We assume that when it fails, it immediately goes to its noncritical section and halts.**
* The process that is outside the critical section must not interfere with another for access to the critical section: **The process with the lowest nonzero value will always be accessing the critical section, and any other process can't interfere with that.**
* When multiple processes access its critical section, they must be allowed access in a finite time: **After every process has exited the critical section, their tid will be set to 0, allowing another process to enter the critical section, until all processes enter and leave the critical area.**

### References
<a id="1">[1](cppsecrets, [2017](https://cppsecrets.com/users/120612197115104981111171149751485164103109971051084699111109/Python-Implementation-of-Bakery-Algorithm.php))</a>