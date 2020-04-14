import numpy as np
import itertools

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = plt.axes(projection='3d')
colors = ['red', 'green', 'blue', 'purple']
rendergraphics = True

filepath = 'Day12/Day12_Input.txt'

class planet():
    def __init__(self, position = [0,0,0], name = "", color = 'black'):
        self.pos = vec(position)
        self.vel = vec()
        self.prev = vec(position)
        self.name = name
        self.color = color

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
    def array(sel):
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

            planets.append(planet([int(x), int(y), int(z)], planetnames[0], colors[0]))
            del planetnames[0]
            del colors[0]

    timestep(planets, steps)

    energy = 0
    for p in planets:
        energy += p.pos.getenergy() * p.vel.getenergy()
    print "Total energy after {} steps: {}".format(steps, energy)

    if rendergraphics:
        plt.show()

    return energy

def timestep(planets, count):
    pairs = list(itertools.combinations(planets, 2))
    for i in range(0, count):
        applygravity(pairs)
        simulatestep(planets)

        if i % 20 == 0:
            print "step " + str(i) + ": " + str(planets)

        if rendergraphics:
            for p in planets:
                ax.plot3D([p.prev.x, p.pos.x,], [p.prev.y, p.pos.y,], [p.prev.z, p.pos.z,], p.color)
                p.prev = p.pos

def applygravity(pairs):
    for p in pairs:
        applygravitybetween(p[0], p[1])

def applygravitybetween(planet1, planet2):
    changep1 = [0,0,0]
    changep2 = [0,0,0]
    for i in range(0, 3):
        if planet1.pos.get(i) > planet2.pos.get(i):
            changep1[i] -= 1
            changep2[i] += 1
        elif planet1.pos.get(i) < planet2.pos.get(i):
            changep1[i] += 1
            changep2[i] -= 1
    planet1.vel += vec(changep1)
    planet2.vel += vec(changep2)

def simulatestep(planets):
    for p in planets:
        p.pos += p.vel

if __name__ == '__main__':
    main(1000)