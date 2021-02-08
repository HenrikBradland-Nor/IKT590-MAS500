import clr
import sys
import os
import time
# check whether python is running as 64bit or 32bit\n",
# to import the right .NET dll\n",
import platform



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
    lep = found_device.Open()
    print("Conected to device: " + found_device.Name)

def getUptime():
    uptime = lep.sys.GetCameraUpTime()
    print("Camera Uptime:", uptime, "\n")
    return uptime
#lep.sys.RunFFCNormalization()
#print("FFC performed", "\n")

pallet = lep.vid.GetPcolorLut()
print("Current colur pallet", pallet, "\n")

#while True:
#    pal = input()
#    lep.vid.SetPcolorLut(pal)

clr.AddReference("ManagedIR16Filters")
from IR16Filters import IR16Capture, NewIR16FrameEvent, NewBytesFrameEvent

import numpy as np
import matplotlib.pyplot as plt

capture = None

from collections import deque

incoming_frames = deque(maxlen=10)
def got_a_frame(short_array, width, height):
    incoming_frames.append((height, width, short_array))

if not capture == None:
    capture.RunGraph()
else:
    capture = IR16Capture()
    capture.SetupGraphWithBytesCallback(NewBytesFrameEvent(got_a_frame))
    capture.RunGraph()

def short_array_to_numpy(height, width, frame):
    return np.fromiter(frame, dtype="uint16").reshape(height, width)

from matplotlib import cm




while len(incoming_frames) == 0:
    time.sleep(0.001)
# To enshure that there is a frame to use


height, width, net_array = incoming_frames[-1]
arr = short_array_to_numpy(height, width, net_array)


try:
    lep.rad.SetTLinearEnableStateChecked(True)
    print("This camera suports tlinear")
except:
    print("Error: This camera does not suport tlinear")

def centikelvin_to_celsius(t):
    return (t - 27315)/100


arr = centikelvin_to_celsius(arr)

print("image shape:", arr.shape)

tmax = np.amax(arr)
tmin = np.amin(arr)

print("Max temperatur:", tmax)
print("Min temperatur:", tmin)


print("\n\n")
print(centikelvin_to_celsius(lep.sys.GetAuxTemperatureKelvin()))

plt.imshow(arr)
sm = plt.cm.ScalarMappable(norm=plt.Normalize(tmin,tmax))
plt.colorbar(sm)
plt.show()
