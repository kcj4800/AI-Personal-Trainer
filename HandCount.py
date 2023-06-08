import cv2
import time
import os
import HandTrackingModule as htm
import math



wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "FingerImages"
myList = os.listdir(folderPath)
# print(myList)
# exit()
overlayList = []

cTime = 0
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]


for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)
    
# print(len(overlayList))
while True :
    success, img = cap.read()
    
    img = detector.findHands(img) # img를 findHands 메소드에 넣으면, 손가락 좌표가 입력된 img를 반환한다. 이를 img에 담아준다. 이때 draw = False라는 파라미터를 넣어주면, 좌표에 점을 찍거나, 선을 그리지 않는다.
    
    lmList, bbox = detector.findPosition(img, draw = False)
    # print(lmList)
    # img를 findPosition 메소드에 넣으면, (id, cx, cy)값을 담은 lmList를 반환한다. 이때 img 다음 파라미터를 생략하거나, draw = True라고 하면, landmark에 보라색 점이 찍히게 되고, draw = False라고 하면, 좌표값만 반환한다.
    
    # 강의 코드
    if len(lmList) != 0:
        fingers = []
        good = []
        # 내가 짜본 엄지 손가락 코드 - 0과 엄지척을 구분 못함.
        # state = 4
        # for id in range(1, 5):
        #     if lmList[4][2] < lmList[tipIds[id]][2]:
        #         state -= 1
        #     else :
        #         state = state
        
        # 시도해 본 비슷한 코드          
        # if lmList[4][2] < lmList[tipIds[id]][2] and lmList[4][2] < lmList[tipIds[id]][2] and lmList[4][2] < lmList[tipIds[id]][2] and lmList[4][2] < lmList[tipIds[id]][2] :
        #     state = "good"
        
        # 실패한 엄지척 코드 - 0과 엄지척을 구분 못함.
        # for id in range(0,5):
        #     x, y = lmList[tipIds[id]][1], lmList[tipIds[id]][2]
        #     x0, y0 = lmList[0][1], lmList[0][2]
        #     good.append((x-x0)**2+(y-y0)**2)
        # # print(good.index(max(good)))
        # good_num = good.index(max(good))
        
                
        if lmList[4][1] < lmList[3][1] : # 왼손용
        # if lmList[4][1] > lmList[3][1] : # 오른손용
            fingers.append(1)
        else :
            fingers.append(0) 
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else :
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1) # fingers 리스트 안의 1의 숫자를 카운트 하는 매소드
        print(totalFingers)

        # 강의에서는 overlayList[totalFingers -1]로 받아서 totalFinger = 0을 입력시 인덱스 번호는 -1이 되어 리스트의 마지막 파일인 6.jpg (주먹 쥔 손)을 얻었다. 
        # 강의에서는 1.jpg ~ 6.jpg 로 파일을 만들었으며 순서대로 1, 2, 3, 4, 5, 0 의 이미지가 들어있다.       
        # h, w, c = overlayList[totalFingers -1].shape
        # img[0:h, 0:w] = overlayList[totalFingers -1]
        
        
        # 엄지척 구현을 위해 시도해본 코드
        # if state == 0:
        #     h, w, c = overlayList[6].shape
        #     img[0:h, 0:w] = overlayList[6]
        # else :            
        #     h, w, c = overlayList[totalFingers].shape
        #     img[0:h, 0:w] = overlayList[totalFingers]

        # if good_num == 0:
        #     h, w, c = overlayList[6].shape
        #     img[0:h, 0:w] = overlayList[6]
        # else :
        #     h, w, c = overlayList[totalFingers].shape
        #     img[0:h, 0:w] = overlayList[totalFingers]

        # 왼쪽 위에 손가락 그림 삽입        
        h, w, c = overlayList[totalFingers].shape
        img[0:h, 0:w] = overlayList[totalFingers]  
             
        # 네모를 추가하여 꾸미자        
        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25) # img를 받아서, 글자를 입력하고, 좌표를 입력, 폰트 입력, 크기 입력, 색깔입력, 굵기(두께) 입력
        


        
        
    '''
    # 내가 짜본 코드
    # if len(lmList) != 0:
    #     finger = []
        # for i in range (4, 21, 4):
        #     x, y = lmList[i][1], lmList[i][2]
        #     x0, y0 = lmList[0][1], lmList[0][2]
        #     length = math.hypot(x-x0, y-y0)
        #     # print(int(length))
        #     if length > 90:
        #         finger.append(1)
        #     # if lmList[i][2] < lmList[i-2][2]:
        #     #     print(f"{i} finger is open")
        #     else :
        #         finger.append(0)
        # # print(finger)
        # if finger == [0, 1, 0, 0, 0]:
        #     finger_image = 1
        # elif finger == [0, 1, 1, 0, 0]:
        #     finger_image = 2
        # elif finger == [0, 1, 1, 1, 0]:
        #     finger_image = 3
        # elif finger == [0, 1, 1, 1, 1]:
        #     finger_image = 4
        # elif finger == [1, 1, 1, 1, 1]:
        #     finger_image = 5
        # elif finger == [0, 0, 0, 0, 0]:
        #     finger_image = 0
        # elif finger == [1, 0, 0, 0, 0]:
        #     finger_image = 6
                
        # h, w, c = overlayList[finger_image].shape
        # img[0:h, 0:w] = overlayList[finger_image]
    '''
    
    # img[0:200, 0:200] = overlayList[2]
    # img[0:200 = limited of hight, 0:200 = limited of width]
    # 위의 방법으로 오버레이 리스트에 저장된 손구락 이미지를 img의 [0:200, 0:200] 위치에 불러올 수 있다. 하지만 이는 200x200 사이즈의 이미지에 해당할 시에만 가능하므로, 각기 다른 사이즈의 이미지를 img의 적당한 위치에 불러오기 위해서 다음의 방법으로 overlayList의 shape를 각각 hight, width, channel에 담아 활용한다.
    
    


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    
    cv2.putText(img, f'FPS = {int(fps)}', (450, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)