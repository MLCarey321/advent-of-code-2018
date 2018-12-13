#!/usr/bin/python3

import sys
import re
import time

lights = []


class Light:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


def get_number_from_pattern(num_name, info):
    num = int(info[num_name])
    if "-" == info[num_name + "_sign"]:
        num = -num
    return num


def print_lights():
    global lights
    grid = []
    for light in lights:
        grid.append(light.position)
    min_x = min(grid, key=lambda coord: coord[0])[0]
    min_y = min(grid, key=lambda coord: coord[1])[1]
    max_x = max(grid, key=lambda coord: coord[0])[0]
    max_y = max(grid, key=lambda coord: coord[1])[1]
    if max_x - min_x > 100 or max_y - min_y > 100:
        return
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            row += "#" if (x, y) in grid else " "
        print row
    print "------------------------------------------------------------------------------------------------------------"
    time.sleep(1)


def update_positions():
    global lights
    for light in lights:
        light.position = tuple(map(sum, zip(light.position, light.velocity)))


light_pattern = r"position\=\<\s*(?P<pos_x_sign>\-?)(?P<pos_x>\d+)\,\s+(?P<pos_y_sign>\-?)(?P<pos_y>\d+)\> " \
                r"velocity\=\<\s*(?P<vel_x_sign>\-?)(?P<vel_x>\d+),\s+(?P<vel_y_sign>\-?)(?P<vel_y>\d+)\>"

print("Paste Puzzle Input:  ")
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        light_info = re.match(light_pattern, line).groupdict()
        pos_x = get_number_from_pattern("pos_x", light_info)
        pos_y = get_number_from_pattern("pos_y", light_info)
        vel_x = get_number_from_pattern("vel_x", light_info)
        vel_y = get_number_from_pattern("vel_y", light_info)
        lights.append(Light((pos_x, pos_y), (vel_x, vel_y)))
    else:
        break

print "------------------------------------------------------------------------------------------------------------"
seconds = 0
while True:
    print "Seconds Elapsed:", seconds
    print_lights()
    update_positions()
    seconds += 1

