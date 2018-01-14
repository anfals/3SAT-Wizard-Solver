import itertools
import sys
import random
import math
from sets import Set

# An early experiment using simulated annealing, implemented with Python 2
# rejected, significantly worse performance than tuned greedy solver


def solve_loop_official(s):
    fin = open(s, "r")
    num_wizards = int(fin.readline().split()[0])

    # Ensures that line 1 and line 2 agree.
    wizards_set = Set()

    # MAkes sure that line 3 is a number between 1 and 500
    line2 = fin.readline().split()
    num_constraints = int(line2[0])

    constraints = []


    # Makes sure that all the constraints match up with the provided perfect ordering.
    for i in range(num_constraints):
        constraint = fin.readline().split()
        for wizard in constraint:
            wizards_set.add(wizard)
        constraints.append(constraint)

    wizards_list = [wizard for wizard in wizards_set]

    possible_swaps = list(itertools.combinations([a for a in range(num_wizards)], 2))
    node_map = annealing_hybrid(wizards_list, constraints, possible_swaps)

    rev_dict = {}
    for key in node_map:
        rev_dict[node_map[key]] = key
    lst = []
    for i in range(num_wizards):
        lst.append(rev_dict[i])
    print lst




def acceptance_probability(energy, new_energy, temperature):
    if new_energy < energy:
        return 1.0
    else:
        return math.exp(((energy - new_energy) * 1.0) / temperature)

def annealing(wizards_list, constraints, possible_swaps):
    temperature = 1000.0
    cooling_rate = 0.00003
    wizards_list = list(wizards_list)
    random.shuffle(wizards_list)
    cur_node_map = {k: v for v, k in enumerate(wizards_list)}
    best_map = cur_node_map
    best_constraints_unsatisfied = constraints_unsatisfied(cur_node_map, constraints)
    while temperature > 1:
        new_solution = dict(cur_node_map)
        rev_dict = {}
        for key in new_solution:
            rev_dict[new_solution[key]] = key
        swap = random.randint(0, len(possible_swaps) - 1)
        swap = possible_swaps[swap]
        swap_a = rev_dict[swap[0]]
        swap_b = rev_dict[swap[1]]
        new_solution[swap_a], new_solution[swap_b] = new_solution[swap_b], new_solution[swap_a]
        cur_energy = constraints_unsatisfied(cur_node_map, constraints)
        neighbor_energy = constraints_unsatisfied(new_solution, constraints)
        if acceptance_probability(cur_energy, neighbor_energy, temperature) > random.randint(0, 1):
            cur_node_map = new_solution
        cur_constraints_unsatisfied = constraints_unsatisfied(cur_node_map, constraints)
        if cur_constraints_unsatisfied < best_constraints_unsatisfied:
            best_map = cur_node_map
            best_constraints_unsatisfied = cur_constraints_unsatisfied
        temperature *= (1 - cooling_rate)
        print cur_constraints_unsatisfied
    print "Best: " + str(best_constraints_unsatisfied)
    return best_map

