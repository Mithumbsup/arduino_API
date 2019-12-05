
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
    #{'deviceName': 'place2', 'sensorName': 'PM 10', 'sensorValue': ' 336 ug/m3', 'time': '2019-12-05 17:35:18'}
    ListOfDict = [ data[key] for key in data.keys()] # dict형식은 반복문을 돌릴 수 없음으로 리스트형식으로 바꿔줌
    deviceValue = ListOfDict[0].strip()   # .strip() 빈 공백 없애주기 
    sensorName = ListOfDict[1].strip()   # "Huminity"
    value = ListOfDict[2].split()[0].strip()   # "33"
    unit = ListOfDict[2].split()[1].strip()    # "%"
    time = ListOfDict[3]

    dictionary = {

    "deviceName" : deviceValue,
    "sensorname"  :sensorName ,
    "value" : value,
    "unit" : unit,
    "time" : time

    }
    print(dictionary)
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