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
    outqueue = Queue.Queue()
    for i in range(count):
        machines.append(machine(i, outqueue))
    
    while True:
        output = outqueue.get()
        if output[0] < count:
            machines[output[0]].inqueue.put(output[1:])
            print output
        else:
            print output
            return

main(50)