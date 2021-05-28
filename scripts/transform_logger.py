import numpy as np
import rospy
import tf
import time
import tf.transformations as tft
import matplotlib.pyplot as plt
import math

def trans_logger():
    listner = tf.TransformListener()
    listner.waitForTransform('/world', '/zivid_optical_frame', rospy.Time(0), rospy.Duration(1.0))
    (cam_pos) = listner.lookupTransform('/world', '/zivid_optical_frame', rospy.Time(0))
    return cam_pos


if __name__ == "__main__":

    print(math.atan(0.0007/1.955))



    rospy.init_node("transform_logger", anonymous=True)
    x = []
    logg_pos = []
    logg_ang = []

    for i in range(1000):
        x.append(i)
        pos, ang = trans_logger()

        ang = tft.euler_from_quaternion(ang)

        logg_ang.append(ang)
        logg_pos.append(pos)
        # time.sleep(.01)

        if i % 100 == 0:
            print(i / 10, "%")

    logg_pos = np.asarray(logg_pos)
    logg_ang = np.asarray(logg_ang)

    f, ax = plt.subplots(6)

    ax[0].scatter(x, logg_pos[:, 0])
    ax[1].scatter(x, logg_pos[:, 1])
    ax[2].scatter(x, logg_pos[:, 2])
    ax[3].scatter(x, logg_ang[:, 0])
    ax[4].scatter(x, logg_ang[:, 1])
    ax[5].scatter(x, logg_ang[:, 2])

    plt.show()
