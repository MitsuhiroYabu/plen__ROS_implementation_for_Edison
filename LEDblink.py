#!/usr/bin/env python
import mraa
import time


class Counter:
    def __init__(self):
        pass

    count = 0


c = Counter()


def GPIOInterupt():
    print("interupt now")
    c.count += 1
    if c.count >= 10:
        x.write(0)
    elif c.count >= 15:
        c.count = 0
        x.write(0)


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

# Loop
while True:
    print "ON"
    time.sleep(0.5)
    print "OFF"
    time.sleep(0.5)
    pwm0.write(value)
    pwm1.write(value)
    value += 0.05
    if value >= 1:
        value = 0.0
