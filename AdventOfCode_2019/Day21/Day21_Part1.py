import sys, os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/Day09/'))

import Day09_Computer as COMPUTER
program = COMPUTER.getprogram('Day21/Day21_Input.txt')

class instructions():
    def __init__(self):
        self.myinstruction = []

    def texttoinstruction(self, text):
        instruction = []
        for c in text:
            instruction.append(ord(c))
        instruction.append(10) #\n
        return instruction

    def add(self, text):
        self.myinstruction.extend(self.texttoinstruction(text))

    def getinstruction(self):
        instruction = self.myinstruction
        instruction.extend(self.texttoinstruction('WALK'))
        return instruction

def main():
    instr = instructions()
    instr.add('NOT A J')
    instr.add('NOT B T')
    instr.add('OR T J')
    instr.add('NOT C T')
    instr.add('OR T J')
    instr.add('AND D J')

    output = COMPUTER.start(program, instr.getinstruction())
    writetoscreen(output)

def writetoscreen(input):
        text = ''
        for c in input:
            try:
                text += str(unichr(c))
            except:
                text += str(c)
        print text

main()