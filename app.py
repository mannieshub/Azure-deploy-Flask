import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import requests
import time

# Create Flask app
app = Flask(__name)

# Load the pickle model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        float_features = [float(x) for x in request.form.values()]
        features = [np.array(float_features)]
        probabilities = model.predict_proba(features)
        probabilities_percent = probabilities * 100
        percent = probabilities_percent[0][1]
        result = {
            "prediction_text": "ความเสี่ยงที่คุณจะเป็นโรคหลอดเลือดหัวใจใน 10 ปีข้างหน้า : {:.2f}%".format(
                probabilities_percent[0][1]
            ),
            "percent": str(round(percent, 2)),
        }
        return jsonify(result)
    except Exception as e:
        error_message = {"error": str(e)}
        return jsonify(error_message), 400

def send_post_request():
    url = 'chd-server.azurewebsites.net/predict'  # เปลี่ยน URL เป็น URL ของเซิร์ฟเวอร์ที่คุณต้องการส่งข้อมูลไป
    data = {
        'gender': '0', 
        'age': '0',
        'education':'0',
        'currentSmoker':'0',
        'cigsPerDay':'0',
        'BPMeds':'0',
        'prevalentStroke':'0',
        'prevalentHyp':'0',
        'diabetes':'0',
        'totChol':'0',
        'sysBP':'0',
        'diaBP':'0',
        'BMI':'0',
        'heartRate':'0',
        'glucose':'0',
        }  # แก้ไขข้อมูลที่คุณต้องการส่ง

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("ส่งคำขอ HTTP POST สำเร็จ")
    else:
        print("เกิดข้อผิดพลาดในการส่งคำขอ")

if __name__ == "__main__":
    # สร้างเธรดสำหรับการส่งคำขอ HTTP POST ทุก 6 ชั่วโมง
    while True:
        send_post_request()
        time.sleep(6 * 60 * 60)  # หน่วยเวลาคือวินาที (6 ชั่วโมง)
