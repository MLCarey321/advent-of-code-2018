#!/usr/bin/python3

import sys
from collections import defaultdict
from copy import deepcopy


class Room:
    def __init__(self, location):
        self.location = location
        self.adjacent_rooms = defaultdict(lambda: None)

    def __repr__(self):
        return "Room at " + str(self.location) + " is adjacent to " + str(self.adjacent_rooms)


def print_rooms():
    global rooms
    y_range = [y for (x, y) in rooms.keys()]
    x_range = [x for (x, y) in rooms.keys()]
    for y in range(min(y_range), max(y_range) + 1):
        row = ""
        for x in range(min(x_range), max(x_range) + 1):
            row += "." if (x, y) in rooms.keys() else " "
        print row

print "Path Regex:"
path_regex = sys.stdin.readline()
movement = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
rooms = defaultdict(lambda: None)
branch_roots = []
current_loc = (0, 0)
prev_loc = (0, 0)
rooms[(0, 0)] = Room((0, 0))
for direction in path_regex:
    if direction in ["^", "$"]:
        continue
    elif direction == "(":
        branch_roots.append(current_loc)
    elif direction == ")":
        prev_loc = branch_roots[-1]
        del branch_roots[-1]
    elif direction == "|":
        prev_loc = branch_roots[-1]
    elif direction in movement.keys():
        prev_room = rooms[prev_loc]
        current_loc = tuple(map(sum, zip(prev_loc, movement[direction])))
        current_room = Room(current_loc)
        current_room.adjacent_rooms[prev_loc] = prev_room
        prev_room.adjacent_rooms[current_loc] = current_room
        rooms[current_loc] = current_room
        prev_loc = current_loc

paths = [[(0, 0)]]
final_path_lengths = defaultdict(int)
while True:
    new_paths = []
    visited = set([n for p in paths for n in p])
    for path in paths:
        for adj in rooms[path[-1]].adjacent_rooms:
            if adj not in path:
                if adj in final_path_lengths.keys():
                    final_path_lengths[adj] = min(len(path), final_path_lengths[adj])
                else:
                    final_path_lengths[adj] = len(path)
                new_path = deepcopy(path)
                new_path.append(adj)
                new_paths.append(new_path)
    if len(new_paths) == 0:
        break
    paths = new_paths

print final_path_lengths
print "Part One:", max(final_path_lengths.values())
print "Part Two:", len([l for l in final_path_lengths.values() if l >= 1000])
