#!/usr/bin/python3

import sys

print("Paste Puzzle Input:")
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        print(line)
    else:
        break
