from Day02_Part1 import main as d2p1

def main(value):
    x = 0
    while (x < 100):
        y = 0
        while (y < 100):
            current = d2p1(x,y)
            if (current == value):
                print ("x={}, y={}, output={}".format(x,y,100 * x + y))
                return 100 * x + y
            y+= 1
        x+= 1

def alt(value, xmin, xmax, ymin, ymax):
    x = 0
    y = 0

    while (xmax - xmin > 1):
        current = d2p1(x,y)
        if (value > current):
            print("too little x")
            xmin = x
            x+= (xmax - x) / 2
        else:
            print("too much x")
            xmax = x
            x-= (x - xmin) / 2

    while (ymax - ymin > 1):
        current = d2p1(xmin,y)
        if (value == current):
            print("just enough y {} {}".format(xmin, y))
            return 100 * xmin + y
        elif (value > current):
            print("too little y")
            ymin = y
            y+= (ymax - y) / 2
        else:
            print("too much y")
            ymax = y
            y-= (y - ymin) / 2

if __name__ == '__main__':
    main(19690720)
    #alt(19690720, 0, 100, 0, 100)