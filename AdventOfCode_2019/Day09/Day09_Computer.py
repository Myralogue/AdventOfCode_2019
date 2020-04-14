import Queue

class computerruntime():
    def __init__(self, aProgram, aInputs, aInputQueue, aOutputQueue, aReturnQueue, outmode, outcount, inmode, infallbackvalue):
        self.numbers = aProgram
        self.outputs = []
        self.inputs = aInputs
        self.mq = aInputQueue
        self.nq = aOutputQueue
        self.rq = aReturnQueue
        self.outmode = outmode
        self.outcount = outcount
        self.inmode = inmode
        self.infallbackvalue = infallbackvalue
        self.opcodeidx = 0
        self.relativebase = 0
        self.opcode = self.numbers[0] % 100
        self.inputidx = 0

    def __repr__(self):
        return str("Computer runtime memory dump: {}, outputs: {}, opcodeidx: {}, relativebase: {} " + self.numbers, self.outputs, self.opcodeidx, self.relativebase)

def getprogram(filepath):
    global loadedprogram

    lines = []
    with open(filepath) as fp:
        for line in fp:
            lines = line.split(",")
        loadedprogram = [int(i) for i in lines] 
        print ("program at {} is loaded".format(filepath))
    return loadedprogram
    

def start(program, inputs = [], inputqueue = Queue.Empty, outputqueue = Queue.Empty, returnqueue = Queue.Empty, outmode = 0, outcount = 1, inmode = 0, infallbackvalue = -1):
    ''' Executes computer with program. 
    [inputs]: start computer with inputs, 
    [inputqueue]: queue to listen to for inputs,
    [outputqueue]: queue to call when program reaches output command,
    [returnqueue]: queue to return when program finishes, 
    [outmode]: mode for outqueue: 0 = direct (send all outputs directly based on outcount) 1 = collated (collect all outputs and send them to outputqueue once input command is reached),
    [outcount]: how many outputs have to be collected before output is sent (only used in outmode 0),
    [inmode]: mode for inputqueue: 0 = wait for input, 1 = use infallbackvalue when no value is in queue,
    [infallbackvalue] value to use when no value is in inputqueue'''
    rt = computerruntime(program, inputs, inputqueue, outputqueue, returnqueue, outmode, outcount, inmode, infallbackvalue)
    output = main(rt)
    return output

