import sys, os
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/Day09/'))

import Day09_Computer as COMPUTER

import Queue
from threading import Thread
from os import system

from getkey import getkey, keys

program = COMPUTER.getprogram('Day13/Day13_Input.txt')

class screen():
    def __init__(self):
        self.cEmpty= ' '
        self.cWall = u'\u2588'
        self.cBlock = '#'
        self.cPaddle = '='
        self.cBall = 'o'

        self.pixels = [[0]]

    def writetoscreen(self):
        #system('cls') 
        for r in self.pixels:
            print self.writerow(r)

    def writerow(self, row):
        line = ''
        for p in row:
            if p == 0:
                line += self.cEmpty
            elif p == 1:
                line += self.cWall
            elif p == 2:
                line += self.cBlock
            elif p == 3:
                line += self.cPaddle
            elif p == 4:
                line += self.cBall
        return line

    def setpixel(self, x, y, value):
        if len(self.pixels) <= y:
            self.pixels.append([0] * len(self.pixels[0]))
        elif len(self.pixels[0]) <= x:
            for i in range(0, len(self.pixels)):
                    self.pixels[i].append(0)

        self.pixels[y][x] = value

def run():
    myscreen = screen()
    inqueue = Queue.Queue()
    outqueue = Queue.Queue()
    returnqueue = Queue.Queue()

    t = Thread(target=COMPUTER.start, args=(program, [], inqueue, outqueue, returnqueue))
    t.start()

    while True:
        try:
            x = outqueue.get(timeout=1)
            y = outqueue.get(timeout=1)
            tileid = outqueue.get(timeout=1)
        except Queue.Empty:
            system('cls')
            myscreen.writetoscreen()

            if not returnqueue.empty():
                return myscreen.pixels

        myscreen.setpixel(x, y, tileid)        

def main():
    pixels = run()
    count = 0
    for r in pixels:
        count += r.count(2)
    print "amount of blocks:" + str(count)
    return count
main()
