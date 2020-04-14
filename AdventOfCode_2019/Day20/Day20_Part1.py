import re

filepath = 'Day20/Day20_Input.txt'

def main():
    portals = {}
    image = []

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
    
    dist = pathfind(image[:], dict(portals), 'AA', 'ZZ')
    print "distance to exit: " + str(dist)

disttogoal = 0
def pathfind(maze, portals, startkey, endkey):
    positions = [getpos(portals[startkey])]
    del portals[startkey]
    dist = 0

    def handlemove(pixel, pos):
        global disttogoal
        if pixel == '.':
            positions.append(pos)
        elif pixel.isalpha():
            try:
                key = portals.keys()[portals.values().index(complex(x, y))]
                if key == endkey:
                    disttogoal = dist
                key = key.upper() if key.islower() else key.lower()
                pos = getpos(portals[key])
                positions.append(pos)
                del portals[key.upper()]
                del portals[key.lower()]
            except:
                return
    
    while disttogoal == 0:
        if dist % 10 == 0: #draw progress
            drawmaze(maze)
        for x,y in positions[:]:
            maze[y][x] = str(dist % 10)
            pixel = getpixel(maze, x, y - 1)
            if pixel != "#": #up
                handlemove(pixel, (x, y - 1))
            pixel = getpixel(maze, x, y + 1)
            if pixel != "#": #down
                handlemove(pixel, (x, y + 1))
            pixel = getpixel(maze, x - 1, y)
            if pixel != '#': #left
                handlemove(pixel, (x - 1, y))
            pixel = getpixel(maze, x + 1, y)
            if pixel != '#': #right
                handlemove(pixel, (x + 1, y))
            del positions[0]
        dist += 1
    return disttogoal

def getpos(portal):
    return (int(portal.real), int(portal.imag))

def getpixel(image, x, y):
    try:
        return image[y][x]
    except:
        return ' '

def drawmaze(maze):
    text = ''
    for line in maze:
        for c in line:
            text += c
        text += '\n'
    print text

main()