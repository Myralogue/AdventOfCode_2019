from Day10_Part1 import vector2, getbestlocation, getastroidfield, getastroids
import math, fractions
import numpy as np

def main():
    stationlocation = getbestlocation()
    astroidfield = getastroidfield()
    astroids = getastroids()
    sortedastroids = []
    fieldsize = vector2(len(astroidfield[0]) - 1, len(astroidfield) - 1)

    removevectorfromlist(astroids, stationlocation) #remove station

    while len(astroids) > 0:
        relative = vector2.relative(stationlocation, astroids[0])
        normalrelative = vector2.normalize(relative)

        angle = -math.atan2(normalrelative.x, normalrelative.y)
        sortedastroids.append([angle])
        
        if relative.x == 0:
            step = vector2(0, relative.y / abs(relative.y))
        elif relative.y == 0:
            step = vector2(relative.x / abs(relative.x), 0)
        else:
            step = relative / fractions.gcd(abs(relative.x), abs(relative.y))      
            
        checkpos = stationlocation + step
        while vector2.insquare(checkpos, vector2(0,0), fieldsize):
            if astroidfield[checkpos.y][checkpos.x] != 0:
                sortedastroids[-1].append(checkpos)
                removevectorfromlist(astroids, checkpos)
            checkpos += step

    sortedastroids.sort(key=takeFirst)

    destroyed = 0
    i = 0
    while destroyed < 199:
        if len(sortedastroids[i]) > 2:
            del sortedastroids[i][1]
            i += 1
        else:
            del sortedastroids[i]

        if i >= len(sortedastroids):
            i = 0
        destroyed += 1

    nr200 = sortedastroids[i][1]
    answer = nr200.x * 100 + nr200.y
    print "The 200th destroyed astroid is: " +str(nr200) + "giving us answer: " + str(answer)
    return answer

def removevectorfromlist(list, vector):
    for i, o in enumerate(list):
        if o == vector:
            del list[i]
            break

def isvalidpos(pos):
    return (0 <= pos.x <= fieldsize.x) and (0 <= pos.y <= fieldsize.y)

def takeFirst(elem):
    return elem[0]

if __name__ == '__main__':
    main()