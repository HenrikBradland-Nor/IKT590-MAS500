#!/usr/bin/env python
import rospy
import rosnode
import dynamic_reconfigure.client
import pcl
from zivid_camera.srv import *
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2, PointCloud
from sensor_msgs import point_cloud2 as pc2
# from sensor_msgs.msg import PointCloud
import pcl_ros
import os
import tf
import tf.transformations as tft
import time
from geometry_msgs.msg import Point
import numpy as np
import matplotlib.pyplot as plt
import pcl_helper
import config


class Sample:
    def __init__(self, cfg):
        self.cfg = cfg

        self.im_num = 0
        self.list_of_pc = []
        self.list_of_color = []

        self.test = []

        # listner = tf.TransformListener()
        # transform = listner.lookupTransform('world','zivid_optical_frame', rospy.Time(0))

        rospy.loginfo("Starting capture.py")

        #ca_suggest_settings_service = "/zivid_camera/capture_assistant/suggest_settings"

        #rospy.wait_for_service(ca_suggest_settings_service, 30.0)


        #self.capture_assistant_service = rospy.ServiceProxy(
        #    ca_suggest_settings_service, CaptureAssistantSuggestSettings
        #)

        rospy.wait_for_service("/zivid_camera/capture", 30.0)
        # trans_cloud = rospy.Publisher('trans_cloud', PointCloud2, queue_size=10)

        self.capture_service = rospy.ServiceProxy("/zivid_camera/capture", Capture)
        rospy.Subscriber('/zivid_camera/points', PointCloud2, self.on_points)

        rospy.loginfo("Enabling the reflection filter")
        general_config_client = dynamic_reconfigure.client.Client(
            "/zivid_camera/capture/general"
        )
        general_config = {"filters_reflection_enabled": True,
                          "filters_contrast_enabled": True, "filters_saturated_enabled": True,
                          "filters_gaussian_enabled": True,
                          "filters_gaussian_sigma": 1.5,
                          "filters_outlier_enabled": True,
                          "filters_outlier_threshold": 5}
        general_config_client.update_configuration(general_config)

        rospy.loginfo("Enabling and configure the first frame")
        frame0_config_client = dynamic_reconfigure.client.Client(
            "/zivid_camera/capture/frame_0"
        )
        #rospy.loginfo("Enabling and configure the first frame")
        #frame1_config_client = dynamic_reconfigure.client.Client(
        #    "/zivid_camera/capture/frame_1"
        #)

        frame0_config = {"enabled": True, "iris": 21, "gain": 1.0, "exposure_time": 10000, "brightness": 1}
        frame0_config_client.update_configuration(frame0_config)

        #frame1_config = {"enabled": True, "iris": 22, "gain": 2.0, "exposure_time": 8333, "brightness": 1}
        #frame1_config_client.update_configuration(frame1_config)



        #frame1_config_client = dynamic_reconfigure.client.Client(
        #    "/zivid_camera/capture/frame_1"
        #)
        #frame1_config = {"enabled": True, "iris": 17, "gain": 1.0, "exposure_time": 60000}
        #frame1_config_client.update_configuration(frame1_config)

        #frame2_config_client = dynamic_reconfigure.client.Client(
        #    "/zivid_camera/capture/frame_2"
        #)
        #frame2_config = {"enabled": True, "iris": 17, "gain": 1.0, "exposure_time": 60000, "brightness": 0.5}
        #frame2_config_client.update_configuration(frame2_config)


        #self.capture_assistant_suggest_settings()



    def capture_assistant_suggest_settings(self):
        max_capture_time = rospy.Duration.from_sec(2.6)
        rospy.loginfo(
            "Calling capture assistant service with max capture time = %.2f sec",
            max_capture_time.to_sec(),
        )
        self.capture_assistant_service(
            max_capture_time=max_capture_time,
            ambient_light_frequency=CaptureAssistantSuggestSettingsRequest.AMBIENT_LIGHT_FREQUENCY_NONE,
        )

    def capture(self):
        rospy.loginfo("Calling capture service")
        self.capture_service()

    def on_points(self, data):

        point_list = list([x for x in pc2.read_points(data, skip_nans=True, field_names=["x", "y", "z", "rgb"])])

        pcl_pc = pcl.PointCloud_PointXYZRGB()
        pcl_pc.from_list(point_list)
        passthrough = pcl_pc.make_passthrough_filter()
        passthrough.set_filter_field_name("z")
        passthrough.set_filter_limits(self.cfg.min_image_depth, self.cfg.max_image_depth)
        pcl_pc = passthrough.filter()
        point_list = pcl_pc.to_list()

        tf_list = tf.TransformListener()
        tf_list.waitForTransform('/world', '/zivid_optical_frame', rospy.Time(0), rospy.Duration(4.0))
        (trans, quats) = tf_list.lookupTransform('/world', '/zivid_optical_frame', rospy.Time(0))
        R = tft.quaternion_matrix(quats)
        T = tft.translation_matrix(trans)
        TR = R + T - np.identity(4)

        trans_points = np.zeros((len(point_list), 4), dtype=np.float32)

        for i, point in enumerate(point_list):
            point_4 = np.array((point[0], point[1], point[2], 1), dtype=np.float32)
            new_point = np.matmul(TR, point_4)
            trans_points[i] = np.array(
                [new_point[0], new_point[1], new_point[2], pcl_helper.float_to_rgb_hex_original(point[3])])
        rospy.loginfo("PointCloud received")

        pcl_pc.from_list(trans_points)
        self.list_of_pc.append(pcl_pc)
        rospy.loginfo("Point cloud appended")


if __name__ == "__main__":
    rospy.init_node("test_capture_py", anonymous=True)

    os.chdir('..')
    s = Sample(config.config())

    s.capture()

    time.sleep(2)

    s.capture()
    rospy.spin()
