#!/usr/bin/env python

import mraa
import rospy
from std_msgs.msg import String
import serial

#Setting Serial communication
ser = serial.Serial("/dev/ttyMFD1", 2000000)
uart_1_ED_RE = mraa.Gpio(36)
uart_1_ED_RE.dir(mraa.DIR_OUT)
uart_1_ED_RE.write(0)

def read():
    global uart_1_ED_RE
    global ser
    uart_1_ED_RE.write(1)
    data = ser.read()
    uart_1_ED_RE.write(0)
	return data

def write(message):
    global uart_1_ED_RE
    global ser
    uart_1_ED_RE.write(1)
	ser.write(message.data)
    ser.write("send")
    uart_1_ED_RE.write(0)

def callback(message):
    rospy.loginfo("controlNode %s", message.data)
    tmp = message.data.split(",")
    if tmp[0] == "w":
        message.data = tmp[1]
    	write(message)
    elif tmp[0] == "r":
        pass
    elif tmp[0] == "data":
        message.data = ",".join(tmp[1:7])
        write(message)

#Setting ROS
rospy.init_node('serialNode', anonymous=True)
rospy.Subscriber('ControlToSerial', String, callback)
pub = rospy.Publisher('SerialToControl', String, queue_size = 10)
r = rospy.Rate(50)#50Hz

while not rospy.is_shutdown():
    if ser.inWaiting() > 0:
        data = ser.read()
        message = String()
        message.data = "data,r"
        pub.publish(message)
        ser.flush()
    r.sleep()

ser.close()
