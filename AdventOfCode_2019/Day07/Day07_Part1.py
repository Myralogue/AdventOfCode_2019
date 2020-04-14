import itertools

import Day07_Computer as COMPUTER

program = COMPUTER.getprogram('Day07/Day07_Input.txt')

def main(phasesettings):
    combinations = list(itertools.permutations(phasesettings, 5))
    maxvalue = 0
    for c in combinations:
        value = COMPUTER.main(program, [c[0], 0])
        value = COMPUTER.main(program, [c[1], value])
        value = COMPUTER.main(program, [c[2], value])
        value = COMPUTER.main(program, [c[3], value])
        value = COMPUTER.main(program, [c[4], value])

        if value > maxvalue:
            maxvalue = value

    print ("Value to thrusters: " + str(maxvalue))
    return maxvalue

if __name__ == '__main__':
    main('01234')