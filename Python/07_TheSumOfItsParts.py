# -*- coding: utf-8 -*-
"""
Created on Thu May 23 10:20:56 2019

--- Day 7: The Sum of Its Parts ---
You find yourself standing on a snow-covered coastline; apparently, you landed a little off course. The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be trying to unpack something that washed ashore. It's quite cold out, so you decide to risk creating a paradox by asking them for directions.

"Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the device on your wrist also be a translator? "Those clothes don't look very warm; take this." They hand you a heavy coat.

"We do need to find our way back to the North Pole, but we have higher priorities at the moment. You see, believe it or not, this box contains something that will solve all of Santa's transportation problems - at least, that's what it looks like from the pictures in the instructions." It doesn't seem like they can read whatever language it's in, but you can: "Sleigh kit. Some assembly required."

"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!" They start excitedly pulling more parts out of the box.

The instructions specify a series of steps and requirements about which steps must be finished before others can begin (your puzzle input). Each step is designated by a single letter. For example, suppose you have the following instructions:

Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
Visually, these requirements look like this:


  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----
Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically. In this example, the steps would be completed as follows:

Only C is available, and so it is done first.
Next, both A and F are available. A is first alphabetically, so it is done next.
Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three.
After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next.
F is the only choice, so it is done next.
Finally, E is completed.
So, in this example, the correct order is CABDFE.

In what order should the steps in your instructions be completed?
@author: A550325
"""

class InstructionSeries:
    def __init__(self, filename):
        with open(filename) as file:
            text = file.readlines()
        self.instructions = []
        self.parse(text)
        self.processed = []
    def parse(self, text):
        for line in text:
            words = line.split()
            self.instructions.append(Instruction(words[1], words[7]))
    def process(self):
        """Processes list of instructions"""
        while True:
            for i in self.instructions:
                if i.first not in self.processed:
                    self.appendAfterIndex(0, i.first)
                if i.then in self.processed:
                    self.checkOrderAndFix(i.first, i.then)
                else:
                    idxAfterFirst = self.processed.index(i.first) + 1 
                    self.appendAfterIndex(idxAfterFirst, i.then)     
            self.fixAlphabetical()
            if self.test1():
                print("Solution found!")
                break
    def checkOrderAndFix(self, first, then):
        """Checks if first is before then in sequence, switches them if not"""
        idxFirst = self.processed.index(first)
        if not self.isOrdered(first, then):
            self.moveToIndex(idxFirst, then)
    def isOrdered(self, first, then):
        """Returns true if first is before then"""
        idxFirst = self.processed.index(first)
        idxThen = self.processed.index(then)
        return (idxFirst < idxThen)
    def moveToIndex(self, index, element):
        """Moves element to given index"""
        self.processed.remove(element)
        self.processed.insert(index, element)
    def appendAfterIndex(self, idx, element):
        """Appends element at the earliest possibility after idx"""
        lngth = len(self.processed)
        if lngth > idx:
            while (True):   
                if element < self.processed[idx]:
                    self.processed.insert(idx, element)
                    break
                else:
                    idx += 1
                    if idx == lngth:
                        self.processed.insert(idx, element)
                        break
        else:
            self.processed.insert(idx, element)  
    def test1(self):
        for i in self.instructions:
            if not self.isOrdered(i.first, i.then):
                return False
        return True
    def fixAlphabetical(self):
        for i in range(1, len(self.processed)):
            prv = self.processed[i-1]
            nxt = self.processed[i]
            if prv > nxt: # find out-of-order char sequences
                if any((i.first == prv and i.then == nxt) for i in self.instructions):
                    pass # there is a rule for it, good
                else: # it is unintended, switch them
                    idxNxt = self.processed.index(nxt)
                    self.moveToIndex(idxNxt, prv)
        print("".join(self.processed))
        
                
class Instruction:
    def __init__(self, first, then):
        self.first = first
        self.then = then
    
filename = "07_input.txt"
ins = InstructionSeries(filename)
ins.process()
print("".join(ins.processed))
    


