filepath = 'Day05/Day05_Input.txt'

def main():
    lines = []
    with open(filepath) as fp:
        for line in fp:
            lines = line.split(",")
        numbers = [int(i) for i in lines] 
        
        outputs = []
        opcodeidx = 0
        opcode = numbers[opcodeidx] % 100
    
        while (opcode != 99):
            if (opcode == 1):   #ADD
                values = getvalues(numbers, opcodeidx)
                numbers[values[2]] = values[0] + values[1]
                opcodeidx += 4
            elif (opcode == 2): #MULTIPLY
                values = getvalues(numbers, opcodeidx)
                numbers[values[2]] = values[0] * values[1]
                opcodeidx += 4
            elif (opcode == 3): #INPUT
                userinput = raw_input("Input Diagnostics System ID: ")
                while not str.isdigit(userinput):
                    userinput = int(raw_input("[{} is invalid] Please input valid Diagnostics System ID: ".format(userinput)))
                numbers[numbers[opcodeidx + 1]] = int(userinput)
                opcodeidx += 2
            elif (opcode == 4): #OUTPUT
                parametermodes = "0" + str(numbers[opcodeidx])[:-2]
                output = numbers[opcodeidx + 1] if parametermodes[-1] == "1" else numbers[numbers[opcodeidx + 1]]
                print ("Output: " + str(output))
                outputs.append(output)
                opcodeidx += 2
            else:
                print ("ERROR: idx: {}, opcode {} is invalid".format(opcodeidx, opcode))
                break

            opcode = numbers[opcodeidx] % 100

        else:
            return(outputs[-1])

def getvalues(numbers, opcodeidx):
    parametermodes = "000" + str(numbers[opcodeidx])[:-2]

    left = numbers[opcodeidx + 1] if parametermodes[-1] == "1" else numbers[numbers[opcodeidx + 1]]
    right = numbers[opcodeidx + 2] if parametermodes[-2] == "1" else numbers[numbers[opcodeidx + 2]]
    target = numbers[opcodeidx + 3]
    return [left, right, target]

if __name__ == '__main__':
    main()