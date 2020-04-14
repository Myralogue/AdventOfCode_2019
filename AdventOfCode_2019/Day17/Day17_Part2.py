import sys, os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/Day09/'))

import Day09_Computer as COMPUTER

import Queue
from threading import Thread

program = COMPUTER.getprogram('Day17/Day17_Input.txt')

class screen():
    def __init__(self, myrobot):
        self.pixels = [[]]
        self.robot = myrobot

    def outputtopixels(self, output):
        self.pixels = []
        width = output.index(10)
        for row in (output[x:x + width] for x in range(0, len(output) - 1, width + 1)):
            self.pixels.append(row)
            if row.count(94) != 0:
                self.robot.pos = [len(self.pixels) - 1, row.index(94)]

    def writetoscreen(self, input, cls = False):
        text = ''
        for c in input:
            text += str(unichr(c))
        if cls:
            os.system('cls')
        print text

    def getpixel(self, pos):
        if pos[0] < 0 or pos[1] < 0:
            return 0
        try:
            return self.pixels[pos[0]][pos[1]]
        except:
            return 0

class robot():
    def __init__(self):
        self.pos = []
        self.dir = [-1, 0]

def main(enablevideofeed):
    myrobot = robot()
    myscreen = screen(myrobot)
    inqueue = Queue.Queue()
    outqueue = Queue.Queue()
    program[0] = 2
    t = Thread(target=COMPUTER.start, args=(program, [], inqueue, outqueue, Queue.Empty, 1))
    t.start()

    output = outqueue.get()
    myscreen.outputtopixels(output)
    myscreen.writetoscreen(output)

    route = pathfind(myscreen, myrobot)
    functions = calcprograms(route)

    movementroutine = createrobotmovementroutine(route, functions)
    robotfunctions = createrobotmovementfunctions(functions)

    inqueue.put(movementroutine)
    print "movement routine: " + str(movementroutine) + '\n'
    output = outqueue.get()
    myscreen.writetoscreen(output)

    inqueue.put(robotfunctions[0])
    print "function A: " + str(robotfunctions[0]) + '\n'
    output = outqueue.get()
    myscreen.writetoscreen(output)

    inqueue.put(robotfunctions[1])
    print "function B: " + str(robotfunctions[1]) + '\n'
    output = outqueue.get()
    myscreen.writetoscreen(output)

    inqueue.put(robotfunctions[2])
    print "function C: " + str(robotfunctions[2]) + '\n'
    output = outqueue.get()
    myscreen.writetoscreen(output)

    inqueue.put([ord(enablevideofeed), 10])
    print "videofeed: " + str(enablevideofeed) + '\n'
    output = outqueue.get()

    dustcollected = output[-1]
    del output[-1]
    myscreen.writetoscreen(output)
    print "total dust collected: " + str(dustcollected)

def pathfind(myscreen, myrobot):
    route = []
    while True:
        if myscreen.getpixel(addvec2(myrobot.pos, rotate(myrobot.dir, True))) == 35:
            myrobot.dir = rotate(myrobot.dir, True)
            instruction = 'R'
        elif myscreen.getpixel(addvec2(myrobot.pos, rotate(myrobot.dir, False))) == 35:
            myrobot.dir = rotate(myrobot.dir, False)
            instruction = 'L'
        else:
            return route

        current = 0
        while myscreen.getpixel(addvec2(myrobot.pos, myrobot.dir)) == 35:
            current += 1
            myrobot.pos = addvec2(myrobot.pos, myrobot.dir)
            if myrobot.pos == [24, 0]:
                pass
        else:
            route.append(instruction + str(current))

def addvec2(vec1, vec2):
    return [vec1[0] + vec2[0], vec1[1] + vec2[1]]

def rotate(current, turnright):
    if turnright:
        return [current[1], -current[0]]
    else:
        return [-current[1], current[0]]

def calcprograms(route):
    for length in range(0, 5):
        remainder = splitbyseq(route, route[:length])
        
        if len(remainder) > 2 or len(remainder[0]) > 10 or len(remainder[1]):
            shortest = remainder[0]
            for r in remainder:
                if len(r) < len(shortest):
                    shortest = r

            for t in range(0, len(shortest) - 1):
                checklist = shortest[:len(shortest) - t]
                newlist = []
                for r in remainder:
                    split = splitbyseq(r, checklist)
                    if split != [[]]:
                        newlist.extend(split)

                isthesame = True
                for i in range(1, len(newlist)):
                    if newlist[i - 1] != newlist[i]:
                        isthesame = False
                if isthesame:
                    return [route[:length], checklist, newlist[0]]
        else:
            return [route[:length], remainder[0], remainder[1]]

def splitbyseq(mylist, seq):
    length = len(seq)
    remainder = []

    if mylist[:length] == seq:
        lastidx = length
    else: 
        lastidx = 0

    for i in range(length + 1, len(mylist) + 1):
        if mylist[i - length:i] == seq:
            remainder.append(mylist[lastidx:i - length])
            lastidx = i        
    if lastidx != len(mylist):        
        remainder.append(mylist[lastidx:len(mylist)])

    return remainder

def createrobotmovementroutine(route, functions):
    robotroute = []
    list = route[:]
    idx = 1
    while list != []:
        segment = list[:idx]
        if segment == functions[0]:
            robotroute.extend([65, 44]) #A
            list = list[idx:]
            idx = 0
        if segment == functions[1]:
            robotroute.extend([66, 44]) #B
            list = list[idx:]
            idx = 0
        if segment == functions[2]:
            robotroute.extend([67, 44]) #C
            list = list[idx:]
            idx = 0
        idx += 1
    else:
        robotroute[-1] = 10
        return robotroute

def createrobotmovementfunctions(functions):
    robotfunctions = [[], [], []]

    for i in range(0, len(functions)):
        for instructions in functions[i]:
            if instructions[0] == 'L':
                robotfunctions[i].extend([76, 44])
            elif instructions[0] == 'R':
                robotfunctions[i].extend([82, 44])

            for c in instructions[1:]:
                robotfunctions[i].append(ord(c))
            robotfunctions[i].append(44)
        robotfunctions[i][-1] = 10
    return robotfunctions

if __name__ == '__main__':
    main('n')