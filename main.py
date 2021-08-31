import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

cap = cv.VideoCapture(0)
cap.set(3,1230)
cap.set(4,720)
detector = HandDetector(detectionCon=0.8)
colorR = (255,0,255)

cx ,cy , w, h = 100, 100, 200 ,200


class DragRect():
    def __init__(self,posCenter,size=[200,200]):
        self.posCenter = posCenter
        self.size = size

    def update(self,cursor):
        cx , cy = self.posCenter
        w , h = self.size

        # if the index finger tip is in the rectangle region
        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            self.posCenter = cursor

rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+120,150]))

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    img = detector.findHands(img)
    lmlist , _ = detector.findPosition(img)
    
    if lmlist:

        l , _ , _ = detector.findDistance(8,12,img, draw = False)
        print(l)

        if l<50:
            cursor = lmlist[8] # index fingure tip landmark

            # call the update here
            for rect in rectList:
                rect.update(cursor)

        # to Draw solid rect
        # for rect in rectList: 
        #     cx , cy = rect.posCenter
        #     w , h = rect.size
        #     cv.rectangle(img , (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv.FILLED)
    
        #     cvzone.cornerRect(img, (cx-w//2, cy-h//2, w, h), 20, rt=0)

    # draw transperant rect
    imgNew = np.zeros_like(img,np.uint8)
    for rect in rectList: 
        cx , cy = rect.posCenter
        w , h = rect.size
        cv.rectangle(imgNew , (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv.FILLED)

        cvzone.cornerRect(imgNew, (cx-w//2, cy-h//2, w, h), 20, rt=0)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    # print(mask.shape)
    out[mask] = cv.addWeighted(img, alpha, imgNew, 1 - alpha , 0)[mask]

    cv.imshow('image', out)
    if cv.waitKey(1) & 0xFF == ord('d'):
        break
    cv.waitKey(1)