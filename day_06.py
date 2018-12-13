#!/usr/bin/python3

import sys
from collections import defaultdict
import itertools

printing_key = defaultdict(str)

def getClosestCoord(coords, unclaimed):
    closest = None
    man_dist = 9999999999999999
    for coord in coords:
        distance = abs(coord[0]-unclaimed[0]) + abs(coord[1]-unclaimed[1])
        if distance < man_dist:
            man_dist = distance
            closest = coord
        elif distance == man_dist:
            closest = None
    return closest

def getCoordSum(coords, unclaimed):
    total = 0
    for coord in coords:
        distance = abs(coord[0]-unclaimed[0]) + abs(coord[1]-unclaimed[1])
        total += distance
    return total

def printGrid(grid, x1, y1, x2, y2):
    for x in range(x1, x2+1):
        row = ""
        for y in range(y1, y2+1):
            row += "." if grid[(x, y)] is None else printing_key[grid[(x, y)]] if (x, y) != grid[(x, y)] else '+'
        print row

grid_one = defaultdict(tuple)
curr_key = 'A'

print "Puzzle Input:"
min_x = 9999999999999999
min_y = 9999999999999999
max_x = -9999999999999999
max_y = -9999999999999999
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        str_coords = line.split(", ")
        x = int(str_coords[0])
        y = int(str_coords[1])
        grid_one[(x, y)] = (x, y)
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
        printing_key.update({(x, y): curr_key})
        curr_key = 'a' if curr_key == 'Z' else chr(ord(curr_key) + 1)
    else:
        break

print len(printing_key)
candidates = set(grid_one.values())
region_size = 0

for x in range(min_x, max_x+1):
    for y in range(min_y, max_y+1):
        grid_one[(x, y)] = getClosestCoord(candidates, (x, y))
        total_dist = getCoordSum(candidates, (x, y))
        if total_dist < 10000:
            region_size += 1

print "All Candidates:", candidates
for x in range(min_x, max_x+1):
    if grid_one[(x, min_y)] in candidates:
        candidates.remove(grid_one[(x, min_y)])
    if grid_one[(x, max_y)] in candidates:
        candidates.remove(grid_one[(x, max_y)])

for y in range(min_y, max_y+1):
    if grid_one[(min_x, y)] in candidates:
        candidates.remove(grid_one[(min_x, y)])
    if grid_one[(max_x, y)] in candidates:
        candidates.remove(grid_one[(max_x, y)])

print "Updated Candidates:", candidates

scores = [(k, len(list(v))) for k, v in itertools.groupby(sorted(grid_one.values()))]
top_score = 0
for score in scores:
    if score[0] in candidates:
        top_score = max(top_score, score[1])

printGrid(grid_one, min_x, min_y, max_x, max_y)

print "Part One:", top_score
print "Part Two:", region_size
