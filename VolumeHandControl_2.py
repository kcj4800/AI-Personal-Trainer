import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

# pip install pycaw - 파이썬으로 윈도우 볼륨 조절할 수 있게 만들어 놓은 모듈 내지는 라이브러리
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


###########################
wCam, hCam = 640, 480
###########################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
cTime = 0
pTime = 0

detector = htm.handDetector(detectionCon = 0.7, maxHands = 1) # 최소 디텍팅 신뢰도를 올려주면 좀 덜 깜박거리게 할 수 있다. maxHands = 1 로 해준다면 손 하나를 찾고나서도 계속 해서 다음 손을 찾기위해 깜빡거리는것을 줄여줄수 있다.


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()

print(volume.GetVolumeRange()) # (-65.25, 0.0, 0.75)
# -65.25 ~ 0.0 까지 볼륨을 조절할 수 있고 0.75는 무시한다.
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(0, None)
# -20.0 = 26%, -40.0 = 6%, -60.0 = 1%, -10.0 = 51% 0.0 = 100%
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
# vol2 = 0
volBar = 400
volPer = 0
# per2 = 0
area = 0
cVol = 0
cVolBar = 400
volColor = (255, 0, 0)
while True:
    success, img = cap.read()
    
    # Find Hand
    img = detector.findHands(img) # 손 추적이 가능해진 이미지를 퉤 뱉어내므로 그걸 다시 줏어서 이미지에 넣자
    
    lmList, bbox = detector.findPosition(img) # 손 좌표(landmarks)의 리스트를 퉤 뱉으므로 리스트에 담아주자.
    if len(lmList) != 0:
              
        # Filter based on size
        area = (bbox[2]-bbox[0]) * (bbox[3]-bbox[1])//100 # /100 : 나누기, //100 : 나눈 몫(정수값)
        # print(area)
        
        if 250 < area < 1250 :
            # print("yes")
            # Find Distance between index and Thumb
            length, img, lineInfo = detector.findDistance(4, 8, img)
            # print(length, lineInfo)
            
            # Convert Volume
            # vol = np.interp(length, [30, 300], [minVol, maxVol]) # volume.SetMasterVolumeLevel(vol, None)의 값을 사용할때 쓰였으나, 이는 비선형값으로 이용하기 용이하지 않다.
            volBar = np.interp(length, [30, 300], [400, 150])
            volPer = np.interp(length, [30, 300], [0, 100])
            
            # volume.SetMasterVolumeLevel(vol, None) # 비선형값으로 써먹기 애매하다.
            
            
            # Reduce Resolution to make it smoother
            smoothness = 10
            volPer = smoothness * round(volPer/smoothness)
            
            # Check which fingers are up
            fingers = detector.fingersUp()
            # print(fingers)

            
            # if pinky is down set volume
            if not fingers[4]:
                cVol = volPer
                cVolBar = volBar
                volume.SetMasterVolumeLevelScalar(volPer / 100, None) # 선형값으로 백분율을 적용하여 이용하기 용이하다. 정규화(nomalize : 값을 0 ~ 1사이 값으로 만든다.)해서 적용한다.
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                volColor = (0, 255, 0)
            else :
                volColor = (255, 0, 0)           
                       
            
            # 여기서부터 length 선언까지의 내용은 모듈로 옮겼으니 detector.findDistance(self, p1, p2, img, draw=True) 매소드를 이용하여 받아온다.
            # print(lmList[4], lmList[8])
            
            # x1, y1 = lmList[4][1], lmList[4][2]
            # x2, y2 = lmList[8][1], lmList[8][2]
            
            # cx, cy = (x1 + x2)//2, (y1 + y2)//2
            
            
            # cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED) # 엄지손가락 좌표에 15직경의 보라색으로 꽉찬 원
            # cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED) # 검지손가락 좌표에 15직경의 보라색으로 꽉찬 원
            # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3) # 두 자표를 잇는 보라색 두께 3짜리 선
            # cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED) # 엄지와 검지 좌표의 중간 좌표에 15직경의 보라색으로 꽉찬 원
            
            # length = math.hypot(x2 - x1, y2 - y1) # 빗변의 길이를 구하는 메소드 루트(x^2+y^2)
            # # print(length)   
            
            # # Hand range 30 ~ 300
            # # Volume Range -65.25 ~ 0
            # # 핸드레인지에서 볼륨레인지로 전환하기 위해 넘파이를 이용하면 간단히 처리할 수 있다.
            
            # vol = np.interp(length, [30, 300], [minVol, maxVol]) # length로 부터 검지와 중지의 거리 데이터를 받아서 거리 50 ~ 300을 -65.25 ~ 0 로 치환해준다.

            # volBar = np.interp(length, [30, 300], [400, 150])
            # volPer = np.interp(length, [30, 300], [0, 100])

            # 나의 방식 - 손을 빼고 넣고 할때 값이 변동 되는 것을 막지 못한다.
            # if lmList[20][2] > lmList[18][2]:
            #     vol2 = vol
            #     volPer2 = volPer
            # volume.SetMasterVolumeLevel(vol2, None)        
            
            # print(int(length), int(vol), int(volBar), int(volPer))

            # volume.SetMasterVolumeLevel(vol, None)
            
            
            # if length < 30:
            #     cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED) # 가운데 녹색 점 lineInfo = [x1, y1, x2, y2, cx, cy]
    
    
    # Drawings - 손을 디텍팅 했을때부터 그림을 표시하려면 if len(lmList) != 0: 안으로 넣어주자
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0, 3))
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'Vol : {int(volPer)}%', (20, 450), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
    
    # 실제 볼륨값을 눈으로 확인 할 수 있도록 표시해주자.
    # cv2.rectangle(img, (550, 150), (585, 400), (0, 255, 0, 3))
    # cv2.rectangle(img, (550, int(cVolBar)), (585, 400), (0, 255, 0), cv2.FILLED)
    # cv2.putText(img, f'cVol : {int(cVol)}%', (450, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    
    # 간단하게 GetMasterVolumeLevelScalar를 통해 표현 가능
    cVol2 = int(volume.GetMasterVolumeLevelScalar()*100) # GetMasterVolumeLevelScalar()를 통해 볼륨레벨이 얼마인지 알수 있다.
    cv2.putText(img, f"cVol2 Set: {int(cVol2)}%", (450, 50), cv2.FONT_HERSHEY_PLAIN, 1, volColor, 2)

    # cv2.putText(img, f'Vol2 : {int(per2)}%', (450, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # Frame rate     
    cTime = time.time()
    fps = 1/(cTime - pTime)
    # cTime - pTime = 1fps
    # (cTime - pTime) / (cTime - pTime) = 1fps / (cTime - pTime)
    # 1sec = 1 / (cTime - pTime) fps
    # print(cTime, pTime, cTime - pTime, fps)
    pTime = cTime
    
    cv2.putText(img, f'FPS : {int(fps)}', (40, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2) # img에 fstring으로 fps값을 넣어주고, 좌표입력, 폰트, 크기, 색깔, 두께 순
    
    
    
    cv2.imshow("Image", img)
    cv2.waitKey(1) # 1미리의 지연을 제공 - 역할이 뭘까요??
    
