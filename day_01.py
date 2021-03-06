#!/usr/bin/python3

import sys

instructions = []
frequencies = []

while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        instructions.append(int(line))
    else:
        break

position = 0
found = False
first_application = 0
while not found:
    for instruction in instructions:
        position += int(instruction)
        if position in frequencies:
            found = True
            break
        frequencies.append(position)
    if first_application == 0:
        first_application = frequencies[-1]

print "Part One:", first_application
print "Part Two:", position
