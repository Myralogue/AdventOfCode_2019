#import os
#print (os.getcwd())

import math

filepath = 'Day01/Day01_Input.txt'
def main():
    with open(filepath) as fp:
       line = fp.readline()
       cnt = 1

       totalFuel = 0
       while line:

           mass = float (line.strip())
           fuel = math.floor(mass/3) - 2
           totalFuel += fuel;
           print("launch {}: mass={} fuel={}".format(cnt, int (mass), int (fuel)))
           line = fp.readline()
           cnt += 1

       print("total fuel needed: {}".format(int (totalFuel)))
    return int (totalFuel)

if __name__ == '__main__':
    main()