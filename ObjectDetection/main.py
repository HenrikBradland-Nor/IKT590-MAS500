from ObjectDetection.preProsessing import dataPreProsessor
from ObjectDetection.graph import graphMaster
from suportFunctions import timer, system_init
from config import *
from ObjectDetection.NN import GCNN






DEVICE = system_init()
t = timer()


net = GCNN()
net.to(DEVICE)


if 'Load' in STATES:
    net.parameters()

opt = torch.optim.Adam(net.parameters())

for i, file_name in enumerate(os.listdir(DATA_PATH+'/label')):

    path_label = DATA_PATH+'/label/'+file_name
    path_data = DATA_PATH+'/pc/'+file_name

    t.resetTimer()
    dpp = dataPreProsessor(path_data)
    dpp.loadPC_XYZRGB()

    dpp.applyVoxelGrid_XYZRGB()
    dpp.computeNormalVectors()
    label = dpp.get_labels_forTrainng(path_label)
    x = dpp.pcl_to_pytorch()
    u, v = dpp.getKNN()

    t.timeStamp("Pre prosessing")
    gm = graphMaster()
    gm.newGrapgFromRelationVector(u, v)
    t.timeStamp("Graphing")
    t.printLog()
    t.emptyLog()

    graph = gm.getGraph()

    graph.ndata['feat'] = x
    graph.ndata['label'] = label

    train_id, val_id = dpp.getTrainValIDs()

    sampler = dgl.dataloading.MultiLayerFullNeighborSampler(4)
    dataloader = dgl.dataloading.NodeDataLoader(
        graph,
        train_id,
        sampler,
        batch_size=BATCH_SIZE
    )

    print(len(dataloader))

    for input_nodes, output_nodes, blocks in dataloader:
        blocks = [b.to(torch.device(DEVICE)) for b in blocks]
        input_features = blocks[0].srcdata['feat']
        output_labels = blocks[-1].dstdata['label']
        output_predictions = net(blocks, input_features)

        print("output_pred", output_predictions)
        print("output_label", output_labels)
        loss = nn.CrossEntropyLoss(output_labels, output_predictions)
        opt.zero_grad()
        loss.backward()
        opt.step()



if 'Train' in STATES:
    pass

if 'Test' in STATES:
    pass







