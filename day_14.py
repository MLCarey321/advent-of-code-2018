#!/usr/bin/python3

import sys

print("Puzzle Input:")
target_recipe = int(sys.stdin.readline())
target_str = str(target_recipe)
scores = [3, 7]
elf_pos = [0, 1]

target_found = -1
while len(scores) < target_recipe + 10 or target_found < 0:
    new_score = str(scores[elf_pos[0]] + scores[elf_pos[1]])
    for score in new_score:
        scores.append(int(score))
    for elf in range(2):
        elf_pos[elf] = (elf_pos[elf] + scores[elf_pos[elf]] + 1) % len(scores)
    if target_found < 0:
        str_score = "".join([str(score) for score in scores[(len(scores)-len(target_str))-2:]])
        if target_str in str_score:
            str_score = "".join([str(score) for score in scores])
            target_found = str_score.find(target_str)

print "Part One:", "".join([str(score) for score in scores[target_recipe:target_recipe + 10]])
print "Part Two:", target_found
