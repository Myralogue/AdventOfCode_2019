import sys, os.path
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/Day09/'))

import Day09_Computer as COMPUTER

import Queue
from threading import Thread

program = COMPUTER.getprogram('Day11/Day11_Input.txt')

class paintrobot():
    def __init__(self, startdir = 0, startpos = [0,0]):
        self.dir = startdir
        self.pos = startpos

    #0 = up, 1 = left, 2 = down, 3 = right
    def rotate(self, dir):
        if dir == 1:
            #right
            if self.dir > 2:
                self.dir = 0
            else:
                self.dir += 1
            return self.dir
        else:
            #left
            if self.dir < 1:
                self.dir = 3
            else:
                self.dir -= 1
            return self.dir
    def move(self):
        if self.dir == 0:   #up
            self.pos[0] += 1
        elif self.dir == 2: #down
            self.pos[0] -= 1
        elif self.dir == 1: #left
            self.pos[1] += 1
        elif self.dir == 3: #right
            self.pos[1] -= 1

def main():
    inqueue = Queue.Queue()
    outqueue = Queue.Queue()
    returnqueue = Queue.Queue()
    t = Thread(target=COMPUTER.start, args=(program, [0], inqueue, outqueue, returnqueue))
    t.start()

    robot = paintrobot()
    minx = 0
    miny = 0
    image = [[0]]
    paintedpositions = []
    
    while True:
        color = outqueue.get(timeout=1)
        rotation = outqueue.get(timeout=1)

        if not returnqueue.empty():
            print len(paintedpositions)
            break

        wascolor = image[robot.pos[0] - minx][robot.pos[1] - miny]
        if wascolor != color:
            image[robot.pos[0] - minx][robot.pos[1] - miny] = color
            if paintedpositions.count([robot.pos[0], robot.pos[1]]) == 0:
                paintedpositions.append([robot.pos[0], robot.pos[1]])

        robot.rotate(rotation)
        robot.move()

        if robot.dir == 0: #up
            if robot.pos[0] >= len(image) + minx:
                l = [0] * len(image[0])
                image.append(l)
        elif robot.dir == 2: #down
            if robot.pos[0] < minx:
                l = [0] * len(image[0])
                image.insert(0, l)
                minx -= 1
        elif robot.dir == 1: #right
            if robot.pos[1] > len(image[0]) + miny - 1:
                for i in range(0, len(image)):
                    image[i].append(0)
        elif robot.dir == 3: #left
            if robot.pos[1] < miny:
                for i in range(0, len(image)):
                    image[i].insert(0, 0)
                miny -= 1

        inqueue.put(image[robot.pos[0] - minx][robot.pos[1] - miny])

if __name__ == '__main__':
    main()
