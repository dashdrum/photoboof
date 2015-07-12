import RPi.GPIO as GPIO
from GPIOlib import wP2board
from time import sleep

def led_on(wPpin):
    try:
        GPIO.output(wP2board(wPpin),GPIO.LOW)
    except:
        pass

def led_off(wPpin):
    try:
        GPIO.output(wP2board(wPpin),GPIO.HIGH)
    except:
        pass

## setup 

led_count = 5
btn_pin = wP2board(5)

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

for i in range(0,led_count):
    GPIO.setup(wP2board(i),GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(btn_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

## led test
def led_test():


    for i in range(led_count-1,-1,-1): ## led_count-1 to 0
        led_off(i)
            
    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
        sleep(0.300)
        for i in range(led_count-1,-1,-1): ## led_count-1 to 0
            led_off(i)
        sleep(0.300)

    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
            sleep(0.100)
            led_off(i)
            sleep(0.100)


    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
            sleep(0.100)
            led_off(i)
        for i in range(led_count-1,-1,-1): ## led_count-1 to 0
            led_on(i)
            sleep(0.100)
            led_off(i)

    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
        sleep(0.300)
        for i in range(led_count-1,-1,-1): ## led_count-1 to 0
            led_off(i)
        sleep(0.300)

    for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)

while True:
    GPIO.wait_for_edge(btn_pin, GPIO.FALLING)
    sleep(0.2) #debounce
    led_test()

GPIO.cleanup()

