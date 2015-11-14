#!/usr/bin/env python
import mraa
import rospy
from std_msgs.msg import String

I2C_PORT = 0   #i2c_port_6
I2C_ADDR = 0x68#mpu6050

def getAccelGyro():
    global mpu
    tmp = []
    accelgyro = []
    for address in [0x3B,0x3C,0x3D,0x3E,0x3F,0x40,0x43,0x44,0x45,0x46,0x47,0x48]:
        tmp.append(mpu.readReg(address))
    for val in [0,2,4,6,8,10]:
        result = (tmp[val] << 8) + tmp[val+1]
        if result > 32767:
            result = (65536-result)*(-1)
        accelgyro.append(result)

    send_accelgyro = String()
    send_accelgyro.data = "data,w"
    for num in range(0,len(accelgyro)):
        send_accelgyro.data += ','+str(accelgyro[num])

    return send_accelgyro
    
def callback(message):
	rospy.loginfo("controlNode %s", message.data)
    tmp = message.data.split(",")
    if tmp[0] == "w":
        pass
    elif tmp[0] == "r":
    	pub = rospy.Publisher('I2cToControl', String, queue_size = 10)
        pub.publish(getAccelGyro())
    else:
    	pass


mpu = mraa.I2c(I2C_PORT)
mpu.address(I2C_ADDR)
mpu.writeReg(0x6B,0x00)
rospy.init_node('i2cNode', anonymous=True)
rospy.Subscriber('ControlToI2c', String, callback)

r = rospy.Rate(10)#20Hz

# Loop
while not rospy.is_shutdown():
    pub = rospy.Publisher('I2cToControl', String, queue_size = 10)
    pub.publish(getAccelGyro())
    r.sleep()


