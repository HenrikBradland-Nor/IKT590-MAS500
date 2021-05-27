import pcl
import numpy as np
import tf
import tf.transformations as tft
import time

pcl_pc = pcl.PointCloud_PointXYZRGBA()

dir_path = "/home/dev/LIBRES_SYS/LIBRES_SYS/PC_for_rotation/rotations"

load_path = dir_path + "/45" + ".pcd"
save_path = dir_path + "/45_50x100y20z_trans000" + ".pcd"
pcl_pc.from_file(load_path)

point_list = pcl_pc.to_array()

trans_points = np.zeros((len(point_list), 4), dtype=np.float32)


R = tft.euler_matrix(np.rad2deg(50), np.rad2deg(100), np.rad2deg(20), axes='sxyz')
T = tft.translation_matrix([0,0,0])
TR = R + T - np.identity(4)
print('Matrix generated')
for i, point in enumerate(point_list):
    point_4 = np.array((point[0], point[1], point[2], 1), dtype=np.float32)
    new_point = np.matmul(TR, point_4)
    trans_points[i] = np.array(
        [new_point[0], new_point[1], new_point[2], point[3]])

pcl_pc.from_list(trans_points)

pcl.save(pcl_pc, save_path, binary=False)