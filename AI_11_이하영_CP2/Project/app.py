
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import capture
import torch
import glob
import shutil
import sys

# 플라스크 실행

app = Flask(__name__)
"""========경로 설정========"""
# 현재 위치 -> "./test" or "./PJ2"
path = os.path.dirname(os.path.abspath(__file__))

video_save_path= path + "/video/"

pt_file_path = "best200.pt"

"""========================="""
@ app.route('/')  # 기본 페이지
def main_html():
    # print("this is main page")
    return render_template('main.html')

@ app.route('/result', methods=['POST', 'GET'])
def result_html():
    # 파일을 받았을 경우
    if request.method == 'POST':
        # 동영상 받아오기
        file = request.files['chooseFile']
        file_name = secure_filename(file.filename)
        # frame 받기
        frame_set = int(request.form.get("frame"))
        # file 저장 _ 저장할 경로 + 파일명
        file.save((video_save_path) + secure_filename(file.filename))
        # 캡쳐 함수 실행 _ 파일 경로 / 파일 이름
        capture.video_cut(video_save_path,file_name, frame_set)
        # 모델 불러오기
        model = torch.hub.load('ultralytics/yolov5', 'custom', pt_file_path)
        # 캡쳐한 이미지 리스트 생성
        capture_list = glob.glob('./img/*.jpg')

        result_list = []     # 결과물 저장 리스트
        for img in capture_list:
            result_img = model(img)
            result_list.append(result_img)

        """==========결과메세지============="""
        # 파일 생성
        sys.stdout = open('ob_results.txt','w')
        print("ob_results")
        # print(reslut) -> 저장
        for i in result_list:
            sys.stdout = open('ob_results.txt','a')
            print(i)
        # 한줄씩 저장
        f = open('ob_results.txt','r', encoding='UTF8')
        one_lines = f.readlines()
        # 결과물만 따로 저장
        results = []
        for i in one_lines:
            if '1/1' in i:
                results.append(i)
            else:
                pass
        # 헬멧 인식 텍스트 저장
        result_message = []
        color = []
        for i in results:
            if 'helmet' in i:
                success = '헬멧이 인식 되었습니다.'
                result_message.append(success)
                Green = 1
                color.append(Green)
            else:
                fail = '헬멧이 인식되지 않았습니다.'
                result_message.append(fail)
                Red = 0
                color.append(Red)

        sys.stdout.close()        
        """================================="""

        # 폴더 생성후 결과물 저장
        for ob_img in result_list:
            ob_img.save('./Project/' ,'ob_results')
        
        # 결과물 출력폴더에 이동시키기
        file_name_list = os.listdir('ob_results')

        for file_name in file_name_list:
            shutil.move('ob_results/' + file_name, './static/capture/')

        """ 출력용 리스트 따로 생성 """
        capture_path = "./static/capture/"
        image_list = os.listdir(capture_path)
        new_list = []
        for image in image_list:
            image_name = "capture/" + image
            new_list.append(image_name)

        total_list = zip(new_list, result_message, color)
        frame = ("Frame : %d" % frame_set)
        return render_template('result.html' ,total_list=total_list, frame=frame)
        # , image_file='capture/aaaa.png'

    return render_template('main.html')



if __name__ == "__main__":
    app.run()
