import re
import pydot, os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

graph = pydot.Dot(graph_type='graph')

filepath = 'Day14/Day14_Input.txt'
conversions = {}

def main():
    global conversions
    with open(filepath) as fp:
        for line in fp:
            line = line.strip()
            line = re.split(', | => | ', line)
            elements = []
            for i in range(0, len(line) - 2):
                if i % 2 == 0:
                    elements.append(int(line[i]))
                else:
                    elements.append(line[i])            
            conversions[line[-1]] = [[int(line[-2]), 0, 0] + elements, []]

    values = conversions.get('FUEL')
    for i in range(0, (len(values[0]) - 3) / 2):
        builddependencymap(values[0][i * 2 + 4], 'FUEL')

    orecount = calculate('FUEL', 1)
    print "required ore for 1 fuel: " + str(orecount)
    graph.write_png('Day14/Day14_Part1_Map.png')
    print ("Wrote map to: 'Day14/Day14_Part1_Map.png'")
    return orecount

def builddependencymap(element, parent):
        values = conversions.get(element)
        if values == None:
            return
        if values[1] == []:    
            values[1].append(parent)
            for i in range(0, (len(values[0]) - 3) / 2):
                builddependencymap(values[0][i * 2 + 4], element)
        elif values[1].count(parent) == 0:
            values[1].append(parent)

def calculate(element, required):
    values = conversions.get(element)
    if values == None:
        return required
    values[0][1] += required
    values[0][2] += 1
    if len(values[1]) > values[0][2]:
        return 0
    else:
        neededreactions = -(-values[0][1] / values[0][0])
        returned = 0
        for i in range(0, (len(values[0]) - 3) / 2):
            returned += calculate(values[0][i * 2 + 4], values[0][i * 2 + 3] * neededreactions)
            edge = pydot.Edge(values[0][i * 2 + 4], element, dir='forward')
            graph.add_edge(edge)
        return returned

if __name__ == '__main__':
    main()