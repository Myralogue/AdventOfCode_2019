import timeit
import itertools

filepath = 'Day18/Day18_Input.txt'

field = []
intersections = {}
keys = {}

def main():
    global field    

    with open(filepath) as fp:
        for line in fp:
            line = line.strip()
            
            if line.count("@") > 0:
                sp = [len(field), line.index("@")]
            field.append(list(line))

    sp = [len(field) / 2, len(field[0]) / 2]
    #replace center
    field[sp[0]][sp[1]] = '#'
    field[sp[0] - 1][sp[1]] = '#'
    field[sp[0] + 1][sp[1]] = '#'
    field[sp[0]][sp[1] - 1] = '#'
    field[sp[0]][sp[1] + 1] = '#'
    field[sp[0] - 1][sp[1] - 1] = '1'
    field[sp[0] + 1][sp[1] - 1] = '2'
    field[sp[0] - 1][sp[1] + 1] = '3'
    field[sp[0] + 1][sp[1] + 1] = '4'

    field1 = indexfield([sp[0] - 1, sp[1] - 1], '1')
    findalldistances(field1)
    field2 = indexfield([sp[0] + 1, sp[1] - 1], '2')
    findalldistances(field2)
    field3 = indexfield([sp[0] - 1, sp[1] + 1], '3')
    findalldistances(field3)
    field4 = indexfield([sp[0] + 1, sp[1] + 1], '4')
    findalldistances(field4)

    keys.update(field1)
    keys.update(field2)
    keys.update(field3)
    keys.update(field4)

    allkeys = ''
    for k in keys.keys():
        allkeys += k
    fastest = findfastestroute({'1', '2', '3', '4'}, set(allkeys) - {'1', '2', '3', '4'})
    print "fastest route length: " + str(fastest)

cache = {}
def findfastestroute(positions, remaining):
    if len(remaining) == 0:
        return 0

    key = ''.join(sorted(positions)) + ''.join(sorted(remaining))
    if key in cache:
            return cache[key]

    shortest = 9999999
    for k in remaining:
        for p in positions:
            if k in keys[p][5]:
                dist = keys[p][5][k]
                if dist < shortest:
                    if keys[k][3].isdisjoint(remaining):
                        dist += findfastestroute((positions - {p}) | {k}, remaining - {k})
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

def findalldistances(mykeys):
    for i,first in enumerate(mykeys.keys()):
        firstkey = mykeys[first]
        distances = {}
        for second in mykeys.keys():
            if first == second:
                continue

            dist = firstkey[2] + mykeys[second][2] - findsplitdist(firstkey[4], mykeys[second][4]) * 2
            distances[second] = dist
        mykeys[first].append(distances)

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

def indexfield(startpos, name):
    keys = {}
    behinddoor = []
    interesting = []
    positions = [[startpos[0], startpos[1], 0, set(), [complex(0, 0)]]] #y, x, dist, behind, path, distances
    keys[name] = positions[0]
    maxid = 1

    while len(positions) > 0:
        p = positions[0]
        value = field[p[0]][p[1]]
        field[p[0]][p[1]] = '~'

        if value.isalpha():
            if value.isupper():
                p[3].add(value.lower())
                pass
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
    return keys

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