#!/usr/bin/python3

import sys
import re
from collections import defaultdict
from copy import deepcopy

instruction_pattern = r"Step (?P<prereq>\w) must be finished before step (?P<step>\w) can begin.*"
steps = set()
requirements = defaultdict(lambda: [])

print("Please provide instructions:")
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        instruction = re.match(instruction_pattern, line).groupdict()
        requirements[instruction["step"]].append(instruction["prereq"])
        steps.update(instruction["step"])
        steps.update(instruction["prereq"])
    else:
        break

possible_first = []
for step in steps:
    if step not in requirements.keys():
        possible_first.append(step)

elves = {0: (), 1: (), 2: (), 3: ()}
second = 0
path = ""

while len(steps) > 0:
    possible_next = deepcopy(possible_first)
    completed = []
    for elf in elves:
        elf_step = elves[elf]
        if elf_step != () and elf_step[0] == second:
            completed.append(elf_step[1])
            steps.remove(elf_step[1])
            path += elf_step[1]
            print(path)
            elves[elf] = ()
    for req in requirements.keys():
        for prereq in completed:
            if prereq in requirements[req]:
                requirements[req].remove(prereq)
        if requirements[req] == []:
            possible_next.append(req)
    for elf in elves.keys():
        if len(possible_next) == 0:
            break
        if elves[elf] == ():
            next_step = sorted(possible_next)[0]
            duration = ord(next_step) - ord('A') + 61
            print(next_step, "==>", duration)
            elves[elf] = (second + duration, next_step)
            print(elves[elf])
            if next_step in requirements.keys():
                del requirements[next_step]
            if next_step in possible_first:
                possible_first.remove(next_step)
            possible_next.remove(next_step)
    second += 1

print(second-1)
