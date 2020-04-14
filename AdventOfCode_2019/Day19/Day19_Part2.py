import sys, os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/Day09/'))

import Day09_Computer as COMPUTER
program = COMPUTER.getprogram('Day19/Day19_Input.txt')
import timeit

def main(size):
    def getpos(x, y):
        return COMPUTER.start(program[:], [x,y])[0]

    def estimateratio(depth, requirement): 
        'returns idx 0: ratio, 1: padding'
        x = depth / 2
        while getpos(x, depth) == 0:
            x += 1
        else:
            width = 1
            while getpos(x + width, depth) == 1:
                width += 1
        return [depth / width, int(float(x) / depth  * requirement)]

    ratio = estimateratio(50, size)
    y = ratio[0] * (size + ratio[1]) + size
    offset = int(y * (ratio[1] / float(size)))
    while True:
        x = offset
        y += 1
        while getpos(x, y) == 0:
            x += 1
        else:
            offset = x
            print 'checked pos: ' + str([x, y])
            if getpos(x + (size - 1), y - (size - 1)) == 1:
                pos = [x, y - (size - 1)]
                print 'found position: ' + str(pos)
                print 'answer: ' + str(pos[0] * 10000 + pos[1])
                return pos
def timer():
    main(100)
print(timeit.timeit(timer, number=1))