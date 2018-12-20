#!/usr/bin/python3

import sys
import re


def execute(operation, val_a, val_b, val_c):
    global registers
    reg_a = 0 if val_a >= len(registers) else registers[val_a]
    reg_b = 0 if val_b >= len(registers) else registers[val_b]
    if operation[:3] == "add":
        registers[val_c] = reg_a + reg_b if operation[3] == "r" else reg_a + val_b
    elif operation[:3] == "mul":
        registers[val_c] = reg_a * reg_b if operation[3] == "r" else reg_a * val_b
    elif operation[:3] == "ban":
        registers[val_c] = reg_a & reg_b if operation[3] == "r" else reg_a & val_b
    elif operation[:3] == "bor":
        registers[val_c] = reg_a | reg_b if operation[3] == "r" else reg_a | val_b
    elif operation[:3] == "set":
        registers[val_c] = reg_a if operation[3] == "r" else val_a
    elif operation[:2] == "gt":
        cmp1 = reg_a if operation[2] == "r" else val_a
        cmp2 = reg_b if operation[3] == "r" else val_b
        registers[val_c] = 1 if cmp1 > cmp2 else 0
    elif operation[:2] == "eq":
        cmp1 = reg_a if operation[2] == "r" else val_a
        cmp2 = reg_b if operation[3] == "r" else val_b
        registers[val_c] = 1 if cmp1 == cmp2 else 0

instruction_pattern = r"(?P<opcode>[a-zA-Z]+)\s(?P<var1>\d+)\s(?P<var2>\d+)\s(?P<var3>\d+).*"

registers = [0, 0, 0, 0, 0, 0]
instructions = []
print "Instruction Pointer Register:"
ip_register = int(sys.stdin.readline())
print "Instructions:  "
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        instructions.append(re.match(instruction_pattern, line).groupdict())
    else:
        break

while registers[ip_register] < len(instructions):
    ip = registers[ip_register]
    instruction = instructions[ip]
    execute(instruction["opcode"], int(instruction["var1"]), int(instruction["var2"]), int(instruction["var3"]))
    registers[ip_register] += 1

registers[ip_register] -= 1
print "Part One:", registers[0]

sum_of_factors = 0
for i in range(1, 10551288):
    if 10551287 % i == 0:
        sum_of_factors += i
print "Part Two:", sum_of_factors
