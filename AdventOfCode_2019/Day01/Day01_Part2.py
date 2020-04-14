import math

filepath = 'Day01/Day01_Input.txt'
def main():
    with open(filepath) as fp:
       line = fp.readline()
       cnt = 1

       totalFuel = 0
       while line:
           fuel = float (line.strip())
           launchfuel = 0.0

           while (fuel > 0.0):
            fuel = max(0, math.floor(fuel/3) - 2)
            launchfuel += fuel

           totalFuel += launchfuel;
           print("launch {}: mass={} fuel={}".format(cnt, line.strip(), int (launchfuel)))
           line = fp.readline()
           cnt += 1

       print("total fuel needed: {}".format(int (totalFuel)))
    return int (totalFuel)

if __name__ == '__main__':
    main()