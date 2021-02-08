import MyCode.Sensors as sens
import os




Lepton = sens.IR_CAM()


Lepton.takeImage(details=True)

Lepton.dispalyIMage()