def main(rt):
    #PROGRAM SWITCH:
    currentoutputs = []
    while (rt.opcode != 99):
        if (rt.opcode == 1):   #ADD
            address = getaddresses(rt, 3)
            alocate(rt.numbers, address[2])
            rt.numbers[address[2]] = getatindex(rt.numbers, address[0]) + getatindex(rt.numbers, address[1])
            rt.opcodeidx += 4

        elif (rt.opcode == 2): #MULTIPLY
            address = getaddresses(rt, 3)
            alocate(rt.numbers, address[2])
            rt.numbers[address[2]] = getatindex(rt.numbers, address[0]) * getatindex(rt.numbers, address[1])
            rt.opcodeidx += 4

        elif (rt.opcode == 3): #INPUT
            if (rt.inputidx < len(rt.inputs)):
                userinput = rt.inputs[rt.inputidx]
                rt.inputidx += 1
            elif rt.mq != Queue.Empty:
                if rt.inmode == 0:
                    if rt.outmode == 1:
                        rt.nq.put(currentoutputs)
                        currentoutputs = []
                    userinput = rt.mq.get()
                elif rt.inmode == 1:
                    try:
                        userinput = rt.mq.get_nowait()
                        if rt.outmode == 1:
                            rt.nq.put(currentoutputs)
                            currentoutputs = []
                    except:
                        userinput = rt.infallbackvalue
                if isinstance(userinput, list): #import array
                    rt.inputs.extend(userinput)
                    userinput = rt.inputs[rt.inputidx]
                    rt.inputidx += 1
            else:
                userinput = raw_input("Input Diagnostics System ID: ")
                while not str.isdigit(userinput): #WAIT FOR VALID INPUT
                    userinput = int(raw_input("[{} is invalid] Please input valid Diagnostics System ID: ".format(userinput)))
            address = getaddresses(rt, 1)
            alocate(rt.numbers, address[0])
            rt.numbers[address[0]] = int(userinput)
            rt.opcodeidx += 2

        elif (rt.opcode == 4): #OUTPUT
            output = getatindex(rt.numbers, getaddresses(rt, 1)[0])
            rt.outputs.append(output)
            if rt.nq != Queue.Empty:
                if rt.outmode == 0:
                    if rt.outcount == 1:
                        rt.nq.put(output)
                    else:
                        currentoutputs.append(output)
                        if len(currentoutputs) >= rt.outcount:
                            rt.nq.put(currentoutputs)
                            currentoutputs = []
                elif rt.outmode == 1:
                    currentoutputs.append(output)
                elif rt.outmode == 2:
                    pass
            rt.opcodeidx += 2

        elif (rt.opcode == 5): #JUMP-IF-TRUE
            address = getaddresses(rt, 2)
            if (getatindex(rt.numbers, address[0]) != 0):
                rt.opcodeidx = getatindex(rt.numbers, address[1])
            else:
                rt.opcodeidx += 3

        elif (rt.opcode == 6): #JUMP-IF-FALSE
            address = getaddresses(rt, 2)
            if (getatindex(rt.numbers, address[0]) == 0):
                rt.opcodeidx = getatindex(rt.numbers, address[1])
            else:
                rt.opcodeidx += 3

        elif (rt.opcode == 7): #LESS THAN
            address = getaddresses(rt, 3)
            alocate(rt.numbers, address[2])
            rt.numbers[address[2]] = 1 if getatindex(rt.numbers, address[0]) < getatindex(rt.numbers, address[1]) else 0
            rt.opcodeidx += 4

        elif (rt.opcode == 8): #EQUALS
            address = getaddresses(rt, 3)
            alocate(rt.numbers, address[2])
            rt.numbers[address[2]] = 1 if getatindex(rt.numbers, address[0]) == getatindex(rt.numbers, address[1]) else 0
            rt.opcodeidx += 4

        elif (rt.opcode == 9): #OFFSET RELATIVE BASE
            address = getaddresses(rt, 1)
            rt.relativebase += getatindex(rt.numbers, address[0])
            rt.opcodeidx += 2

        else:
            print ("ERROR: idx: {}, opcode {} is invalid".format(rt.opcodeidx, rt.opcode))
            break

        rt.opcode = rt.numbers[rt.opcodeidx] % 100

        if rt.rq != Queue.Empty:
            try:
                if rt.rq.get_nowait() == -1:
                    print 'early out of thread because return queue = -1'
                    rt.opcode = 99
            except:
                pass

    else:
        if rt.nq != Queue.Empty and rt.outmode == 1:
            rt.nq.put(currentoutputs)
            currentoutputs = []
        if rt.rq != Queue.Empty:
            rt.rq.put(rt.outputs[-1])
        return rt.outputs

def getaddresses(rt, count):
    output = []
    parametermodes = "000" + str(rt.numbers[rt.opcodeidx])[:-2]

    for i in range(1, count + 1):
        if parametermodes[-i] == "0":   #POSITION MODE
            output.append(rt.numbers[rt.opcodeidx + i])
        elif parametermodes[-i] == "1": #IMMEDIATE MODE
            output.append(rt.opcodeidx + i)
        elif parametermodes[-i] == "2": #RELATIVE MODE
            output.append(rt.relativebase + rt.numbers[rt.opcodeidx + i])

    return output

def alocate(list, address):
    count = address - len(list) + 1
    if count > 0:
        list.extend([0] * count)

def getatindex(list, address, fallback = 0):
    value = list[address:address + 1]
    if value != []:
        return value[0]
    else:
        return fallback