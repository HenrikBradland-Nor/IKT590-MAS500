
import tf.transformations
import numpy as np
import batpiv as bp
class config:
    def __init__(self):
        # Sceen parameters

        # small battery .18
        # big battery .22
        self.pallet_height = .18
        self.max_work_space_z = .75

        self.batteri_pos_x = 3.6
        # big battery batteri_pos_y = 5.1
        # small battery batteri_pos_y = 6.5
        self.batteri_pos_y = 6.5

        self.batteri_length_x = 1.0
        #Big battery batteri_length_y = 2.3
        # small battery batteri_length_y = 1.2
        self.batteri_length_y = 1.2

        self.min_image_depth = 0.6
        self.max_image_depth = 1.6


        # Filtering
        self.voxel_grid_leaf_size = 0.001



        #### POINTS
        self.p1 = point([3.3, 6.3, 0.90], [1.3087151694609415, 1.1710170611405144, 1.32071516512365])
        self.p2 = point([3.2, 6.45, 0.90], [0.21155554664879492, 1.2930785482720229, 0.2258100592267419])
        self.p3 = point([3.3, 6.70, 0.90], [-0.656599232586658, 1.396548903822593, -0.6])
        self.p4 = point([3.3, 5, 0.90], [-0.656599232586658, 1.396548903822593, -0.6])
        #pos og quats
        self.p5 = point([3.2, 6.5, 0.90], [0, 3.14/2, 0])#[0.0, 0.707, 0.0, 0.707])
        self.p6 = point([3.5, 6.1, 0.90], [-2.326, 1.304, 3.103]) # [0.2266783436574, 0.7341654354535, 0.304734543545, 0.562843545345345])
        self.p7 = point([3.4, 6.5, 0.50], [np.deg2rad(-45), np.deg2rad(60), np.deg2rad(45)])
        self.p8 = point([3.4, 6.5, 0.50], [np.deg2rad(0), np.deg2rad(60), np.deg2rad(45)])
        self.p9 = point([3.4, 6.5, 0.50], [np.deg2rad(0), np.deg2rad(90-20), np.deg2rad(20)])


        #### Ponts for taking picture of large battery.
        #squence 1
        self.bp1 = point(bp.batpiv([3.4, 5.1, 0.3], [0, 0, 0.3], 30, 45))
        self.bp2 = point(bp.batpiv([3.4, 5.1, 0.3], [0, 0, 0.3], -30, -20))
        self.bp3 = point(bp.batpiv([3.4, 5.3, 0.3], [0, 0, 0.3], -30, 20))
        self.bp4 = point(bp.batpiv([3.4, 5.3, 0.3], [0, 0, 0.3], 30, -45))
        # big bat sequence 2
        self.bp5 = point(bp.batpiv([3.5, 5.1, 0.3], [0, 0, 0.0], 25, -45))
        self.bp6 = point(bp.batpiv([3.5, 5.1, 0.3], [0, 0, 0.0], 20, 0))
        self.bp7 = point(bp.batpiv([3.5, 4.8, 0.3], [0, 0, 0.0], 20, 0))
        self.bp8 = point(bp.batpiv([3.5, 4.5, 0.3], [0, 0, 0.0], 20, 0))
        self.bp9 = point(bp.batpiv([3.5, 4.5, 0.3], [0, 0, 0.0], -20, 0))
        self.bp10 = point(bp.batpiv([3.5, 4.8, 0.3], [0, 0, 0.0], -20, 0))
        self.bp11 = point(bp.batpiv([3.5, 5.1, 0.3], [0, 0, 0.0], -20, 0))
        self.bp12 = point(bp.batpiv([3.5, 5.1, 0.3], [0, 0, 0.0], -20, 45))
        # small bat sequence 2
        # self.bp13 = point(bp.batpiv([3.4, 6.5, 0.4], [0, 0, 0.0], 0, 0))
        #self.bpsb1 = point(bp.batpiv([3.5, 6.7, 0.25], [0, 0, 0.0],-0,0))
        #self.bpsb2 = point(bp.batpiv([3.5, 6.3, 0.25], [0, 0, 0.0], -25, 0))
        #self.bpsb3 = point(bp.batpiv([3.5, 6.2, 0.20], [0, 0, 0.0], -40, -60))
        #self.bpsb4 = point(bp.batpiv([3.3, 6.2, 0.20], [0, 0, 0.0], -40, -90))
        #self.bpsb5 = point(bp.batpiv([3.3, 6.4, 0.25], [0, 0, 0.0], -60, -130))
        #self.bpsb6 = point(bp.batpiv([3.4, 6.4, 0.25], [0, 0, 0.0], -50, -180))
        #self.bpsb7 = point(bp.batpiv([3.45, 6.6, 0.25], [0, 0, 0.0], -50, 130))
        #self.bpsb8 = point(bp.batpiv([3.3, 6.3, 0.25], [0, 0, 0.0], 20, 0))

        #self.bpsb9 = point(bp.batpiv([3.4, 6.4, 0.3], [0, 0, 0], -30, -130))
        #self.bpsb10 = point(bp.batpiv([3.4, 6.4, 0.3], [0, 0, 0], -20, -20))
        #self.bpsb11 = point(bp.batpiv([3.4, 6.2, 0.3], [0, 0, 0], -30, 20))
        #self.bpsb12 = point(bp.batpiv([3.4, 6.3, 0.3], [0, 0, 0], -30, 130))

        #big bat seq
        #self.bpbb1 = point(bp.batpiv([3.5, 5, 0.3], [0, 0, 0], -30, 45))
        #self.bpbb2 = point(bp.batpiv([3.5, 5, 0.3], [0, 0, 0], -30, -45))
        #self.bpbb3 = point(bp.batpiv([3.5, 5, 0.3], [0, 0, 0], -30, -130))
        #self.bpbb4 = point(bp.batpiv([3.5, 5, 0.3], [0, 0, 0], -30, 130))
        #self.bpbb1 = point(bp.batpiv([3.5, 5.3, 0.3], [0, 0, 0], -30, 45))
        #self.bpbb2 = point(bp.batpiv([3.5, 5.3, 0.3], [0, 0, 0], -30, 0))
        #self.bpbb3 = point(bp.batpiv([3.5, 4.9, 0.3], [0, 0, 0], -30, 0))
        #self.bpbb4 = point(bp.batpiv([3.5, 4.6, 0.3], [0, 0, 0], -30, -45))
        #self.bpbb5 = point(bp.batpiv([3.4, 4.6, 0.3], [0, 0, 0], 30, 45))
        #self.bpbb6 = point(bp.batpiv([3.4, 5, 0.3], [0, 0, 0], 30, 0))
        #self.bpbb7 = point(bp.batpiv([3.4, 5, 0.3], [0, 0, 0], 30, -45))
        #self.bpbb1 = point(bp.batpiv([3.5, 6.5, 0.3], [0, 0, 0], -30, 0))
        #self.bpbb2 = point(bp.batpiv([3.4, 6.5, 0.3], [0, 0, 0], -30, -90))
        #self.bpbb3 = point(bp.batpiv([3.5, 6.5, 0.3], [0, 0, 0], 30, 0))
        #self.bpbb4 = point(bp.batpiv([3.65, 6.5, 0.3], [0, 0, 0], -30, 90))
        #self.bpbb5 = point(bp.batpiv([3.5, 6.5, 0.3], [0, 0, 0], 0, 0))

        #self.bpbb1 = point(bp.batpiv([3.5, 5, 0.3], [0, 0, 0], -45, 90))
        #self.bpbb2 = point(bp.batpiv([3.5, 5, 0.3], [0, 0, 0], -45, 45))
        #self.bpbb3 = point(bp.batpiv([3.5, 5, 0.3], [0, 0, 0], -20, 0))
        #self.bpbb4 = point(bp.batpiv([3.5, 5, 0.3], [0, 0, 0], -45, -45))
        #self.bpbb5 = point(bp.batpiv([3.5, 5, 0.3], [0, 0, 0], -45, -90))
        #self.bpbb6 = point(bp.batpiv([3.5, 5, 0.3], [0, 0, 0], -45, 180))

        #self.bpsb1 = point(bp.batpiv([3.55, 6, 0.1], [0, 0, 0], 0, 0))
        #self.bpsb1 = point(bp.batpiv([3.7, 6, 0.1], [0, 0, 0], 30, 0))
        #self.bpsb2 = point(bp.batpiv([3.40, 6, 0.1], [0, 0, 0], -30, 0))
        #self.bpsb3 = point(bp.batpiv([3.55, 6.3, 0.1], [0, 0, 0], -30, -90))
        #self.bpsb4 = point(bp.batpiv([3.55, 6.1, 0.1], [0, 0, 0], 30, -90))

        #self.bpsb1 = point(bp.batpiv([3.5, 6.1, 0.1], [0, 0, 0], 0, 0))
        #self.bpsb2 = point(bp.batpiv([3.5, 6.5, 0.1], [0, 0, 0], 0, 0))
        #self.bpsb3 = point(bp.batpiv([3.2, 6.5, 0.1], [0, 0, 0], 0, 0))
        #self.bpsb4 = point(bp.batpiv([3.2, 6.1, 0.1], [0, 0, 0], 0, 0))



        self.bpsb1 = point(bp.batpiv([3.7, 6, 0.1], [0, 0, 0], 30, 0))
        self.bpsb2 = point(bp.batpiv([3.45, 6.05, 0.1], [0, 0, 0], -30, 33.3))
        self.bpsb3 = point(bp.batpiv([3.45, 6, 0.1], [0, 0, 0], -30, -33.3))

        #self.bpsb4 = point(bp.batpiv([3.7, 6.4, 0.1], [0, 0, 0], 30, 0))
        #self.bpsb5 = point(bp.batpiv([3.45, 6.45, 0.1], [0, 0, 0], -30, 33.3))
        #self.bpsb6 = point(bp.batpiv([3.45, 6.4, 0.1], [0, 0, 0], -30, -33.3))

        #self.bpsb1 = point(bp.batpiv([3.7, 6, 0.1], [0, 0, 0], 30, 0))
        #self.bpsb2 = point(bp.batpiv([3.45, 6.05, 0.1], [0, 0, 0], -30, 33.3))
        #self.bpsb3 = point(bp.batpiv([3.45, 6, 0.1], [0, 0, 0], -30, -33.3))

        #self.bpsb4 = point(bp.batpiv([3.55, 6.1, 0.1], [0, 0, 0], 30, -90))

        #self.bpsb1 = point(bp.batpiv([3.2, 6.35, 0.3], [0, 0, 0], 20, 0))
        #self.bpsb2 = point(bp.batpiv([3.4, 6.35, 0.3], [0, 0, 0], -20, 0))

        #self.bpsb1 = point(bp.batpiv([3.2, 6.6, 0.3], [0, 0, 0], 20, 0))
        #self.bpsb2 = point(bp.batpiv([3.2, 6.1, 0.3], [0, 0, 0], 20, 0))
        #self.bpsb3 = point(bp.batpiv([3.4, 6.6, 0.3], [0, 0, 0], -20, 0))
        #self.bpsb4 = point(bp.batpiv([3.4, 6.1, 0.3], [0, 0, 0], -20, 0))

        #self.bpsb1 = point(bp.batpiv([3.55, 6.5, 0.3], [0, 0, 0], -20, 30))
        #self.bpsb1 = point(bp.batpiv([3.45, 6.1, 0.3], [0, 0, 0], -20, -30))

        #self.bpsb2 = point(bp.batpiv([3.5, 6.3, 0.3], [0, 0, 0], 30, 0))
        #self.bpsb3 = point(bp.batpiv([3.5, 5.3, 0.3], [0, 0, 0], 30, 0))
        #self.bpsb4 = point(bp.batpiv([3.5, 4.5, 0.3], [0, 0, 0], -20, 0))
        #self.bpsb5 = point(bp.batpiv([3.5, 5, 0.3], [0, 0, 0], -20, 0))
        #self.bpsb6 = point(bp.batpiv([3.5, 5.3, 0.3], [0, 0, 0], -20, 0))

        #self.bpbb1 = point(bp.batpiv([3.6, 5, 0.3], [0, 0, 0], 0, 0))
        #self.bpbb2 = point(bp.batpiv([3.6, 5, 0.3], [0, 0, 0], -30, 0))


class point:
    def __init__(self, pos, ang=None):

        if len(pos) == 2:
            ang = pos[1]
            pos = pos[0]

        self.pos = pos

        if len(ang) == 3:
            self.ang = ang
            self.quart = tf.transformations.quaternion_from_euler(ang[0], ang[1], ang[2])
        elif len(ang) == 4:
            self.ang = tf.transformations.euler_from_quaternion(ang)
            self.quart = ang
        else:
            Exception('Wrong format of ang')

        self.q = np.array((self.quart[0], self.quart[1], self.quart[2], self.quart[3],
                           self.pos[0], self.pos[1], self.pos[2]))