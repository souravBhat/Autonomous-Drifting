#!/usr/bin/env python
import rospy
import gym
import gym_drift_car
from std_msgs.msg import Int8, Float64, Float64MultiArray
import numpy 
import os
import subprocess
import time
import math

from xbee.thread import XBee
import serial

def callback(data, args):
    action = data.data[0]
    takenOn = data.data[1]
    rospy.loginfo(rospy.get_caller_id() + ' Action: %s', data.data)
    
    env = args[0]
    pub = args[1]
    # xbee = args[2]
    
    if takenOn == 0: # Action to be taken on the Gazebo Sim
        if(action == -1000):
            rospy.loginfo('Resetting Env . . . \n\n')
            env.reset()
            return
    
        state, reward, done, _ = env.step(action)
        stateArray = Float64MultiArray()
        stateArray.data = state.tolist()
        pub.publish(stateArray)
    else: # Action to be taken on the actual car
        if(action == -1000):
            rospy.loginfo('Resetting Env . . . \n\n')
            #TODO figure out reset of car
            return
        
        action = math.degrees(action)

    # if done:
    #     env.reset()

if __name__ == '__main__':
    #rospy.init_node('matlab_bridge', anonymous=True)
    tmp = os.popen("ps -Af").read()
    roscore_count = tmp.count('roscore')
    if roscore_count == 0:
        subprocess.Popen("roscore")
        time.sleep(1)
        print ("Roscore launched!")

    env = gym.make('DriftCarGazeboContinuous-v0')
    pub = rospy.Publisher('matlab_bridge/state', Float64MultiArray, queue_size=1) 

    # PORT = '/dev/ttyUSB0'
    # BAUD_RATE = 9600
    # # Open serial port
    # ser = serial.Serial(PORT, BAUD_RATE)
    # # Create API object
    # xbee = XBee(ser)
   
    rospy.Subscriber('matlab_bridge/action', Float64MultiArray, callback, (env, pub))
    
    env.reset()
    rospy.spin()