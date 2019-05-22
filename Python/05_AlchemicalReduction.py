# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 08:56:49 2018
--- Day 5: Alchemical Reduction ---
You've managed to sneak in to the prototype suit manufacturing lab. The Elves are making decent progress, but are still struggling with the suit's size reduction capabilities.

While the very latest in 1518 alchemical technology might have solved their problem eventually, you can do better. You scan the chemical composition of the suit's material and discover that it is formed by extremely long polymers (one of which is available as your puzzle input).

The polymer is formed by smaller units which, when triggered, react with each other such that two adjacent units of the same type and opposite polarity are destroyed. Units' types are represented by letters; units' polarity is represented by capitalization. For instance, r and R are units with the same type but opposite polarity, whereas r and s are entirely different types and do not react.

For example:

In aA, a and A react, leaving nothing behind.
In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
In abAB, no two adjacent units are of the same type, and so nothing happens.
In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.
Now, consider a larger example, dabAcCaCBAcCcaDA:

dabAcCaCBAcCcaDA  The first 'cC' is removed.
dabAaCBAcCcaDA    This creates 'Aa', which is removed.
dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
dabCBAcaDA        No further actions can be taken.
After all possible reactions, the resulting polymer contains 10 units.

How many units remain after fully reacting the polymer you scanned? (Note: in this puzzle and others, the input is large; if you copy/paste your input, make sure you get the whole thing.)

@author: A550325
"""
class Polymer:
    def __init__(self, chain):
        self.chain = chain
        self.processed = []
        self.latest = ""
        self.current = ""
    def process(self):
        self.processed = []
        """Processes whole chain, triggering reactions"""
        for ch in self.chain:
            self.processUnit(ch)
        return len(self.processed)
    def processInput(self, chain):
        self.processed = []
        for ch in chain:
            self.processUnit(ch)
        return len(self.processed)
    def processUnit(self, ch):
        """Processes next unit, i.e checks if it is destroyed or not"""
        self.current = ch
        if (self.unitsReact()):
            self.delete()
        else:
            self.goOn()
    def delete(self):
        """Destroys reacting units"""
        self.processed.pop()
        self.latest = self.processed[-1] if len(self.processed) else ""
    def goOn(self):
        """Stores last unit of chain which was processed"""
        self.latest = self.current
        self.processed.append(self.latest)   
    def unitsReact(self):
        """Returns true if adjacent units react,
           i.e. types (letters) match, polarities (case) are opposite"""
        current = ord(self.current) if self.current else 0
        latest = ord(self.latest) if self.latest else 0
        if (current == (latest + 32)) or (current == latest - 32):
            return True
        else:
            return False
    def remove(self, toRemove):
        res = ""
        for unit in self.chain:
            if (unit == toRemove) or (ord(unit) == ord(toRemove)-32):
                pass
            else:
                res += unit
        return res
    
filename = "05_input.txt"
with open(filename) as file:
    polymerChain = file.read()
    
polymer = Polymer(polymerChain)
print(polymer.process())


"""
--- Part Two ---
Time to improve the polymer.

One of the unit types is causing problems; it's preventing the polymer from collapsing as much as it should. Your goal is to figure out which unit type is causing the most problems, remove all instances of it (regardless of polarity), fully react the remaining polymer, and measure its length.

For example, again using the polymer dabAcCaCBAcCcaDA from above:

Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer produces dbCBcD, which has length 6.
Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this polymer produces daCAcaDA, which has length 8.
Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer produces daDA, which has length 4.
Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this polymer produces abCBAc, which has length 6.
In this example, removing all C/c units was best, producing the answer 4.

What is the length of the shortest polymer you can produce by removing all units of exactly one type and fully reacting the result?
"""
def char_range(c1, c2):
    for i in range(ord(c1), ord(c2)):
        yield chr(i)
        
polymer2 = Polymer(polymerChain)
#print(len(polymerChain))
res = len(polymerChain)
for ch in char_range('a', 'z'):
    withoutCh = polymer.remove(ch)
    lngth = polymer.processInput(withoutCh)
    print(lngth)
    if lngth < res:
        res = lngth
print(res)
#print(len(withoutA))
#print(withoutA.find('A'))
#print(polymer.processInput(withoutA))  


