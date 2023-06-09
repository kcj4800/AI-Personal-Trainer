# AI-Personal-Trainer

## 개인적으로 만들어본 개인 프로젝트이지만 생에 첫 프로젝트입니다.

## 라이브러리는 opencv, mediapipe, dlib, face_recognition 등이 필요합니다.

### 설정 방법은
1. VSCode 터미널에서 python -m venv env
2. F1 - select interpreter - 방금 만든 가상환경 선택
3. (env)가 앞에 잘 붙어있으면 성공
4. 권한이 없어서 에러가 뜨고 안된다면

  4.1 검색 - powershell 관리자 권한으로 실행
  4.2 Set-ExecutionPolicy RemoteSigned
5. pip install opencv-python 으로 opencv 선택
6. python -m pip install --upgrade pip
7. 코드를 실행해서 잘 나오는지 확인
8. pip install mediapipe
9. visual studio 커뮤니티 무료 버전을 다운 받고, desktop에서 C++ 체크 해준 뒤 설치.
10. dlib 및 face_recognition 설치 순서 - 헤매지 말고 이대로!

  10.1 pip install cmake
  10.2 pip install wheel
  10.3 pip install dlib
  10.4 pip install face_recognition
11. 나머지 라이브러리 설치.

  11.1 pip install just-playback
  11.2 pip install pycaw
