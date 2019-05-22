# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 09:00:21 2018

--- Day 4: Repose Record ---
You've sneaked into another supply closet - this time, it's across from the prototype suit manufacturing lab. You need to sneak inside and fix the issues with the suit, but there's a guard stationed outside the lab, so this is as close as you can safely get.

As you search the closet for anything that might help, you discover that you're not the first person to want to sneak in. Covering the walls, someone has spent an hour starting every midnight for the past few months secretly observing this guard post! They've been writing down the ID of the one guard on duty that night - the Elves seem to have decided that one guard was enough for the overnight shift - as well as when they fall asleep or wake up while at their post (your puzzle input).

For example, consider the following records, which have already been organized into chronological order:

[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
Timestamps are written using year-month-day hour:minute format. The guard falling asleep or waking up is always the one whose shift most recently started. Because all asleep/awake times are during the midnight hour (00:00 - 00:59), only the minute portion (00 - 59) is relevant for those events.

Visually, these records show that the guards are asleep at these times:

Date   ID   Minute
            000000000011111111112222222222333333333344444444445555555555
            012345678901234567890123456789012345678901234567890123456789
11-01  #10  .....####################.....#########################.....
11-02  #99  ........................................##########..........
11-03  #10  ........................#####...............................
11-04  #99  ....................................##########..............
11-05  #99  .............................................##########.....
The columns are Date, which shows the month-day portion of the relevant day; ID, which shows the guard on duty that day; and Minute, which shows the minutes during which the guard was asleep within the midnight hour. (The Minute column's header shows the minute's ten's digit in the first row and the one's digit in the second row.) Awake is shown as ., and asleep is shown as #.

Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up. For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order you found them. You'll need to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 10 * 24 = 240.)

@author: A550325
"""
import re

class Guards:
    def __init__(self):
        self.currentGuard = 0
        self.fellAsleep = 0
        self.wokeUp = 0
        self.sleepingTime = {}      # Stores amount of time slept in minutes per guard
        self.sleepPerMinute = {}    # Stores number of shifts slept per minute per guard
    def process(self, log):
        log.sort()
        for line in log:
            self.parse(line)
    def parse(self, event):
        """Parse what happens in event"""
        splitLine = event.split()
       # print(splitLine)
        if splitLine[2] == "Guard":
            self.currentGuard = int(splitLine[3][1:])
        elif splitLine[3] == "asleep":
            minute = int(re.split(':|]', splitLine[1])[1])
            self.sleep(minute)
        elif splitLine[2] == "wakes":
            minute = int(re.split(':|]', splitLine[1])[1])
            self.wakeUp(minute)
    def sleep(self, minute):
        """Store minute guard fell asleep"""
        self.fellAsleep = minute
    def wakeUp(self, minute):
        """Process wake-up event"""
        self.wokeUp = minute
        self.incrementSleepingTime()
        self.storeSleepingMinutes()
        
    def incrementSleepingTime(self):
        sleepingTime = self.wokeUp - self.fellAsleep
        self.sleepingTime[self.currentGuard] = self.sleepingTime.get(self.currentGuard, 0) + sleepingTime
    def storeSleepingMinutes(self):
        """Increment nested dictionary values to store which guard sleeps when"""
        for m in range(self.fellAsleep, self.wokeUp):
            # If first shift of guard, initialize inner dictionary
            if self.currentGuard not in self.sleepPerMinute:
                self.sleepPerMinute[self.currentGuard] = {}
            # Get current value in dictionary, 0 if not present
            currentEntry = self.sleepPerMinute[self.currentGuard].get(m, 0)
            self.sleepPerMinute[self.currentGuard][m] = currentEntry + 1
        pass
    def print(self):
        print(self.currentGuard, self.sleepingTime, self.sleepPerMinute)
    def laziestGuard(self):
        """Returns laziest guard in terms of sleeping time"""
        return max(self.sleepingTime, key=self.sleepingTime.get)
    def solution1(self):
        """Returns product of id of lazy guard and his laziest minute"""
        guard = self.laziestGuard()
        laziestMinute = max(self.sleepPerMinute[guard], key=self.sleepPerMinute[guard].get)
        return guard * laziestMinute
    def solution2(self):
        res = 0
        guard = 0
        minute = -1
        for g in self.sleepPerMinute:
            for m in self.sleepPerMinute[g]:
                if self.sleepPerMinute[g][m] > res:
                    res = self.sleepPerMinute[g][m]
                    guard = g
                    minute = m
                    print(res, g, m)
        return guard * minute

filename = "04_input.txt"
with open(filename) as file:
    log = file.readlines()
    
guards = Guards()
guards.process(log)

print(guards.solution1())
print(guards.sleepPerMinute[1783])
print(guards.solution2())