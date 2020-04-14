import pydot
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

from collections import defaultdict

filepath = 'Day06/Day06_Input.txt'

planets = []
connections = []

graph = pydot.Dot(graph_type='graph')

def main(rendergraphics):
    global planets
    global connections

    input = []
    with open(filepath) as fp:
        for line in fp:
            lastline = line.strip()
            input.append(lastline.split(")"))
    
    for i in range(0, len(input)):
        try:
            index = planets.index(input[i][0])
            connections[index].extend([input[i][1]])
        except:
            planets.append(input[i][0])
            connections.append([input[i][1]])

    orbitcount = countorbits(planets.index('COM'), 0)
    print ("Orbit Count Checksum: " + str(orbitcount))

    if (rendergraphics):
        #Graphics
        print ("Rendering graphics map...")
        map = {}
        map['COM'] = buildmap(planets.index('COM'))
        graph.write_png('Day06/Day06_Part1_Map.png')
        print ("Wrote map to: 'Day06/Day01_Part1_Map.png'")

    return orbitcount

def countorbits(idx, depth): 
    myconnections = connections[idx]
    returndepth = depth
    
    for c in connections[idx]:
        try:
            returndepth += countorbits(planets.index(c), depth + 1)
        except:
            returndepth += depth + 1

    return returndepth

def buildmap(idx):
    myconnections = connections[idx]

    mymap = {}
    for c in connections[idx]:
        edge = pydot.Edge(planets[idx], c)
        graph.add_edge(edge)
        try:
            mymap[c] = buildmap(planets.index(c))
        except:
            mymap[c] = {}
    return mymap

if __name__ == '__main__':
    main(True)  