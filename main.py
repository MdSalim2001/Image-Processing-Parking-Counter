import cv2
import pickle
import cvzone
import numpy as np

width = 107
height = 48

cap = cv2.VideoCapture('data/carPark.mp4')

with open('position', 'rb') as f:
        posList = pickle.load(f)

def checkParkingSpace(imgProc):
     counter = 0
     for pos in posList:
        x,y = pos
        
        imgCrop = imgProc[y:y+height, x:x+width]
        # cv2.imshow(str(x+y),imgCrop)
        count = cv2.countNonZero(imgCrop)
        

        if(count < 900):
            color = (0,255,0)
            thickness =5
            counter+=1
        else:
            color = (0,0,255)
            thickness = 2

        cv2.rectangle(img,pos ,(pos[0]+width,pos[1]+height),color,thickness)
     cvzone.putTextRect(img,f'Spaces: {str(counter)}/{len(posList)}',(100,50), scale= 3,thickness=5,offset=20,colorR=(0,0,0))
while True:

    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == cap.get(cv2.CAP_PROP_POS_FRAMES):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255 , cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 25,16)

    imgMedian = cv2.medianBlur(imgThreshold, 5)
    imgDialate = cv2.dilate(imgMedian, np.ones((3,3),np.uint8), iterations=1)
    
    checkParkingSpace(imgDialate)

    
    
    cv2.imshow("Image",img)
    # cv2.imshow("ImageG",imgGray)
    # cv2.imshow("ImageB",imgBlur)
    # cv2.imshow("ImageT",imgThreshold)
    # cv2.imshow("ImageM",imgDialate)
    cv2.waitKey(10)