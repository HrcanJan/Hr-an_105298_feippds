# An implementation of the Bakery algorithm

## A fully functional EXAMPLE project written in python to showcases the Bakery algorithm in action

This repository showcases the how Bakery algorithm works. This algorithm solves the critical section problem for n processes in software. The basic idea is that of a bakery; customers take numbers, and whoever has the lowest number gets service next. Here, of course, "service" means entry to the critical section. 
All process threads must take a number and wait their turn to use a shared computing resource or to enter their critical section. The number can be any of the global variables, and processes with the lowest number will be processed first. If there is a tie or similar number shared by both processes, it is managed through their process ID. If a process terminates before its turn, it has to start over again in the process queue. [[1]](#1)

## Why Bakery algorithm is an optimal solution

Let's look at all conditions of mutual exclusion and if it fulfill all of them: 

* Mutual exclusion should be ensured in the middle of different processes when accessing shared resources. There must not be two processes within their critical sections at any time.
* Assumptions should not be made as to the respective speed of the unstable processes.
* The process that is outside the critical section must not interfere with another for access to the critical section.
* When multiple processes access its critical section, they must be allowed access in a finite time, i.e. they should never be kept waiting in a loop that has no limits.

## References
<a id="1">[1](cppsecrets, [2017](https://cppsecrets.com/users/120612197115104981111171149751485164103109971051084699111109/Python-Implementation-of-Bakery-Algorithm.php))</a>