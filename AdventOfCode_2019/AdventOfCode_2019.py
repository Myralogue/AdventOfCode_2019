import sys, os

# Stop printing
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Start printing
def enablePrint():
    sys.stdout = sys.__stdout__

sys.path.append(sys.path[0]+'\\Day01')
sys.path.append(sys.path[0]+'\\Day02')
sys.path.append(sys.path[0]+'\\Day03')
sys.path.append(sys.path[0]+'\\Day04')
sys.path.append(sys.path[0]+'\\Day05')
sys.path.append(sys.path[0]+'\\Day06')
sys.path.append(sys.path[0]+'\\Day07')
sys.path.append(sys.path[0]+'\\Day08')
sys.path.append(sys.path[0]+'\\Day09')

from Day01_Part1 import main as d1p1
from Day01_Part2 import main as d1p2
from Day02_Part1 import main as d2p1
from Day02_Part2 import main as d2p2
from Day03_Part1 import main as d3p1
from Day03_Part2 import main as d3p2
from Day04_Part1 import main as d4p1
from Day04_Part2 import main as d4p2
from Day05_Part1 import main as d5p1
from Day05_Part2 import main as d5p2
from Day06_Part1 import main as d6p1
from Day06_Part2 import main as d6p2
from Day07_Part1 import main as d7p1
from Day07_Part2 import main as d7p2
from Day08_Part1 import main as d8p1
from Day08_Part2 import main as d8p2
from Day09_Part1 import main as d9p1
from Day09_Part2 import main as d9p2

print ("for correct answers these inputs are required: 1, 5")
#print all results
blockPrint()
printstr = "Answers: d1p1={}, d1p2={}, d2p1={}, d2p2={}, d3p1={}, d3p2={}, d4p1={}, d4p2={}, d5p1={}, d5p2={}, d6p1={}, d6p2={}, d7p1={}, d7p2={}, d8p1={}, d8p2=see image, d9p1={}, d9p2={}".format(d1p1(), d1p2(), d2p1(12, 2), d2p2(19690720), d3p1(), d3p2(), d4p1(206938, 679128), d4p2(206938, 679128), d5p1(), d5p2(), d6p1(False), d6p2('YOU', 'SAN', False), d7p1('01234'), d7p2('56789'), d8p1(25, 6), d9p1(), d9p2())

#render images
d8p2(25, 6)
enablePrint()

print(printstr)