def annealing_hybrid(wizards_list, constraints, possible_swaps):
    temperature = 1000.0
    cooling_rate = 0.00003
    wizards_list = list(wizards_list)
    random.shuffle(wizards_list)
    cur_node_map = {k: v for v, k in enumerate(wizards_list)}
    best_map = cur_node_map
    best_constraints_unsatisfied = constraints_unsatisfied(cur_node_map, constraints)
    while temperature > 1:
        rev_dict = {}
        for key in cur_node_map:
            rev_dict[cur_node_map[key]] = key
        unsatisfied = constraints_unsatisfied(cur_node_map, constraints)
        const_unsat_percent = (unsatisfied * 1.0) / len(constraints)
        if const_unsat_percent > 0.15:
            best_neighbor = None
            best_neighbor_energy = len(constraints)
            for i in possible_swaps:
                swap_a = rev_dict[i[0]]
                swap_b = rev_dict[i[1]]
                neighbor = dict(cur_node_map)
                neighbor[swap_a], neighbor[swap_b] = neighbor[swap_b], neighbor[swap_a]
                cur_neighbor_energy = constraints_unsatisfied(neighbor, constraints)
                if cur_neighbor_energy < best_neighbor_energy:
                    best_neighbor = neighbor
                    best_neighbor_energy = cur_neighbor_energy
            cur_energy = constraints_unsatisfied(cur_node_map, constraints)
            if acceptance_probability(cur_energy, best_neighbor_energy, temperature) > random.randint(0, 1):
                cur_node_map = best_neighbor
        else:
            new_solution = dict(cur_node_map)
            swap = random.randint(0, len(possible_swaps) - 1)
            swap = possible_swaps[swap]
            swap_a = rev_dict[swap[0]]
            swap_b = rev_dict[swap[1]]
            new_solution[swap_a], new_solution[swap_b] = new_solution[swap_b], new_solution[swap_a]
            cur_energy = constraints_unsatisfied(cur_node_map, constraints)
            neighbor_energy = constraints_unsatisfied(new_solution, constraints)
            if acceptance_probability(cur_energy, neighbor_energy, temperature) > random.randint(0, 1):
                cur_node_map = new_solution
        cur_constraints_unsatisfied = constraints_unsatisfied(cur_node_map, constraints)
        if cur_constraints_unsatisfied < best_constraints_unsatisfied:
            best_map = cur_node_map
            best_constraints_unsatisfied = cur_constraints_unsatisfied
        temperature *= (1 - cooling_rate)
        print best_constraints_unsatisfied
    print "Best: " + str(best_constraints_unsatisfied)
    return best_map


def solver(unaltered_list, constraints, possible_swaps):
    wizards_list = list(unaltered_list)
    random.shuffle(wizards_list)
    node_map = {k: v for v, k in enumerate(wizards_list)}
    failures = constraints_unsatisfied(node_map, constraints)
    seen_failures_map = {}
    while failures > 0:
        rev_dict = {}
        for key in node_map:
            rev_dict[node_map[key]] = key
        best_map = node_map
        for i in possible_swaps:
            swap_a = rev_dict[i[0]]
            swap_b = rev_dict[i[1]]
            cur_map = dict(node_map)
            cur_map[swap_a], cur_map[swap_b] = cur_map[swap_b], cur_map[swap_a]
            cur_fail = constraints_unsatisfied(cur_map, constraints)
            if cur_fail < failures:
                failures = cur_fail
                best_map = cur_map
        node_map = best_map
        if failures in seen_failures_map:
            seen_failures_map[failures] += 1
            if seen_failures_map[failures] > 3:
                if failures > 10:
                    num_random_swaps = random.randint(5, 15)
                    print "Swaps: " + str(num_random_swaps)
                else:
                    num_random_swaps = random.randint(1, 10)
                for i in range(num_random_swaps):
                    rev_dict = {}
                    for key in node_map:
                        rev_dict[node_map[key]] = key
                    swap = random.randint(0, len(possible_swaps) - 1)
                    swap = possible_swaps[swap]
                    swap_a = rev_dict[swap[0]]
                    swap_b = rev_dict[swap[1]]
                    node_map[swap_a], node_map[swap_b] = node_map[swap_b], node_map[swap_a]
                    failures = constraints_unsatisfied(node_map, constraints)
                seen_failures_map = {}

        else:
            seen_failures_map[failures] = 1
        print failures
    return node_map, failures





def constraints_unsatisfied(node_map, constraints):
    num_failed = 0
    for constraint in constraints:
        wiz_a = node_map[constraint[0]]
        wiz_b = node_map[constraint[1]]
        wiz_mid = node_map[constraint[2]]
        if (wiz_a < wiz_mid < wiz_b) or (wiz_b < wiz_mid < wiz_a):
            num_failed += 1
    return num_failed

if __name__ == '__main__':
    solve_loop_official(sys.argv[1])

