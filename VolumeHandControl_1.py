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

detector = htm.handDetector(detectionCon = 0.7) # 최소 디텍팅 신뢰도를 올려주면 좀 덜 깜박거리게 할 수 있다.


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
rect = 400
per = 0

while True:
    success, img = cap.read()
    
    # Find Hand
    img = detector.findHands(img) # 손 추적이 가능해진 이미지를 퉤 뱉어내므로 그걸 다시 줏어서 이미지에 넣자
    
    lmList = detector.findPosition(img, draw = False) # 손 좌표(landmarks)의 리스트를 퉤 뱉으므로 리스트에 담아주자.
    if len(lmList) != 0:
        
        
        
        # Filter based on size
        
        # Find Distance between index and Thumb
        
        # Convert Volume
        # Reduce Resolution to make it smoother
        # Check fingers up
        # if pinky is down set volume
        # Drawings
        
        # print(lmList[4], lmList[8])
        
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2
        
        
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED) # 엄지손가락 좌표에 15직경의 보라색으로 꽉찬 원
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED) # 검지손가락 좌표에 15직경의 보라색으로 꽉찬 원
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3) # 두 자표를 잇는 보라색 두께 3짜리 선
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED) # 엄지와 검지 좌표의 중간 좌표에 15직경의 보라색으로 꽉찬 원
        
        length = math.hypot(x2 - x1, y2 - y1) # 빗변의 길이를 구하는 메소드 루트(x^2+y^2)
        # print(length)   
        
        # Hand range 30 ~ 300
        # Volume Range -65.25 ~ 0
        # 핸드레인지에서 볼륨레인지로 전환하기 위해 넘파이를 이용하면 간단히 처리할 수 있다.
        
        vol = np.interp(length, [30, 300], [minVol, maxVol]) # length로 부터 검지와 중지의 거리 데이터를 받아서 거리 50 ~ 300을 -65.25 ~ 0 로 치환해준다.
        rect = np.interp(length, [30, 300], [400, 150])
        per = np.interp(length, [30, 300], [0, 100])
        print(int(length), int(vol), int(rect), int(per))
        volume.SetMasterVolumeLevel(vol, None)
        
        
        if length < 30:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED) # 가운데 녹색 점
    
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0, 3))
    cv2.rectangle(img, (50, int(rect)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'Vol : {int(per)}%', (20, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
         
    cTime = time.time()
    fps = 1/(cTime - pTime)
    # cTime - pTime = 1fps
    # (cTime - pTime) / (cTime - pTime) = 1fps / (cTime - pTime)
    # 1sec = 1 / (cTime - pTime) fps
    # print(cTime, pTime, cTime - pTime, fps)
    pTime = cTime
    
    cv2.putText(img, f'FPS : {int(fps)}', (40, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3) # img에 fstring으로 fps값을 넣어주고, 좌표입력, 폰트, 크기, 색깔, 두께 순
    

    
    cv2.imshow("Image", img)
    cv2.waitKey(1) # 1미리의 지연을 제공 - 역할이 뭘까요??
    
