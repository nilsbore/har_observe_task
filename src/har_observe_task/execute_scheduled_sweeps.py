#!/usr/bin/python
from strands_executive_msgs import task_utils
from strands_executive_msgs.msg import Task
import strands_executive_msgs
from strands_executive_msgs.srv import AddTasks
from find_waypoints import *
from create_tasks import *
import rospy
import sys
from datetime import datetime
import numpy as np

class HARTaskManager():
    def __init__(self):
        self.minutes=[]
        self.previoustasktimeslot = -1
        self.add_tasks_srv_name = '/task_executor/add_tasks'
        self.set_exe_stat_srv_name = '/task_executor/set_execution_status'
        #self.deep_object_detection_srv_name = 'deep_net/detect_objects'
        try:
            rospy.wait_for_service(add_tasks_srv_name,timeout=10)
        except:
            rospy.logerr("Service not available!!")
            #sys.exit(-1)
        try:
            rospy.wait_for_service(set_exe_stat_srv_name,timeout=10)
        except:
            rospy.logerr("Service not available!!")

        self.createTimeSlotArray()
        self.checkTimeSlot()
        create_har_sweep_tasks("journalExpKTH","roi","configHARRooms")
            #sys.exit(-1)



    def createTimeSlotArray(self):
        self.minutes = [-1]*1440
        count = 0
        arange = np.arange(1,10.1,0.5)
        #print arange
        for i in arange:
            for j in range(-15,15):
                self.minutes[int((i+8)*60)+j] = count
            count+=1

    def checkTimeSlot(self):
        currentTime = rospy.Time.now().secs
        date = datetime.fromtimestamp(currentTime)
        print dir(date)
        print date.hour,date.minute
        timeminutes = date.hour*60 + date.minute
        if(self.minutes[timeminutes] > 0 and self.minutes[timeminutes] is not self.previoustasktimeslot):
            rospy.loginfo("Now it is time to do a task")
            self.previoustasktimeslot = self.minutes[timeminutes]



    def send_tasks(self, roi_db_name,roi_collection_name,roi_config):
        tasks = create_har_sweep_tasks()
        print len(tasks)

        add_tasks_srv = rospy.ServiceProxy(add_tasks_srv_name, AddTasks)
        set_execution_status = rospy.ServiceProxy(set_exe_stat_srv_name, strands_executive_msgs.srv.SetExecutionStatus)
        try:
            # add task to the execution framework
            task_id = add_tasks_srv([tasks[6]])
            # make sure the executive is running -- this only needs to be done once for the whole system not for every task
            set_execution_status(True)
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

if __name__ =="__main__":

    rospy.init_node('har_task_manager')
    print 'hello'
    #send_tasks()
    HARTaskManager()
    rospy.spin()