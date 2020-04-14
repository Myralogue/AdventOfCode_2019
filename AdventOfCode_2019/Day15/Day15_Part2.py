import sys, os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/Day09/'))

import Day09_Computer as COMPUTER

import Queue
from threading import Thread

program = COMPUTER.getprogram('Day15/Day15_Input.txt')

class screen():
    def __init__(self):
        self.pixels = [[-1]]
        self.minx = 0
        self.miny = 0

    def writetoscreen(self):
        text = ''
        robotvalue = self.pixels[myrobot.y - self.miny][myrobot.x - self.minx]      
        self.pixels[myrobot.y - self.miny][myrobot.x - self.minx] = -3
        if oxygensyspos != []:
            oxygenvalue = self.pixels[oxygensyspos[1] - self.miny][oxygensyspos[0] - self.minx]
            self.pixels[oxygensyspos[1] - self.miny][oxygensyspos[0] - self.minx] = - 4

        for r in self.pixels:
            text += self.writerow(r) + '\n'

        self.pixels[myrobot.y - self.miny][myrobot.x - self.minx] = robotvalue
        if oxygensyspos != []:
            self.pixels[oxygensyspos[1] - self.miny][oxygensyspos[0] - self.minx] = oxygenvalue

        os.system('cls')
        print text

    def writerow(self, row):
        line = ''
        for p in row:
            if p == -1:
                line += '?'
            elif p == -2:
                line += u'\u2588'
            elif p == -3:
                line += '*'
            elif p == -4:
                line += 'X'
            elif p == -5:
                line += 'O'
            else:
                line += str(p % 10)
        return line

    def setpixel(self, x, y, value):
        if len(self.pixels) + self.miny <= y: #north
            self.pixels.append([-1] * len(self.pixels[0]))
        elif y < self.miny: #south
            self.pixels.insert(0, [-1] * len(self.pixels[0]))
            self.miny -= 1
        elif len(self.pixels[0]) + self.minx <= x: #west
            for i in range(0, len(self.pixels)):
                self.pixels[i].append(-1)
        elif x < self.minx: #east
            for i in range(0, len(self.pixels)):
                self.pixels[i].insert(0, -1)
            self.minx -= 1

        self.pixels[y - self.miny][x - self.minx] = value

    def getpixel(self, x, y):
        try:
            ypos = y - self.miny
            xpos = x - self.minx
            if xpos < 0 or ypos < 0:
                return -1
            return self.pixels[ypos][xpos]
        except:
            return -1

class robot():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dir = 1

    def move(self):
        if self.dir == 1:
            self.y -= 1
        elif self.dir == 2:
            self.y += 1
        elif self.dir == 3:
            self.x += 1
        elif self.dir == 4:
            self.x -= 1

    def moveback(self):
        if self.dir == 1:
            self.y += 1
            inqueue.put(2)
        elif self.dir == 2:
            self.y -= 1
            inqueue.put(1)
        elif self.dir == 3:
            self.x -= 1
            inqueue.put(4)
        elif self.dir == 4:
            self.x += 1
            inqueue.put(3)
        outqueue.get()

myscreen = screen()
myrobot = robot()
inqueue = Queue.Queue()
outqueue = Queue.Queue()
returnqueue = Queue.Queue()

oxygensyspos = []

def main(rendersteps):
    global render 
    render = rendersteps
    t = Thread(target=COMPUTER.start, args=(program, [1], inqueue, outqueue, returnqueue, 0))
    t.start()
    
    pathfind(0, -1, 1, 1)

    maxdistfromoxygen = simulateoxygen(oxygensyspos)
    print "time to oxygen saturation: " + str(maxdistfromoxygen)
    return maxdistfromoxygen

def pathfind(x, y, dir, dist = 0):
    global oxygensyspos
    output = outqueue.get()
    if output != 0:
        myrobot.move()

        if output == 2: #found oxygen system
            oxygensyspos = [x, y]

        myscreen.setpixel(myrobot.x, myrobot.y, dist)
        if render:
            myscreen.writetoscreen()

        if myscreen.getpixel(x, y - 1) == -1: #up
            inqueue.put(1)
            myrobot.dir = 1
            pathfind(x, y - 1, 1, dist + 1)
        if myscreen.getpixel(x, y + 1) == -1: #down
            myrobot.dir = 2
            inqueue.put(2)
            pathfind(x, y + 1, 2, dist + 1)
        if myscreen.getpixel(x + 1, y)  == -1: #right
            myrobot.dir = 3
            inqueue.put(3)
            pathfind(x + 1, y, 3, dist + 1)
        if myscreen.getpixel(x - 1, y)  == -1: #left
            myrobot.dir = 4
            inqueue.put(4)
            pathfind(x - 1, y, 4, dist + 1)

        myrobot.dir = dir
        myrobot.moveback()
    else:
        y = 1 if myrobot.dir == 2 else 0
        y -= 1 if myrobot.dir == 1 else 0
        x = 1 if myrobot.dir == 3 else 0
        x -= 1 if myrobot.dir == 4 else 0
        myscreen.setpixel(myrobot.x + x, myrobot.y + y, -2)

    if render:
        myscreen.writetoscreen()

def simulateoxygen(oxygensyspos):
    maxdist = -1
    current = [oxygensyspos]

    while len(current) > 0:
        newlist = []
        for p in current:
            if myscreen.getpixel(p[0], p[1] - 1) > 0: #up
                newlist.append([p[0], p[1] - 1])
            if myscreen.getpixel(p[0], p[1] + 1) > 0: #down
                newlist.append([p[0], p[1] + 1])
            if myscreen.getpixel(p[0] + 1, p[1]) > 0: #right
                newlist.append([p[0] + 1, p[1]])
            if myscreen.getpixel(p[0] - 1, p[1]) > 0: #left
                newlist.append([p[0] - 1, p[1]])

            myscreen.setpixel(p[0], p[1], -5)

        maxdist += 1
        current = newlist

        if render:
            myscreen.writetoscreen()
    else:
        return maxdist

if __name__ == '__main__':
    main(True)