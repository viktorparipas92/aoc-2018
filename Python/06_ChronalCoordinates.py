# -*- coding: utf-8 -*-
"""
Created on Wed May 22 14:50:51 2019

--- Day 6: Chronal Coordinates ---
The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?
@author: A550325
"""

import re
    
class Coordinates:
    def __init__(self, points):
        self.points = set()
        self.readPoints(points)
    def readPoints(self, lines):
        """Fills underlying set of Point objects from lines"""
        for line in lines:
            point = self.parse(line)
            self.points.add(point)
    def parse(self, line):
        """Returns a Point described by line"""
        coords = [int(c) for c in re.split(', ', line)]
        return Point(coords[0], coords[1])
    def outerRectangle(self):
        """Yields a generator over the befoglaló téglalap"""
        minX = min(p.x for p in self.points)
        minY = min(p.y for p in self.points)
        maxX = max(p.x for p in self.points)
        maxY = max(p.y for p in self.points)
        #return (minX, minY, maxX, maxY)
        for x in range(minX, maxX+1):
            for y in range(minY, maxY+1):
                yield (x,y)
    def outerRectanglePlus(self):
        """Yields a bit larger rectangle for comparison"""
        minX = min(p.x for p in self.points)
        minY = min(p.y for p in self.points)
        maxX = max(p.x for p in self.points)
        maxY = max(p.y for p in self.points)
        #return (minX, minY, maxX, maxY)
        for x in range(minX-1, maxX+2):
            for y in range(minY-1, maxY+2):
                yield (x,y)
    
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def manhattan(self, other):
        """Returns manhattan distance to another Point"""
        xDist = abs(self.x - other.x)
        yDist = abs(self.y - other.y)
        return xDist + yDist
    def closestPoint(self, coords):
        """Returns a Point out of coords closest to self"""
        minDist = 10000;
        closest = Point()
        for p in coords.points:
            dist = self.manhattan(p)
            if dist < minDist: # new closest point found
                minDist = dist
                closest = p
            elif dist == minDist: # if two are equally close, neither is good
                closest = Point()
        if closest.x or closest.y:
            return closest
    """FOR PART 2"""
    def totalDistance(self, coords):
        return sum(self.manhattan(p) for p in coords.points)
    def isSafe(self, coords):
        return self.totalDistance(coords) < 10000
        
filename = "06_input.txt"
with open(filename) as file:
    points = file.readlines()

coords = Coordinates(points)
# Consider the necessary rectangle
areas1 = {}
for x,y in coords.outerRectangle():
    closest = Point(x,y).closestPoint(coords)
    areas1[closest] = areas1.get(closest, 0) + 1

# Consider a rectangle incrementally larger
areas2 = {}
for x,y in coords.outerRectanglePlus():
    closest = Point(x,y).closestPoint(coords)
    areas2[closest] = areas2.get(closest, 0) + 1

# Consider only areas with the same size in both cases
# then take the maximum area out of the eligible ones
solution = max(v for k,v in areas1.items() if areas1[k] == areas2[k])
print(solution)

"""
--- Part Two ---
On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.
In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as follows, where abs() is the absolute value function:

Distance to coordinate A: abs(4-1) + abs(3-1) =  5
Distance to coordinate B: abs(4-1) + abs(3-6) =  6
Distance to coordinate C: abs(4-8) + abs(3-3) =  4
Distance to coordinate D: abs(4-3) + abs(3-4) =  2
Distance to coordinate E: abs(4-5) + abs(3-5) =  3
Distance to coordinate F: abs(4-8) + abs(3-9) = 10
Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30
Because the total distance to all coordinates (30) is less than 32, the location is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.

What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?
"""

safeRegionSize = sum(Point(x,y).isSafe(coords) for x,y in coords.outerRectangle())
print(safeRegionSize)

