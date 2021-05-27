#!/usr/bin/env python

import sys
import copy
import rospy
import numpy as np
import dynamic_reconfigure.client
from zivid_camera.srv import *
# from sensor_msgs.msg import PointCloud2
# import cv2
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge, CvBridgeError
import time
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import random
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

import matplotlib.pyplot as plt

import batpiv as bp
import tf.transformations
import capture as tc
from config import config


class capture_point_cloud:
    def __init__(self, cfg):

        self.cfg = cfg

        # intialize movitcommander and the node
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('robot_irb', anonymous=True)
        # Instantiate a RobotCommander object. Provides information

        self.robot = moveit_commander.RobotCommander()
        # Instantiate a PlanningSceneInterface object. This provides a remote interface for getting,

        self.scene = moveit_commander.PlanningSceneInterface()

        # define the groupname
        self.group_name = 'righty_tcp'
        self.move_group = moveit_commander.MoveGroupCommander(self.group_name)
        self.move_group.set_planner_id('RTTConnect')
        self.move_group.set_goal_position_tolerance(0.0001)
        self.move_group.set_goal_orientation_tolerance(0.0001)
        self.move_group.set_num_planning_attempts(50)
        self.move_group.set_planning_time(50)

        self.ql = []

        #self.ql.append(self.cfg.p7.q)
        #self.ql.append(self.cfg.p8.q)
        #self.ql.append(self.cfg.p9.q)
        #self.ql.append(self.cfg.p2.q)
        #self.ql.append(self.cfg.p3.q)
        #self.ql.append(self.cfg.p4.q)
        #self.ql.append(self.cfg.p5.q)
        #self.ql.append(self.cfg.p6.q)

        #self.ql.append(self.cfg.bp5.q)
        #self.ql.append(self.cfg.bp6.q)
        #self.ql.append(self.cfg.bp7.q)
        #self.ql.append(self.cfg.bp8.q)
        #self.ql.append(self.cfg.bp9.q)
        #self.ql.append(self.cfg.bp10.q)
        #self.ql.append(self.cfg.bp11.q)
        #self.ql.append(self.cfg.bp12.q)
        #self.ql.append(self.cfg.bp13.q)

        self.ql.append(self.cfg.bpsb1.q)
        self.ql.append(self.cfg.bpsb2.q)
        self.ql.append(self.cfg.bpsb3.q)
        #self.ql.append(self.cfg.bpsb4.q)
        #self.ql.append(self.cfg.bpsb5.q)
        #self.ql.append(self.cfg.bpsb6.q)
        #self.ql.append(self.cfg.bpsb7.q)
        #self.ql.append(self.cfg.bpsb8.q)
        #self.ql.append(self.cfg.bpsb9.q)
        #self.ql.append(self.cfg.bpsb10.q)
        #self.ql.append(self.cfg.bpsb11.q)
        #self.ql.append(self.cfg.bpsb12.q)

        #self.ql.append(self.cfg.bpbb1.q)
        #self.ql.append(self.cfg.bpbb2.q)
        #self.ql.append(self.cfg.bpbb3.q)
        #self.ql.append(self.cfg.bpbb4.q)
        #self.ql.append(self.cfg.bpbb5.q)
        #self.ql.append(self.cfg.bpbb6.q)
        #self.ql.append(self.cfg.bpbb6.q)

        self.captured_point_clouds = []

        # define the Publisher
        display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                       moveit_msgs.msg.DisplayTrajectory,
                                                       queue_size=20)
        self.s = tc.Sample(self.cfg)

    def run_robot(self):
        if len(self.ql) == 0:
            Exception("No points added to move list")
        pose_goal = geometry_msgs.msg.Pose()
        for i, q in enumerate(self.ql):
            rospy.loginfo("Moving to pose number: " + str(1+i)+"/"+str(len(self.ql)))
            pose_goal.orientation.x = q[0]
            pose_goal.orientation.y = q[1]
            pose_goal.orientation.z = q[2]
            pose_goal.orientation.w = q[3]
            pose_goal.position.x = q[4]
            pose_goal.position.y = q[5]
            pose_goal.position.z = q[6]

            self.move_group.set_pose_target(pose_goal)
            self.move_group.go(pose_goal, wait=True) # plan =
            # Calling `stop()` ensures that there is no residual movement
            self.move_group.stop()
            time.sleep(2)
            self.s.capture()
            time.sleep(25)

        self.ql = []

        '''

        red_0 = np.bincount(np.array([x[0] for x in self.s.list_of_color]))
        blue_0 = np.bincount(np.array([x[1] for x in self.s.list_of_color]))
        green_0 = np.bincount(np.array([x[2] for x in self.s.list_of_color]))

        red = np.zeros(256)
        blue = np.zeros(256)
        green = np.zeros(256)

        for ind, val in enumerate(red_0):
            red[ind] = val
        for ind, val in enumerate(blue_0):
            blue[ind] = val
        for ind, val in enumerate(green_0):
            green[ind] = val

        f, ax = plt.subplots(3)

        for idx in range(256):
            ax[0].bar(idx, red[idx])
            ax[1].bar(idx, blue[idx])
            ax[2].bar(idx, green[idx])

        plt.show()
        '''

    def add_position_to_move_list(self, pos, ang):
        if len(ang) == 3:
            q = tf.transformations.quaternion_from_euler(ang[0], ang[1], ang[2])
        elif len(ang) == 4:
            q = ang
        else:
            Exception("Wrong format of ang")
        q = np.append(q, [pos[0], pos[1], pos[2]])
        self.ql.append(q)

    def get_captured_point_clouds(self):
        pcs = self.s.list_of_pc
        self.s.list_of_pc = []
        return pcs


if __name__ == '__main__':
    cpc = capture_point_cloud()
    cpc.run_robot()
