#!/usr/bin/python3

import re
from copy import deepcopy


def cmp_registers(set1, set2):
    return int(set1["r1"]) == int(set2["r1"]) and \
           int(set1["r2"]) == int(set2["r2"]) and \
           int(set1["r3"]) == int(set2["r3"]) and \
           int(set1["r4"]) == int(set2["r4"])


def get_all_possibilities(init, val_a, val_b, val_c):
    register_mapping = {0: "r1", 1: "r2", 2: "r3", 3: "r4"}
    possibilities = {}
    reg_a = int(init[register_mapping[val_a]])
    reg_b = int(init[register_mapping[val_b]])
    reg_c = register_mapping[val_c]
    addr = deepcopy(init)
    addr[reg_c] = reg_a + reg_b
    possibilities.update({"addr": addr})
    addi = deepcopy(init)
    addi[reg_c] = reg_a + val_b
    possibilities.update({"addi": addi})
    mulr = deepcopy(init)
    mulr[reg_c] = reg_a * reg_b
    possibilities.update({"mulr": mulr})
    muli = deepcopy(init)
    muli[reg_c] = reg_a * val_b
    possibilities.update({"muli": muli})
    banr = deepcopy(init)
    banr[reg_c] = reg_a & reg_b
    possibilities.update({"banr": banr})
    bani = deepcopy(init)
    bani[reg_c] = reg_a & val_b
    possibilities.update({"bani": bani})
    borr = deepcopy(init)
    borr[reg_c] = reg_a | reg_b
    possibilities.update({"borr": borr})
    bori = deepcopy(init)
    bori[reg_c] = reg_a | val_b
    possibilities.update({"bori": bori})
    setr = deepcopy(init)
    setr[reg_c] = reg_a
    possibilities.update({"setr": setr})
    seti = deepcopy(init)
    seti[reg_c] = val_a
    possibilities.update({"seti": seti})
    gtir = deepcopy(init)
    gtir[reg_c] = 1 if val_a > reg_b else 0
    possibilities.update({"gtir": gtir})
    gtri = deepcopy(init)
    gtri[reg_c] = 1 if reg_a > val_b else 0
    possibilities.update({"gtri": gtri})
    gtrr = deepcopy(init)
    gtrr[reg_c] = 1 if reg_a > reg_b else 0
    possibilities.update({"gtrr": gtrr})
    eqir = deepcopy(init)
    eqir[reg_c] = 1 if val_a == reg_b else 0
    possibilities.update({"eqir": eqir})
    eqri = deepcopy(init)
    eqri[reg_c] = 1 if reg_a == val_b else 0
    possibilities.update({"eqri": eqri})
    eqrr = deepcopy(init)
    eqrr[reg_c] = 1 if reg_a == reg_b else 0
    possibilities.update({"eqrr": eqrr})
    return possibilities


def execute(operation, val_a, val_b, val_c):
    global registers
    reg_a = registers[val_a]
    reg_b = registers[val_b]
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


register_pattern = r".*(?P<r1>\d+),\s(?P<r2>\d+),\s(?P<r3>\d+),\s(?P<r4>\d+).*"
all_possibilities = {}
all_results = []
clue_file = open("16a.in", "r")
program_file = open("16b.in", "r")

while True:
    line = clue_file.readline()
    if len(line) > 1:
        before_registers = re.match(register_pattern, line).groupdict()
        line = clue_file.readline()
        instruction = [int(v) for v in line.split()]
        line = clue_file.readline()
        after_registers = re.match(register_pattern, line).groupdict()
        line = clue_file.readline()
        current_possibilities = get_all_possibilities(before_registers, int(instruction[1]),
                                                      int(instruction[2]), int(instruction[3]))
        possible_opcodes = [k for k in current_possibilities.keys()
                            if cmp_registers(current_possibilities[k], after_registers)]
        opcode = int(instruction[0])
        if opcode in all_possibilities.keys():
            all_possibilities[opcode] = list(set(all_possibilities[opcode]) & set(possible_opcodes))
        else:
            all_possibilities.update({opcode: possible_opcodes})
        all_results.append(possible_opcodes)
    else:
        break

print "Part One:", len([r for r in all_results if len(r) >= 3])

while len([p for p in all_possibilities.keys() if len(all_possibilities[p]) > 1]) > 0:
    for code in all_possibilities.keys():
        ops = [c for c in all_possibilities[code] if c not in
               [all_possibilities[o][0] for o in all_possibilities if o != code and len(all_possibilities[o]) == 1]]
        all_possibilities[code] = ops

registers = {0: 0, 1: 0, 2: 0, 3: 0}
while True:
    line = program_file.readline()
    if len(line) > 1:
        instruction = [int(v) for v in line.split()]
        execute(all_possibilities[instruction[0]][0], instruction[1], instruction[2], instruction[3])
    else:
        break

print "Part Two:", registers[0]
