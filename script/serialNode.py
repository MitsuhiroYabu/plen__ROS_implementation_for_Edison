#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial

def read():
	ser = serial.Serial("/dev/ttyMFD1",9600)
	#data = ser.readline()#read to the end of the line '\n'
	data = ser.read()
    ser.close()
	return data

def write(message):
	ser = serial.Serial("/dev/ttyMFD1",9600)
	ser.write(message.data)
	ser.close()

def callback(message):
    rospy.loginfo("controlNode %s", message.data)
    tmp = message.data.split(",")
    if tmp[0] == "w":
        message.data = tmp[1]
    	write(message)
    elif tmp[0] == "r":
        buf = String()
    	buf.data = read()
    	pub = rospy.Publisher('SerialToControl', String, queue_size = 10)
    	pub.publish(buf)
    else:
    	pass

rospy.init_node('serialNode', anonymous=True)
rospy.Subscriber('ControlToSerial', String, callback)

rospy.spin()
