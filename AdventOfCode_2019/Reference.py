import matplotlib.pyplot as plt

	
Mercury =	3.301*10**23
Venus   =   4.867*10**24
Earth   =   5.972*10**24
Mars	=   6.417*10**23
#Jupiter	=   1.899*10**27 
Saturn	=   5.685*10**26
Uranus	=   8.682*10**25
Neptune	=   1.024*10**26

scale = Earth


def createplanets(planets, scale, colors):
    offset = 0
    circles = []
    for p in planets:
        size = p / scale
        print size
        try: c = colors[planets.index(p)]
        except: pass
        circles.append(plt.Circle((size + offset, size), size, color=c))
        offset += size
    return circles

circles = createplanets([Mercury, Venus, Earth, Mars, Saturn, Uranus, Neptune], Earth * 95, ['b', 'r'])


fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
# (or if you have an existing figure)
# fig = plt.gcf()
# ax = fig.gca()

for c in circles:
    ax.add_artist(c)


fig.savefig('plotcircles.png')

with open('Day06/Day06_Output.txt', 'w') as f:
    pass
    #json.dump(map, f, indent=1)

def buildmap(idx):
    global planets
    global connections
    
    myconnections = connections[idx]

    mymap = {}
    for c in connections[idx]:
        edge = pydot.Edge(planets[idx], c)
        graph.add_edge(edge)
        try:
            mymap[c] = buildmap(planets.index(c))
        except:
            mymap[c] = {}
    return mymap

import threading
import Queue

def drive(speed_queue):
    speed = 1
    while True:
        try:
            speed = speed_queue.get()
            if speed == 0:
                break
        except Queue.Empty:
            pass
        print("speed:", speed)

def main():
    speed_queue = Queue.Queue()
    threading.Thread(target=drive, args=(speed_queue,)).start()
    while True:
        speed = int(input("Enter 0 to Exit or 1/2/3 to continue: "))
        speed_queue.put(speed)
        if speed == 0:
            break

#main()