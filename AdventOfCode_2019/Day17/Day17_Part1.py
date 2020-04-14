import sys, os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/Day09/'))

import Day09_Computer as COMPUTER

import Queue
from threading import Thread

program = COMPUTER.getprogram('Day17/Day17_Input.txt')

class screen():
    def __init__(self):
        self.pixels = [[]]
        self.intersections = []

    def outputtopixels(self, output):
        potentialintersections = []
        self.pixels = []
        width = output.index(10)
        for row in (output[x:x + width] for x in range(0, len(output) - 1, width + 1)):
            self.pixels.append(row)

            for i in range(0, len(row) - 2):
                if sum(row[i:i+3]) == 105:
                       potentialintersections.append([len(self.pixels) - 1, i + 1])

        for p in potentialintersections:
            if self.getpixel(p[1], p[0] - 1) +  self.getpixel(p[1], p[0] + 1) == 70:
                self.intersections.append(p)
                self.pixels[p[0]][p[1]] = 79

    def writetoscreen(self):
        text = ''
        for r in self.pixels:
            text += self.writerow(r) + '\n'
        os.system('cls')
        print text

    def writerow(self, row):
        line = ''
        for p in row:
            line += str(unichr(p))
        return line

    def getpixel(self, x, y):
        try:
            return self.pixels[y][x]
        except:
            return -1

def main():
    myscreen = screen()
    outqueue = Queue.Queue()
    t = Thread(target=COMPUTER.start, args=(program, [], Queue.Empty, outqueue, Queue.Empty, 1))
    t.start()

    output = outqueue.get()
    myscreen.outputtopixels(output)
    myscreen.writetoscreen()

    sum = 0
    for i in myscreen.intersections:
        sum += i[0] * i[1]
    print "allignment parameter sum: " + str(sum)

main()