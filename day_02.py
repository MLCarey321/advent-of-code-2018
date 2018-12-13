#!/usr/bin/python3

import sys

box_ids = []
twos = 0
threes = 0
isTwo = False
isThree = False
substrings = dict()
common = ""

print("Paste Puzzle Input:")
while True:
    box_id = sys.stdin.readline()
    if len(box_id) > 1:
        box_ids.append(box_id)
        counts = dict((letter, box_id.count(letter)) for letter in set(box_id))
        for k, v in counts.items():
            isTwo = isTwo or v == 2
            isThree = isThree or v == 3
        if isTwo:
            twos += 1
            isTwo = False
        if isThree:
            threes += 1
            isThree = False
        if common == "":
            for index in range(0, len(box_id)-1):
                substring = box_id[:index] + box_id[index+1:]
                if index not in substrings.keys():
                    substrings[index] = []
                if substring in substrings[index]:
                    common = substring
                else:
                    substrings[index].append(substring)
    else:
        break

print("Part One:", twos * threes)
print("Part Two:", common)
