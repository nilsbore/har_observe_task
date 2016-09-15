#!/usr/bin/env python

import rospy
import actionlib
from geometry_msgs.msg import Pose
from std_msgs.msg import Empty
from har_observe_task.msg import ObserveHarAction, ObserveHarGoal, ObserveHarResult, ObserveHarFeedback

class ObserveHARActionServer(object):
    # Create feedback and result messages
    _feedback = ObserveHarFeedback()
    _result   = ObserveHarResult()

    def __init__(self):
        rospy.init_node("observe_har_actionserver")

        rospy.loginfo("Starting %s", "observe_har_actionserver")
        self._action_name = "/observe_har"
        rospy.loginfo("Creating action server.")
        self._as = actionlib.SimpleActionServer(self._action_name, ObserveHarAction, execute_cb = self.executeCallback, auto_start = False)
        self._as.register_preempt_callback(self.preemptCallback)
        rospy.loginfo(" ...starting")
        self._as.start()
        rospy.loginfo(" ...done")

        #Publishers
        self.empty_pub = rospy.Publisher("/direct_ptu_at_origin", Empty)
        self.pose_pub = rospy.Publisher("/direct_ptu_at_point", Pose)

        rospy.loginfo(" ... Init done")


    def executeCallback(self, goal):
        self.cancelled = False

        goal_pose = Pose()
        goal_pose.position.x = goal.x
        goal_pose.position.y = goal.y
        goal_pose.position.z = goal.z
        goal_pose.orientation.x = 0.0
        goal_pose.orientation.y = 0.0
        goal_pose.orientation.z = 0.0
        goal_pose.orientation.w = 1.0

        self.pose_pub.publish(goal_pose)

        rate = rospy.Rate(1.0)
        start = rospy.Time().now()
        while not rospy.is_shutdown():
            rate.sleep()
            self._as.publish_feedback(self._feedback)
            print "Sleeping..."
            now = rospy.Time().now()
            if now - start > rospy.Duration(60.0*0.25) or self.cancelled:
                print "Damn, now I got cancelled in the loop"
                break

        if not self.cancelled:
            self.empty_pub.publish(Empty())
            self._result.success = True
            self._as.set_succeeded(self._result)


    def preemptCallback(self):
        print "Damn, now I got cancelled in the callback"

        self.cancelled = True

        self.empty_pub.publish(Empty())

        self._result.success = False
        self._as.set_preempted(self._result)

if __name__ == '__main__':

    ps = ObserveHARActionServer()
    rospy.spin()
