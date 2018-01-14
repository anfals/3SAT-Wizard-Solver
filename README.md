# 3SAT-Wizard-Solver
CS 170 (Algorithms) - UC Berkeley Fall 2017 Project

Given a list of constraints of the form "Wizard1 Wizard2 Wizard3", which specifies that the age of Wizard3 is not between the ages
of Wizard1 and Wizard2, return an ordering of the wizards that satisifies all the constraints in the input file. 

This can be shown to be an NP-Complete problem, meaning there is no efficient way of solving (unless P = NP). This problem can be reduced
to another well known NP-Complete Problem, 3SAT. We can also cope with the NP-Completeness of the problem by tackling it using common
strategies like greedy approximation and simulated annealing, which are explored in my implementation of the "Solver."

Refer to the "Project Write Up" PDF for a full breakdown of the reduction to 3SAT and the usage of a greedy approximator for input
files that are too large to be completed using a standard 3SAT solver without the use of powerful computing resources.

Also, the "annealing" and "backtracker" branches offer implementations of the solver that try different approximation approaches. Both were ultimately rejected for not being accurate enough/fast enough, but provide reference for implementations of two well-known approaches to NP-Complete problems.

