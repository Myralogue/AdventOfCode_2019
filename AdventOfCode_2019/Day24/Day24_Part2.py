filepath = 'Day24/Day24_Input.txt'
width = 5
height = 5

state = []
defaultlist = [''] * height

def getpixel(l, y, x):
    if (-1 < y < height) and (-1 < x < width):
        return state[l][y][x]
    else:
        if l == 0:
            return '.'
        if y == -1:
            return state[l - 1][1][2]
        elif y == height:
            return state[l - 1][3][2]
        elif x == -1:
            return state[l - 1][2][1]
        elif x == width:
            return state[l - 1][2][3]

def getadjacent(l, y, x):
    adjacent = []
    if y == 3 and x == 2: #go into next (above)
        if l < len(state) - 1:
            adjacent.extend(list(state[l + 1][-1]))
        else:
            adjacent.extend(['.'] * width)
    else:
        adjacent.extend(getpixel(l, y - 1, x))

    if y == 1 and x == 2: #go into next (below)
        if l < len(state) - 1:
            adjacent.extend(list(state[l + 1][0]))
        else:
            adjacent.extend(['.'] * width)
    else:
        adjacent.extend(getpixel(l, y + 1, x))

    if y == 2 and x == 3: #go into next (left)
        if l < len(state) - 1:
            adjacent.extend([item[-1] for item in state[l + 1]])
        else:
            adjacent.extend(['.'] * height)
    else:
        adjacent.extend(getpixel(l, y, x - 1))

    if y == 2 and x == 1: #go into next (right)
        if l < len(state) - 1:
            adjacent.extend([item[0] for item in state[l + 1]])
        else:
            adjacent.extend(['.'] * height)
    else:
        adjacent.extend(getpixel(l, y, x + 1))

    return adjacent

def main(minutes):
    global state
    minlayer = 0
    with open(filepath) as file:   
        initiallayer = []       
        for line in file.read().split('\n'):
            initiallayer.append(line)
        state.append(initiallayer)

        text = 'initial state: \n'
        for y in range(height):
            for l in range(len(state)):
                text += state[l][y] + "  "
            text += '\n'
        print text

    for minute in range(1, minutes + 1):
        #find new state
        newstate = [defaultlist[:] for _ in range(len(state))]
        for l in range(len(state)):
            for y in range(height):
                for x in range(width):
                    if state[l][y][x] == '?':
                        newstate[l][y] += '?'
                    elif state[l][y][x] == '#':
                        newstate[l][y] += '#' if getadjacent(l, y, x).count('#') == 1 else '.'
                    else:
                        newstate[l][y] += '#' if 1 <= getadjacent(l, y, x).count('#') <= 2 else '.'

        #add first and last if needed
        firstlayer = []
        firstlayer.append('#' if 1 <= state[0][0].count('#') <= 2 else '.')
        firstlayer.append('#' if 1 <= state[0][-1].count('#') <= 2 else '.')
        firstlayer.append('#' if 1 <= [item[-1] for item in state[0]].count('#') <= 2 else '.')
        firstlayer.append('#' if 1 <= [item[0] for item in state[0]].count('#') <= 2 else '.')
        if firstlayer.count('#') > 0:
            newlayer = ['.....', '..' + firstlayer[0] + '..', '.' + firstlayer[3] + '?' + firstlayer[2] + '.', '..' + firstlayer[1] + '..', '.....']                
            newstate.insert(0, newlayer)
            minlayer -= 1

        lastlayer = [getpixel(-1, 1, 2), getpixel(-1, 3, 2), getpixel(-1, 2, 3), getpixel(-1, 2, 1)]
        if lastlayer.count('#') > 0:
            newlayer = [('#' if lastlayer[3] == '#' or lastlayer[0] == '#' else '.') + lastlayer[0] * 3 + ('#' if lastlayer[2] == '#' or lastlayer[0] == '#' else '.'),\
                lastlayer[3] + '...' + lastlayer[2],\
                lastlayer[3] + '.?.' + lastlayer[2],\
                lastlayer[3] + '...' + lastlayer[2],\
                ('#' if lastlayer[3] == '#' or lastlayer[1] == '#' else '.') + lastlayer[1] * 3 + ('#' if lastlayer[2] == '#' or lastlayer[1] == '#' else '.')]    
            newstate.append(newlayer)  
                 
        state = newstate
        
        #print all layers
        def doprint():
            text = 'minute: ' + str(minute) + ': ' + str(len(state)) + ' layers\n' 
            for i in range(len(state) / 10 + 1):
                for y in range(height):
                    for l in range(min(10, len(state) - i * 10)):
                        text += state[l + (i * 10)][y] + "  "
                    text += '\n'
                text += 'layers: ' + str(minlayer + i * 10) + ' to ' + str(minlayer + i * 10 + 9) + '\n'
                print text
        doprint()

    print "number of insects after " + str(minutes) + " minutes: " + str(str(state).count("#"))


main(200)