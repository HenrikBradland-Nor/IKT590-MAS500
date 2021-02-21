from config import *


class dataPreProsessor:
    def __init__(self, path):
        self.path = path
        self.pc = pcl.PointCloud.PointXYZRGB()
        self.label_pc = pcl.PointCloud.PointXYZRGB()
        self.pc_normal = None
        self.dim = None

    def getKNN(self, k = GRAPH_K):
        kd = pcl.kdtree.KdTreeFLANN.PointXYZRGB()
        kd.setInputCloud(self.pc)
        k_i = pclpy.pcl.vectors.Int()
        k_s = pclpy.pcl.vectors.Float()
        u = 0
        edg_b = np.ones((self.pc.size() * k), dtype=int)
        edg_n = np.ones((self.pc.size() * k), dtype=int)
        for i, p in enumerate(self.pc.points):
            kd.nearestKSearch(p, k, k_i, k_s)
            for index in k_i:
                edg_b[u] = i
                edg_n[u] = index
                u += 1
        return torch.tensor(edg_n), torch.tensor(edg_b)

    def get_labels_forTrainng(self, label_path):
        reader = pcl.io.PCDReader()
        label_pc = pcl.PointCloud.PointXYZRGBL()
        reader.read(label_path, label_pc)
        label = np.zeros((label_pc.size(), CLASSES), dtype=np.float32)
        index = np.asarray(label_pc.label, dtype=int)
        for i, ind in enumerate(index):
            label[i][ind] = 1

        return torch.tensor(label, dtype=torch.float32)

    def loadPC_XYZRGB(self, filter=True):
        reader = pcl.io.PCDReader()
        reader.read(self.path, self.pc)
        if filter:
            ind = pclpy.pcl.vectors.Int()
            pcl.filters.removeNaNFromPointCloud(self.pc, self.pc, ind)
        self.dim =DIM_XYZRGBN

    def applyVoxelGrid_XYZRGB(self, leaf_size=LEAF_SIZE):
        vg = pcl.filters.VoxelGrid.PointXYZRGB()
        vg.setInputCloud(self.pc)
        vg.setLeafSize(leaf_size, leaf_size, leaf_size)
        vg.filter(self.pc)

    def applyPassThroughFilter(self, bound=Z_REFFERSNCE_PASSTHROUGH_FILTER):
        ptf = pcl.filters.PassThrough.PointXYZRGB()
        ptf.setInputCloud(self.pc)
        ptf.setFilterFieldName("z")
        ptf.setFilterLimits(bound[0], bound[1])
        ptf.filter(self.pc)

    def applyRandomReductionFilter(self):
        if self.getSize() > TARGET_GRAPH_SIZE:
            xyz = np.zeros((TARGET_GRAPH_SIZE, self.dim), dtype=np.float32)
            rgb = np.zeros((TARGET_GRAPH_SIZE, self.dim), dtype=np.uint8)
            for i, p in enumerate(np.random.choice(range(self.getSize()), TARGET_GRAPH_SIZE, replace=False)):
                xyz[i][0] = self.pc.points[p].x
                xyz[i][1] = self.pc.points[p].y
                xyz[i][2] = self.pc.points[p].z
                rgb[i][0] = self.pc.points[p].r
                rgb[i][1] = self.pc.points[p].g
                rgb[i][2] = self.pc.points[p].b
            self.pc = self.pc.from_array(xyz, rgb)

            '''Mulighet for å implementere raskere algoritme for random selection. Bare gi alle datapunkter en sansylighet for å bli inkludert i den nye pc'en (p > r).
            Metoden om er der nå beserer seg på å finne en liste med unike indexed, noe som gir mye kolisjoner og høy time-complexity.'''

        else:
            print("Point cloud (" + str(self.getSize()) + ") is smaller than target value (" + str(TARGET_GRAPH_SIZE) + ")")

    def pcl_to_pytorch(self):

        if self.pc_normal is None or not len(self.pc_normal) == self.getSize():
            self.computeNormalVectors()

        n = np.zeros((TARGET_GRAPH_SIZE, self.dim))
        g = 0
        if self.dim == 9:
            if self.getSize() > TARGET_GRAPH_SIZE:
                for i, p in enumerate(np.random.choice(range(self.getSize()), TARGET_GRAPH_SIZE, replace=False)):
                    n[i][0] = self.pc.points[p].x
                    n[i][1] = self.pc.points[p].y
                    n[i][2] = self.pc.points[p].z
                    n[i][3] = self.pc.points[p].r
                    n[i][4] = self.pc.points[p].g
                    n[i][5] = self.pc.points[p].b
                    n[i][6] = self.pc_normal[p][0]
                    n[i][7] = self.pc_normal[p][1]
                    n[i][8] = self.pc_normal[p][2]
                    if np.isnan(self.pc_normal[p][0]):
                        g += 1
            else:
                for i, p in enumerate(self.pc.points):
                    n[i][0] = p.x
                    n[i][1] = p.y
                    n[i][2] = p.z
                    n[i][3] = p.r
                    n[i][4] = p.g
                    n[i][5] = p.b
                    n[i][6] = self.pc_normal[i][0]
                    n[i][7] = self.pc_normal[i][1]
                    n[i][8] = self.pc_normal[i][2]
                    if np.isnan(self.pc_normal[i][0]):
                        g += 1
            if not g == 0:
                print("Number of Nan", g)
            return torch.tensor(n, dtype=DATA_TYPE)
        else:
            print("NOT SUPORTED OPPERATION!!")

    def computeNormalVectors(self):
        self.pc_normal = pclpy.compute_normals(self.pc, k=NORMAL_VECTOR_K)
        self.pc_normal = self.pc_normal.normals

    def printNormalVsPoint(self):
        i = random.randint(0, self.getSize() - 1)
        if self.pc_normal is None or not len(self.pc_normal) == self.getSize():
            self.computeNormalVectors()
        print(self.pc_normal[i])
        print(np.sqrt(self.pc_normal[i][0] ** 2 +
                      self.pc_normal[i][1] ** 2 +
                      self.pc_normal[i][2] ** 2))
        print(self.pc.xyz[i])

    def getTrainValIDs(self):
        n = range(0, self.getSize())
        train, val = train_test_split(n, train_size=DATA_SPLIT_RATIO)
        return train, val


    def getSize(self):
        return self.pc.size()

    def getPC(self):
        return self.pc
