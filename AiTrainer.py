import cv2
import numpy as np
import time
import PoseModule as pm
import HandTrackingModule as htm
import os
import face_recognition
from just_playback import Playback

'''
진행 상황
0. 유저 인식 - 70%
1. 메인 - 60%
2. 스쿼트 - 70%
3. 푸쉬업 - 70%
4. 숄더 프레스 - 70%
5. 덤벨 컬 - 70%
6. 풀업 - 70%
7. 하이 - 70%
8. 카운트 - 70%
9. 뮤직 - 40%
10. 유저 - 50%
11. 크윝 - 80%
12. 음원 - 0%
'''


cap = cv2.VideoCapture(0)
psTime = 0
pDetector = pm.poseDetector()
hDetector = htm.handDetector(maxHands=1)
count = 0
dcount = 10
dir = 0
state = ""
user = ""
mTime = time.time()
endTime = 50
age = {"Chan" : 30, "Hana" : 25}
sex = {"Chan" : "Male", "Hana" : "Female"}
music = ["Love Love Love", "Dinosaur", "Holy Moly"]
# Background Image List
folderPath = "Background"
myList = os.listdir(folderPath)
overlayList = []
videoPath = "PoseVideos"

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

background = overlayList[0]

# User Recognition Image List
iPath = 'FaceImages'
uImages = []
classNames = []

myList = os.listdir(iPath)
print(myList)
for cl in myList:
    cImg = cv2.imread(f'{iPath}/{cl}')
    uImages.append(cImg)
    classNames.append(os.path.splitext(cl)[0])
    
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # faceLoc = face_recognition.face_locations(img)[0]
        encodeimg = face_recognition.face_encodings(img)[0]
        # cv2.rectangle(img, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)
        encodeList.append(encodeimg)
    return encodeList
encodeListKnown = findEncodings(uImages)


