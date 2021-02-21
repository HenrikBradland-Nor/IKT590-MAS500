from config import *
from suportFunctions import timer



class GCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = dglnn.EdgeConv(in_feat=X_FEATS, out_feat=H1_FEATS)
        self.conv2 = dglnn.EdgeConv(in_feat=H1_FEATS, out_feat=H2_FEATS)
        self.conv3 = dglnn.EdgeConv(in_feat=H2_FEATS, out_feat=H3_FEATS)
        self.conv4 = dglnn.EdgeConv(in_feat=H3_FEATS, out_feat=H4_FEATS)
        self.L1 = nn.Linear(in_features=H4_FEATS, out_features=L1_FEATS)
        self.L2 = nn.Linear(in_features=L1_FEATS, out_features=L2_FEATS)
        self.L3 = nn.Linear(in_features=L2_FEATS, out_features=CLASSES)
        self.SoftMax = nn.Softmax(dim=1)

    def forward(self, blocks, inputs):
        h = self.conv1(blocks[0], inputs)
        h = self.conv2(blocks[1], h)
        h = F.leaky_relu(h)
        # AvgPool/MaxPool ???

        h = self.conv3(blocks[2], h)
        h = self.conv4(blocks[3], h)
        h = F.leaky_relu(h)
        # AvgPool/MaxPool ???

        h = self.L1(h)
        h = self.L2(h)
        h = self.L3(h)
        out = self.SoftMax(h)
        return out
