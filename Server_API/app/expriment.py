
# Connect MongoDB with flask server :
# -> https://medium.com/@riken.mehta/full-stack-tutorial-flask-react-docker-ee316a46e876

import os

from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from flask_pymongo import PyMongo 
from datetime import datetime
app = Flask(__name__)

# add mongo url to flask config, so that flask_pymongo can use it to make connection
app.config['MONGO_URI'] = os.environ.get('DB')
db = PyMongo(app, uri="mongodb://localhost:27017/test")

# initialize database migration management
# migrate = Migrate(app, db)

@app.route("/")
def hello():
    return "Hello World!"

# 우리가 확인해야할 것 

# SAVE DATA TO DB
@app.route("/add", methods=["POST"]) 
def add():

    data = request.get_json()   # json으로 전송된 데이터[formData - 형식은 "dict" ]를 불러오기 
    ListOfDict = [ [key,val] for key, val in data.items()] # dict 로 저장된 값을 key, value 로 나누어 리스트에 저장하기 
                # [ ["deviceName", " 미선"], ["Huminity", "33 %"],  ["Huminity", "33 %"] ''']
    deviceName = ListOfDict[0][0].strip()    
    deviceValue = ListOfDict[0][1].strip()  

    # 센서값을 DB 형시에 맞추어 저장되도록 파싱하기 
               # 센서값이 있는 [1:]부터 시작 
    for val in ListOfDict[1:]:    
        # print(type(val))  # val = ["Huminity", "33 %"] 
        sensorName = val[0].strip()   # "Huminity"
        # val[1].split() = 센서값과 센서측정단위를 구분해서 저장해주기 위한 처리  "33 %"--> ["33" ,  " %"]
        value = val[1].split()[0].strip()   # "33"
        unit = val[1].split()[1].strip()    # "%"
        time  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        dictionary = {
            "deviceName" : deviceValue,
            "sensorname"  :sensorName ,
            "value" : value,
            "unit" : unit,
            "time" : time 
        }

        i = len(ListOfDict[1:])
        print(i, dictionary)
        db.db.sensor.insert_one(dictionary)
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
    app.debug = True
    app.run(host='0.0.0.0')