#!/usr/bin/python3

import sys
import re
from collections import defaultdict

claim_pattern = r"\#(?P<id>\d*) \@ (?P<left>\d*),(?P<top>\d*)\: (?P<width>\d*)x(?P<height>\d*).*"
claims = []
fabric = defaultdict(int)
part_one = 0
part_two = 0
found = True

print("Paste Puzzle Input:  ")
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        pattern = re.match(claim_pattern, line)
        claim = pattern.groupdict()
        claims.append(claim)
        left = int(claim["left"])
        top = int(claim["top"])
        width = int(claim["width"])
        height = int(claim["height"])
        for x in range(left, left+width):
            for y in range(top, top+height):
                fabric[(x, y)] += 1
    else:
        break

for val in fabric.itervalues():
    if val > 1:
        part_one += 1

for claim in claims:
    left = int(claim["left"])
    top = int(claim["top"])
    width = int(claim["width"])
    height = int(claim["height"])
    for x in range(left, left+width):
        for y in range(top, top+height):
            if fabric[(x, y)] > 1:
                found = False
    if found:
        part_two = int(claim["id"])
        break
    found = True

print "Part One:", part_one
print "Part Two:", part_two
