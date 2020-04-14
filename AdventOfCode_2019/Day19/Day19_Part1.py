import sys, os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/Day09/'))

import Day09_Computer as COMPUTER
program = COMPUTER.getprogram('Day19/Day19_Input.txt')

def main():
    #positions = [x[i] for x in itertools.permutations(range(0,50), 2) for i in range(0, 2)]
    def getrow(y, offset):
        for x in range(offset + 1, 50):
            if COMPUTER.start(program[:], [x,y])[0] == 0:
                return complex(offset, x - offset)
    rows = []
    offset = 0
    for y in range(0, 50):
        for x in range(offset, 50):
            if COMPUTER.start(program[:], [x,y])[0] == 1:
                offset = x
                rows.append(getrow(y, offset))
                break
        else:
            rows.append(complex(0,0))
    
    text = ''
    count = 0
    for r in rows:
        text += int(r.real)*' ' + int(r.imag)*u'\u2588' + int(50 - r.real - r.imag)*' ' + '\n'
        count += r.imag
    print text
    print "affected points: " + str(int(count))
    return count

main()