import pcl
import pcl.pcl_visualization
import numpy as np
from config import config



def pc_combo(list_of_pc, cfg):
    pcl_pc = pcl.PointCloud_PointXYZRGB()

    new_pc = np.zeros((1,4), dtype=np.float32)
    for pc in list_of_pc:
        pc_npy = pc.to_array()
        new_pc = np.append(new_pc, pc_npy, axis=0)
    pcl_pc.from_list(new_pc[1:,:])

    #Filtering
    passthrough = pcl_pc.make_passthrough_filter()
    passthrough.set_filter_field_name("z")
    passthrough.set_filter_limits(cfg.pallet_height, cfg.max_work_space_z)
    pcl_pc = passthrough.filter()

    passthrough = pcl_pc.make_passthrough_filter()
    passthrough.set_filter_field_name("x")
    passthrough.set_filter_limits(cfg.batteri_pos_x - cfg.batteri_length_x/2, cfg.batteri_pos_x + cfg.batteri_length_x/2)
    pcl_pc = passthrough.filter()

    passthrough = pcl_pc.make_passthrough_filter()
    passthrough.set_filter_field_name("y")
    passthrough.set_filter_limits(cfg.batteri_pos_y - cfg.batteri_length_y/2, cfg.batteri_pos_y + cfg.batteri_length_y/2)
    pcl_pc = passthrough.filter()

    voxel_filter = pcl_pc.make_voxel_grid_filter()
    voxel_filter.set_leaf_size(cfg.voxel_grid_leaf_size, cfg.voxel_grid_leaf_size, cfg.voxel_grid_leaf_size)
    pcl_pc = voxel_filter.filter()





    print(pcl_pc.size)

    return pcl_pc

def visualisePointcloud(pc):
    visual = pcl.pcl_visualization.CloudViewing()
    visual.ShowColorCloud(pc)
    v = True
    while v:
        v = not (visual.WasStopped())