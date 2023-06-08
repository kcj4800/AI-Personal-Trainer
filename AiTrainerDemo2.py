import cv2
import numpy as np
import time
import PoseModule as pm
import HandTrackingModule as htm
import os
import face_recognition
from just_playback import Playback # if 조건으로 감싸서 헛도는 것을 방지해줘야 한다.


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
11. 종료 - 80%
12. 음원 - 0%
'''
# Video Setting
cap = cv2.VideoCapture(0)
psTime = 0
play = Playback()
play.set_volume(1.0)
play1 = Playback()
play1.set_volume(0.3)
# play2 = Playback()
# play2.set_volume(0.3)
# play3 = Playback()
# play3.set_volume(0.3)
# play4 = Playback()
# play4.set_volume(0.3)
# play5 = Playback()
# play5.set_volume(0.3)
# play6 = Playback()
# play6.set_volume(0.3)
# play7 = Playback()
# play7.set_volume(0.3)
# play8 = Playback()
# play8.set_volume(0.3)
# play9 = Playback()
# play9.set_volume(0.3)
# play10 = Playback()
# play10.set_volume(0.3)
# play11 = Playback()
# play11.set_volume(0.3)
# play12 = Playback()
# play12.set_volume(0.3)
# play13 = Playback()
# play13.set_volume(0.3)

# Module Setting
pDetector = pm.poseDetector()
hDetector = htm.handDetector(maxHands=1)

# Background Setting
folderPath = "Background"
myList = os.listdir(folderPath)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

background = overlayList[11]

# BGM Setting
myBgm = os.listdir('Audios/bgm')
print(len(myBgm))
# exit()
# play1.load_file(f"./Audios/bgm/{myBgm[0]}")
# play2.load_file(f"./Audios/bgm/{myBgm[1]}")
# play3.load_file(f"./Audios/bgm/{myBgm[2]}")
# play4.load_file(f"./Audios/bgm/{myBgm[3]}")
# play5.load_file(f"./Audios/bgm/{myBgm[4]}")
# play6.load_file(f"./Audios/bgm/{myBgm[5]}")
# play7.load_file(f"./Audios/bgm/{myBgm[6]}")
# play8.load_file(f"./Audios/bgm/{myBgm[7]}")
# play9.load_file(f"./Audios/bgm/{myBgm[8]}")
# play10.load_file(f"./Audios/bgm/{myBgm[9]}")
# play11.load_file(f"./Audios/bgm/{myBgm[10]}")
# play12.load_file(f"./Audios/bgm/{myBgm[11]}")
# play13.load_file(f"./Audios/bgm/{myBgm[12]}")



# for imPath in myList:
#     bgmList.append(imPath)
print(myBgm)


# Parameters Setting
count = 0
pCount = 0
dcount = 10
dir = 0
state = ""
user = ""
user_state = 0
userTime = 50
pbLimit = 0
bgm = 0
bgmm = 1

# main Time
mTime = time.time()

# End Timer
endTime = 50

# User Infomation
age = {"Chan" : 30, "Hana" : 25}
sex = {"Chan" : "Male", "Hana" : "Female"}
music = ["Love Love Love", "Dinosaur", "Holy Moly"]
option = ""

# User Recognition!
iPath = 'FaceImages'
uImages = []
classNames = []

myList = os.listdir(iPath)

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

# Exercise List
squat = ['squat', [0, 1, 0, 0, 0], 1, [24, 26, 28], 20, 70, 0, 100, 450, 150]
push_up = ['push_up', [0, 1, 1, 0, 0], 2, [12, 14, 16], 10, 90, 0, 100, 450, 150]
shoulder_press = ['shoulder_press', [0, 1, 1, 1, 0], 3, [12, 14, 16], 30, 110, 100, 0, 150, 450]
dumbbel_r = ['dumbbel_r', [0, 1, 1, 1, 1], 4, [12, 14, 16], 10, 135, 0, 100, 450, 150]
dumbbel_l = ['dumbbel_l', [0, 1, 1, 2, 2], 4, [11, 13, 15], 10, 135, 0, 100, 450, 150]
pull_up = ['pull_up', [1, 1, 1, 1, 1], 5, [12, 14, 16], 20, 90, 0, 100, 450, 150]
exerciseList =[squat, push_up, shoulder_press, dumbbel_r, dumbbel_l, pull_up]

# Option List
hi = ['hi', [1, 0, 0, 0, 0], 6]
countOpt = ['count', [1, 1, 0, 0, 0], 7]
musicOpt = ['music', [0, 1, 0, 0, 1], 8]
userOpt = ['user', [1, 0, 0, 0, 1], 9]
quitOpt =  ['quit', [1, 1, 0, 0, 1], 10]
optionList = [hi, countOpt, musicOpt, userOpt, quitOpt]

while True :
    # Program Start!
    success, img = cap.read()
    img = cv2.resize(img, (640, 480))
    
    # User Recognition!
    if state == "" and user == "":

        if pbLimit == 0:
            play.load_file(f"./Audios/hi.mp3")
            play.play()
            pbLimit = 1
            
        # Image Resizing
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
                user_state = 1
                pbLimit = 0
                state = 'main'
    
    # Main!
    if state == 'main':       
        img = hDetector.findHands(img)
        lmList, bbox = hDetector.findPosition(img, draw = False)
        if len(lmList) != 0:
            fingers = hDetector.fingersUp()
            hTime = time.time()
            # print(fingers, int(hTime - mTime))
            
            # Select Exercise
            for i in exerciseList:
                
                if fingers == i[1]:
                    endTime -= 0.5
                    cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                    if endTime == 0:
                        background = overlayList[i[2]]
                        endTime = 50
                        option = "exercise"
                        state = i[0]
                        
                 # Except Reset
                elif fingers == [0, 0, 0, 0, 0]:
                    endTime = 50
                    
            # Select Option
            for i in optionList:
                
                if fingers == i[1]:
                    endTime -= 0.5
                    cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                    if endTime == 0:
                        background = overlayList[i[2]]
                        endTime = 50
                        option = "option"
                        state = i[0]
                        
                 # Except Reset
                elif fingers == [0, 0, 0, 0, 0]:
                    endTime = 50
    
    # Exercise!
    if option == "exercise":

        for i in exerciseList:
            if state == i[0]:
                if pbLimit == 0:
                    play.load_file(f"./Audios/countdown.mp3")
                    play.play()
                    pbLimit = 1
                    
                img = pDetector.findPose(img, False)
                lmList = pDetector.findPosition(img, False)
                pTime = time.time()
                if pTime - hTime <= 3:
                    cv2.putText(img, f'{3 - int(pTime-hTime)}', (200, 400), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 15, (0, 0, 255), 4)
                
                if len(lmList) != 0 and pTime - hTime > 3:
                    if pbLimit == 1:
                        play.load_file(f"./Audios/{i[0]}.mp3")
                        play.play()
                        pbLimit = 2                    
                    # Find Angle
                    angle, lineList = pDetector.findAngle(img, i[3][0], i[3][1], i[3][2])
                    angle = abs(angle - 180)
                    per = np.interp(angle, (i[4], i[5]), (i[6], i[7]))
                    sq = np.interp(angle, (i[4], i[5]), (i[8], i[9]))
                    
                    # Check for the exercise
                    color = (255, 0, 255)
                    if per == 100:
                        color = (0, 255, 0)
                        if dir == 0:
                            count += 1
                            dir = 1
                    if per < 10:
                        color = (0, 255, 0)
                        if dir == 1:
                            dir = 0
                    
                    # Draw Bar
                    cv2.rectangle(img, (20, 150), (70, 450), color, 3)
                    cv2.rectangle(img, (20, int(sq)), (70, 450), color, cv2.FILLED)
                    cv2.putText(img, f'{int(per)}%', (15, 480), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
                    # cv2.putText(img, f'{int(angle)}', (400, 100), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)
                    
                    # Count
                    cv2.putText(img, f'{int(count)}/{dcount}', (10, 130), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
                    if int(pCount) != int(count):
                        play.load_file(f"./Audios/{int(count % 10)}.mp3")
                        play.play()
                        # os.system(f'python playCountSound.py {int(count)}')
                        pCount = count
                    
                    if count == dcount:
                        count = 0
                        pCount = 0
                        endTime = 50
                        pbLimit = 0
                        
                        if state == "dumbbel_r":
                            state = "dumbbel_l"
                            
                        else:
                            background = overlayList[0]
                            option = 'main'
                            state = 'main'
                        
                    # End Mission!
                    if lmList[16][2] < lmList[14][2] and lmList[14][2] < lmList[12][2] and lmList[15][2] < lmList[13][2] and lmList[13][2] < lmList[11][2] and lmList[16][1] > lmList[15][1] and lmList[14][1] < lmList[13][1]:
                        endTime -= 1
                        cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                            
                        if endTime == 0:
                            background = overlayList[0]
                            endTime = 50
                            pCount = 0
                            count = 0
                            pbLimit = 0
                            option = 'main'
                            state = 'main'
                    else :
                        endTime = 50
    # Option!           
    elif option == "option":
        
        # Hi!       
        if state == "hi":
            if pbLimit == 0:
                play.load_file(f"./Audios/welcome.mp3")
                play.play()
                pbLimit = 1
            endTime -= 0.5
            cv2.putText(img, f'Hi! {user}!', (50, 200), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 3)
            cv2.putText(img, f'Welcome to the', (50, 300), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 3)
            cv2.putText(img, f'A.I World!', (50, 400), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 3)
            if endTime == 0:
                pbLimit = 0
                background = overlayList[0]
                endTime = 50
                option = 'main'
                state = 'main'
                
        # Count!            
        elif state == 'count':
            if pbLimit == 0:
                play.load_file(f"./Audios/count.mp3")
                play.play()
                pbLimit = 1
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
    
                    # If pinky is down set count
                    if fingers[4] == 0 and (countTime - hTime) > 3:
                        endTime -= 0.5
                        cColor = (0, 255, 0)
                        cPer = per
                        dcount = cPer
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, cColor, cv2.FILLED) # lineInfo = [x1, y1, x2, y2, cx, cy]
                        cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                        if endTime == 0:
                            pbLimit = 0
                            endTime = 50
                            background = overlayList[0]
                            option = 'main'
                            state = 'main'                        

                    else :
                        cColor = (255, 0, 0)
                        endTime = 50
                        
                    # Draw
                    cv2.rectangle(img, (bbox[0]-20,bbox[1]-20), (bbox[2]+20, bbox[3]+20), (0, 255, 0), 2)   
                    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 2)
                    cv2.rectangle(img, (50, int(bar)), (85, 400), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'Count : {int(per)}', (10, 450), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

        # User!
        elif state == "user":
            if pbLimit == 0:
                play.load_file(f"./Audios/user_info.mp3")
                play.play()
                pbLimit = 1
                
            endTime -= 0.5
            cv2.putText(img, f'Name : {user}!', (50, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.putText(img, f'Age : {age[user]}, sex : {sex[user]}', (50, 300), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.putText(img, f'Have a good Exercise!', (50, 400), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            if endTime == 0:
                pbLimit = 0
                background = overlayList[0]
                endTime = 50
                option = 'main'
                state = 'main'
                
        # Music!        
        elif state == "music":
            if pbLimit == 0:
                play.load_file(f"./Audios/bgm.mp3")
                play.play()
                pbLimit = 1
            img = hDetector.findHands(img)
            lmList, bbox = hDetector.findPosition(img, draw = False)
            cPer = dcount

            if len(lmList) != 0:
                countTime = time.time()
                area = (bbox[2]-bbox[0]) * (bbox[3]-bbox[1])//100
            
                if 100 < area < 1250 :
                    length, img, lineInfo = hDetector.findDistance(4, 8, img)
                    bar = np.interp(length, [20, 200], [50, 410])
                    per = np.interp(length, [20, 200], [1, 13])

                    # Reduce Resolution to make it smoother
                    # smoothness = 1
                    # per = smoothness * round(per/smoothness)
                    
                    # Check which fingers are up
                    fingers = hDetector.fingersUp()
    
                    # If pinky is down set count
                    if fingers[4] == 0 and (countTime - hTime) > 3:
                        endTime -= 0.5
                        cColor = (0, 255, 0)
                        cPer = int(per) - 1

                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, cColor, cv2.FILLED) # lineInfo = [x1, y1, x2, y2, cx, cy]
                        cv2.putText(img, f"Select : {int(endTime/10)}", (50, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
                        if endTime == 0:
                            pbLimit = 0
                            endTime = 50
                            background = overlayList[0]
                            bgm = cPer
                            option = 'main'
                            state = 'main'                        

                    else :
                        cColor = (255, 0, 0)
                        endTime = 50
                        
                    # Draw
                    cv2.rectangle(img, (bbox[0]-20,bbox[1]-20), (bbox[2]+20, bbox[3]+20), (0, 255, 0), 2)   
                    # cv2.rectangle(img, (50, 150), (85, 450), (0, 255, 0), 2)
                    cv2.rectangle(img, (50, int(bar)-10), (85, int(bar)+10), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'Music Num : {int(per)}. {myBgm[int(per)-1]}', (10, 450), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                    
                    for i in range(len(myBgm)):
                        cv2.putText(img, f'{i+1} : {myBgm[i]}', (100, 50+i*30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
            
            # cv2.putText(img, f'1. : {music[0]}', (50, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            # cv2.putText(img, f'2. : {music[1]}', (50, 300), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            # cv2.putText(img, f'3. : {music[2]}', (50, 400), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            if endTime == 0:
                pbLimit = 0
                background = overlayList[0]
                endTime = 50
                option = 'main'
                state = 'main'
                    
                    
        # Quit!
        if state == "quit":
            if pbLimit == 0:
                play.load_file(f"./Audios/bye.mp3")
                play.play()
                pbLimit = 1
                
            cv2.putText(img, f"Good Bye! {user}", (50, 200), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,255), 3)
            cv2.putText(img, "Have a Nice Day", (50, 300), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,255), 3)
            endTime -= 0.5
            if endTime == 0:
                break
    
    # User Recognition
    if user_state == 1:
        if pbLimit == 0:
            play.load_file(f"./Audios/{user}.mp3")
            play.play()
            pbLimit = 1
           
        cv2.putText(img, f'Hi {user}!', (120, 250), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 2)
        userTime -= 0.5
        if userTime == 0:
            pbLimit = 0
            user_state = 0


    # Video Showing!
    cTime = time.time()
    fps = int(1 / (cTime - psTime))
    psTime = cTime
    cv2.putText(img, f'FPS = {fps}', (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
    cv2.putText(img, f"Count Set: {int(dcount)}", (500, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    cv2.putText(img, f'User : {user}', (350, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
    cv2.putText(img, f'{state}', (200, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
    background[160:640, 320:960] = img
    cv2.imshow("A.I Exercise", background)
    
    
    # for i in range(len(myBgm)):

    # if bgm == 0:
    #     msTime = time.time()
    #     play1.load_file(f"./Audios/bgm/{myBgm[bgm]}") 
    #     play1.play()
    #     print(int(msTime - mTime), bgm)
    #     if int(msTime - mTime) > 20:
    #         bgm = 1
            
    if bgm != bgmm:
        play1.load_file(f"./Audios/bgm/{myBgm[bgm]}")
        play1.play()
        bgmm = bgm 

    # if bgm == 1:
    #     play1.load_file(f"./Audios/bgm/{myBgm[bgm]}") 
    #     play1.play()
    #     bgm = 2
        
    cv2.waitKey(1)
    
