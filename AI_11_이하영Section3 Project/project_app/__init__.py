from flask import Flask, render_template, request
import pandas as pd
import pickle

model = None
with open('model.pkl','rb') as pickle_file:
   model = pickle.load(pickle_file)

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

# 페이지 구성
@app.route('/')
def main_html():
    return render_template('main.html')

@app.route('/test')
def test_html():
    return render_template('test.html')

@app.route('/result', methods = ['POST', 'GET'])
def result_html():
    if request.method == 'POST':
        # 데이터 가져오기
        age = int(request.form.get("age"))
        gender = int(request.form.get("gender"))
        height = int(request.form.get("height"))
        weight = float(request.form.get("weight"))
        ap_hi = int(request.form.get("ap_hi"))
        ap_lo = int(request.form.get("ap_lo"))
        cholesterol = int(request.form.get("cholesterol"))
        gluc = int(request.form.get("gluc"))
        smoke = int(request.form.get("smoke"))
        alco = int(request.form.get("alco"))
        active = int(request.form.get("active"))
        # 데이터 합치기
        data = [[age,gender,height,weight,ap_hi,ap_lo,cholesterol,gluc,smoke,alco,active]]
        # 컬럼 이름 지정
        column_name = ["age","gender","height","weight","ap_hi","ap_lo","cholesterol","gluc","smoke","alco","active"]
        # 데이터 프레임으로 변환
        input_data = pd.DataFrame(data, columns=column_name)
        # 모델 실행
        y_pred = model.predict(input_data)
        # 예측결과
        if y_pred == 0:
            result_mag = " 심혈관 질환에 대한 위험도가 낮습니다. "
        else:
            result_mag = " 심혈관 질환에 대한 위험도가 높습니다. "

        return render_template('result.html', result_mag = result_mag)

    # result_mag = " 심혈관 질환에 대한 위험도가 낮습니다. "
    return render_template('result.html')
    
