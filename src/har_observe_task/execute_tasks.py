#!/usr/bin/python
from strands_executive_msgs import task_utils
from strands_executive_msgs.msg import Task
import strands_executive_msgs
from strands_executive_msgs.srv import AddTasks 
from find_waypoints import *
from create_tasks import *
import rospy

def send_tasks():
  tasks = create_har_observation_tasks()
  print len(tasks)
  add_tasks_srv_name = '/task_executor/add_tasks'
  set_exe_stat_srv_name = '/task_executor/set_execution_status'
  rospy.wait_for_service(add_tasks_srv_name)
  rospy.wait_for_service(set_exe_stat_srv_name)
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

    rospy.init_node('har_task_executor')
    print 'hello'
    send_tasks()
    rospy.spin()
