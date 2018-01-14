import random

jla = ["Clark", "Bruce", "Diana", "Barry", "Hal", "Arthur", "John", "Oliver", "Ray", "Carter", "Dinah", "Ralph",
       "Zatanna", "Ronnie", "Martin", "Hank", "Mari", "Ted", "Billy", "Kara"]

"""
  Given a list of wizards, creates ~500 constraints, where in half the cases Wizard 3 is greater than Wizard 1 and 2
  and in the other half, it is less

  Checks to see if every wizard is used at least once, and prints true if so at the end 

  Also, checks to ensure that we don't repeat constraints (or flip wizard 1 and 2 and use that)

  Sometimes produces more than 500 constraints, sometimes less.... but script will tell you how many constraints it produced

  Not at all elegant, and there is no justification on difficulty. In fact, with 500 constraints, it may actually be easily solved
"""
seen = []
wizards_used = []
constraints = 0
num_constraints = 10
num_wiz = 5

while constraints < num_constraints:
    a = random.randint(0, num_wiz)
    b = random.randint(0, num_wiz)
    i = random.randint(0, 500)
    if (i % 2 == 0):
        c = random.randint(max(a, b), num_wiz)
    else:
        c = random.randint(0, min(a, b))
    if (c != a and c != b and a != b):
        constraint_ab = jla[a] + " " + jla[b] + " " + jla[c]
        constraint_ba = jla[b] + " " + jla[a] + " " + jla[c]
        if constraint_ba not in seen and constraint_ab not in seen:
            print(constraint_ab)
            constraints += 1
            seen.append(constraint_ab)
            wizards_used.append(jla[a])
            wizards_used.append(jla[b])
            wizards_used.append(jla[c])
for i in range(num_wiz + 1):
    if jla[i] not in wizards_used:
        print(False)
