#! /usr/bin/env python

import rospy 
import numpy as np
import serial 
#import ackermann_msgs

from ackermann_msgs.msg import AckermannDrive



"""
Power train:
ID  Length  D[0]    D[1]    D[2]        D[3]        D[4]
84  5       PWM     Enable  Direction   Low gear    High Gear

PWM: 0-255     
Enable: 0-1   
Direction(fordward or backwards): 0-1 
Low gear: 0-1
High gear: 0-1

######################################

Steer:
ID  Length  D[0]    
83  1       Angle

Angle: 0-100 

brakes 
ID  Length  D[0]    
66  1       pos



"""
steerMin= -17
steerMax = 17


ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    rtscts=True,
    timeout = 1
)

ser.isOpen()

def callback(msg):
    angle = msg.steering_angle
    speed = msg.speed

    if angle > 17 :
        angle = 17
    elif angle < -17:
        angle = -17

    directionScaled = float(angle + 17) / float(34)
    mapped_angle = int((directionScaled*(100)))

    # ser.write("83 1 " + str(mapped_angle))
    ser.write(str.encode("83 1 50 "))
    print("gaming time")

def listener():
    topic = rospy.get_param('~topic', '/pure_pursuit/control')
    rospy.Subscriber(topic, AckermannDrive, callback)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('pylistener', anonymous = True)
    listener()

