#!/usr/bin/env python
import rospy
import rosnode
import dynamic_reconfigure.client
import pcl
from zivid_camera.srv import *
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
import pcl_ros
import os
import time
import geometry_msgs
import tf
import tf.transformations as tft
import numpy as np


#class frame_trans():

    #def __init__(self):
        #rospy.init_node('frame_transformer')
        #rospy.Subscriber('frame_transformer',self.trans_pos, queue_size=1)
        #rospy.spin()

    #def


def main():
    rospy.init_node('frame_transformer')

    listner = tf.TransformListener()



    #tf.frameExsist('/world')
    listner.waitForTransform('/world','/zivid_optical_frame', rospy.Time(0), rospy.Duration(4.0))
    (trans,quats) = listner.lookupTransform('/world','/zivid_optical_frame', rospy.Time(0))


    #listner.waitForTransform('/zivid_optical_frame', '/world', rospy.Time(0), rospy.Duration(4.0))
    #(trans, rot) = listner.lookupTransform('/zivid_optical_frame', '/world', rospy.Time(0))

    R = tft.quaternion_matrix(quats)
    T = tft.translation_matrix(trans)
    TR = R+T-np.identity(4)
    quat_test = tf.transformations.quaternion_from_euler(np.rad2deg(80), np.rad2deg(-10), 0, axes='syzx')

    print(R)
    print(T)
    print(R+T-np.identity(4))
    print('----------quat_test-------')
    print(quat_test)



if __name__ == "__main__":
    main()
