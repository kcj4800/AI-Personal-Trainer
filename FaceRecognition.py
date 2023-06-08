import cv2
import numpy as np
import face_recognition


####################################
# dlib 설치 순서 - 헤매지말고 이대로!
# pip install cmake
# pip install wheel
# pip install dlib
# pip install face_recognition까지 마치면 완성!
####################################
# cap = cv2.VideoCapture(0)
# success, img = cap.read()
# 일론머스크 이미지와 테스트 이미지를 불러와 face_recognition하기
imgElon = face_recognition.load_image_file('FaceImages/Elon Musk.jpg')
imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)
imgTest = face_recognition.load_image_file('FaceImages/Bill Gates.jpg')
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

# face_recognition한 이미지의 face_location 정보를 불러와 사각형으로 표시해준다.
faceLoc = face_recognition.face_locations(imgElon)[0] # facelocation을 찾기위한 이미지를 보내주기
encodeElon = face_recognition.face_encodings(imgElon)[0]
cv2.rectangle(imgElon, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)
print(faceLoc)  # (118, 304, 304, 118) top right bottom left

faceLocTest = face_recognition.face_locations(imgTest)[0] # facelocation을 찾기위한 이미지를 보내주기
encodeTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

results = face_recognition.compare_faces([encodeElon], encodeTest)

faceDis = face_recognition.face_distance([encodeElon], encodeTest)
# 같은 사람의 경우 0.5 이하로 일치함을 갖으며, 다른 사람의 경우 0.5 이상의 값을 갖는다.

print(results, faceDis) 


cv2.putText(imgTest, f'{results}{round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


cv2.imshow('Elon Musk', imgElon)
cv2.imshow('Elon Test', imgTest)
cv2.waitKey(0)








'''
테스트 코딩
# import the libraries
import os
import face_recognition
 
# make a list of all the available images
images = os.listdir('images')
print(images)
 
# load your image
image_to_be_matched = face_recognition.load_image_file('my_image.jpg')
 
# encoded the loaded image into a feature vector
image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)[0]
 
# iterate over each image
for image in images:
    # load the image
    current_image = face_recognition.load_image_file("images/" + image)
    # encode the loaded image into a feature vector
    current_image_encoded = face_recognition.face_encodings(current_image)[0]
    # match your image with the image and check if it matches
    result = face_recognition.compare_faces(
        [image_to_be_matched_encoded], current_image_encoded)
    # check if it was a match
    if result[0] == True:
        print("Matched: " + image)
    else:
        print("Not matched: " + image)
'''