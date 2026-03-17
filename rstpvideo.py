import cv2 as cv
import numpy as np

#rstp영상을 불러온다(설치위치명:세집매 삼거리, 설치위치명:충청남도 천안시 서북구 신당동 482-22)
rstp_url = "rtsp://210.99.70.120:1935/live/cctv001.stream"
rstp_video = cv.VideoCapture(rstp_url)

#첫 번째 프레임을 미리 읽어서 img와 display를 초기화합니다.
valid, img = rstp_video.read()

# 동영상 width, height 선언
width = int(rstp_video.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(rstp_video.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = rstp_video.get(cv.CAP_PROP_FPS)

#fps값을 넣어주어서 파일이 비정상적으로 생성되는 것을 방지.
if fps <= 0 or fps > 60: 
    fps = 20.0

#프레임당 대기 시간
delay = int(1000/fps)

# 가로로 두 영상을 붙이므로 가로 크기를 2배로 설정
fourcc = cv.VideoWriter_fourcc(*'mp4v')
savevideo = cv.VideoWriter('rstpvideo.mp4', fourcc, fps, (width * 2, height))

pause = False
display = img.copy()  # 이전 프레임을 저장할 변수

while rstp_video.isOpened():
    if not pause:
        valid, current_img = rstp_video.read() 
        if not valid:
            break
        img = current_img 
        wt = 1
    else:
        wt = delay#일시정지 시 녹화된 부분이 실제 시간과 같도록 함.

    #image subtraction
    diff = np.abs(img.astype(np.int32) - display.astype(np.int32)).astype(np.uint8)
    display = img.copy()

    # 화면 표시용(UI 포함) 프레임 생성
    frame = img.copy()
    if pause:
        cv.rectangle(frame, (20, 20), (40, 40), (0, 0, 0), -1)
    else:
        cv.circle(frame, (30, 30), 10, (0, 0, 255), -1)

    # 원본과 subtraction 영상을 가로로 결합
    merge = np.hstack((frame, diff))
    
    savevideo.write(merge)
    cv.imshow('record', merge)

    key = cv.waitKey(wt)
    if key == 32: # Spacebar를 누르면 일시정지
        pause = not pause
    elif key == 27: # ESC를 누르면 종료
        break

rstp_video.release()
savevideo.release()
cv.destroyAllWindows()
