from config import *
from dgl import knn_graph
from suportFunctions import timer, showPC
from dgl.nn.pytorch.factory import KNNGraph
from ObjectDetection.preProsessing import *
from ObjectDetection.graph import *
from ObjectDetection.NN import GCNN

dpp = dataPreProsessor(DATA_PATH+'/pc/001.pcd')



t = timer()
gr = graphMaster()

os.chdir('Code')

t.resetTimer()


dpp.getTrainValIDs()

dpp.loadPC_XYZRGB()
print("original size", dpp.getSize())
dpp.applyPassThroughFilter()
print("after ptf", dpp.getSize())
dpp.applyVoxelGrid_XYZRGB()
print("after vg", dpp.getSize())
t.resetTimer()
dpp.applyRandomReductionFilter()
print("after rrf", dpp.getSize())

t.timeStamp("rrf")
u, v = dpp.getKNN()
gr.newGrapgFromRelationVector(u, v)
t.timeStamp("knn new")

gr.printGraph()

t.printLog()


sys.exit()


dpp.applyVoxelGrid_XYZRGB()
dpp.computeNormalVectors()


t.timeStamp("Pre prosessing")



t.timeStamp("Graphing")
t.printLog()


net = GCNN()
opt = torch.optim.Adam(net.parameters())

net.train()

'''
for epoch in EPOCHS:
    with tqdm(train_loader, unit="batch") as tepoch:
'''


Y = net.forward(gr.getGraph(), X)








sys.exit()

k = 20

t = timer()

pc = tensor

t.timeStamp()
g = knn_graph(pc[:, :3], k)
g.ndata['feat'] = pc
t.timeStamp("Graph KNN 1:")


kg = KNNGraph(k)

g2 = kg(pc[:, :3])
g2.ndata['feat'] = pc
t.timeStamp("Graph KNN 2:")

t.printLog()



sys.exit()

nx_g = g.to_networkx().to_undirected()

pos = nx.kamada_kawai_layout(nx_g)
nx.draw(nx_g, pos, with_labels=True, node_color=[[.7, .7, .7]])

plt.show()

