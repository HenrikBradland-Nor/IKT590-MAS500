import numpy as np
import tf.transformations as tft

def batpiv(batpos,toolpos,from_z,from_yz):
    batpos = np.append(batpos, 0)
    piv_l = np.append(toolpos, 0)

    quart = tft.quaternion_from_euler(0, np.deg2rad(90 - from_z), np.deg2rad(from_yz), )  # sxyz
    rot = tft.euler_matrix(0, np.deg2rad(from_z), np.deg2rad(-from_yz), axes='rxyz')

    pos = (np.matmul(piv_l, rot))
    posw = pos + batpos
    return posw, quart

def batpiv_alt(batpos,toolpos,from_z,from_yz):
    batpos = np.append(batpos, 0)
    piv_l = np.append(toolpos, 0)
    #15.16
    quart = tft.quaternion_from_euler( np.deg2rad(90),from_z, np.deg2rad(from_yz), axes='syxz')  # sxyz
    rot = tft.euler_matrix(0, np.deg2rad(from_z), np.deg2rad(-from_yz), axes='rxyz')
    ### offset
    offset =np.array([0, 0.28643823000065208, 0.06414706542794772, 0])
    pos = (np.matmul(piv_l, rot))
    offset = (np.matmul(offset, rot))
    postest = pos - offset
    poswtest = postest + batpos
    posw = pos + batpos
    print('--------postest---------')
    print(poswtest)
    print('--------posw---------')
    print(posw)
    return posw, quart

def _batpiv_original(batpos,toolpos,from_z,from_yz):
    batpos = np.append(batpos, 0)
    piv_l = np.append(toolpos, 0)
    #print(piv_l)


    #piv_l = np.transpose(np.zeros(3))
    #piv_l[2] = toolpos[2] - batpos[2]

    #r = R.from_euler('z', 90, degrees=True)
    #r.as_quats()
    #r.as_rotvec()
    #r.as_dcm()
    #print (r.as_dcm())

    quart = tft.quaternion_from_euler(0, np.deg2rad(90-from_z), np.deg2rad(from_yz),axes='rxyz') # sxyz
    rot = tft.euler_matrix(0, np.deg2rad(from_z), np.deg2rad(-from_yz), axes='rxyz')

    #rot = euler_matrix(np.deg2rad(from_xz),np.deg2rad(-from_yz),0,'ryzx')

    #print(rot)
    #roty = np.identity(4)
    #roty = tf.rotation_matrix(np.deg2rad(90),(0,1,0))

    #print(rotytest)
    #ori = np.matmul(rot,roty)
    #test1 = np.matmul(roty, np.array([0,0,1,0]))
    #test2 = np.matmul(ori, np.array([0, 0, 1, 0]))

    #print('-------roty--------')
    #print(test1)
    #print('------------ori---------')
    #print(test2)
    #rot2 = euler_matrix(np.deg2rad(90-from_xz),np.deg2rad(-from_yz),0,'ryxz')
    #quat = quaternion_from_matrix(rot2)
    #rot = rot[0:3,0:3]
    pos = (np.matmul(piv_l, rot))

    print(pos)
    #piv_lz = np.transpose(np.zeros(3))
    #piv_lz[2] = toolpos[2] - batpos[2]
    #piv_ly = np.transpose(np.zeros(3))
    #piv_ly[1] = toolpos[2] - batpos[2]
    #print(piv_l)
    #posz = (np.matmul(piv_lz, rot))
    #posy = (np.matmul(piv_ly, rot))
    #xaks = np.array([1,0,0])
    #yaks = np.array([1,0,0])
    #ori = np.identity(4)
    #ori[0:3,0:3] = rotation_matrix_from_vectors(xaks, -1*pos)
    #yrot = (np.matmul(yaks, orix[0:3,0:3]))
    #ori = np.identity(4)
    #ori[0:3, 0:3] = rotation_matrix_from_vectors(posy, yrot)
    #oritot = np.matmul(oriy,orix)



    posw = pos + batpos
    #print (ori)
    #quats = quaternion_from_matrix(ori)
    #print('-----quatstest---')
    #print(quats)
    #quat = quaternion_from_euler(np.deg2rad(from_xz),(np.pi/2-np.deg2rad(from_yz)),0, 'rzyx')

    #rot2 = np.matmul(Ry(alpha), Rz(beta))
    #rot_for_quat = np.matmul(rot2,Ry(theta))
    #print(R.from_matrix(Ry(theta)))
    #r = R.from_matrix(rot_for_quat)
    #r = R.from_matrix(rot)
    #quat = r.as_quat()

    #ql = np.zeros(4)
    #ql[0:4] = quart
    #ql = np.append(ql, posw)
    #qltest = np.zeros(4)
    #qltest[0:4] = quats
    #qltest = np.append(qltest, posw)

    return quart, posw

if __name__ == '__main__':
    batpos = np.array([3.4, 6.55, 0.3])
    toolpos = np.array([0, 0, 0.6])
    ql = batpiv(batpos,toolpos,20,-20)
    print('---------ql--------')
    print(ql)

#ql = batpiv(batpos,toolpos,-20,20)
#print(ql)
#print(pos)
#print('------------ Rx alpha')
#print(alpha)
#print(Rx(alpha))
#print('-------------- Rz beta')
#print(beta)
#print(Rz(beta))
#print('---------------- R_piv')
#print(R_piv(alpha,beta))
#print(np.dot(Rx(alpha), Rz(beta)))
#print(batpiv(batpos,toolpos,alpha,beta))
#print(R.from_matrix(R_piv(alpha,beta)))
#print(Rz(beta)*Rx(alpha))

#v = np.matmul(batpos, toolpos)
#u = np.dot(batpos, toolpos)
#w = np.cross(batpos, toolpos)
#q = np.linalg.

#print(v)
#print(u)
#print(w)