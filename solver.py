import argparse
import pycosat
import itertools
import sys
import networkx as nx
import queue
import random

"""
======================================================================
  Complete the following function.
======================================================================
"""


def solve(num_wizards, num_constraints, wizards, constraints):
    """
    Write your algorithm here.
    Input:
        num_wizards: Number of wizards
        num_constraints: Number of constraints
        wizards: An array of wizard names, in no particular order
        constraints: A 2D-array of constraints,
                     where constraints[0] may take the form ['A', 'B', 'C']i

    Output:
        An array of wizard names in the ordering your algorithm returns
    """
    opt_ordering, failed_constraints = backtrack(wizards, constraints)

    if failed_constraints > 0 or len(opt_ordering) != num_wizards:
        print("Something went wrong")
    return opt_ordering

def backtrack(wizards, constraints):
    # Solver that makes use of backtracking, instead of 3SAt
    # start with a directed graph with no edges between the nodes
    DG = nx.DiGraph()
    DG.add_nodes_from(wizards)

    cur_number = 1

    # the priority queue, where entries are of the form (priority, (randomint, cur_constraint, graph))
    pq = queue.PriorityQueue()
    pq.put((len(constraints), (cur_number, 0, DG)))
    cur_number += 1
    while not pq.empty():
        # remove the item from the queue
        priority, tup = pq.get()
        nonsense, cur_constraint_num, cur_DG = tup
        cur_constraint = constraints[cur_constraint_num]
        # create two new graphs
        DG_less = nx.DiGraph(cur_DG)
        DG_greater = nx.DiGraph(cur_DG)

        # add an edge from wizard0, wizard1 to wizard3, as wizard3 is greater
        DG_less.add_edge(cur_constraint[0], cur_constraint[2])
        DG_less.add_edge(cur_constraint[1], cur_constraint[2])

        # add an edge from wizard3 to wizard, wizard2, as they are both greater
        DG_greater.add_edge(cur_constraint[2], cur_constraint[0])
        DG_greater.add_edge(cur_constraint[2], cur_constraint[1])

        if nx.is_directed_acyclic_graph(DG_less):
            new_priority = priority - 1
            new_constraint_num = cur_constraint_num + 1
            if new_constraint_num == len(constraints):
                return topsort(DG_less, constraints)
            item = (new_priority, (cur_number, new_constraint_num, DG_less))
            cur_number += 1
            pq.put(item)
        if nx.is_directed_acyclic_graph(DG_greater):
            new_priority = priority - 1
            new_constraint_num = cur_constraint_num + 1
            if new_constraint_num == len(constraints):
                return topsort(DG_greater, constraints)
            item = (new_priority, (cur_number, new_constraint_num, DG_greater))
            cur_number += 1
            pq.put(item)


def topsort(DG, constraints):
    top_sort = nx.topological_sort(DG)
    opt_ordering = []
    for wizard in top_sort:
        opt_ordering.append(wizard)
    return opt_ordering, constraints_unsatisfied(opt_ordering, constraints)


def constraints_unsatisfied(ordering, constraints):
    node_map = {k: v for v, k in enumerate(ordering)}
    num_failed = 0
    for constraint in constraints:
        wiz_a = node_map[constraint[0]]
        wiz_b = node_map[constraint[1]]
        wiz_mid = node_map[constraint[2]]
        if (wiz_a < wiz_mid < wiz_b) or (wiz_b < wiz_mid < wiz_a):
            num_failed += 1
    return num_failed


"""
======================================================================
   No need to change any code below this line
======================================================================
"""


def read_input(filename):
    with open(filename) as f:
        num_wizards = int(f.readline())
        num_constraints = int(f.readline())
        constraints = []
        wizards = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            for w in c:
                wizards.add(w)

    wizards = list(wizards)
    return num_wizards, num_constraints, wizards, constraints


def write_output(filename, solution):
    with open(filename, "w") as f:
        for wizard in solution:
            f.write("{0} ".format(wizard))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Constraint Solver.")
    parser.add_argument("input_file", type=str, help="___.in")
    parser.add_argument("output_file", type=str, help="___.out")
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    write_output(args.output_file, solution)



