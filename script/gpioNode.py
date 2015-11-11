#!/usr/bin/env python

#plem_gpio_node
import rospy
import mraa
from std_msgs.msg import String

PLEN_LEFT_EYE   = 14 #left eye pin number
PLEN_RIGHT_EYE  = 20 #right eye pin number

plen_state      = 0 #plen's state
pwm_value       = 0.0 #pwm
add_pwm_value   = 0.0 #add pwm_value

def callback(message):
    rospy.loginfo("GPIO:%s", message.data)
    tmp = message.data.split(",")
    if tmp[0] == "w" and tmp[1] == "on":
        global pwm_value
        pwm_value = 1.0
    elif tmp[0] == "w" and tmp[1] == "off":
        global pwm_value
        global add_pwm_value
        pwm_value = 0.0
        add_pwm_value = 0.0
    elif tmp[0] == "w" and tmp[1] == "act":
        global pwm_value
        global add_pwm_value
        pwm_value = 0.0
        add_pwm_value = 0.01         
    else:
        pass
    
# Setup
pwm0 = mraa.Pwm(PLEN_LEFT_EYE)
pwm0.period_us(700)
pwm0.enable(True)
pwm1 = mraa.Pwm(PLEN_RIGHT_EYE)
pwm1.period_us(700)
pwm1.enable(True)

#ros setup
rospy.init_node('gpioNode', anonymous=True)
pub = rospy.Publisher('GpioToControl', String, queue_size = 10)
sub = rospy.Subscriber('ControlToGpio', String, callback)
r = rospy.Rate(20)#20Hz

# Loop
while not rospy.is_shutdown():
    pwm_value += add_pwm_value
    if pwm_value >= 1.0:
        add_pwm_value = 0.0
        pwm_value = 1.0

    #pwm output
    pwm0.write(pwm_value)
    pwm1.write(pwm_value)
    pub.publish(str(plen_state))#gpio state output
	r.sleep(0.05)
