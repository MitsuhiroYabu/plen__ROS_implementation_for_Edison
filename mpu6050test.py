#!/usr/bin/env python
import mraa
import time

I2C_PORT = 0
I2C_ADDR = 0x68

mpu = mraa.I2c(I2C_PORT)
print mpu
mpu.address(I2C_ADDR)
mpu.writeReg(0x6B,0x00)
mpu.writeReg(0x1C,0x00)
print(str(mpu.readWordReg(0x1C)))

i = 0
while i<100:
        accel_x=mpu.readReg(0x3B)
        accel_x=(accel_x << 8) + mpu.readReg(0x3C)
        if accel_x > 32767:
		accel_x = (65536-accel_x)*(-1)
	print(accel_x)
	accel_x = 0
	i = i + 1
	time.sleep(0.05)
