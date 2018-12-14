#!/usr/bin/python3

import sys
from collections import defaultdict


class Track:
    def __init__(self, style):
        self.style = style

    def intersection(self):
        return self.style == "+"

    def leftturn(self, orientation):
        return (self.style == "\\" and orientation in {"^", "v"}) or (self.style == "/" and orientation in {"<", ">"})

    def rightturn(self, orientation):
        return (self.style == "/" and orientation in {"^", "v"}) or (self.style == "\\" and orientation in {"<", ">"})


class Cart:
    def __init__(self, orientation, location):
        self.orientation = orientation
        self.next_intersection = 0
        self.location = location

    def takeintersection(self):
        if self.next_intersection == 0:
            self.turnleft()
        elif self.next_intersection == 2:
            self.turnright()
        self.next_intersection += 1
        self.next_intersection %= 3

    def nextlocation(self):
        relative = {"<": (-1, 0), ">": (1, 0), "v": (0, 1), "^": (0, -1)}[self.orientation]
        return tuple(map(sum, zip(self.location, relative)))

    def turnright(self):
        self.orientation = {"<": "^", "^": ">", ">": "v", "v": "<"}[self.orientation]

    def turnleft(self):
        self.orientation = {"<": "v", "v": ">", ">": "^", "^": "<"}[self.orientation]


tracks = defaultdict(lambda: None)
carts = []

print("Paste Puzzle Input:  ")
y = 0
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        x = 0
        for char in line:
            if char in {"-", "<", ">"}:
                tracks[(x, y)] = Track("-")
            elif char in {"|", "v", "^"}:
                tracks[(x, y)] = Track("|")
            elif char in {"/", "\\", "+"}:
                tracks[(x, y)] = Track(char)
            if char in {"<", ">", "v", "^"}:
                carts.append(Cart(char, (x, y)))
            x += 1
        y += 1
    else:
        break


first_collision = None
while len(carts) > 1:
    for cart in carts:
        next_coord = cart.nextlocation()
        track = tracks[next_coord]
        if track.leftturn(cart.orientation):
            cart.turnleft()
        elif track.rightturn(cart.orientation):
            cart.turnright()
        elif track.intersection():
            cart.takeintersection()
        if next_coord in [other.location for other in carts]:
            if first_collision is None:
                first_collision = next_coord
            carts = [other for other in carts if other.location not in (cart.location, next_coord)]
        cart.location = next_coord

print "Part One: %d,%d" % first_collision
print "Part Two: %d,%d" % carts[0].location
