import re
import itertools
import timeit

filepath = 'Day20/Day20_Input.txt'

image = []
connections = {}
def main():
    portals = {}
    connectdistances = {}

    def getname(portal):
        return portal.lower() if portal in portals else portal

    with open(filepath) as fp:
        for line in fp:
            image.append(list(line.replace('\n', '')))
            for match in re.finditer(r'\w+', line):
                portal = line[match.start():match.end()]
                if len(portal) == 1:
                    pixel = getpixel(image, match.start(), -2)
                    if pixel.isalpha():
                        portal = pixel + portal
                        y = len(image) - 3 if getpixel(image, match.start(), -3) == '.' else len(image)
                        portals[getname(portal)] = complex(match.start(), y)
                else:
                    x = match.start() - 1 if line[match.start() - 1] == '.' else match.end()
                    portals[getname(portal)] = complex(x, len(image) - 1)

    pathfind(getimagecopy(), dict(portals), 'AA')
    finddistancetoexit('AA', 'ZZ')

def pathfind(maze, portals, startkey, startchild = True):
    positions = [getpos(portals[startkey])]
    dist = 0
    localconnections = {}

    def handlemove(pixel, pos):
        if pixel == '.':
            positions.append(pos)
        elif pixel.isalpha():
            try:
                key = portals.keys()[portals.values().index(complex(x, y))]
                if key == startkey: return
                localconnections[key] = dist
            except:
                return
    
    while positions != []:
        if dist % 100 == 0: #draw progress
            pass
            #drawmaze(maze)

        for _ in range(0, len(positions)):
            x,y = positions[0]
            maze[y][x] = str(dist % 10)

            nearby = getnearbypixels(maze, x, y)            
            if nearby[0] != "#": #up
                handlemove(nearby[0], (x, y - 1))
            if nearby[1] != "#": #down
                handlemove(nearby[1], (x, y + 1))
            if nearby[2] != '#': #left
                handlemove(nearby[2], (x - 1, y))
            if nearby[3] != '#': #right
                handlemove(nearby[3], (x + 1, y))
            del positions[0]
        dist += 1
    if len(localconnections) > 0:
        connections[startkey] = [getisinner(portals[startkey]), localconnections]
        if startchild:
            if len(localconnections) == 1:
                if startkey == 'ie':
                    pass
                connections[localconnections.keys()[0]] = [getisinner(portals[localconnections.keys()[0]]), {startkey: localconnections.values()[0]}]
            else:
                for c in localconnections:
                    pathfind(getimagecopy(), portals, c, False)

            for c in localconnections:
                if c != 'ZZ': pathfind(maze, portals, getpartner(c))

def getpartner(portal):
    return portal.upper() if portal.islower() else portal.lower()

def getpos(portal):
    return (int(portal.real), int(portal.imag))

def getpixel(image, x, y):
    try:
        return image[y][x]
    except:
        return ' '

def getnearbypixels(image, x, y):
    return getpixel(image, x, y - 1), getpixel(image, x, y + 1), getpixel(image, x - 1, y), getpixel(image, x + 1, y)

def getimagecopy():
    return [x[:] for x in image]

def drawmaze(maze):
    text = ''
    for line in maze:
        for c in line:
            text += c
        text += '\n'
    print text

def getisinner(pos):
    return (5 < pos.real < len(image[0]) - 5) and (5 < pos.imag < len(image) - 5)

route = []
def finddistancetoexit(startkey, endkey):
    positions = [[0, 0, startkey, startkey + "(0), "]] # dist, depth, key, routestring
    cache = {}
    while positions != []:
        positions.sort()
        pos = positions[0]
        cachestring = str(pos[1]) + pos[2]
        if cachestring not in cache: 
            cache[cachestring] = pos[0]
            portal = connections[pos[2]]
            for c in portal[1]:
                if c == startkey: continue
                newdepth = pos[1] + (1 if connections[c][0] else -1)
                if newdepth >= 0:
                    if c != endkey:
                        positions.append([pos[0] + portal[1][c] + 1, newdepth, getpartner(c), pos[3] + c + "(" + str(newdepth) + "), "])
                elif pos[1] == 0 and c == endkey:
                    print "route: " + pos[3] + "ZZ"
                    totalsteps = pos[0] + portal[1][c]
                    print 'Total steps:' + str(totalsteps)
                    return totalsteps
        del positions[0]
        
print timeit.timeit(main, number=1)
#main()