#!/usr/bin/python3

import sys


def manhattan(c1, c2):
    return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]) + abs(c1[2]-c2[2]) + abs(c1[3]-c2[3])

bot_positions = []
print("Paste Puzzle Input:  ")
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        coord = [int(c) for c in line.strip().split(",")]
        bot_positions.append(coord)
    else:
        break

constellations = []
while len(bot_positions) > 0:
    constellation = [bot_positions[0]]
    del bot_positions[0]
    size = 0
    while size != len(constellation):
        size = len(constellation)
        for bot in bot_positions:
            for coord in constellation:
                if manhattan(bot, coord) <= 3:
                    constellation.append(bot)
                    bot_positions.remove(bot)
                    break
    constellations.append(constellation)
print("Part One:", len(constellations))
