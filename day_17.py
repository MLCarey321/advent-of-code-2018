#!/usr/bin/python3

import sys
import re
from collections import defaultdict
from copy import deepcopy


def fill_down(start_x, start_y):
    global scan, min_y, max_y
    current_x = start_x
    current_y = start_y
    while scan[(current_x, current_y + 1)] is None and current_y < max_y:
        current_y += 1
        scan[current_x, current_y] = "|"
    if current_y < max_y:
        edges = find_edges(current_x, current_y)
        last_edges = None
        while edges[0] is not None and edges[1] is not None and current_y >= min_y:
            last_edges = deepcopy(edges)
            for x in range(edges[0], edges[1] + 1):
                scan[(x, current_y)] = "~"
            if scan[(edges[0], current_y + 1)] is None or scan[(edges[1], current_y + 1)] is None:
                break
            current_y -= 1
            edges = find_edges(current_x, current_y)
        if last_edges is not None:
            for x in range(last_edges[0], last_edges[1]+1):
                scan[(x, current_y)] = "|"
        if edges[0] is not None and edges[1] is not None:
            if scan[(edges[0], current_y + 1)] is None:
                fill_down(edges[0], current_y)
            if scan[(edges[1], current_y + 1)] is None:
                fill_down(edges[1], current_y)


def find_edges(start_x, start_y):
    global scan
    left_x = deepcopy(start_x)
    right_x = deepcopy(start_x)
    while scan[(left_x, start_y+1)] is not None and \
            (scan[(left_x-1, start_y)] is None or scan[(left_x-1, start_y)] in ["~", "|"]):
        left_x -= 1
    if scan[(left_x, start_y+1)] is None and scan[(left_x+1, start_y+1)] in ["~", "|"]:
        left_x = None
    while scan[(right_x, start_y+1)] is not None and \
            (scan[(right_x+1, start_y)] is None or scan[(right_x+1, start_y)] in ["~", "|"]):
        right_x += 1
    if scan[(right_x, start_y+1)] is None and scan[(right_x-1, start_y+1)] in ["~", "|"]:
        right_x = None
    return left_x, right_x


def print_scan():
    global scan, min_y, max_y
    min_x = min([x for (x, y) in scan.keys()])
    max_x = max([x for (x, y) in scan.keys()])
    for y in range(min_y, max_y+1):
        row = ""
        for x in range(min_x, max_x+1):
            row += "." if scan[(x, y)] is None else scan[(x, y)]
        print row
    print "------------------------------------------------------------------------------------------------------------"

vertical_pattern = r"x\=(?P<x>\d+),\sy\=(?P<y1>\d+)\.\.(?P<y2>\d+).*"
horizontal_pattern = r"y\=(?P<y>\d+),\sx\=(?P<x1>\d+)\.\.(?P<x2>\d+).*"

scan = defaultdict(lambda: None)
print("Paste Puzzle Input:  ")
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        vein = re.match(vertical_pattern, line)
        if vein is None:
            vein = re.match(horizontal_pattern, line)
            if vein is None:
                break
            vein = vein.groupdict()
            y = int(vein["y"])
            for x in range(int(vein["x1"]), int(vein["x2"])+1):
                scan[(x, y)] = "#"
        else:
            vein = vein.groupdict()
            x = int(vein["x"])
            for y in range(int(vein["y1"]), int(vein["y2"])+1):
                scan[(x, y)] = "#"
    else:
        break

min_y = min([y for (x, y) in scan.keys()])
max_y = max([y for (x, y) in scan.keys()])

print_scan()
fill_down(500, 0)
print_scan()

print "Part One:", len([s for s in scan.keys() if scan[s] in ["~", "|"] and s[1] in range(min_y, max_y+1)])
print "Part Two:", len([s for s in scan.keys() if scan[s] == "~" and s[1] in range(min_y, max_y+1)])
