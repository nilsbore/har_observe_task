#!/usr/bin/python
import rospy
from topological_utils import queries
from strands_navigation_msgs.msg import TopologicalNode
from mongodb_store.message_store import MessageStoreProxy
from geometry_msgs.msg import *
from strands_perception_msgs.msg import Table
import math

def distance(p0,p1):

    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)



def getNodes():
    #print queries.get_nodes(""," ")
    msg_store = MessageStoreProxy(collection="topological_maps")
    objs= msg_store.query(TopologicalNode._type,{"pointset":"kth_floorsix_y2"})
    nodes,metas = zip(*objs)

    return nodes

def getTables():
    '''Get the tables '''
    msg_store2 = MessageStoreProxy(collection="paddedtablestrial")
    objs = msg_store2.query(Table._type, message_query={"update_count":{"$gte":5}})
    tables,meta = zip(*objs)

    return tables


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
     #print topological_nodes[minindex].pose.position
     #print table.pose.pose.position
