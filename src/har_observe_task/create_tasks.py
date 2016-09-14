from strands_executive_msgs import task_utils
from strands_executive_msgs.msg import Task
from find_waypoints import *

def create_har_observation_tasks(duration=rospy.Duration(30*60)):

    topological_nodes = getNodes()
    tables = getTables()

    tablenodepairs = []

    for table in tables:
         table_position = [table.pose.pose.position.x, table.pose.pose.position.y]
         distances = []
         for topological_node in topological_nodes:
             node_position = [topological_node.pose.position.x, topological_node.pose.position.y]
             distances.append(distance(table_position,node_position))
         minindex =  distances.index(min(distances))
         tablenodepairs.append((table_position, topological_nodes[minindex]))

    tasks = []

    for pair in tablenodepairs:
        task = Task(start_node_id=pair[1].name, end_node_id=pair[1].name, action='observe_har', max_duration=duration)
        task_utils.add_float_argument(task, pair[0].x)
        task_utils.add_float_argument(task, pair[0].y)
        task_utils.add_float_argument(task, 1.0)
        tasks.append(task)

    return tasks
