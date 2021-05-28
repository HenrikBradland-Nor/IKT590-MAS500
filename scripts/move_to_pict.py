#!/usr/bin/env python

import sys
import copy
import rospy
import numpy as np
import dynamic_reconfigure.client
from zivid_camera.srv import *
from sensor_msgs.msg import PointCloud2
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

def main():
#intialize movitcommander and the node
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('robot_irb', anonymous=True)
#Instantiate a RobotCommander object. Provides information
    s = Sample_01()
    robot = moveit_commander.RobotCommander()
#Instantiate a PlanningSceneInterface object. This provides a remote interface for getting,

    scene = moveit_commander.PlanningSceneInterface()

#define the groupname
    group_name = 'righty_tcp'
    move_group = moveit_commander.MoveGroupCommander(group_name)
    move_group.set_planner_id('PRM')
    move_group.set_goal_position_tolerance(0.5)

    #define the Publisher
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)

    print "============ Printing robot state"
    print robot.get_current_state()    
    #pose goal in quaternions
    print move_group.get_current_joint_values()
    print move_group.get_goal_tolerance()
    pose_goal = geometry_msgs.msg.Pose()

    #q= [0.2677762,0.1967738,0.9304776,0.1542317]
    #txyz= [-559.017,-181.636,809.017]
    #txyz = np.array(txyz)*0.001
    #pose_goal.orientation.x = q[1]
    #pose_goal.orientation.y = q[2]
    #pose_goal.orientation.z = q[3]
    #pose_goal.orientation.w = q[0]
    #pose_goal.position.x = txyz[0]+1.7
    #pose_goal.position.y = txyz[1]+0.2
    #pose_goal.position.z = txyz[2]+0.9
    pose_goal.orientation.x = 0.0
    pose_goal.orientation.y = 0.0
    pose_goal.orientation.z = 0.0
    pose_goal.orientation.w = 1.0
    pose_goal.position.x = 3.77999999861
    pose_goal.position.y = 3.86900000381
    pose_goal.position.z = 2.0945
    #joint_goal = move_group.get_current_joint_values()
    #print joint_goal
    #joint_goal[5] = 0

    move_group.set_pose_target(pose_goal)
    print pose_goal 
    #plan= move_group.go(joint_goal, wait=True)   
    plan = move_group.go(wait=True)
    print '2'
    # Calling `stop()` ensures that there is no residual movement
    move_group.stop()
    s.capture()
    # It is always good to clear your targets after planning with poses.
    # Note: there is no equivalent function for clear_joint_value_targets()
    move_group.clear_pose_targets()
    
class Sample_01:
    def __init__(self):
        #Node declaration

        #wait until the service is available
        rospy.loginfo( 'waiting for the service')
        rospy.wait_for_service("/zivid_camera/capture", 30.0)
        #create a subscriber
        self.image_sub = rospy.Subscriber('/zivid_camera/color/image_color', Image, self.callback)
        #call the capture service
        self.capture_service = rospy.ServiceProxy("/zivid_camera/capture", Capture)
        self.bridge = CvBridge()
        rospy.loginfo("Enabling the reflection filter")
        general_config_client = dynamic_reconfigure.client.Client(
            "/zivid_camera/capture/general/"
        )
        general_config = {"filters_reflection_enabled": True}
        general_config_client.update_configuration(general_config)

        rospy.loginfo("Enabling and configure the first frame")
        frame0_config_client = dynamic_reconfigure.client.Client(
            "/zivid_camera/capture/frame_0"
        )
        frame0_config = {"enabled": True, "iris": 21, "exposure_time": 20000}
        frame0_config_client.update_configuration(frame0_config)
      
    def callback(self,data):
        rospy.loginfo( 'I have the image')

    def capture(self):
        rospy.loginfo("Calling capture service")
        self.capture_service()


if __name__ == '__main__':
    main()
