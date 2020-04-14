import timeit
import itertools

filepath = 'Day18/Day18_Input.txt'

field = []
keys = {}
intersections = {}
startpos = []

def main():
    global field
    global startpos

    with open(filepath) as fp:
        for line in fp:
            line = line.strip()
            
            if line.count("@") > 0:
                startpos = [len(field), line.index("@")]
            field.append(list(line))

    #drawfield()
    indexfield(startpos)
    findalldistances()

    allkeys = ''
    for k in keys.keys():
        allkeys += k
    dist = findfastestroute('@', set(allkeys) - {'@'})
    print dist
    print len(cache)

cache = {}
def findfastestroute(current, remaining):
    if len(remaining) == 0:
        return 0

    key = current + ''.join(remaining)
    if key in cache:
            return cache[key]

    shortest = 9999999
    currentkey = keys[current]
    for k in remaining:
        dist = keys[current][5][k]
        if dist < shortest:
            if keys[k][3].isdisjoint(remaining):
                dist += findfastestroute(k, remaining - {k})
                if shortest > dist:
                    shortest = dist

    cache[key] = shortest
    return shortest

def findsplitdist(listA, listB):
    for i in range(1, min(len(listA), len(listB))):
        if listA[i].real != listB[i].real:
            return int(listA[i - 1].imag)
    else:
        if listA == [] or listB == []:
            return 0
        if len(listA) < len(listB):
            return int(listA[-1].imag)
        else:
            return int(listB[-1].imag)

def findalldistances():
    for i,first in enumerate(keys.keys()):
        firstkey = keys[first]
        distances = {}
        for second in keys.keys():
            if first == second:
                continue

            splitdist = findsplitdist(firstkey[4], keys[second][4])

            #silly hack but I want this to be over with
            if splitdist == 0:
                if firstkey[1] > startpos[1] and keys[second][1] > startpos[1]\
                   or firstkey[1] < startpos[1] and keys[second][1] < startpos[1]:
                    splitdist += 1
            dist = firstkey[2] + keys[second][2] - splitdist * 2
            distances[second] = dist
        keys[first].append(distances)

def drawfield():
    line = ''
    for l in field:
        for c in l:
            if type(c) == complex:
                line += str(int(c.real) % 10)
            elif type(c) == int:
                line += str(c % 10)
            elif c == '#':
                line += u'\u2588'
            else:
                line += c
        line += '\n'
    print line

def indexfield(startpos):
    global keys
    behinddoor = []
    interesting = []
    positions = [[startpos[0], startpos[1], 0, set(), [complex(0, 0)]]] #y, x, dist, behind, path
    keys['@'] = positions[0]
    maxid = 1

    while len(positions) > 0:
        p = positions[0]
        value = field[p[0]][p[1]]
        field[p[0]][p[1]] = '~'

        if value.isalpha():
            if value.isupper():
                p[3].add(value.lower())
            else:
                keys[value] = p[:]
                p[4].append(complex(maxid, p[2]))
                maxid += 1
        else:
            nearby = getnearbypixels([p[0], p[1]])
            count = 0
            for n in nearby:
                if n != '#':
                    count += 1
            if count > 2: #is 'interesting'
                p[4].append(complex(maxid, p[2]))
                maxid += 1

        if getpixel([p[0] - 1, p[1]]) != '#' and getpixel([p[0] - 1, p[1]]) != '~':
            positions.append([p[0] - 1, p[1], p[2] + 1, set(p[3]), p[4][:]])
        if getpixel([p[0] + 1, p[1]]) != '#' and getpixel([p[0] + 1, p[1]]) != '~':
            positions.append([p[0] + 1, p[1], p[2] + 1, set(p[3]), p[4][:]])
        if getpixel([p[0], p[1] - 1]) != '#' and getpixel([p[0], p[1] - 1]) != '~':
            positions.append([p[0], p[1] - 1, p[2] + 1, set(p[3]), p[4][:]])
        if getpixel([p[0], p[1] + 1]) != '#' and getpixel([p[0], p[1] + 1]) != '~':
            positions.append([p[0], p[1] + 1, p[2] + 1, set(p[3]), p[4][:]])

        del positions[0] 

def getpixel(pos):
    try:
        if pos[0] < 0 or pos[1] < 0:
            return '#'
        return field[pos[0]][pos[1]]
    except:
        return '#'

def getnearbypixels(pos):
    return getpixel([pos[0] - 1, pos[1]]), getpixel([pos[0] + 1, pos[1]])\
        , getpixel([pos[0], pos[1] - 1]), getpixel([pos[0], pos[1] + 1])

print (timeit.timeit(main, number=1))