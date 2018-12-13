#!/usr/bin/python3

import sys
from collections import defaultdict

serial = int(sys.stdin.readline())
grid = defaultdict(int)


def get_power_level(coord):
    global grid
    if coord not in grid:
        calculate_power_level(coord)
    return grid[coord]


def calculate_power_level(coord):
    global serial
    rack_id = coord[0] + 10
    power_level = rack_id * coord[1]
    power_level += serial
    power_level *= rack_id
    power_level /= 100
    power_level %= 10
    power_level -= 5
    grid[coord] = power_level


def get_3x3_total(top_corner):
    square = []
    square.append(get_power_level(top_corner))
    square.append(get_power_level(tuple(map(sum, zip(top_corner, (1, 0))))))
    square.append(get_power_level(tuple(map(sum, zip(top_corner, (2, 0))))))
    square.append(get_power_level(tuple(map(sum, zip(top_corner, (0, 1))))))
    square.append(get_power_level(tuple(map(sum, zip(top_corner, (1, 1))))))
    square.append(get_power_level(tuple(map(sum, zip(top_corner, (2, 1))))))
    square.append(get_power_level(tuple(map(sum, zip(top_corner, (0, 2))))))
    square.append(get_power_level(tuple(map(sum, zip(top_corner, (1, 2))))))
    square.append(get_power_level(tuple(map(sum, zip(top_corner, (2, 2))))))
    return sum(square)


def get_best_square_for_corner(top_corner, current_max_total):
    global grid
    size = 2
    total = get_3x3_total(top_corner)
    previous_total = total
    limit = min(300-top_corner[0], 300-top_corner[1])
    for width in range(3, limit+1):
        new_total = previous_total
        for x in range(0, width):
            new_total += get_power_level(tuple(map(sum, zip(top_corner, (x, width)))))
        for y in range(0, width):
            new_total += get_power_level(tuple(map(sum, zip(top_corner, (width, y)))))
        new_total += get_power_level(tuple(map(sum, zip(top_corner, (width, width)))))
        if new_total > total:
            total = new_total
            size = width
            if total > current_max_total:
                current_max_total = total
                print "New Max Total!"
                print "\tTop Corner:", top_corner
                print "\tSquare Size:", size + 1
                print "\tSummation:", total
        previous_total = new_total
        max_possible = pow(limit+1, 2) - pow(width+1, 2)
        max_possible *= 4
        if previous_total <= current_max_total - max_possible:
            break
    return total, size + 1


square_sums = defaultdict(tuple)
square_sizes = defaultdict(tuple)
for x in range(1, 299):
    for y in range(1, 299):
        summation = get_3x3_total((x, y))
        square_sums[summation] = (x, y)

print "Part One:"
print max(square_sums.keys())
print square_sums[max(square_sums.keys())]

for x in range(1, 299):
    for y in range(1, 299):
        max_square = get_best_square_for_corner((x, y), 0 if len(square_sizes.keys()) == 0 else max(square_sizes.keys()))
        square_sizes[max_square[0]] = (x, y, max_square[1])
    print x

print "Part Two:"
print max(square_sizes.keys())
print square_sizes[max(square_sizes.keys())]
