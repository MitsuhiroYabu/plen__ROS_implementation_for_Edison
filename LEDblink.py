#!/usr/bin/env python
import mraa
import time


class Counter:
    def __init__(self):
        pass

    count = 0


c = Counter()


def GPIOInterupt(args):
    print("interupt now")
    c.count += 1
    if c.count >= 5:
        x.write(0)
        c.count = 0
    elif c.count >= 0:
        x.write(1)


# Setup
print("mraa Version: %s" % mraa.getVersion())
x = mraa.Gpio(8)
inputGPIO = mraa.Gpio(12)
x.dir(mraa.DIR_OUT)
inputGPIO.dir(mraa.DIR_IN)
inputGPIO.isr(mraa.EDGE_BOTH, GPIOInterupt, GPIOInterupt)
pwm0 = mraa.Pwm(3)
pwm0.period_us(700)
pwm0.enable(True)
pwm1 = mraa.Pwm(5)
pwm1.period_us(700)
pwm1.enable(True)
value = 0.0
add = 0.01

# Loop
while True:
    time.sleep(0.05)
    pwm0.write(value)
    pwm1.write(value)
    value += add
    if value >= 1:
        add = -0.01
    elif value <= 0:
        add = 0.01
