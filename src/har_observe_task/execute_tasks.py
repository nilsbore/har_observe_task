#!/usr/bin/python
from strands_executive_msgs import task_utils
from strands_executive_msgs.msg import Task
from find_waypoints import *
from create_tasks import *


def send_tasks():
  tasks = create_har_observation_tasks()

  add_tasks_srv_name = '/task_executor/add_tasks'
  set_exe_stat_srv_name = '/task_executor/set_execution_status'
  rospy.wait_for_service(add_tasks_srv_name)
  rospy.wait_for_service(set_exe_stat_srv_name)
  add_tasks_srv = rospy.ServiceProxy(add_tasks_srv_name, strands_executive_msgs.srv.AddTask)
  set_execution_status = rospy.ServiceProxy(set_exe_stat_srv_name, strands_executive_msgs.srv.SetExecutionStatus)

try:
    # add task to the execution framework
    task_id = add_tasks_srv([tasks[0]])
    # make sure the executive is running -- this only needs to be done once for the whole system not for every task
    set_execution_status(True)
except rospy.ServiceException, e:
    print "Service call failed: %s"%e

def __init__():

    rospy.init_node('har_task_executor')
    send_tasks()
    rospy.spin()
