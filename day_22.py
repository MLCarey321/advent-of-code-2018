#!/usr/bin/python3

from collections import defaultdict


def get_geo_index(coord):
    global geo, target
    if geo[coord] is not None:
        return geo[coord]
    if coord == (0, 0):
        geo_index = 0
    elif coord == target:
        geo_index = 0
    elif coord[1] == 0:
        geo_index = coord[0] * 16807
    elif coord[0] == 0:
        geo_index = coord[1] * 48271
    else:
        erosion1 = get_erosion_level(tuple(map(sum, zip(coord, (-1, 0)))))
        erosion2 = get_erosion_level(tuple(map(sum, zip(coord, (0, -1)))))
        geo_index = erosion1 * erosion2
    geo[coord] = geo_index
    return geo_index


def get_erosion_level(coord):
    global depth, erosion
    if erosion[coord] is None:
        erosion[coord] = (get_geo_index(coord) + depth) % 20183
    return erosion[coord]


def get_risk_level(coord):
    global risk
    if risk[coord] is None:
        risk[coord] = get_erosion_level(coord) % 3
    return risk[coord]


def get_adjacent_squares(coord):
    squares = [tuple(map(sum, zip(coord, (0, 1)))), tuple(map(sum, zip(coord, (1, 0))))]
    if coord[1] > 0:
        squares.append(tuple(map(sum, zip(coord, (0, -1)))))
    if coord[0] > 0:
        squares.append(tuple(map(sum, zip(coord, (-1, 0)))))
    return squares


def get_proximity_base(coord):
    global target
    return abs(target[0] - coord[0]) + abs(target[1] - coord[1])

depth = 510
target = (10, 10)
geo = defaultdict(lambda: None)
erosion = defaultdict(lambda: None)
risk = defaultdict(lambda: None)
total_risk = 0
for y in range(target[1] + 1):
    for x in range(target[0] + 1):
        total_risk += get_risk_level((x, y))

print("Part One:", total_risk)

tools = [0, 1, 2]
valid_tools = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
visit_minutes = defaultdict(lambda: 99999999)
visited = [(get_proximity_base((0, 0)), 0, 0, 0, 1)]
while len(visited) > 0:
    visited = sorted(visited)
    trash, lapsed, curr_x, curr_y, tool = visited[0]
    del visited[0]
    if visit_minutes[(curr_x, curr_y, tool)] <= lapsed:
        continue
    visit_minutes[(curr_x, curr_y, tool)] = lapsed
    if (curr_x, curr_y) == target:
        if tool == 1:
            print("Part Two:", lapsed)
            break
        else:
            proximity = get_proximity_base((curr_x, curr_y)) + lapsed + 7
            visited.append((proximity, lapsed + 7, curr_x, curr_y, 1))
    else:
        current_risk = risk[(curr_x, curr_y)]
        adjacent = get_adjacent_squares((curr_x, curr_y))
        for adj in adjacent:
            if tool not in valid_tools[get_risk_level(adj)]:
                new_tool = [t for t in tools if t in valid_tools[get_risk_level(adj)] and t in valid_tools[current_risk]][0]
                proximity = get_proximity_base((curr_x, curr_y)) + lapsed + 7
                visited.append((proximity, lapsed + 7, curr_x, curr_y, new_tool))
            else:
                proximity = get_proximity_base(adj) + lapsed + 1
                visited.append((proximity, lapsed + 1, adj[0], adj[1], tool))
