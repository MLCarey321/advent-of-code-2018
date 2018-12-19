#!/usr/bin/python3

import sys
from collections import defaultdict
from copy import deepcopy
from operator import itemgetter


def transition(current_layout):
    new_layout = deepcopy(current_layout)
    for new_acre in new_layout.keys():
        adjacent = [current_layout[acre] for acre in current_layout.keys()
                    if abs(new_acre[0] - acre[0]) <= 1 and abs(new_acre[1] - acre[1]) <= 1 and new_acre != acre]
        contents = new_layout[new_acre]
        if contents == "." and adjacent.count("|") >= 3:
            new_layout[new_acre] = "|"
        elif contents == "|" and adjacent.count("#") >= 3:
            new_layout[new_acre] = "#"
        elif contents == "#" and (adjacent.count("|") == 0 or adjacent.count("#") == 0):
            new_layout[new_acre] = "."
    return new_layout


def print_layout(current_layout):
    for r in range(max(k[1] for k in current_layout.keys())):
        row = ""
        for c in range(max(k[0] for k in current_layout.keys())):
            row += current_layout[(c, r)]
        print row
    print "------------------------------------------------------------------------------------------------------------"

print("Paste Puzzle Input:  ")
y = 0
acreage = {}
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        x = 0
        for char in line:
            acreage.update({(x, y): char})
            x += 1
        y += 1
    else:
        break

resource_counts = defaultdict(int)
repeats = None
minute = 1
while True:
    acreage = transition(acreage)
    resource_counts[minute] = acreage.values().count("|") * acreage.values().count("#")
    if resource_counts.values().count(resource_counts[minute]) >= 3:
        gaps = [k for k in resource_counts.keys() if resource_counts[k] == resource_counts[minute]]
        gaps.sort(reverse=True)
        if gaps[0] - gaps[1] == gaps[1] - gaps[2]:
            repeats = [{k: v} for k, v in resource_counts.items() if k in range(gaps[1], gaps[0])]
            break
    minute += 1

print "Part One:", resource_counts[10]
remaining = 1000000000 - minute
final_count = remaining % len(repeats)
print "Part Two:", resource_counts[minute - len(repeats) + final_count]
