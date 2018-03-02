#!/usr/bin/env python
#encoding=utf-8

import rospy
import move
import threading
import config
from socket import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion

run=0
rospy.init_node('Navigator', anonymous=False)
navigator = move.Move()

def Monitor_thread():
	global run
	global navigator
	host="localhost"
	port=10000
	addr=(host,port)

	tcpServer = socket(AF_INET,SOCK_STREAM)
	tcpServer.bind(addr)
	tcpServer.listen(10)

	while True:
		print("begin listen...........!")
		tcpClient,addr = tcpServer.accept()
		print("connected from:",addr)
		
		data=tcpClient.recv(1024)
		if not data:
			break
		else:
			if data == "door":
				run=1
			if data == "counter":
				run=2
			if data == "atm":
				run=3
		tcpClient.close()

threading.Thread(target = Monitor_thread,name="Monitor").start()
places=config.getPlaces()

while True:
	try:
		if run == 0:
			continue
		if run == 1:
			run=0
			position = places["door"][0]
			quaternion = places["door"][1]
			rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
			success = navigator.goto(position, quaternion)
			if success:
				rospy.loginfo("reached the desired pose")
			else:
				rospy.loginfo("The base failed to reach the desired pose")
		if run == 2:
			run=0
			position = places["counter"][0]
			quaternion = places["counter"][1]
			rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
			success = navigator.goto(position, quaternion)
			if success:
				rospy.loginfo("reached the desired pose")
			else:
				rospy.loginfo("The base failed to reach the desired pose")
		if run == 3:
			run=0
			position = places["atm"][0]
			quaternion = places["atm"][1]
			rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
			success = navigator.goto(position, quaternion)
			if success:
				rospy.loginfo("reached the desired pose")
			else:
				rospy.loginfo("The base failed to reach the desired pose")
	except rospy.ROSInterruptException:
		rospy.loginfo("Ctrl-C Quitting")
