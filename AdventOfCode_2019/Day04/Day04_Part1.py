#global vars
nr = []
maxidx = 0
number = 0
count = 0
maxnr = 0

def main(min, max):
    global nr
    global maxnr
    global maxidx

    maxnr = max
    maxidx = len(str(max)) - 1
    min_str = str(min)
    
    for i in range(0, len(min_str)):
        nr.append(0)

    itterate(0, int(min_str[0]), 10)

    print("There are {} valid passwords".format(count))
    return count
    
def itterate(index, min, max):
    global number
    global maxidx
    global count
    global maxnr

    number += (10 ** (maxidx - index)) * min
    nr[index] = min

    for i in range(min, max):
        if (index < maxidx):
            itterate(index + 1, nr[index], 9)
        if (number > maxnr):
            return

        #count the nr if adjacent
        if adjacent():
            print(str(number))
            count += 1
        
        #increment
        number += 1
        nr[index] += 1
    else:
        if (index < maxidx):
            itterate(index + 1, nr[index], 9)
        
def adjacent():
    for i in range(1, len(nr)):
        if nr[i - 1] == nr[i]:
            return True

if __name__ == '__main__':
    main(206938, 679128)