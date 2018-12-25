#!/usr/bin/python3

import re
from z3 import *
from collections import defaultdict


def get_map_from_dict(bot_dict):
    x = int(bot_dict["x_coord"])
    if bot_dict["x_neg"]:
        x = -x
    y = int(bot_dict["y_coord"])
    if bot_dict["y_neg"]:
        y = -y
    z = int(bot_dict["z_coord"])
    if bot_dict["z_neg"]:
        z = -z
    r = int(bot_dict["range"])
    return x, y, z, r


def manhattan(bot1, bot2):
    return abs(bot1[0]-bot2[0]) + abs(bot1[1]-bot2[1]) + abs(bot1[2]-bot2[2])


def in_range(bot1, bot2, r):
    return manhattan(bot1, bot2) <= r


def z3_abs(val):
    return If(val >= 0, val, -val)


def z3_manhattan(bot1, bot2):
    return z3_abs(bot1[0]-bot2[0]) + z3_abs(bot1[1]-bot2[1]) + z3_abs(bot1[2]-bot2[2])


bot_pattern = r"pos\=\<(?P<x_neg>-?)(?P<x_coord>\d+)\,(?P<y_neg>-?)(?P<y_coord>\d+)\,(?P<z_neg>-?)(?P<z_coord>\d+)\>" \
              r"\,\sr\=(?P<range>\d+).*"
bots = defaultdict()
x = Int('x')
y = Int('y')
z = Int('z')
orig = (x, y, z)
cost = Int('cost')
cost_expr = x * 0

print("Paste Puzzle Input:  ")
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        pattern = re.match(bot_pattern, line)
        bot = get_map_from_dict(pattern.groupdict())
        pos = bot[:3]
        bots[pos] = bot[3]
        cost_expr += If(z3_manhattan(orig, pos) <= bot[3], 1, 0)
    else:
        break

strongest = [coord for coord in bots.keys() if bots[coord] == max(bots.values())][0]
signal = bots[strongest]
count = 0

for coord in bots.keys():
    if in_range(strongest, coord, signal):
        count += 1

print("Part One:", count)

opt = Optimize()
opt.add(cost == cost_expr)
opt.maximize(cost)
opt.minimize(z3_manhattan((0, 0, 0), (x, y, z)))
opt.check()
model = opt.model()
pos = (model[x].as_long(), model[y].as_long(), model[z].as_long())
# print(model)
# print("Coordinates:", pos)
# print("Number of bots in range:", model[cost].as_long())
print("Part Two:", manhattan((0, 0, 0), pos))
