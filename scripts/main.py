from robot import capture_point_cloud
from pointCloudFunctions import *
import time
import os
import config



def super_print(a, b=None):
    print(" ")
    if b is None:
        print(str(a))
    else:
        print(str(a) + " " + str(b))
    print(" ")


def main():
    os.chdir('..')

    cfg = config.config()


    prosess1 = capture_point_cloud(cfg)
    prosess1.run_robot()

    time.sleep(1)

    pc = prosess1.get_captured_point_clouds()

    print(" ")
    print(50 * '=')
    print('Number of PointClouds taken:', len(pc))
    print(50 * '-')

    for i, p in enumerate(pc):
        print("PointCloud number:", i)
        print("Size:", p.size)
        print(50 * '-')

    super_pc = pc_combo(pc, cfg)

    pc_id = str(len(os.listdir('PC/super_test')))
    path = 'PC/super_test/' + pc_id + '.ply'
    pcl.save(super_pc, path)
    pc_id = str(1+len(os.listdir('PC/final_pc_ascii')))
    path = 'PC/final_pc_ascii/' + pc_id + '.pcd'
    pcl.save(super_pc, path, binary=False)

    print("New super PointCloud")
    print("Size:", super_pc.size)
    print("Saved to:", path)

    print(50 * '=')
    print(" ")

    visualisePointcloud(super_pc)


if __name__ == '__main__':
    main()
