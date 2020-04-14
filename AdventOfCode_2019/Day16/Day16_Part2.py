filepath = 'Day16/Day16_Input.txt'

def main():
    sequence = []
    with open(filepath) as fp:
        for line in fp:
            line = line.strip()
            offset = int(line[:7])
            for c in line:
                sequence.append(int(c))
    sequence = (sequence * 10000)[offset:]
    
    for _ in range(100):
        for i in range(-2, -len(sequence)-1, -1):
            sequence[i] = (sequence[i] + sequence[i+1]) % 10

    message = getstring(sequence, 0, 8)
    print "FFTed message:" + message
    return message

def getstring(sequence, fromidx, toidx):
    string = ''
    for i in range(fromidx, toidx):
        string += str(sequence[i])
    return string

if __name__ == '__main__':
    main()