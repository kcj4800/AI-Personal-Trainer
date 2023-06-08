import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'FaceImages'
images = []
classNames = []

myList = os.listdir(path)
print(myList)
for cl in myList:
    cImg = cv2.imread(f'{path}/{cl}')
    images.append(cImg)
    classNames.append(os.path.splitext(cl)[0]) # os.path.splitext = split extension 의 약자로 파일의 경로나 파일명을 직접 입력해주면, [0]에 파일명을 [1]에 확장자를 담아준다.
        
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # faceLoc = face_recognition.face_locations(img)[0]
        encodeimg = face_recognition.face_encodings(img)[0]
        # cv2.rectangle(img, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)
        encodeList.append(encodeimg)
    return encodeList

# 출석시스템
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        # print(myDataList)
        nameList = []
        
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dtstring}')

    
    

encodeListKnown = findEncodings(images)
# print(len(encodeListKnown))
print("Encoding Complete")

cap = cv2.VideoCapture(0)

while True :
    success, img = cap.read()
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
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            markAttendance(name)
        
    cv2.imshow("Images", img)
    cv2.waitKey(1)


        
'''

# zip함수
numbers = [1, 2, 3]
letters = ["A", "B", "C"]
for pair in zip(numbers, letters):
print(pair)

>>>>
(1, 'A')
(2, 'B')
(3, 'C')


# zip함수 병렬처리
for number, upper, lower in zip("12345", "ABCDE", "abcde"):
print(number, upper, lower)

>>>>
1 A a
2 B b
3 C c
4 D d
5 E e


# 고로 위의 경우
for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):

print(encodeFace, faceLoc)

>>>>
encodesCurFrame[0] facesCurFrame[0]
encodesCurFrame[1] facesCurFrame[1]
encodesCurFrame[2] facesCurFrame[2]
encodesCurFrame[3] facesCurFrame[3]
'''