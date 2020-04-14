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
        self.pixels = [[0]]

    def writetoscreen(self):
        text = ''
        for r in self.pixels:
            text += self.writerow(r) + '\n'
        system('cls')
        print text

    def writerow(self, row):
        line = ''
        for p in row:
            if p == 0:
                line += ' '
            elif p == 1:
                line += u'\u2588'
            elif p == 2:
                line += '#'
            elif p == 3:
                line += '='
            elif p == 4:
                line += 'o'
        return line

    def setpixel(self, x, y, value):
        if len(self.pixels) <= y:
            self.pixels.append([0] * len(self.pixels[0]))
        elif len(self.pixels[0]) <= x:
            for i in range(0, len(self.pixels)):
                    self.pixels[i].append(0)

        self.pixels[y][x] = value

def run(runAI, render):
    myscreen = screen()
    inqueue = Queue.Queue()
    outqueue = Queue.Queue()
    returnqueue = Queue.Queue()
    program[0] = 2 # insert coins
    t = Thread(target=COMPUTER.start, args=(program, [], inqueue, outqueue, returnqueue, 1))
    t.start()

    ballx = 0
    paddlex = 0
    score = 0

    while True:
        try:
            output = outqueue.get(timeout=1)
            for i in range(0, len(output) / 3):
                x = output[i * 3]
                y = output[i * 3 + 1]
                tileid = output[i * 3 + 2]

                if x == -1:
                    score = tileid
                elif tileid == 4:
                    ballx = x
                elif tileid == 3:
                    paddlex = x

                myscreen.setpixel(x, y, tileid)

            if render:
                myscreen.writetoscreen()
            print "score: " + str(score)

            if not returnqueue.empty():
                return score

            if runAI:
                if ballx > paddlex:
                    inqueue.put(1)
                elif ballx < paddlex:
                    inqueue.put(-1) 
                else:
                    inqueue.put(0)
            else:
                key = getkey()
                if key == keys.LEFT:
                    inqueue.put(-1)
                elif key == keys.RIGHT:
                    inqueue.put(1)
                else:
                        inqueue.put(0)
        except Queue.Empty: #no more updates
            if not returnqueue.empty():
                return score

def main():
    score = run(True, True)
    return score

if __name__ == '__main__':
    main()