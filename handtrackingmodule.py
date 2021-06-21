import cv2
import mediapipe as mp
import time

class Handdetector():
    def __init__(self,mode=False,maxHands = 2,detectionconf = 0.5, trackconf = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionconf = detectionconf
        self.trackconf = trackconf
    
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode,self.maxHands,self.detectionconf,self.trackconf)
        self.mpdraw = mp.solutions.drawing_utils
    
    def findhands(self,img, draw = True):
        img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(img_rgb)
        # print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:
            for handlms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img,handlms,self.mphands.HAND_CONNECTIONS)

        return img

    def findposition(self,img, handno=0, draw = True):
        lmlist = []
        if self.result.multi_hand_landmarks:
            myhand = self.result.multi_hand_landmarks[handno]
            for id,lm in enumerate(myhand.landmark):
                    h,w,c = img.shape
                    cx,cy = int(lm.x*w), int(lm.y*h)
                    lmlist.append([id,cx,cy])
        return lmlist

def main():
    pTime = 0
    cTime = 0
    cam = cv2.VideoCapture(0)
    detector = Handdetector()
    while(True):
        _,img = cam.read()
        detector.findhands(img)
        lmlist = detector.findposition(img)
        # if len(lmlist)!=0:
        #     print(lmlist[0])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_ITALIC,1,(255,0,255),2)
        cv2.imshow('w',img)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    main()