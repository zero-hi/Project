# 동영상 캡쳐
import cv2
import os

def video_cut(path, file_name, frame_set):

    # 영상 경로 설정
    video_path = path + file_name
    print(video_path)

    # VideoCapture : 동영상 파일 또는 카메라 열기
    capture = cv2.VideoCapture(video_path)
    count = 0

    while True:
        # read : 프레임 읽기
        # [return]
        # 1) 읽은 결과(True / False)
        # 2) 읽은 프레임
        retval, frame = capture.read()

        # 읽은 프레임이 없는 경우 종료
        if not retval:
            break
        
        resize_frame = cv2.resize(frame, (740, 480), interpolation=cv2.INTER_AREA)

        if(int(capture.get(1)) % frame_set == 0):      #50 frame당 한 frame만 저장 (1.7초)
            # print('Saved frame number: '+str(int(capture.get(1))))
            cv2.imwrite("./img/frame%d.jpg" % count, resize_frame)#새롭게 .jpg 파일로 저장
            print('Saved frame%d.jpg' % count)
            count += 1

        # 프레임 출력
        # cv2.imshow("resize_frame", resize_frame)
        
        # 'q' 를 입력하면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 동영상 파일 또는 카메라를 닫고 메모리를 해제
    capture.release()

    # 모든 창 닫기
    cv2.destroyAllWindows()

