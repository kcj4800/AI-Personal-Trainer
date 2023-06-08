import cv2 # 이미지 처리에 사용할 라이브러리
import mediapipe as mp # 게시물을 가져올 수 있는 프레임 워크
import time
import math
import numpy as np

# 함수형 프로그램이지만 클래스를 만들면 더 좋을 것 같으니 만들겠다.

class handDetector():
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5): # 손 디텍터에 필요한 기본 매개변수(파라미터)
# github의 mp.solutions.hands.Hands()의 파라미터를 참고.
        # static_image_mode = False, 
        # max_num_hands = 2,
        # min_detection_confidence=0.5,
        # min_tracking_confidence=0.5
        self.mode = mode # 자체변수를 가지는 객체(object)를 만들거다라는 뜻
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        
        # self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        # 문제 발생 : 업데이트 되면서 mp.solutions.hands.mpHands.Hands의 파라미터 순서나 위치가 바뀌거나 추가되는 내용이 있는 듯 하다. 그래서 static_image_mode = self.mode 처럼 본래의 속성값의 이름과 새로만든 속성값의 이름인 self.mode를 매칭시켜 줌으로써 해결하였다.
        self.hands = self.mpHands.Hands(static_image_mode = self.mode, max_num_hands = self.maxHands,
                                        min_detection_confidence = self.detectionCon, min_tracking_confidence = self.trackCon)
        
        
        
        self.mpDraw = mp.solutions.drawing_utils # results.multi_hand_landmarks 이러한 정보를 이용해 선을 따준다
        # def mp.Hands.Hands(self,
        #              static_image_mode = False, => 정적 이미지 모드 추적 감지 False = 때때로 감지, 때때로 추적, True = 전체 시간동안 계속 감지 추적 느려짐. False로 놓고 신뢰도가 높다면, 그대로 사용하는 것이 좋다. 속도가 빠르므로.
        #              max_num_hands = 2,
        #              min_detection_confidensce = 0.5, 최소 디텍팅 신뢰도 =0.5 
        #              min_tracking_confidence = 0.5): 최소 추적 신뢰도 = 0.5
        self.tipIds = [4, 8, 12, 16, 20]
        
        
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # 이 클라스는 RGB이미지만을 사용하므로 일반적인 BGR에서 RGB로 바꿔줘야 한다.
        self.results = self.hands.process(imgRGB)
        # result에 RGB로 바꾼 이미지를 핸즈 클라스에 담아서 넣는다.
        # print(results) # results에 담기는 것이 뭔지 확인 <class 'mediapipe.python.solution_base.SolutionOutputs'>
        # print(results.multi_hand_landmarks) # 손을 가져다 대기 전 None (= False) 상태에서 손을 가져다 대면 손의 좌표 (= True)를 표시한다. 이를 이용하여 손의 유무로 조건식을 세울 수 있다.
        
        #     landmark {
        #   x: 0.47883284091949463
        #   y: 0.2476905882358551
        #   z: -0.09612901508808136
        #     }
        
        if self.results.multi_hand_landmarks : # 손의 유무로 True or False를 도출하는 조건식.
            for handLms in self.results.multi_hand_landmarks: # 손의 좌표를 프레임별로 순서대로 불러온다
                if draw :
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) # RGB로 변형한 RGBimg가 아닌 오리지날 img를 사용하여, 손의 좌표 점을 찍고, 점들을 선으로 이어 그린다.
        return img
                        

    def findPosition(self, img, handNo = 0, draw = True):
        
        xList = [] # hand land mark의 x좌표 리스트
        yList = [] # hand land mark의 y좌표 리스트
        bbox = []        
        self.lmList = [] # self.lmList로 바꿔줌으로써 모듈내의 다른 메소드에서도 self.lmList를 이용하여 손가락의 좌표를 받아 볼수 있게되었다.
        if self.results.multi_hand_landmarks : # 손의 유무로 True or False를 도출하는 조건식. 손이 존재시 Ture
            myHand = self.results.multi_hand_landmarks[handNo] # 0번째 손 즉 첫번째 감지된 손의 좌표를 반환한다.
            for id, lm in enumerate(myHand.landmark): # 불러온 프레임의 손의 좌표를 차례대로 인덱싱 해서 id 넘버를 준다. 0이면 바닥이되고 1이면 중앙, 4면 엄지 손끝 등등 0 ~ 20까지 존재.
                # print(id, lm) # id 와 lm 0이면 아마 손바닥 위치.
                
                # 0 x: 0.25707507133483887
                # y: 0.8157018423080444
                # z: 5.522352353182214e-07
                # 여기서 얻어지는 x와 y 좌표는 픽셀을 비율로 나타낸다.
                h, w, c  = img.shape # img의 shape을 높이, 너비, 채널로 각각 담아준다.
                cx, cy = int(lm.x * w), int(lm.y * h) # center x좌표 = lm의 x좌표 * img의 너비, center y좌표 = lm의 y좌표 * img의 높이
                # print(id, cx, cy)
                xList.append(cx) # hand land mark의 x좌표를 담아준다.
                yList.append(cy) # hand land mark의 y좌표를 담아준다.
                self.lmList.append([id, cx, cy])
                # 0 170 365
                # 1 222 387
                # 2 278 389
                if draw:
                    
                # if id == 0: # id가 0(손바닥)이면
                    # cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED) # img의 (cx, cy) 좌표에 반경이 15인 보라색으로 가득찬 원을 그리세요. 라는 뜻
                # elif id == 4: # id가 4(엄지 손끝)이면
                #     cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED) # 모든 id 값의 좌표에 15 반경의 보라색으로 가득찬 원을 그리세요.
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)    
            bbox = xmin, ymin, xmax, ymax # bounding box
            
            if draw:
                cv2.rectangle(img, (bbox[0]-20,bbox[1]-20), (bbox[2]+20, bbox[3]+20), (0, 255, 0), 2)
            
        return self.lmList, bbox
    
    def fingersUp(self): # self.fingersup()으로 호출한다.
        fingers = []
        
        # Thumb - 오른손 전용
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else :
            fingers.append(0)
            
        # 4 Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else :
                fingers.append(0)
        return fingers   # 펴진 손가락 리스트[0, 0, 0, 0, 0]를 리턴해준다.
    
    
    def findDistance(self, p1, p2, img, draw=True):
        
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        if draw : # 만약 draw가 True라면 두 손가락 끝과 그 중앙에 점을 찍고 선으로 잇는 그림을 그려준다.
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        return length, img, [x1, y1, x2, y2, cx, cy]
                    
    
def main():
    pTime = 0 # 과거시간 0으로 초기화
    cTime = 0 # 현재시간 0으로 초기화
    cap = cv2.VideoCapture(0)
    detector = handDetector() # 위에서 handDetector 클래스의 기본 파라미터(매개변수)들을 지정해줬으므로, 따로 적지 않는다. detector라는 속성은 handDetector라는 클래스 안의 기본값을 속성값으로 갖고 추가된다.
    
    while True:
        success, img = cap.read()
        # img = detector.findHands(img)
        img = detector.findHands(img, draw = False) # detector가 handDetector라는 클래스 안의 매소드 findHands()를 호출
        # lmList = detector.findPosition(img)
        lmList = detector.findPosition(img, draw = False)
        # if len(lmList) != 0:
        #     print(lmList[4]) # [4, 359, 305]

        
        cTime = time.time() # 현재시간을 담고
        fps = 1/(cTime - pTime) # 1/(현재시간 - 과거시간) frame per sec
        pTime = cTime # 과거시간을 담는다.
        
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3) # 텍스트를 img에 담는다, str(int(fps))라는 문구 정수로 표현, position = (10, 70), 폰트는 아무거나 담고, 3번 스케일(크기) = 3, 컬러BGR(255, 0, 255) = 보라색, thickness(두께) = 3,
        
        cv2.imshow("Image", img)
        cv2.waitKey(1)




if __name__ == "__main__":
    main()    



# vscode 가상 환경 설정 
# 1. 카메라 연결 후, 검색에서 카메라 앱 실행 후 확인
# 2. VSCode 터미널에서 python -m venv cv_env
# 3. F1 - select interpreter - 방금 만든 가상환경 선택
# 4. (cv_env)가 앞에 잘 붙어있으면 성공
# 5. 안된다면
#     5.1 검색 - powershell 관리자 권한으로 실행
#     5.2 Set-ExecutionPolicy RemoteSigned
# 6. pip install opencv-python 으로 opencv 선택
# 7. python -m pip install --upgrade pip
# 8. 코드를 실행해서 잘 나오는지 확인
# 9. pip install mediapipe