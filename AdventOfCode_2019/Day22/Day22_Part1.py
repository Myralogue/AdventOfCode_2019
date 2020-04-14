filepath = 'Day22/Day22_Input.txt'

def main(decksize):
    deck = range(decksize)

    with open(filepath) as fp:
        for line in fp:
            if 'deal into new stack' in line:
                dealstack(deck)
            elif 'deal with increment' in line:
                deck = dealincrement(deck, int(line[20:]))
            elif 'cut' in line:
                deck = cut(deck, int(line[4:]))

    print 'index of card 2019: ' + str(deck.index(2019))

def dealstack(deck):
    deck.reverse()
    return deck

def dealincrement(deck, value):
    decksize = len(deck)
    temp = [-1] * decksize
    for i in range(decksize):
        temp[(i * value) % decksize] = deck[i]
    return temp

def cut(deck, value):
    deck = deck[value:] + deck[:value]
    return deck

main(10007)