import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
import math


##################################
brushThickness = 15
eraserThickness = 50
mode = "select"
##################################

folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
drawColor = (255, 0, 255)

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

header = overlayList[0]

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = htm.handDetector(detectionCon = 0.65) # 높은 디텍팅 신뢰도 - 그림을 잘그리기 위해서
xp , yp = 0, 0
imgCanvas = np.zeros((480, 640, 3), np.uint8) # 640*480 크기의 3가지 색상 채널을 갖는 8비트 부호없는 정수(unsigned integer 8bit - 0 ~ 255값을 가지므로 거의 모든것을 표현할 수 있다.)

fingers = [8, 12]

while True:
    # 1. Import image 
    success, img = cap.read()
    
    img = cv2.flip(img, 1) # img를 1번 방향(좌우)로 반전 - 캠상에서 그림을 그리면 반대로 움직이기 때문에 좌우 반전을 준다. 
    
    
    
    # 2. Find Hand Landmarks
    img = detector.findHands(img) # img를 findHands 매소드에 담으면 손 좌표를 이은 img를 얻을 수 있다.
    
    lmList, bbox = detector.findPosition(img, draw = False) # img를 findPosition 매소드에 담으면 손좌표에 커다란 점을 찍어준다. draw = False로 하면 화면에 표시되지는 않는다. 그리고 이 21개 점들의 좌표를 (id, x좌표, y좌표)형태로 lmList에 담아 반환해준다.
    
    if len(lmList) != 0 :
        
        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        
        # length between index and middle fingers
        # length = math.hypot(x1-x2, y1-y2)
        
        # if length < 40 :
        #     cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
    
        # 3. Check which fingers are up
    
        fingers = detector.fingersUp() # fingersUp() 메소드를 호출하면 펼쳐져있는 손가락의 갯수를 세서 반환해 준다.
        # print(fingers)
    
        # 4. If Selection mode - Two fingers are up
        if fingers[1] and fingers[2]:
            cv2.rectangle(img, (x1, y1-25),(x2, y2+25), drawColor, cv2.FILLED)
            # print("Selection Mode")
            # mode = "select"
            xp, yp = 0, 0
            # Checking for the click
            # print (x1, y1)
            if y1 < 62 :
                if 160 < x1 < 210:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 185 < x1 < 335:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 405 < x1 < 455:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 520 < x1 < 600:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
                
    
        # 5. If Drawing Mode - Index finger is up
        if fingers[1] and fingers[2] == False :
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            # print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

                
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)            
            else :    
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)            
            xp, yp = x1, y1
    
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)        
    # _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV) # 문제 발생 : 파란색이 제대로 표현이 안된다. 해결 : 50 -> 20 바꿔준다.
    _, imgInv = cv2.threshold(imgGray, 20, 255, cv2.THRESH_BINARY_INV)
    # imgIn = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    
    img = cv2.bitwise_and(img, imgInv) # img와 imgInv의 중복되는 부분을 합친다.
    img = cv2.bitwise_or(img, imgCanvas) # img와 imgCanvas의 중복되지 않는 부분을 합친다?
    
    
    # Setting the header image
    img[0:62, 0:640] = header
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0) # 두개의 이미지를 0.5씩 혼합하여 img에 넣어준다. 감마값은 0으로 하여 이미지를 주지 않는다.
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.imshow("gray", imgInv)
    # cv2.imshow("Inv", imgIn)
    cv2.waitKey(1)
    