#!/usr/bin/python3

import sys
import re
from collections import defaultdict

print("Initial State:")
initial_state = sys.stdin.readline()
note_pattern = r"(?P<prereq>.+) => (?P<pot>.)"
pots = defaultdict(bool)
notes = defaultdict(bool)


def print_pots():
    global pots
    first_pot = min(k for k in pots.keys() if pots[k] is True)
    last_pot = max(k for k in pots.keys() if pots[k] is True)
    row = ""
    for key in pots.keys():
        row += "#" if pots[key] else "."
    #print "Starting at", first_pot, "; Ending at", last_pot
    #print row
    pot_sum = sum(k for k in pots.keys() if pots[k] is True)
    print pot_sum

pot_id = 0
for pot in initial_state:
    pots[pot_id] = pot == '#'
    pot_id += 1

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

print "Starting State:"
print_pots()
for generation in range(1000):
    first_pot = min(k for k in pots.keys() if pots[k] is True) - 5
    last_pot = max(k for k in pots.keys() if pots[k] is True) + 5
    new_pots = defaultdict(bool)
    for pot_id in range(first_pot, last_pot+1):
        prereq = tuple(pots[k] for k in range(pot_id-2, pot_id+3))
        new_pots[pot_id] = notes[prereq]
    pots = new_pots
    print_pots()

#first_pot = min(pots.keys(), key=lambda k: pots[k] is True)
#last_pot = max(pots.keys(), key=lambda k: pots[k] is True)
print pots
pot_sum = sum(k for k in pots.keys() if pots[k] is True)
print "Part One:", pot_sum
