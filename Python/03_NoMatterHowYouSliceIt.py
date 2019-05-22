# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 08:59:42 2018

--- Day 3: No Matter How You Slice It ---
The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.
A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........
The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?
@author: A550325
"""
import re


class Fabric():
    """A class representing the fabric"""
    def __init__(self, x, y):
        """Initializes dictionary for the whole fabric"""
        self.dict = {}
        for i in range(x):
            for j in range(y):
                self.dict[(i,j)] = 0
        self.claims = {}
    def mark(self, claim):
        """Mark a given rectangle derived from claim"""
        (_, coord, size) = parse(claim)
        mark(coord, size)
    def mark(self, coord, size):
        """Mark a given rectangle on the fabric"""
        for i in range(coord[0], coord[0]+size[0]):
            for j in range(coord[1], coord[1]+size[1]):
                self.dict[(i,j)] += 1
        
        
    def overlap(self):
        """Calculate area which has overlapping claims"""
        s = sum(1 for v in self.dict.values() if v >= 2)
        return s
    
    # Part 2
    def markWithId(self, claim):
        (claimId, coord, size) = parse(claim)
        markWithId(claimId, coord, size)
    def markWithId(self, claimId, coord, size):
        """ Mark areas with claim if not already claimed
            and invalidate overlapping claims"""
        self.claims[claimId] = True
        for i in range(coord[0], coord[0]+size[0]):
            for j in range(coord[1], coord[1]+size[1]):
                if self.dict[(i,j)]:
                    # If area already used by another claim, invalidate both
                    self.claims[self.dict[(i,j)]] = False
                    self.claims[claimId]          = False
                else: # not used yet
                    self.dict[(i,j)] = claimId
    def bestClaim(self):
        """Returns highest claim which does not overlap with others"""
        return max(self.claims, key=self.claims.get)
            
                
def parse(line):
    """ Return parsed string as a tuple
        line should be of format "#ID @ coord1,coord2: size1xsize2" """
    splitLine = line.split()
    ID = int(splitLine[0][1:])
    coord = [int(i) for i in re.split(',|:', splitLine[2])[:-1]]
    size  = [int(i) for i in re.split('x',   splitLine[3])]
    return (ID, coord, size)

    
filename = "03_input.txt"
with open(filename) as file:
    lines = file.readlines()

squareSize = (1000, 1000)
fabric = Fabric(*squareSize)
for line in lines:
    (_, coord, size) = parse(line)
    fabric.mark(coord, size)
result = fabric.overlap()

print(result)

"""--- Part Two ---
Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?"""

fabric2 = Fabric(*squareSize)
for line in lines:
    (claimId, coord, size) = parse(line)
    fabric2.markWithId(claimId, coord, size)
print(fabric2.bestClaim())