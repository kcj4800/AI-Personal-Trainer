import cv2 # 이미지 처리에 필요한 라이브러리
import mediapipe as mp # 게시물을 가져올수 있는 프레임워크
import time
import math

class poseDetector():
    
    def __init__(self, mode = False, complexity = 1 , smooth = True, detectionCon = 0.5, trackCon = 0.5):
        
        self.mode = mode
        self.complexity = complexity # 모델 복잡도
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        # self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, self.detectionCon, self.trackCon)
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, min_detection_confidence = self.detectionCon, min_tracking_confidence = self.trackCon)
        
        
        
    def findPose(self, img, draw = True): # 랜드마크를 찾아서 그려주는 매소드
        
        # 이미지를 BGR에서 RGB로 변환하여 pose.process 메소드에 넣어준다.            
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        

        if self.results.pose_landmarks: # 랜드마크 = True일때
            if draw : # draw = True 일때
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS) #  랜드마크를 이어주는 선을 그려라.
        return img
    
    # 랜드마크 좌표를 얻는 매소드
    def findPosition(self, img, draw = True):
        self.lmList = []
        if self.results.pose_landmarks :
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
            
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append( [id, cx, cy] )
                if draw :
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        return self.lmList
    
    
    def findAngle(self, img, p1, p2, p3, draw = True) :
        
        # Get the landmarks
        
        # 이런식으로 _를 써서 id 넘버를 무시하고 줄 수 있다.
        # _, x1, x2 = self.lmList[p1]
        # _, x2, y2 = self.lmList[p2]
        # _, x3, y3 = self.lmList[p3]
        
        # lmList의 리스트가 많지 않으니 아래의 방법으로 했다.
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        
        lineList = [x1, y1, x2, y2, x3, y3]
        
        # Calculate the Angle
        
        # a1 = math.atan2(4, 4) # 0.7853 => 45' 좌표를 입력받아 절대각도를 라디안으로 뱉음.
        # a2 = math.atan2(3, 4) # 0.6435 => 36.86'
        # a3 = math.degrees(a1 - a2) # 8.1301' 라디안 값을 입력받아 각도로 뱉음
        # a4 = a1 - a2 # 0.1418 => 8.13'
        # print(angle, a1, a2, a3, a4)
        
        # atan과 atan2의 차이점 - 참고 : https://spiralmoon.tistory.com/entry/프로그래밍-이론-두-점-사이의-절대각도를-재는-atan2
        # atan과 atan2은 두 점 사이의 θ의 절대각을 구하는 함수이다.
        
        # atan은 두 점 사이의 탄젠트값을 받아 절대각을 -π/2 ~ π/2의 라디안 값으로 반환한다. (-90 ~ 90도)
        
        # atan2는 두 점 사이의 상대좌표(x, y)를 받아 절대각(+x축과의 각도)을 -π ~ π의 라디안 값으로 반환한다. (-180 ~ 180도)
        
        # 도를 라디안으로 바꿀 때는 π/180(= 0.0174533)를 곱한다.
        # 라디안을 도로 바꿀 때는 180/π(= 57.2958)를 곱한다.
        
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)) # 각도를 radian 단위로 제공하고 변환하게 도와준다.
        if angle < 0 :
            angle += 360
        # print(angle)
       
        # Draw
        if draw :
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3 )
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3 )
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            # cv2.putText(img, str(int(angle)), (x2 -20 , y2 + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        return angle, lineList
    
    
    def findDistance(self, p1, p2, img, draw=True):
        
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        if draw : # 만약 draw가 True라면 두 지점 끝과 그 중앙에 점을 찍고 선으로 잇는 그림을 그려준다.
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        return length, img, [x1, y1, x2, y2, cx, cy]



def main():
    cap = cv2.VideoCapture("PoseVideos/2.mp4")
    pTime = 0
    detector = poseDetector()
    while True :
        success, img = cap.read()
        img = detector.findPose(img, draw = False)
        lmList = detector.findPosition(img, draw = False) # main에서 받는 lmList는 위의 클래스에서 받는 slef.lmList와 별개이다.
        if len(lmList) !=0:
            # print(lmList)
            cv2.circle(img, (lmList[12][1], lmList[12][2]), 20, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 20, (0, 0, 255), cv2.FILLED)
            cv2.line(img, (lmList[12][1], lmList[12][2]),(lmList[14][1], lmList[14][2]), (0, 0, 255), 2)
            cv2.circle(img, (lmList[16][1], lmList[16][2]), 20, (0, 0, 255), cv2.FILLED)
            cv2.line(img, (lmList[14][1], lmList[14][2]),(lmList[16][1], lmList[16][2]), (0, 0, 255), 2)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, 'FPS = {}'.format(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3 )
        
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main() # 이것을 자체적으로 실행할 경우 메인함수가 실행되고, 그렇지 않을 경우에는 실행하지 않고 호출된 함수만을 실행한다.
    
    
    
