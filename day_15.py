#!/usr/bin/python3

import sys
import operator
from copy import deepcopy
import thread


class Goblin:
    def __init__(self, location):
        self.hp = 200
        self.attack = 3
        self.location = location

    def __repr__(self):
        return "Goblin with %d HP at %d, %d" % ((self.hp,) + self.location)


class Elf:
    def __init__(self, location):
        self.hp = 200
        self.attack = 3
        self.location = location

    def __repr__(self):
        return "Elf with %d HP at %d, %d" % ((self.hp,) + self.location)


def get_manhattan(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])


def take_turn(combatant, enemies):
    print "Taking turn for", combatant
    target = get_target_enemy(combatant.location, enemies)
    if target is None:
        available_enemies = deepcopy(enemies)
        for enemy in available_enemies:
            adjacent_locs = get_adjacent_locations(enemy.location)
            boxed = True
            for adj in adjacent_locs:
                if adj in cave and cave[adj] is None:
                    boxed = False
            if boxed:
                available_enemies.remove(enemy)
        if len(available_enemies) == 0:
            return
        closest_enemy = get_closest_enemy(combatant.location, available_enemies)
        if closest_enemy is not None:
            print "\tTarget Found!"
            target = closest_enemy.keys()[0]
            target_path = closest_enemy[target]
            print "\t\tMoving", combatant, "to", target_path[1]
            cave[combatant.location] = None
            cave[target_path[1]] = combatant
            combatant.location = target_path[1]
            target = get_target_enemy(target_path[1], enemies)
        else:
            print "\t!!!DANGER!!! NO TARGET FOUND!!! DOUBLE CHECK RESULTS!!!"
            print "\t\t", combatant
    else:
        print "\tAlready adjacent to enemy!"
    if target is not None:
        print combatant, "attacking", target
        target.hp -= combatant.attack
        if target.hp <= 0:
            print "\tTarget Vanquished!"
            cave[target.location] = None


def get_adjacent_locations(center):
    return [(center[0], center[1]-1),
            (center[0]-1, center[1]),
            (center[0]+1, center[1]),
            (center[0], center[1]+1)]


def get_target_enemy(center, enemies):
    global cave
    adjacent = get_adjacent_locations(center)
    eligible = [e for e in enemies if e.location in adjacent]
    if eligible is None or len(eligible) == 0:
        return None
    min_hp = min([e.hp for e in eligible])
    eligible = [(e.location + (e,)) for e in eligible if e.hp == min_hp]
    return sorted(eligible, key=operator.itemgetter(1, 0))[0][2]


def get_closest_enemy(start, enemies):
    global cave
    paths = [[start]]
    while len(paths) > 0:
        new_paths = []
        visited = set([n for p in paths for n in p])
        closest_enemies = []
        for path in paths:
            adjacent = get_adjacent_locations(path[-1])
            for adj in adjacent:
                if adj in [e.location for e in enemies]:
                    enemy = cave[adj]
                    closest_enemies.append(enemy.location + ({enemy: deepcopy(path)},))
                if len(closest_enemies) == 0 and adj not in visited and adj in cave.keys() and cave[adj] is None:
                    new_path = deepcopy(path)
                    new_path.append(adj)
                    new_paths.append(new_path)
                    visited.add(adj)
        if len(closest_enemies) > 0:
            closest_enemy = sorted([e for e in closest_enemies], key=operator.itemgetter(1, 0))[0][2]
            return closest_enemy
        paths = new_paths
    return None


def print_cave():
    global cave
    for y in range(max(k[1] for k in cave.keys())+2):
        row = ""
        for x in range(max(k[0] for k in cave.keys())+2):
            if (x, y) not in cave.keys():
                row += "#"
            else:
                square = cave[(x, y)]
                row += "." if square is None else square.__class__.__name__[0]
        print row


def print_combatants():
    global cave
    for place in sorted([l for l in cave.keys() if cave[l] is not None], key=operator.itemgetter(1, 0)):
        print place, cave[place]


cave = {}

print("Paste Puzzle Input:  ")
y = 0
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        x = 0
        for char in line:
            if char == "E":
                cave.update({(x, y): Elf((x, y))})
            elif char == "G":
                cave.update({(x, y): Goblin((x, y))})
            elif char == ".":
                cave.update({(x, y): None})
            x += 1
        y += 1
    else:
        break

winners = None
fight_round = 0
while winners is None:
    for location in sorted([loc for loc in cave.keys() if cave[loc] is not None], key=operator.itemgetter(1, 0)):
        elves = [e for e in cave.values() if e is not None and e.__class__ == Elf]
        goblins = [g for g in cave.values() if g is not None and g.__class__ == Goblin]
        if len(elves) == 0 or len(goblins) == 0:
            winners = elves if len(elves) > 0 else goblins
            break
        occupant = cave[location]
        if occupant is None:
            continue
        oc = occupant.__class__
        if oc == Elf:
            take_turn(occupant, goblins)
        else:
            take_turn(occupant, elves)
    fight_round += 1
    print "ROUND %d RESULTS" % fight_round
    print_cave()
    for place in sorted([l for l in cave.keys() if cave[l] is not None], key=operator.itemgetter(1, 0)):
        print cave[place]
    print "------------------------------------------------------------------------------------------------------------"

fight_round -= 1
print "Round:", fight_round
print "Combined Winning HP:", sum([winner.hp for winner in winners])
print "Part One:", fight_round * sum([winner.hp for winner in winners])
