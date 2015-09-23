import mraa
import time

# Setup
print("mraa Version: %s" % mraa.getVersion())
x = mraa.Gpio(8)
x.dir(mraa.DIR_OUT)
pwm = mraa.Pwm(3)
pwm.period_us(700)
pwm.enable(True)
value = 0.0

# Loop
while True:
    x.write(0)
    print "ON"
    time.sleep(0.5)
    x.write(0)
    print "OFF"
    time.sleep(0.5)
    pwm.write(value)
    value = value + 0.05
    if value >= 1:
    	value = 0.0
