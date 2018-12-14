#!/usr/bin/python3

import operator
from collections import defaultdict

num_players = 464
max_marble = 7091800

players = defaultdict(int)
circle = [0]
current_marble = 1
current_position = 0
current_player = 1

while current_marble <= max_marble:
    if current_marble % 23 == 0:
        players[current_player] += current_marble
        current_position -= 7
        if current_position < 0:
            current_position += len(circle)
        marble_value = circle[current_position]
        circle.remove(circle[current_position])
        players[current_player] += marble_value
    else:
        current_position = 0 if len(circle) == 0 else (current_position + 2) % len(circle)
        circle.insert(current_position, current_marble)
    if current_marble == max_marble / 100:
        winning_player = max(players.items(), key=operator.itemgetter(1))[0]
        winning_score = players[winning_player]
        print "Part One:", winning_score
    current_marble += 1
    current_player = (current_player % num_players) + 1

winning_player = max(players.items(), key=operator.itemgetter(1))[0]
winning_score = players[winning_player]
print "Part Two:", winning_score
