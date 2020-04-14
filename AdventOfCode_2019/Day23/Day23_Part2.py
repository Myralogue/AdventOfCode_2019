import sys, os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/Day09/'))

import Queue
from threading import Thread

import Day09_Computer as COMPUTER
program = COMPUTER.getprogram('Day23/Day23_Input.txt')

machines = []
class machine():
    def __init__(self, id, outqueue):
        self.id = id
        self.inqueue = Queue.Queue()
        self.thread = Thread(target=COMPUTER.start, args=(program[:], [id], self.inqueue, outqueue, Queue.Empty, 0, 3, 1))
        self.thread.start()

def main(count):
    NATpacketmemory = [0,0]
    lastNAT = -1
    outqueue = Queue.Queue()
    for i in range(count):
        machines.append(machine(i, outqueue))
    
    while True:
        try:
            output = outqueue.get(timeout=10) #TODO: Find better method of detecting idle
            if output[0] < count:
                machines[output[0]].inqueue.put(output[1:])
                print output
            elif output[0] == 255:
                NATpacketmemory = output[1:]
                print "setting new NAT packet memory: "  + str(NATpacketmemory)
        except:
            if NATpacketmemory[1] == lastNAT:
                print "NAT y is same as last NAT y: " + str(lastNAT)
                return lastNAT
            else:
                print 'network is idle, inputting NAT packet: ' + str(NATpacketmemory)
                machines[0].inqueue.put(NATpacketmemory)
                lastNAT = NATpacketmemory[1]


main(50)