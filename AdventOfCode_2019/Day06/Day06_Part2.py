import pydot
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

from collections import defaultdict

filepath = 'Day06/Day06_Input.txt'

planets = []
connections = []
pfrom = ""
phtowards = ""

graph = pydot.Dot(graph_type='graph')

def main(pathfrom, pathtowards, rendergraphics):
    global planets
    global connections

    planets = []
    connections = []

    input = []
    with open(filepath) as fp:
        for line in fp:
            lastline = line.strip()
            input.append(lastline.split(")"))
    
    #Build look up table
    for i in range(0, len(input)):
        try:
            index = planets.index(input[i][0])
            connections[index].extend([input[i][1]])
        except:
            planets.append(input[i][0])
            connections.append([input[i][1]])

    mypath = findpathbetween(pathfrom, pathtowards)

    print ("Your route: " + str(mypath) + '\n')
    print ("Required orbital transfers: " + str(len(mypath) - 3))

    if (rendergraphics):
        #Graphics
        print ("Rendering graphics map...")
        map = {}
        map['COM'] = buildmap(planets.index('COM'), mypath)
        graph.write_png('Day06/Day06_Part2_Map.png')
        print ("Wrote map to: 'Day06/Day06_Part2_Map.png'")

    return len(mypath) - 3

def countorbits(idx, depth):
    myconnections = connections[idx]
    returndepth = depth
    
    for c in connections[idx]:
        try:
            returndepth += countorbits(planets.index(c), depth + 1)
        except:
            returndepth += depth + 1

    return returndepth

foundpath = []
def findpathbetween(pathfrom, pathtowards):
    global foundpath
    global pfrom
    global ptowards

    foundpath = []
    pfrom = pathfrom
    ptowards = pathtowards

    pathfinding(planets.index('COM'))

    if foundpath[0] != pathfrom:
        foundpath = foundpath[::-1]
    return foundpath

def pathfinding(idx):
    global foundpath

    myconnections = connections[idx]
    path = []

    for c in connections[idx]:
        if c == pfrom or c == ptowards:
            return [c]
        else:
            try:
                point = pathfinding(planets.index(c))
                if (point != []):
                    if path != []:
                        path.append(planets[idx])
                        path.append(c)
                        path.extend(point[::-1])
                        foundpath = path
                        break
                    else:
                        path = point
                        path.append(c)
            except:
                continue

    if foundpath == []:
        return path

def buildmap(idx, path):
    myconnections = connections[idx]

    for c in connections[idx]:
        try:
            pointinpath = path.index(planets[idx])
            if path[pointinpath - 1 : pointinpath + 2].count(c):
                edge = pydot.Edge(planets[idx], c, color='red', penwidth=5)
            else:
                edge = pydot.Edge(planets[idx], c)
        except:
            edge = pydot.Edge(planets[idx], c)

        graph.add_edge(edge)
        try:
            buildmap(planets.index(c), path)
        except:
            pass

if __name__ == '__main__':
    main('YOU', 'SAN', True)