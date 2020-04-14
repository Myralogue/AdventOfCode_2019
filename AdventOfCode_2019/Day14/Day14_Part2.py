import re, math

filepath = 'Day14/Day14_Input.txt'
conversions = {}
totalore = 1000000000000

def main():
    with open(filepath) as fp:
        for line in fp:
            line = line.strip()
            line = re.split(', | => | ', line)
            elements = []
            for i in range(0, len(line) - 2):
                if i % 2 == 0:
                    elements.append(float(line[i]))
                else:
                    elements.append(line[i])            
            conversions[line[-1]] = [float(line[-2]), 0, 0] + elements

    conversions['ORE'] = [1,0,0]
    values = conversions.get('FUEL')
    for i in range(0, (len(values) - 3) / 2):
        builddependencymap(values[i * 2 + 4], values[i * 2 + 3])
    
    totalfuel = int(calculate('FUEL', 1.0))
    print "fuel produced from 1.000.000.000.000 ore: " + str(totalfuel)
    return totalfuel

def builddependencymap(element, required):
        values = conversions.get(element)
        neededreactions = required / values[0]
        values[2] += required
        for i in range(0, (len(values) - 3) / 2):
            builddependencymap(values[i * 2 + 4], values[i * 2 + 3] * neededreactions)

def calculate(element, required):
    values = conversions.get(element)

    if element == 'ORE':
        return math.floor(totalore / values[2]) * required

    neededreactions = required / values[0]
    returned = 0
    production = totalore
    for i in range(0, (len(values) - 3) / 2):
        minprod = values[i * 2 + 3] * neededreactions
        maxprod = calculate(values[i * 2 + 4], minprod)
        production = min(production, maxprod / minprod)

    return production * required

if __name__ == '__main__':
    main()