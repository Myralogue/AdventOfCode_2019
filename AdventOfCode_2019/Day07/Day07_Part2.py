import itertools

import Queue
from threading import Thread

import Day07_Computer as COMPUTER

program = COMPUTER.getprogram('Day07/Day07_Input.txt')

def main(phasesettings):
    combinations = list(itertools.permutations(phasesettings, len(phasesettings)))
    maxvalue = 0
    bestcombination = []
    for c in combinations:
        value = 0
        qlist = [Queue.Queue()]
        for i in range(1, len(c)):
            nq = Queue.Queue()
            t = Thread(target=COMPUTER.main, args=(program, [c[i - 1], value], qlist[i - 1], nq))
            qlist.append(nq)
            t.start()

            value = qlist[i].get() #Wait for value
        
        rq = Queue.Queue()
        t = Thread(target=COMPUTER.main, args=(program, [c[-1], value], qlist[-1], qlist[0], rq))
        t.start()  
        
        value = rq.get()
        if value > maxvalue:
            maxvalue = value
            bestcombination = c

        print ("Return {} from combination: {}".format(value, c))
    
    print ("Max value {} found in combination {}".format(maxvalue, bestcombination))
    return maxvalue

if __name__ == '__main__':
    main('56789')