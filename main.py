import cv2
import sys
import os

# 수화 영상 목록
signvideolist = os.listdir('C:/Users/2019A00296/sample/videodata')
# 수화별 영상 수
signclass = int(len(signvideolist) / 5)
# 배경 목록
backgroundlist = os.listdir('C:/Users/2019A00296/sample/background')
# 배경 수
bgclass = int(len(backgroundlist))
# 수화 영상 방향
direction = ['D', 'F', 'L', 'R', 'U']

# 배경 수
for i in range(1, bgclass+1):
    # 수화별 영상 수
    for j in range(1, signclass+1):
        # 수화 영상 방향 수
        for k in direction:

            cap1 = cv2.VideoCapture('C:/Users/2019A00296/sample/videodata/NIA_SL_SEN%d_REAL01_%s.mp4' % (j, k))

            if not cap1.isOpened():
                print('video open failed!')
                sys.exit()

            cap2 = cv2.VideoCapture('C:/Users/2019A00296/sample/background/%d_bedroom.mp4' % i)

            if not cap2.isOpened():
                print('video open failed!')
                sys.exit()

            w = round(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = round(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_cnt1 = round(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_cnt2 = round(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = round(cap1.get(cv2.CAP_PROP_FPS))

            delay = int(1000 / fps)

            do_composit = True

            fourcc = cv2.VideoWriter_fourcc(*'XMP4')
            writer = cv2.VideoWriter('BG%d_NIA_SL_SEN%d_REAL01_%s.mp4' % (i, j, k), fourcc, 30.0, (w, h))

            while True:
                ret1, frame1 = cap1.read()

                if not ret1:
                    break

                if do_composit:
                    ret2, frame2 = cap2.read()

                    if not ret2:
                        break

                    # 수어 영상 RGB > HSV로 색 변환
                    hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
                    # 수어 영상의 파란색 영역 추출
                    mask = cv2.inRange(hsv, (90, 120, 25), (140, 255, 255))
                    # 마스크 연산(추출된 영역 + 복잡한 배경)
                    cv2.copyTo(frame2, mask, frame1)

                writer.write(frame1)
                key = cv2.waitKey(delay)

            cap1.release()
            cap2.release()
            writer.release()