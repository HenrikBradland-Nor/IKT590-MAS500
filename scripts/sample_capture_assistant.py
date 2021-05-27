#!/usr/bin/env python

import rospy
import rosnode
from zivid_camera.srv import *
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2, Image
from sensor_msgs import point_cloud2 as pc2
import time
import pcl
from pointCloudFunctions import *


class Sample:
    def __init__(self):
        self.pc = pcl.PointCloud_PointXYZRGB()
        rospy.init_node("sample_capture_assistant_py", anonymous=True)

        rospy.loginfo("Starting sample_capture_assistant.py")

        ca_suggest_settings_service = "/zivid_camera/capture_assistant/suggest_settings"

        rospy.wait_for_service(ca_suggest_settings_service, 30.0)

        self.capture_assistant_service = rospy.ServiceProxy(
            ca_suggest_settings_service, CaptureAssistantSuggestSettings
        )
        self.capture_service = rospy.ServiceProxy("/zivid_camera/capture", Capture)

        rospy.Subscriber("/zivid_camera/points", PointCloud2, self.on_points)
        rospy.Subscriber("/zivid_camera/color/image_color", Image, self.on_image_color)

    def capture_assistant_suggest_settings(self):
        max_capture_time = rospy.Duration.from_sec(1.20)
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
        rospy.loginfo("PointCloud received")
        point_list = list([x for x in pc2.read_points(data, skip_nans=True, field_names=["x", "y", "z", "rgb"])])
        self.pc.from_list(point_list)


    def on_image_color(self, data):
        rospy.loginfo("2D color image received")


if __name__ == "__main__":
    s = Sample()
    s.capture_assistant_suggest_settings()
    s.capture()
    time.sleep(20)
    visualisePointcloud(s.pc)


