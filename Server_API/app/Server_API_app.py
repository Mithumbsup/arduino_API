
# Connect MongoDB with flask server :
# -> https://medium.com/@riken.mehta/full-stack-tutorial-flask-react-docker-ee316a46e876

import os

from flask import Flask, render_template, request, jsonify 
from flask_migrate import Migrate
from flask_pymongo import PyMongo 

app = Flask(__name__)

# add mongo url to flask config, so that flask_pymongo can use it to make connection
app.config['MONGO_URI'] = os.environ.get('DB')
db = PyMongo(app, uri="mongodb://localhost:27017/test")

# initialize database migration management
# migrate = Migrate(app, db)

@app.route("/")
def hello():
    return "Hello World!"

# SAVE DATA TO DB
@app.route("/add", methods=["POST",'PATCH']) #몽고DB를 작성["POST"]하고, 수정['PATCH']할 수 있는 통신 방법
def add():
    # formdata로 받은 센서값
    data = request.get_json() #{ "Humidity" : "48.90 %","Humidity" : "48.90 %" ,,, }
    # json으로 받은 문장형 데이터들을 단어를 나누어 
    # 몽고 DB에 있는 데이터필드 sensor_name, value , unit 에 넣어줘야함
    # 1. split   - 문장을 나눠준다
        # 1.1 딕트를 리스트로 형식으로 변환!
        # 1.2 /n = 문자열 안에서 줄을 바꾸는 것을 기준으로 리스트에 담에 저장해라!
    DicToList = data.split('\n')

    # 2. slicing  - 문장에서 단어로 나눠준다 
    for i in DicToList:    
        sentence = i.split()  # 공백이 보이면 나눠라 
        print(sentence) # Humidity: 48.90 % 
        SentenceToWords = sentence.split(":") #['Humidity', ' 48.90 %']
        ValuePlusUnit = SentenceToWords[1].rstrip().lstrip() # 48.90 %  rstrip = 오른쪽 공백 제거 lstrip= 왼쪽 공백 제거
        SeperateUnit = ValuePlusUnit.split()  # ['48.90', '%']

        # 2.1 단어로 나눠서 "data" json파일로 저장해준다
        data['sensor_name'] = SentenceToWords[0].rstrip().lstrip() # Humidity
        data['value'] = SeperateUnit[0].rstrip().lstrip() # 48.90
        data['unit'] = SeperateUnit[1].rstrip().lstrip() # % 

    # sensor 테이블에 "data"파일을 넣어줌 
    db.db.sensor.insert_one(data) 
    return jsonify({'ok': True, 'message': 'Sensor created successfully!'}), 200
        
@app.route("/getlimit/<limit_>")
def get_limit(limit_):
    from Server_API_models import SensorData
    try:
        sensorData=SensorData.query.limit(limit_)
        return  jsonify([e.serialize() for e in sensorData])
    except Exception as e:
        return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    #from Server_API_models import SensorData
    try:
        sensorData=db.db.sensor.find_one_or_404({"unit":id_})
        return jsonify(sensorData)
    except Exception as e:
        return(str(e))

if __name__ == '__main__':
    app.run(host='127.0.0.1')