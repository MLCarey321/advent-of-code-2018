import re
from copy import deepcopy


class Group:
    def __init__(self, units, unit_hp, weaknesses, immunities, dmg_amount, dmg_type, initiative):
        self.units = units
        self.unit_hp = unit_hp
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.dmg_amount = dmg_amount
        self.dmg_type = dmg_type
        self.initiative = initiative
        self.dmg_taken = 0

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memodict))
        return result

    def get_effective_power(self):
        return self.units * self.dmg_amount

    def get_damage_amount(self, other):
        dmg_amount = self.get_effective_power()
        if self.dmg_type in other.weaknesses:
            dmg_amount *= 2
        return dmg_amount

    def receive_damage(self, dmg_amount):
        self.units -= dmg_amount // self.unit_hp
        if self.units < 0:
            self.units = 0

    def __lt__(self, obj):
        my_power = self.get_effective_power()
        their_power = obj.get_effective_power()
        return my_power < their_power if my_power != their_power else self.initiative < obj.initiative

    def __gt__(self, obj):
        my_power = self.get_effective_power()
        their_power = obj.get_effective_power()
        return my_power > their_power if my_power != their_power else self.initiative > obj.initiative

    def __le__(self, obj):
        my_power = self.get_effective_power()
        their_power = obj.get_effective_power()
        return my_power < their_power or my_power == their_power and self.initiative < obj.initiative

    def __ge__(self, obj):
        my_power = self.get_effective_power()
        their_power = obj.get_effective_power()
        return my_power > their_power or my_power == their_power and self.initiative > obj.initiative

    def __eq__(self, obj):
        my_power = self.get_effective_power()
        their_power = obj.get_effective_power()
        return my_power == their_power and self.initiative == obj.initiative

    def __repr__(self):
        return "Group with %d units each with %d hit points with an attack that does %d %s damage at initiative %d " \
               "has an effective power of %d" % (self.units, self.unit_hp, self.dmg_amount, self.dmg_type,
                                                 self.initiative, self.get_effective_power())


def fight(armies, boost):
    for key in armies:
        if key[0] == "m":
            armies[key].dmg_amount += boost
    while len(set([name[0] for name in armies.keys()])) > 1:
        start_count = sum([army.units for army in armies.values()])
        order = sorted(armies.keys(), key=lambda key: armies[key], reverse=True)
        targets = {}
        for army in order:
            dmg_type = armies[army].dmg_type
            possibilities = sorted([group for group in armies.keys() if group not in targets.values() and group[0] != army[0]
                                    and dmg_type not in armies[group].immunities], key=lambda name: armies[name], reverse=True)
            if len(possibilities) > 0:
                weak = sorted([group for group in possibilities if dmg_type in armies[group].weaknesses],
                              key=lambda name: armies[name], reverse=True)
                if len(weak) > 0:
                    targets.update({army: weak[0]})
                else:
                    targets.update({army: possibilities[0]})
        targets = dict(sorted(targets.items(), key=lambda item: armies[item[0]].initiative, reverse=True))
        for attacker in targets.keys():
            if attacker not in armies.keys():
                continue
            defender = targets[attacker]
            dmg_amount = armies[attacker].get_damage_amount(armies[defender])
            armies[defender].receive_damage(dmg_amount)
            if armies[defender].get_effective_power() == 0:
                armies.pop(defender)
        end_count = sum([army.units for army in armies.values()])
        if start_count == end_count:
            for immune_group in [g for g in armies.keys() if g.startswith("m")]:
                armies.pop(immune_group)
    return armies


with open("day_24.txt") as reader:
    lines = reader.readlines()

input_pattern = r"(?P<unit_count>\d+) units each with (?P<hp>\d+) hit points (?P<conditions>\(.+\) )?" \
                r"with an attack that does (?P<dmg_amount>\d+) (?P<dmg_type>\w+) damage at initiative (?P<init>\d+)"

prefix = "m"
init = {}
index = 1
for line in lines:
    if len(line.strip()) == 0:
        prefix = "f"
        index = 1
    else:
        pattern = re.match(input_pattern, line.strip())
        if pattern is not None:
            group_dict = pattern.groupdict()
            conditions = group_dict["conditions"]
            weaknesses = []
            immunities = []
            if conditions is not None:
                conditions = conditions.strip(" ()").split("; ")
                for condition in conditions:
                    if condition.startswith("weak to"):
                        weaknesses = condition[8:].split(", ")
                    elif condition.startswith("immune to"):
                        immunities = condition[10:].split(", ")
            group = Group(units=int(group_dict["unit_count"]),
                          unit_hp=int(group_dict["hp"]),
                          dmg_amount=int(group_dict["dmg_amount"]),
                          dmg_type=group_dict["dmg_type"],
                          initiative=int(group_dict["init"]),
                          weaknesses=weaknesses,
                          immunities=immunities)
            init.update({"%s%d" % (prefix, index): group})
            index += 1

result = fight(deepcopy(init), 0)
print("Part One: %d" % sum(army.units for army in result.values()))

boost_range = (0, 1000)
solution = 0
result = fight(deepcopy(init), boost_range[1])
while list(result.keys())[0][0] == "f":
    lower = boost_range[1]
    upper = boost_range[1] * 2
    boost_range = (lower, upper)
    result = fight(deepcopy(init), upper)

solution = sum(army.units for army in result.values())

while boost_range[1] - boost_range[0] > 1:
    lower = boost_range[0]
    upper = boost_range[1]
    new_boost = lower + ((upper - lower) // 2)
    if lower == new_boost or upper == new_boost:
        break
    result = fight(deepcopy(init), new_boost)
    winner = list(result.keys())[0][0]
    if winner == "f":
        boost_range = (new_boost, upper)
    else:
        solution = sum(army.units for army in result.values())
        boost_range = (lower, new_boost)

print("Part Two: %d" % solution)
