import cv2
import handtrackingmodule as htm
import time
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
minvol = vol_range[0]
maxvol = vol_range[1]

cam = cv2.VideoCapture(0)
detector = htm.Handdetector(detectionconf=0.7)

vol = volper = 0
volbar = 400
while(cam.isOpened()):
    _,img = cam.read()
    img = detector.findhands(img)
    lmlist = detector.findposition(img,draw=False)
    try:
        x1,y1 = lmlist[4][1], lmlist[4][2]
        x2,y2 = lmlist[8][1], lmlist[8][2]
        cv2.circle(img,(x1,y1),10,(255,255,255),-1)
        cv2.circle(img,(x2,y2),10,(255,255,255),-1)
        cv2.line(img,(x1,y1),(x2,y2),(0,0,0),2)
        length = math.hypot(x2-x1, y2-y1)
        #1-213
        vol = np.interp(length,[1,200],[minvol,maxvol])
        volbar = np.interp(length,[1,200],[400,150])
        volper = np.interp(length,[1,200],[0,100])
        
        volume.SetMasterVolumeLevel(vol, None)

    except: 
        pass
    cv2.rectangle(img,(50,150),(85,400),(0,0,255),3)
    cv2.rectangle(img,(50,int(volbar)),(85,400),(0,255,0),-1)
    cv2.putText(img,f"{int(volper)} %",(40,50),cv2.FONT_ITALIC,1,(255,0,0),3)
    
    cv2.imshow('w',img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
# print(m1,m2)

cam.release()
cv2.destroyAllWindows()