import numpy as np
import itertools
import fractions

filepath = 'Day12/Day12_Input.txt'

class planet():
    def __init__(self, name = "", position = [0,0,0]):
        self.pos = vec(position)
        self.vel = vec()
        self.name = name

    def __repr__(self):
        return "<{}: pos: {}, vel: {}>".format(self.name, self.pos, self.vel)

class vec():
    def __init__(self, value = [0,0,0]):
        self.x = value[0]
        self.y = value[1]
        self.z = value[2]
    def __add__(self, other):
        return vec([self.x + other.x, self.y + other.y, self.z + other.z])
    def __eq__(self, other):
         return [self.x, self.y, self.z] == [other.x, other.y, other.z]
    def __repr__(self):
        return str([self.x, self.y, self.z])
    def get(self, idx = -1):
        if idx == -1:
            return([self.x, self.y, self.z])
        else:
            return self.get()[idx]
    def getenergy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)
    def asarray(self):
        return([self.x, self.y, self.z])

def main(steps):
    planets = []
    planetnames = ["Io", "Europa", "Ganymede", "Callisto"]
    with open(filepath) as fp:
        for line in fp:
            line = line.strip()
            x = line[3:line.find(",")]
            line = line[5 + len(x):]
            y = line[2:line.find(",")]
            line = line[6 + len(y):]
            z = line[:-1]

            planets.append(planet(planetnames[0], [int(x), int(y), int(z)]))
            del planetnames[0]

    return findduration(planets)

def findduration(planets):
    startenergy = 0
    planetcount = len(planets)
    numbers = []

    for i in range(0, 3):
        singledimension = []
        for p in planets:
            singledimension.append([p.pos.get(i), 0])

        startstate = str(singledimension) 
        pairs = list(itertools.combinations(singledimension, 2))

        count = 0
        while True:
            energy = move(pairs, singledimension, planetcount)
            count += 1
            if energy == startenergy:
                numbers.append(count)
                print "dimension: "+ str(i) + ": " + str(count)
                break

    answer = numbers[0]
    for i in range (1, len(numbers)):
        gcd = fractions.gcd(answer, numbers[i])
        answer = answer / gcd * numbers[i]
    answer *= 2
    print "total steps: " + str(answer)
    return answer

def move(pairs, singledimension, planetcount):
    for p in pairs:
        if p[0][0] > p[1][0]:
            p[0][1] -= 1
            p[1][1] += 1
        elif p[0][0] < p[1][0]:
            p[0][1] += 1
            p[1][1] -= 1
    
    energy = 0
    for i in range(0, planetcount):
        singledimension[i][0] += singledimension[i][1]
        energy += abs(singledimension[i][1])

    return energy

if __name__ == '__main__':
    main(1000)