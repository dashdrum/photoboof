
def wP2board(wPpin):

    ''' Convert the pin assignments used in wiringPi.c to their board equivalents
        See http://wiringpi.com/pins/ for details '''
    
    wPpins =     [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16]
    board_pins = [11,12,13,15,16,18,22, 7, 3, 5,24,26,19,21,23, 8,10]

    if wPpin in wPpins:
        return board_pins[wPpin]

    return None

