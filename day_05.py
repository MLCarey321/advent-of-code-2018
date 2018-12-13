#!/usr/bin/python3

from copy import deepcopy

def get_reduced_polymer(polymer):
    reaction = True

    while reaction:
        reaction = False
        for index in range(0, len(polymer) - 1):
            unit1 = polymer[index]
            unit2 = polymer[index+1]
            if unit1 != unit2 and unit1.lower() == unit2.lower():
                polymer = polymer[:index] + polymer[index+2:]
                reaction = True
                break
    return polymer

initial = str(input("? "))
print "Part One:", len(get_reduced_polymer(deepcopy(initial)))

unique_units = set(initial.lower())
shortest = len(initial)
for unit in unique_units:
    copied = deepcopy(initial)
    copied = copied.replace(unit, '')
    copied = copied.replace(unit.upper(), '')
    new_polymer = get_reduced_polymer(copied)
    length = len(new_polymer)
    if length < shortest:
        shortest = length

print "Part Two:", shortest
