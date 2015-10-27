#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial

ser = serial.Serial("/dev/ttyMFD1",9600)

def callback(message):
        ser.write(message.data)
	    rospy.loginfo("I heard %s", message.data)

rospy.init_node('listener')
sub = rospy.Subscriber('chatter', String, callback)
rospy.spin()
ser.close()
