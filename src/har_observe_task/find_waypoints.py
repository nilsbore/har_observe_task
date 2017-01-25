#!/usr/bin/python
import rospy
from topological_utils import queries
from strands_navigation_msgs.msg import TopologicalNode
from mongodb_store.message_store import MessageStoreProxy
from soma_msgs.msg import SOMAROIObject
#from soma_manager.srv import SOMAQueryROIs
from geometry_msgs.msg import *
from strands_perception_msgs.msg import Table
import math

def distance(p0,p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def getNodes():
    #print queries.get_nodes(""," ")
    msg_store = MessageStoreProxy(collection="topological_maps")
    objs= msg_store.query(TopologicalNode._type,{"pointset":"dynamic_tmap"})
    nodes,metas = zip(*objs)

    return nodes

def getTables(table_collection="paddedtablestrial"):
    '''Get the tables '''
    msg_store2 = MessageStoreProxy(collection=table_collection)
    objs = msg_store2.query(Table._type, message_query={"update_count":{"$gte":5}})
    tables,meta = zip(*objs)

    return tables

def getRegions(db_name="message_store",collection="roi",roi_config=""):
    msg_store = MessageStoreProxy(database=db_name,collection=collection)
    objs = msg_store.query(SOMAROIObject._type,message_query={"config":roi_config})
    regions,meta = zip(*objs)
    return regions
