filepath = 'Day02/Day02_Input.txt'

def main(first, second):
    lines = []
    with open(filepath) as fp:
        for line in fp:
            lines = line.split(",")
        numbers = [int(i) for i in lines] 

        #insert inputs
        numbers[1] = first
        numbers[2] = second

        opcodeidx = 0
        opcode = numbers[opcodeidx]
    
        while (opcode != 99):
            if (opcode == 1):
                numbers[numbers[opcodeidx + 3]] = numbers[numbers[opcodeidx + 1]] + numbers[numbers[opcodeidx + 2]]
            elif (opcode == 2):
                numbers[numbers[opcodeidx + 3]] = numbers[numbers[opcodeidx + 1]] * numbers[numbers[opcodeidx + 2]]
            else:
                print ("ERROR: idx: {}, opcode {} is invalid".format(opcodeidx, opcode))
                break

            opcodeidx += 4
            opcode = numbers[opcodeidx]
        else:
            return(numbers[0])

if __name__ == '__main__':
    main(12, 2)