print(myList)
while True :

    success, img = cap.read()
    img = cv2.resize(img, (640, 480))
    if state == "" and user == "":
        imgS = cv2.resize(img,(0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
            
            if matches[matchIndex]:
                name = classNames[matchIndex]
                print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                user = name            
                background = overlayList[0]
                endTime = 50
                state = 'main'                
    
    
    if state == 'main':       
        img = hDetector.findHands(img)
        lmList, bbox = hDetector.findPosition(img, draw = False)
        if len(lmList) != 0:
            fingers = hDetector.fingersUp()
            hTime = time.time()
            print(fingers, int(hTime - mTime))
            # Select Exercise
            if fingers == [0, 1, 0, 0, 0]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                if endTime == 0:
                    background = overlayList[1]
                    endTime = 50
                    state = "squat"
                    
                               
            elif fingers == [0, 1, 1, 0, 0]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                if endTime == 0:
                    background = overlayList[2]
                    endTime = 50
                    state = "push_up"
                    
            elif fingers == [0, 1, 1, 1, 0]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                if endTime == 0:
                    background = overlayList[3]
                    endTime = 50
                    state = "shoulder_press"
                    
            elif fingers == [0, 1, 1, 1, 1]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                if endTime == 0:
                    background = overlayList[4]
                    endTime = 50
                    state = "dumbbel_r"
                    
            elif fingers == [1, 1, 1, 1, 1]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                if endTime == 0:
                    background = overlayList[5] 
                    endTime = 50
                    state = "pull_up"
                    
            # Select Option           
            elif fingers == [1, 0, 0, 0, 0]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                if endTime == 0:
                    background = overlayList[6]
                    endTime = 50
                    state = "hi"  
                    
            elif fingers == [1, 1, 0, 0, 0]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                if endTime == 0:
                    background = overlayList[7]
                    endTime = 50
                    state = "count"
                    
            elif fingers == [0, 1, 0, 0, 1]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                if endTime == 0:
                    background = overlayList[8]
                    endTime = 50
                    state = "music"  
                    
            elif fingers == [1, 0, 0, 0, 1]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                if endTime == 0:
                    background = overlayList[9]
                    endTime = 50
                    state = "user" 
                    
            elif fingers == [1, 1, 0, 0, 1]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                if endTime == 0:
                    background = overlayList[10]
                    endTime = 50
                    state = "quit"  
            
            # Except Reset
            else :
                endTime = 50

        # print(lmList)
    elif state == 'squat':    
        img = pDetector.findPose(img, False)
        lmList = pDetector.findPosition(img, False)
        pTime = time.time()
        if len(lmList) != 0:
            # Right Leg
            angle, lineList = pDetector.findAngle(img, 24, 26, 28)
            angle = abs(angle - 180)
            per = np.interp(angle, (20, 70), (100, 0))
            sq = np.interp(angle, (20, 70), (150, 450))
            
            # Check for the dumbbell culrs
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per < 20:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0
            print(count)
            
            # Draw Bar
            cv2.rectangle(img, (20, 150), (70, 450), color, 3)
            cv2.rectangle(img, (20, int(sq)), (70, 450), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (15, 480), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
            cv2.putText(img, f'{int(angle)}', (400, 100), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)
            
            # Squat Count
            cv2.putText(img, f'{int(count)}/{dcount}', (10, 130), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            if count > dcount:
                background = overlayList[0]
                count = 0
                endTime = 50
                state = 'main'
                
            # End Mission!
            if lmList[16][2] < lmList[14][2] and lmList[14][2] < lmList[12][2] and lmList[15][2] < lmList[13][2] and lmList[13][2] < lmList[11][2] and lmList[16][1] > lmList[15][1] and lmList[14][1] < lmList[13][1]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                    
                if endTime == 0:
                    background = overlayList[0]
                    endTime = 50
                    count = 0
                    state = 'main'
            else :
                endTime = 50
                                        
    
    elif state == 'push_up':    
        img = pDetector.findPose(img, False)
        lmList = pDetector.findPosition(img, False)
        pTime = time.time()
        if len(lmList) != 0:
            # Right Arm
            angle, lineList = pDetector.findAngle(img, 12, 14, 16)
            per = np.interp(angle, (65, 170), (0, 100))
            sq = np.interp(angle, (65, 170), (450, 150))
            
            # Check for the dumbbell culrs
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0
            print(count)
            
            # Draw Bar
            cv2.rectangle(img, (20, 150), (70, 450), color, 3)
            cv2.rectangle(img, (20, int(sq)), (70, 450), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (15, 480), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
            
            # Push Up Count
            cv2.putText(img, f'{int(count)}/{dcount}', (10, 130), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            if count > dcount:
                background = overlayList[0]
                count = 0
                endTime = 50
                state = 'main'
            # End Mission!
            if lmList[16][2] < lmList[14][2] and lmList[14][2] < lmList[12][2] and lmList[15][2] < lmList[13][2] and lmList[13][2] < lmList[11][2] and lmList[16][1] > lmList[15][1] and lmList[14][1] < lmList[13][1]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                    
                if endTime == 0:
                    background = overlayList[0]
                    endTime = 50
                    count = 0
                    state = 'main'
            else :
                endTime = 50

    elif state == 'shoulder_press':    
        img = pDetector.findPose(img, False)
        lmList = pDetector.findPosition(img, False)
        pTime = time.time()
        if len(lmList) != 0:
            # Right Arm
            angle, lineList = pDetector.findAngle(img, 12, 14, 16)
            angle = abs(angle - 180)
            per = np.interp(angle, (30, 110), (100, 0))
            sq = np.interp(angle, (30, 110), (150, 450))
            
            # Check for the dumbbell culrs
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0
            print(count)
            
            # Draw Bar
            cv2.rectangle(img, (20, 150), (70, 450), color, 3)
            cv2.rectangle(img, (20, int(sq)), (70, 450), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (15, 480), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
            
            # Shoulder Press Count
            cv2.putText(img, f'{int(count)}/{dcount}', (10, 130), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            if count > dcount:
                background = overlayList[0]
                count = 0
                endTime = 50
                state = 'main'
                
            # End Mission!
            if lmList[16][2] < lmList[14][2] and lmList[14][2] < lmList[12][2] and lmList[15][2] < lmList[13][2] and lmList[13][2] < lmList[11][2] and lmList[16][1] > lmList[15][1] and lmList[14][1] < lmList[13][1]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                    
                if endTime == 0:
                    background = overlayList[0]
                    endTime = 50
                    count = 0
                    state = 'main'
            else :
                endTime = 50

                    
    elif state == 'dumbbel_r':
        img = pDetector.findPose(img, False)
        lmList = pDetector.findPosition(img, False)
        pTime = time.time()
        print(int(pTime -mTime), int(pTime - hTime))
        if len(lmList) != 0:
            # Right Arm
            angle, lineList = pDetector.findAngle(img, 12, 14, 16)
            angle = abs(angle - 180)
            per = np.interp(angle, (10, 135), (0, 100))
            sq = np.interp(angle, (10, 135), (450, 150))

            print(angle)
            
            # Check for the dumbbell culrs
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0
            print(count)
            
            # Draw Bar
            cv2.rectangle(img, (20, 150), (70, 450), color, 3)
            cv2.rectangle(img, (20, int(sq)), (70, 450), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (23, 465), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)
            cv2.putText(img, str(int(angle)), (lineList[2] -20 , lineList[3] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
            
            # Right Arm Dumbbel Curl Count
            cv2.putText(img, f'{int(count)}/{dcount}', (10, 130), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            if count > dcount:
                background = overlayList[0]
                count = 0
                endTime = 50
                state = 'dumbbel_l'
                
            # End Mission!
            if lmList[16][2] < lmList[14][2] and lmList[14][2] < lmList[12][2] and lmList[15][2] < lmList[13][2] and lmList[13][2] < lmList[11][2] and lmList[16][1] > lmList[15][1] and lmList[14][1] < lmList[13][1]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                    
                if endTime == 0:
                    background = overlayList[0]
                    endTime = 50
                    count = 0
                    state = 'main'
            else :
                endTime = 50
                        
                 
                
                
    elif state == 'dumbbel_l':   
        img = pDetector.findPose(img, False)
        lmList = pDetector.findPosition(img, False)
        pTime = time.time()
        if len(lmList) != 0:
            # Right Arm
            angle, lineList = pDetector.findAngle(img, 11, 13, 15)
            angle = abs(angle - 180)
            per = np.interp(angle, (10, 135), (0, 100))
            sq = np.interp(angle, (10, 135), (450, 150))

            print(angle)
            
            # Check for the dumbbell culrs
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0
            print(count)
            
            # Draw Bar
            cv2.rectangle(img, (20, 150), (70, 450), color, 3)
            cv2.rectangle(img, (20, int(sq)), (70, 450), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (15, 480), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
            cv2.putText(img, str(int(angle)), (lineList[2] -20 , lineList[3] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                        
            # Left Arm Dumbbel Curl Count
            cv2.putText(img, f'{int(count)}/{dcount}', (10, 130), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            if count > dcount:
                background = overlayList[0]
                count = 0
                endTime = 50
                state = 'main'
                
            # End Mission!
            if lmList[16][2] < lmList[14][2] and lmList[14][2] < lmList[12][2] and lmList[15][2] < lmList[13][2] and lmList[13][2] < lmList[11][2] and lmList[16][1] > lmList[15][1] and lmList[14][1] < lmList[13][1]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                    
                if endTime == 0:
                    background = overlayList[0]
                    endTime = 50
                    count = 0
                    state = 'main'
            else :
                endTime = 50
                
    elif state == 'pull_up':    
        img = pDetector.findPose(img, False)
        lmList = pDetector.findPosition(img, False)
        pTime = time.time()
        if len(lmList) != 0:
            # Right Arm
            angle, lineList = pDetector.findAngle(img, 12, 14, 16)
            angle = abs(angle - 180)
            per = np.interp(angle, (20, 90), (0, 100))
            sq = np.interp(angle, (20, 90), (450, 150))
            
            # Check for the dumbbell culrs
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0
            print(count)
            
            # Draw Bar
            cv2.rectangle(img, (20, 150), (70, 450), color, 3)
            cv2.rectangle(img, (20, int(sq)), (70, 450), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (15, 480), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
            
            # Push UP Count
            cv2.putText(img, f'{int(count)}/{dcount}', (10, 130), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            if count > dcount:
                background = overlayList[0]
                count = 0
                endTime = 50
                state = 'main'
                
            # End Mission!
            if lmList[16][2] < lmList[14][2] and lmList[14][2] < lmList[12][2] and lmList[15][2] < lmList[13][2] and lmList[13][2] < lmList[11][2] and lmList[16][1] > lmList[15][1] and lmList[14][1] < lmList[13][1]:
                endTime -= 1
                cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                    
                if endTime == 0:
                    background = overlayList[0]
                    endTime = 50
                    count = 0
                    state = 'main'
            else :
                endTime = 50                
                
    elif state == "hi":
        endTime -= 0.5
        cv2.putText(img, f'Hi! {user}!', (50, 200), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 3)
        cv2.putText(img, f'Welcome to the', (50, 300), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 3)
        cv2.putText(img, f'A.I World!', (50, 400), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 3)
        if endTime == 0:
            background = overlayList[0]
            endTime = 50
            state = 'main'
    
                
    elif state == 'count':
        img = hDetector.findHands(img)
        lmList, bbox = hDetector.findPosition(img, draw = False)
        cPer = dcount

        if len(lmList) != 0:
            countTime = time.time()
            area = (bbox[2]-bbox[0]) * (bbox[3]-bbox[1])//100
        
            if 100 < area < 1250 :
                length, img, lineInfo = hDetector.findDistance(4, 8, img)
                bar = np.interp(length, [20, 200], [400, 150])
                per = np.interp(length, [20, 200], [0, 50])

                # Reduce Resolution to make it smoother
                smoothness = 5
                per = smoothness * round(per/smoothness)
                
                # Check which fingers are up
                fingers = hDetector.fingersUp()
                # print(fingers)
                
                
                # if pinky is down set count
                if fingers[4] == 0 and (countTime - hTime) > 3:
                    endTime -= 1
                    cColor = (0, 255, 0)
                    cPer = per
                    dcount = cPer
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, cColor, cv2.FILLED) # lineInfo = [x1, y1, x2, y2, cx, cy]
                    cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                    if endTime == 0:
                        background = overlayList[0]
                        state = 'main'                        

                else :
                    cColor = (255, 0, 0)
                    endTime = 50
                cv2.rectangle(img, (bbox[0]-20,bbox[1]-20), (bbox[2]+20, bbox[3]+20), (0, 255, 0), 2)   
                cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0, 3))
                cv2.rectangle(img, (50, int(bar)), (85, 400), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'Count : {int(per)}', (10, 450), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)


    elif state == "user":
        endTime -= 0.5
        cv2.putText(img, f'Name : {user}!', (50, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.putText(img, f'Age : {age[user]}, sex : {sex[user]}', (50, 300), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.putText(img, f'Have a good Exercise!', (50, 400), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        if endTime == 0:
            background = overlayList[0]
            endTime = 50
            state = 'main'
            
            
    elif state == "music":
        endTime -= 0.5
        cv2.putText(img, f'1. : {music[0]}', (50, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.putText(img, f'2. : {music[1]}', (50, 300), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.putText(img, f'3. : {music[2]}', (50, 400), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        if endTime == 0:
            background = overlayList[0]
            endTime = 50
            state = 'main'
                
                
    # Quit!
    if state == "quit":
        cv2.putText(img, f"Good Bye! {user}", (50, 200), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,255), 3)
        cv2.putText(img, "Have a Nice Day", (50, 300), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,255), 3)
        endTime -= 1
        if endTime == 0:
            break                    
    
    # capture = cv2.VideoCapture(f"{videoPath}/{state}.mp4")
    # _, videos = capture.read()
    cTime = time.time()
    fps = int(1 / (cTime - psTime))
    psTime = cTime
    cv2.putText(img, f'FPS = {fps}', (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
    cv2.putText(img, f"Count Set: {int(dcount)}", (500, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    cv2.putText(img, f'User : {user}', (350, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
    cv2.putText(img, f'{state}', (200, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
    background[160:640, 320:960] = img
    cv2.imshow("Image", background)

    cv2.waitKey(1)
    
