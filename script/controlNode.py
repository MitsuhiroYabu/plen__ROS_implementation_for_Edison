#!/usr/bin/env python
import rospy
from std_msgs.msg import String

accelgyro = [0,0,0,0,0,0]#ax,ay,az,gx,gy,gz

def send_message_to_gpioNode(message):
	gpiopub = rospy.Publisher('ControlToGpio', String, queue_size = 10)
	gpiopub.publish(message.data)

def send_message_to_serialNode(message):
	serialpub =	rospy.Publisher('ControlToSerial', String, queue_size = 10)
	serialpub.publish(message.data)

def send_message_to_bleNode(message):
	blepub = rospy.Publisher('ControlToBle', String, queue_size = 10)
	blepub.publish(message.data)

def send_message_to_i2cNode(message):
	i2cpub = rospy.Publisher('ControlToI2c', String, queue_size = 10)
	i2cpub.publish(message.data)

def publish_control(message):
	tmp = message.data.split(",")#destination,w,r:read or write,message
	send = String()
	
	if tmp[0] == "gpio":
		send.data = ",".join(tmp[1:3])
		send_message_to_gpioNode(send)
	elif tmp[0] == "serial":
		send.data = ",".join(tmp[1:3])
		send_message_to_serialNode(send)
	elif tmp[0] == "ble":
		send.data = ",".join(tmp[1:3])
		send_message_to_bleNode(send)
	elif tmp[0] == "i2c":
		send.data = ",".join(tmp[1:3])
		send_message_to_i2cNode(send)
	elif tmp[0] == "data":
		if tmp[1] == "w":
			for val in range(0,6):
				global accelgyro 
				accelgyro[val] = tmp[val+1]
		elif tmp[1] == "r":
			send.data = "data"
			global accelgyro
			for num in range(0,len(accelgyro)):
        		send.data += ','+str(accelgyro[num])
        	send_message_to_serialNode(send)
		else:
			pass
	else:
		pass

def callback_gpio(message):
    rospy.loginfo("gpioNode %s", message.data)
    publish_control(message)

def callback_serial(message):
    rospy.loginfo("serialNode %s", message.data)
    publish_control(message)

def callback_ble(message):
    rospy.loginfo("bleNode %s", message.data)
    publish_control(message)

def callback_i2c(message):
    rospy.loginfo("i2cNode %s", message.data)
    publish_control(message)

rospy.init_node('ControlNode', anonymous=True)

rospy.Subscriber('GpioToControl', String, callback_gpio)
rospy.Subscriber('SerialToControl', String, callback_serial)
rospy.Subscriber('BleToControl', String, callback_ble)
rospy.Subscriber('I2cToControl', String, callback_i2c)

rospy.spin()
