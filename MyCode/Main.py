import MyCode.Sensors as sens
import pcl
import os


print(os.getcwd())
p = pcl.PointCloud()


Lepton = sens.IR_CAM()


Lepton.takeImage(details=True)