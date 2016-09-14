#!/usr/bin/python

import numpy as np
from geometry_msgs.msg import Pose, PoseStamped
import tf
import rospy
import math
from scitos_ptu.msg import PtuGotoAction, PtuGotoGoal,  PtuGotoResult
from actionlib_msgs.msg import *
import actionlib

class DirectPTUServer(object):

    def __init__(self):

        rospy.init_node('direct_ptu_server')
        rospy.Subscriber("/direct_ptu_at_point", Pose, self.direct_ptu_at)

        #self.t = tf.TransformerROS(True, rospy.Duration(4.0))
        self.t = tf.TransformListener()
        self.action_client = actionlib.SimpleActionClient('/SetPTUState', PtuGotoAction)
        rospy.loginfo("Waiting for ptu action...")
        self.action_client.wait_for_server()
        rospy.loginfo("Got ptu action server")

    def direct_ptu_at(self, p):

        msg = PoseStamped()
        msg.pose = p
        msg.header.frame_id = "map"
        msg.header.stamp = rospy.Time.now()
        #msgq = self.t.transformPose("/ptu_pan_motor", msg)
        while True:
            try:
                msgq = self.t.transformPose("ptu_pan_motor", msg)
                break
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                rospy.Duration(0.01).sleep()


        q = np.array([msgq.pose.position.x, msgq.pose.position.y, msgq.pose.position.z])
        q = q / np.linalg.norm(q)
        theta = 180.0/math.pi*math.acos(q[2])
        phi = 180.0/math.pi*math.atan2(p[1], p[0])

        print "Directing at point ", q
        print "With theta ", theta
        print "and phi ", phi

        goal = PtuGotoGoal()
        goal.pan = theta
        goal.tilt = phi
        goal.pan_vel = 30
        goal.tilt_vel = 30

        self.action_client.send_goal(goal)
        self.action_client.wait_for_result()

if __name__ == '__main__':
    server = DirectPTUServer()
    rospy.spin()
