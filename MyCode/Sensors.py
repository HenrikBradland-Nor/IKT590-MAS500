import clr
import sys
import os
import time
# check whether python is running as 64bit or 32bit\n",
# to import the right .NET dll\n",
import platform
import numpy as np
import matplotlib.pyplot as plt

def short_array_to_numpy(height, width, frame):
    return np.fromiter(frame, dtype="uint16").reshape(height, width)

def centikelvin_to_celsius(t):
    return (t - 27315) / 100

class IR_CAM():
    def __init__(self):
        bits, name = platform.architecture()
        if bits == "64bit":
            folder = ["x64"]
        else:
            folder = ["x86"]

        sys.path.append(os.path.join("..", *folder))
        print(folder)

        os.chdir("..")
        os.chdir("Lepton-SDK_PureThermal_Windows10_1.0.2/" + folder[0])
        clr.AddReference("LeptonUVC")

        from Lepton import CCI

        found_device = None
        for device in CCI.GetDevices():
            if device.Name.startswith("PureThermal"):
                found_device = device
                break

        if not found_device:
            print("Error: Could not find device")
        else:
            self.lep = found_device.Open()
            print("Conected to device: " + found_device.Name)

        clr.AddReference("ManagedIR16Filters")
        from IR16Filters import IR16Capture, NewIR16FrameEvent, NewBytesFrameEvent


        self.capture = None

        from collections import deque

        self.incoming_frames = deque(maxlen=10)


        if not self.capture == None:
            self.capture.RunGraph()
        else:
            self.capture = IR16Capture()
            self.capture.SetupGraphWithBytesCallback(NewBytesFrameEvent(self.got_a_frame))
            self.capture.RunGraph()

        try:
            self.lep.rad.SetTLinearEnableStateChecked(True)
        except:
            print("Error: This camera does not suport tlinear")

    def got_a_frame(self, short_array, width, height):
        self.incoming_frames.append((height, width, short_array))

    def getUptime(self):
        uptime = self.lep.sys.GetCameraUpTime()
        print("Camera Uptime:", uptime, "\n")
        return uptime

    def takeImage(self, celsius=True, details=False):
        while len(self.incoming_frames) == 0:
            time.sleep(0.001)

        height, width, net_array = self.incoming_frames[-1]
        arr = short_array_to_numpy(height, width, net_array)

        if celsius:
            arr = centikelvin_to_celsius(arr)

        if details:
            print("image shape:", arr.shape)
            print("Max temperatur:", np.amax(arr))
            print("Min temperatur:", np.amin(arr))

        return arr

    def dispalyIMage(self):
        arr = self.takeImage()

        tmax = np.amax(arr)
        tmin = np.amin(arr)

        plt.imshow(arr)
        sm = plt.cm.ScalarMappable(norm=plt.Normalize(tmin, tmax))
        plt.colorbar(sm)
        plt.show()

# lep.sys.RunFFCNormalization()
# print("FFC performed", "\n")

#pallet = lep.vid.GetPcolorLut()
#print("Current colur pallet", pallet, "\n")

# while True:
#    pal = input()
#    lep.vid.SetPcolorLut(pal)









from matplotlib import cm



