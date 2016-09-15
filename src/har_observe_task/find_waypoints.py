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
