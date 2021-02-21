import pclpy.pcl as pcl
import pclpy
from ObjectDetection import preProsessing

import os
import sys

reader = pcl.io.PCDReader()
writer = pcl.io.PCDWriter()
pc = pcl.PointCloud.PointXYZRGB()




os.chdir("PC-test/2_cabels")

for path in os.listdir("bin"):
    _, __, n = path.split('_')

    path_in = "bin/"+path
    path_out = "ASCII/"+n

    dpp = preProsessing.dataPreProsessor(path_in)
    dpp.loadPC_XYZRGB()
    dpp.applyPassThroughFilter()
    dpp.applyVoxelGrid_XYZRGB()
    dpp.applyRandomReductionFilter()
    print(path_in)
    print(path_out)

    writer.writeASCII(path_out, dpp.getPC())