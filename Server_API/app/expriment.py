from datetime import datetime

data = {  
    "divicename" : "미선",  
    "Humidity": "100 %",
    "Temperature":"90 *C",
    "Fire ": "80 %",
    "sound": "70 %",
    "sensorValue": "60 %",
    "Vol":"50 %", 
    "ppm": "5000 %"
 
 } 
    
ListOfDict = [ [key,val] for key, val in data.items()]

deviceName = ListOfDict[0][0]   
deviceValue = ListOfDict[0][1].rstrip().lstrip()

save = []

for val in ListOfDict[1:]:
    sensorName = val[0].rstrip().lstrip()
    value = val[1].split()[0].rstrip().lstrip()
    unit = val[1].split()[1].rstrip().lstrip()
    time  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    dictionary = {
            "deviceName" : deviceValue,
            "sensorname"  :sensorName,
            "value" : value,
            "unit" : unit,
            "time" : time 
        }

    save.append(dictionary)
print(save)

    # for key, val in data():
    #     print(data[i])
    #     value = data[i].split()[0]
    #     unit  = data[i].split()[1]
    #     time  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #     dictionary = {
    #         "sensorname"  : i,
    #         "value" : value,
    #         "unit" : unit,
    #         "time" : time 
    #     }
    #     print(dictionary)
    #     db.db.sensor.insert_one(dictionary)
    # return jsonify({'ok': True, 'message': 'Sensor created successfully!'}), 200