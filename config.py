# LIBs

import dgl
import dgl.nn as dglnn
import pclpy
from time import time
import networkx as nx
from pclpy import pcl
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
import sys
import matplotlib.pyplot as plt
import random
import tqdm
from sklearn.model_selection import train_test_split


# Global

STATES = ['Train', 'Test', 'PrePros']
DATA_TYPE = torch.float32

# Data
DATA_PATH = 'Code/data/train'
DATA_ATTRIBUTES = ['rgb', 'xyz', 'normal']
DATA_LABELS = ['background', 'cable']
DIM_XYZRGBN = 9

# Pre prosessing
LEAF_SIZE = 2
NORMAL_VECTOR_K = 8
Z_REFFERSNCE_PASSTHROUGH_FILTER = [0, 1900]

# Graph
GRAPH_K = 20
TARGET_GRAPH_SIZE = 50000


# Neural Network
X_FEATS = len(DATA_ATTRIBUTES)*3
H1_FEATS = 64
H2_FEATS = 64
H3_FEATS = 64
H4_FEATS = 64
L1_FEATS = 512
L2_FEATS = 256
CLASSES = len(DATA_LABELS)

# Training
SUPORTS_CUDA = None
DEVICE = None

DATA_SPLIT_RATIO = 0.8

BATCH_SIZE = 1024

EPOCHS = 10



