import cv2
import pickle



width = 107
height = 48
try:
    with open('position', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # print(x,y)
        posList.append((x,y))
    if event == cv2.EVENT_RBUTTONDOWN:
        # print("Right Click")
        for i, pos in enumerate(posList):
            x1,y1 = pos
            if x < x1+width and x > x1 and y < y1+height and y > y1:
                posList.pop(i)
    
    with open('position', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread('data/carParkImg.png')
    for pos in posList:
        cv2.rectangle(img,pos ,(pos[0]+width,pos[1]+height),(0,255,0),2)

    cv2.imshow("Image",img)
    cv2.setMouseCallback('Image',mouseClick)
    cv2.waitKey(1)