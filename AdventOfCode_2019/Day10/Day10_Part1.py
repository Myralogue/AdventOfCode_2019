import fractions, math

filepath = 'Day10/Day10_Input.txt'

class vector2():
     def __init__(self, x, y):
         self.x = x
         self.y = y

     def __div__(self, other):
        x = self.x / other if self.x != 0 else 0
        y = self.y / other if self.y != 0 else 0
        return vector2(x, y)

     def __mul__(self, other):
        return vector2(self.x * other, self.y * other)

     def __add__(self, other):
        return vector2(self.x + other.x, self.y + other.y)

     def __eq__(self, other):
         return self.x == other.x and self.y == other.y

     def __repr__(self):
        return str([self.x, self.y])

     def relative(source, target):
        return vector2(target.x - source.x, target.y - source.y)

     def normalize(source):
        length = math.sqrt(source.x**2 + source.y**2)
        return source / length

     def insquare(vector, min, max):
         return (min.x <= vector.x <= max.x) and (min.y <= vector.y <= max.y)

astroids = []
astroidfield = []
bestlocation = vector2(0,0)

def main():
    global astroids
    global astroidfield
    global bestlocation

    with open(filepath) as fp:
        y = 0
        for line in fp:
            line = line.strip()
            astroidfield.append([])
            for x in range (0, len(line)):
                if x == 19 and y == 11:
                    pass
                if line[x] == "#":
                    astroids.append(vector2(x,y))
                    astroidfield[y].append(1)
                else:
                    astroidfield[y].append(0)
            y += 1

        bestcount = 0
        for astroid in astroids:
            count = loscheck(astroid)
            if count > bestcount:
                bestcount = count
                bestlocation = astroid
        print ("the best location is {} and can see: {} astroids".format(bestlocation, bestcount))
        return bestcount

def loscheck(astroid):
    visible = 0
    for other in astroids:
        if astroid == other:
            continue

        relative = vector2.relative(astroid, other)
        if relative.x == 0:
            count = abs(relative.y)
            step = vector2(0, relative.y / count)
        elif relative.y == 0:
            count = abs(relative.x)
            step = vector2(relative.x / count, 0)
        else:
            count = fractions.gcd(abs(relative.x), abs(relative.y))
            step = relative / count                

                
        if count != 1:
            cansee = True
            for c in range (1, count):
                checkpos = astroid + (step * c)
                if astroidfield[checkpos.y][checkpos.x] != 0:
                    cansee = False
                    break
            if cansee == True:
                visible += 1
        else:
            visible += 1
    return visible

def getbestlocation():
    if bestlocation == vector2(0,0):
        main()
    return bestlocation

def getastroidfield():
    if astroidfield == []:
        main()
    return astroidfield

def getastroids():
    if astroids == []:
        main()
    return astroids
    
if __name__ == '__main__':
    main()