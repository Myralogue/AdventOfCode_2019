filepath = 'Day16/Day16_Input.txt'

def main():
    sequence = []
    pattern = [0, 1, 0, -1]

    with open(filepath) as fp:
        for line in fp:
            line = line.strip()
            for c in line:
                sequence.append(int(c))

    for i in range(0, 100):
        newsequence = phase(newsequence, pattern)
    message = getstring(newsequence, 0, 8)
    print "FFTed message:" + message
    return message
    
def phase(sequence, pattern):
    sequencelength = len(sequence)
    newsequence = [0] * sequencelength

    for i in range(1, len(sequence) + 1):
        value = 0
        idx = 0
        for seg in (sequence[x:x + i] for x in range(-1, sequencelength, i)):
            if idx == 1:
                value += sum(seg)
            elif idx == 3:
                value -= sum(seg)
            idx = (idx + 1) % 4
        newsequence[i - 1] = abs(value) % 10
    return newsequence

def getstring(sequence, fromidx, toidx):
    string = ''
    for i in range(fromidx, toidx):
        string += str(sequence[i])
    return string

if __name__ == '__main__':
    main()