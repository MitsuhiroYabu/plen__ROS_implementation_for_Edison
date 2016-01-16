#!/usr/bin/env python

import mraa
from strcut import *
import rospy
from std_msgs.msg import String
import serial

#Setting Serial communication
ser = serial.Serial("/dev/ttyMFD1", 2000000)
uart_1_ED_RE = mraa.Gpio(36)
uart_1_ED_RE.dir(mraa.DIR_OUT)
uart_1_ED_RE.write(0)
acgydata = ['0','0','0','0','0','0']

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
    ser.flush()
    uart_1_ED_RE.write(0)

def writeacgy(acgydata):
    global uart_1_ED_RE
    global ser
    uart_1_ED_RE.write(1)
    ser.write(acgydata)
    ser.write("\n")
    ser.flush()
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
        acgydata = pack(">hhhhhh",int(tmp[1]),int(tmp[2]),int(tmp[3]),int(tmp[4]),int(tmp[5]),int(tmp[6]))
        writeacgy(acgydata)

def call_sensor_data(message):
    global acgydata
    rospy.loginfo("sensor data")
    tmp = message.data.split(",")
    for num in range(2,8):
        acgydata[num - 2] = tmp[num]

    #acgydata = pack(">hhhhhh",int(tmp[1]),int(tmp[2]),int(tmp[3]),int(tmp[4]),int(tmp[5]),int(tmp[6]))




#Setting ROS
rospy.init_node('serialNode', anonymous=True)
rospy.Subscriber('ControlToSerial', String, callback)
rospy.Subscriber('I2cToControl', String, call_sensor_data)
pub = rospy.Publisher('SerialToControl', String, queue_size = 10)
r = rospy.Rate(50)#50Hz

while not rospy.is_shutdown():
    if ser.inWaiting() > 0:
        data = ser.read()
        writeacgy(pack(">hhhhhh",int(acgydata[0]),int(acgydata[1]),int(acgydata[2]),int(acgydata[3]),int(acgydata[4]),int(acgydata[5])))
        #message = String()
        #message.data = "data,r"
        #pub.publish(message)
    r.sleep()

ser.close()
