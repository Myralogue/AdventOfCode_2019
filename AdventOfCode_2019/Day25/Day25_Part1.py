import sys, os, itertools

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/Day09/'))

import Queue
from threading import Thread

import Day09_Computer as COMPUTER
program = COMPUTER.getprogram('Day25/Day25_Input.txt')

layout = {}
routetopressuresensitivefloor = []
banneditems = [] #['escape pod', 'giant electromagnet', 'photons', 'infinite loop', 'molten lava']
items = []
lastitem = ''
alive = True

def writetoscreen(output):
    text = ''
    for c in output:
        text += unichr(c)
    print text
    return text

def tounicodelist(string):
    unicodelist = []
    for c in string:
        unicodelist.append(ord(c))
    unicodelist.append(10)
    return unicodelist

def oposite(dir):
    if dir == 'north':
        return 'south'
    if dir == 'south':
        return 'north'
    if dir == 'west':
        return 'east'
    if dir == 'east':
        return 'west'

def explore(route, dir):
    global alive
    if not alive: return
    route.append(dir)
    inqueue.put(tounicodelist(dir))
    
    try:
        output = outqueue.get(timeout = 3)
        text = writetoscreen(output)
        startidx = text.index("==") + 3
        endidx = text[startidx:].index("==")
        room = str(text[startidx:endidx + startidx - 1])

        if room == "Pressure-Sensitive Floor":
            global routetopressuresensitivefloor
            routetopressuresensitivefloor = route

        textlist = text.strip().split('\n')
        if u'Items here:' in textlist:
            idx = textlist.index(u'Items here:') + 1
            text = textlist[idx]
            while text != u'':
                item = str(text[2:])
                idx += 1
                text = textlist[idx]
                if item not in items: items.append(item)
                if item in banneditems: continue
                global lastitem
                lastitem = item
                inqueue.put(tounicodelist("take " + item))
                output = outqueue.get(timeout = 3)
                if 'Command?' not in writetoscreen(output):
                    alive = False
                    banneditems.append(item)
                    return                

        for nextdir in textlist[4:8]:
            if not alive: return
            if nextdir == '- north' and route[-1] != 'south':
                explore(route[:], 'north')
            if nextdir == '- south' and route[-1] != 'north':
                explore(route[:], 'south')
            if nextdir == '- west' and route[-1] != 'east':
                explore(route[:], 'west')
            if nextdir == '- east' and route[-1] != 'west':
                explore(route[:], 'east')
    except:
       alive = False
       banneditems.append(lastitem)
       return

    inqueue.put(tounicodelist(oposite(dir)))
    output = outqueue.get()

inqueue = Queue.Queue()
outqueue = Queue.Queue()
def main():
    global inqueue
    global outqueue
    global alive

    alive = True
    inqueue = Queue.Queue()
    outqueue = Queue.Queue()
    returnqueue = Queue.Queue()
    t = Thread(target=COMPUTER.start, args=(program[:], [], inqueue, outqueue, returnqueue, 1))
    t.start()    

    output = outqueue.get()
    text = writetoscreen(output)

    startidx = text.index("==") + 3
    endidx = text[startidx:].index("==")
    room = str(text[startidx:endidx + startidx])
    layout[room] = {}

    textlist = text.strip().split('\n')
    for dir in textlist[4:8]:
        if not alive: break
        if dir == '- north':
            explore([], 'north')
        if dir == '- south':
            explore([], 'south')
        if dir == '- west':
            explore([], 'west')
        if dir == '- east':
            explore([], 'east')

    if alive:
        for s in routetopressuresensitivefloor[:-1]:
            inqueue.put(tounicodelist(s))
            output = outqueue.get()
            writetoscreen(output)

        myitems = [item for item in items if item not in banneditems]
        itemsininventory = myitems[:]
        print "Items with drone: " + str(myitems)

        for l in range(1, len(myitems)):
            combinations = list(itertools.combinations(myitems, l))
            for c in combinations:
                dropitems = list(set(itemsininventory) - set(c))
                takeitems = list(set(c) - set(itemsininventory))

                instruction = []
                for i in dropitems:
                    itemsininventory.remove(i)
                    instruction.extend(tounicodelist('drop ' + i))
                for i in takeitems:
                    itemsininventory.append(i)
                    instruction.extend(tounicodelist('take ' + i))

                inqueue.put(instruction)
                writetoscreen(outqueue.get())
                inqueue.put(tounicodelist(routetopressuresensitivefloor[-1]))
                result = writetoscreen( outqueue.get())
                if "Alert!" not in result:
                    number = int(result[result.index('typing') + 7:-36])
                    return number
    else:
        returnqueue.put(-1) #kill failed threads
        os.system('cls')
        print "try again, banned items: " + str(banneditems) 
        main()

main()