import Day09_Computer as COMPUTER

program = COMPUTER.getprogram('Day09/Day09_Input.txt')

def main():
    return str(COMPUTER.start(program, [1])[0])

if __name__ == '__main__':
    print main()