# 3. Solution APIs    
# 3.1. STATIC_IMAGE_MODE (정적_이미지_모드)
# False로 설정할 경우, 이 솔루션은 비디오 스트림을 입력받습니다. 비디오 스트림의 경우 첫 프레임에서 가장 중요한 사람을 감지하려 시도하고 감지가 성공적으로 완료되면 포즈 랜드마크를 해당 사람에게 집중합니다. 그 후에는 후속 이미에서 추적을 잃기 전까지는 다른 감지를 호출하지 않고 해당 랜드 랜드마크를 추적하여 계산 및 대기 시간을 줄입니다. 만약 True로 설정할 경우 모든 입력 이미지에 사람 감지를 적용합니다. 이는 관련없는 이미지나 일괄적 정적 이미지 처리에 이상적인 모델입니다. 기본값은 False입니다.

# 3.2. MODEL_COMPLEXITY (모델_복잡성)
# 포즈 랜드마크 모델의 복잡성입니다. 0,1,2. 모델 복잡성이 높을 수록 랜드마크의 정확도와 추론 지연 시간이 늘어납니다. 기본값은 1입니다.

# 3.3. SMOOTH_LANDMARKS (부드러운_랜드마크)
# True로 설정한다면 솔루션 필터가 지터를 줄이기 위해 다른 입력 이미지에 랜드마크를 표시합니다. 만약 '정적 이미지 모드'가 True로 설정되어 있다면 '부드러운 랜드마크'를 무시합니다. 기본값은 True입니다.

# 3.4. ENABLE_SEGMENTATION (분할_허용)
# True로 설정합니다면 포즈 랜드마크 외에도 솔루션에서 분할 마스크를 적용합니다. 기본값은 False입니다.

# 3.5. SMOOTH_SEGMENTATION (부드러운_분할)
# True로 설정하다면 포즈 랜드마크 외에도 솔루션에서 분할 마스크를 생성합니다. '분할 허용'이 False로 설정되어 있거나, '정적 이미지 모드'가 True일 경우 '부드러운 분할'을 무시합니다. 기본값은 True입니다.

# 3.6. MIN_DETECTION_CONFIDENCE (최소_탐지_신뢰값)
# 탐지가 성공한 것으로 간주하는 사람 탐지 모델의 최소 신뢰값은 ([0.0, 1.0])입니다. 기본값은 0.5입니다. 

# 3.7. MIN_TRACKING_CONFIDENCE (최소_추적_신뢰값)
# 탐지가 성공한 것으로 간주하는 사람 탐지 모델의 최소 신뢰값은 ([0.0, 1.0])입니다. 추적에 실패하면 다음 이미지 입력에서 사람 감지가 자동으로 호출됩니다. 추적 신뢰값을 높게 설정하면 솔루션의 견고함이 증가하지만 대기시간도 증가합니다. 정적 이미지 모드가 True일 경우 무시됩니다. 기본값은 0.5입니다. 


# 4. OUT PUT
# 4.1. POSE_LANDMARKS (포즈_랜드마크)
# 포즈 랜드마크의 리스트입니다. 각 랜드마크는 다음과 같이 구성됩니다.

# x와 y : 랜드마크의 좌표는 각각 이미지의 너비와 높이로 [0.0, 1.0]로 표준화됩니다.
# z : 엉덩이 중간 지점의 깊이를 원점으로 하여 랜드마크의 깊이를 나타내며, 랜드마크가 카메라에 가까울수록 값이 작아집니다. z의 크기는 x와 거의 비슷한 척도를 사용합니다.
# 가시성 : 이미지에 랜드마크가 보일 가능성(신체가 가려지지 않고 보일 경우) [0.0, 1.0] 가시성의 값입니다.

# 4.2. POSE_WORLD_LANDMARKS
# 세계 좌표에 있는 또 다른 포즈 랜드마크 리스트입니다. 각 랜드마크는 다음과 같이 구성됩니다. 
# x, y, z: 엉덩이 사이의 중심에 원점이 있는 실제 3D 좌표(미터 단위)입니다.
# 가시성: 해당 pose_landmark에 정의된 것과 동일합니다.

# 4.3. SEGMENTATION_MASK(마스크 분할)
# enable_segmentation이 True로 설정된 경우에만 작동하는 예측 출력 분할 마스크입니다. 마스크는 입력 이미지와 너비와 높이가 동일하며 [0.0, 1.0] 값을 포함합니다. 여기서 1.0과 0.0은 각각 "사람" 및 "배경" 픽셀의 높은 확실성을 나타냅니다. 자세한 사용 방법은 아래 플랫폼별 사용 예를 참조하십시오.