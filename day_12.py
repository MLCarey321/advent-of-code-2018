#!/usr/bin/python3

import sys
import re
from collections import defaultdict

print("Initial State:")
initial_state = sys.stdin.readline()
note_pattern = r"(?P<prereq>.+) => (?P<pot>.)"
pots = defaultdict(bool)
notes = defaultdict(bool)
pot_id = 0

for pot in initial_state:
    pots[pot_id] = pot == '#'
    pot_id += 1

print("Notes:")
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        note = re.match(note_pattern, line).groupdict()
        prereq = []
        for pot in note["prereq"]:
            prereq.append(pot == '#')
        notes[tuple(prereq)] = note["pot"] == "#"
    else:
        break

prev_sum = 0
diff = 0
generation = 1
while True:
    first_pot = min(k for k in pots.keys() if pots[k] is True) - 5
    last_pot = max(k for k in pots.keys() if pots[k] is True) + 5
    new_pots = defaultdict(bool)
    for pot_id in range(first_pot, last_pot+1):
        prereq = tuple(pots[k] for k in range(pot_id-2, pot_id+3))
        new_pots[pot_id] = notes[prereq]
    pots = new_pots
    pot_sum = sum(k for k in pots.keys() if pots[k] is True)
    if generation == 20:
        print "Part One:", pot_sum
    if diff == pot_sum - prev_sum:
        prev_sum = pot_sum
        break
    diff = pot_sum - prev_sum
    generation += 1
    prev_sum = pot_sum

final_sum = (50000000000 - generation) * diff
final_sum += prev_sum
print "Part Two:", final_sum
