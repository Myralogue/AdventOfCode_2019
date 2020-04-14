filepath = 'Day24/Day24_Input.txt'
width = 5
height = 5

state = []
previousstates = []

def getbiodiversity():
    return sum([2**(y*5+x) for y in range(height) for x in range(width) if state[y][x] == '#'])

def getpixel(y, x):
    if (-1 < y < height) and (-1 < x < width):
        return state[y][x]
    else:
        return ' '

def getadjacent(y, x):
    return [getpixel(y - 1, x), getpixel(y + 1, x), getpixel(y, x - 1), getpixel(y, x + 1)]

def main():
    global state
    with open(filepath) as file:          
        for line in file.read().split('\n'):
            state.append(line)

        while True:         
            biodiversisty = getbiodiversity()

            #print
            for l in state:
                print l
            print str(biodiversisty) + '\n'

            #check previous states
            if biodiversisty in previousstates:
                print "found repeated state: " + str(biodiversisty)
                return biodiversisty
            else:
                previousstates.append(biodiversisty)

            #find new state
            newstate = [''] * height
            for y in range(height):
             for x in range(width):
                if state[y][x] == '#':
                    newstate[y] += '#' if getadjacent(y, x).count('#') == 1 else '.'
                else:
                    newstate[y] += '#' if 1 <= getadjacent(y, x).count('#') <= 2 else '.'

            state = newstate

main()
