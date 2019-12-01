
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

# SAVE DATA TO DB
@app.route("/add", methods=["POST"]) 
def add():
    data = request.get_json() #{ "Humidity" : "48.90 %","Humidity" : "48.90 %" ,,, }
        #  dict 
    for i in data:  # key : "Humidity" 
        print(data[i])  #  "48.90 %"
        # ["48.90"," %"] 
        value = data[i].split()[0]  # "48.90"
        unit  = data[i].split()[1]  # "%"
        time  = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #
        
        dictionary = {
            "sensorname"  : i, 
            "value" : value ,
            "unit" : unit ,
            "time" : time ,
        }

    for key, row in data.items(): # key : "Humidity" 
        print(data[i])  #  "48.90 %"
        # ["48.90"," %"] 
        value = data[i].split()[0]  # "48.90"
        unit  = data[i].split()[1]  # "%"
        time  = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #

        dictionary = {
            "sensorname"  : i, 
            "value" : value ,
            "unit" : unit ,
            "time" : time ,
        }
        print(dictionary)
        # listOfDicts.append(dictionary)
        db.db.sensor.insert_one(dictionary)
    # print(listOfDicts)
    # db.db.sensor.insert_one(listOfDicts) 
    #     data['sensor_name'] = SentenceToWords[0].rstrip().lstrip() # Humidity
    #     data['value'] = SeperateUnit[0].rstrip().lstrip() # 48.90
    #     data['unit'] = SeperateUnit[1].rstrip().lstrip() # % 
        
    # db.db.sensor.insert_one(data) 
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
    app.run(host='0.0.0.0')