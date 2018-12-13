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
while not found:
    for instruction in instructions:
        position += int(instruction)
        if position in frequencies:
            print("Found!")
            found = True
            break
        frequencies.append(position)

print(position)
