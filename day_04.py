#!/usr/bin/python3

import sys
import re
import operator
from datetime import datetime
from collections import defaultdict

time_fmt = "%Y-%m-%d %H:%M"
entry_pattern = r"\[(?P<timestamp>.+)\] (?P<activity>.+)"
guard_pattern = r"Guard #(?P<id>\d*) begins shift"
activities = dict()

print("Paste Puzzle Input:")
while True:
    line = sys.stdin.readline()
    if len(line) > 1:
        entry = re.match(entry_pattern, line).groupdict()
        timestamp = datetime.strptime(entry["timestamp"], time_fmt)
        activities.update({timestamp: entry["activity"]})
    else:
        break

sleep_log = defaultdict(dict)
sleep_sums = defaultdict(int)
guard = 0
sleep_minute = datetime
wake_minute = datetime

for timestamp in sorted(activities):
    activity = activities[timestamp]
    if "falls asleep" == activity:
        sleep_minute = timestamp
    elif "wakes up" == activity:
        wake_minute = timestamp
        start_time = int(sleep_minute.minute) if sleep_minute.hour == 0 else 0
        end_time = int(wake_minute.minute) if wake_minute.hour == 0 else 60
        for minute in range(start_time, end_time):
            if minute not in sleep_log[guard].keys():
                sleep_log[guard].update({minute: 0})
            sleep_log[guard][minute] += 1
            sleep_sums[guard] += 1
    else:
        guard = int(re.match(guard_pattern, activity).groupdict()["id"])

longest_rest = 0
sleepiest_guard = 0
for sleeper in sleep_sums.keys():
    if sleep_sums[sleeper] > longest_rest:
        longest_rest = sleep_sums[sleeper]
        sleepiest_guard = sleeper

sleepiest_minute = max(sleep_log[sleepiest_guard].items(), key=operator.itemgetter(1))[0]
consistent_guard = 0
consistent_minute = 0
total_occurrences = 0

for log in sleep_log.keys():
    for minute in sleep_log[log].keys():
        if sleep_log[log][minute] > total_occurrences:
            consistent_guard = log
            consistent_minute = minute
            total_occurrences = sleep_log[log][minute]

print("Part One:", sleepiest_guard * sleepiest_minute)
print("Part Two:", consistent_guard * consistent_minute)
