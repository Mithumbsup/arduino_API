# pySerial API : https://pyserial.readthedocs.io/en/latest/pyserial_api.html

import serial
from datetime import datetime
import time
time.sleep(1)

ser = serial.Serial('COM15', 9600) # Serial(Comport,baudrate)
ser.flushInput()

while True:
    try:
        # 1. 아두이노에서 받은 시리얼값을 문자열로 인코딩해서 리스트에 담기  
        
        SVT = []
        serial = ser.readline().decode() # 문자열로 10개 센서에 해당하는 시리얼값 변환
        SVT = serial.split(",")  # , 를 구분으로 센서이름과 값 SVT 리스트로 담기 
        sensorToList = [x.strip() for x in SVT if x.strip()]  # SVT 리스트에 공백제거
        sensor =   [ oneSensor.split(":")  for oneSensor in sensorToList ]  # 센서이름, 센서값 리스트로 분리해서 담기 
        # print(sensor)

        # 2. 문자열로 인코딩한 시리얼값을 받은 리스트에 센서값만 따로 리스트에 담기  

        sensorValue = [] # 센서값들의 총추출 값이 들어갈 리스트
        for Value in sensor:    # 센서값 추출 
            sensorValue.append(Value[1])
        print(sensorValue)

        # 3. 모든 센서값(10개)가 리스트에 담기면 formData로 서버로 전송, 아니면 지우기 
        if len(sensorValue) == 11:
            import requests 
            API_ENDPOINT = "http://203.255.67.238:5000/add"

            formData = {

                'deviceName': "미선",
                'sensorValue': sensorValue[0],
                'Vol ':  sensorValue[1], 
                'ppm':  sensorValue[2],
                'PM 1.0': sensorValue[3],
                'PM 2.5': sensorValue[4],
                'PM 10': sensorValue[5],
                'Humidity':  sensorValue[6],
                'Temperature':  sensorValue[7],
                'Fire1 ': sensorValue[8],
                'Fire2 ': sensorValue[9],
                'sound ':  sensorValue[10]
               
            }
            
            response = requests.post(url = API_ENDPOINT, json = formData)
            print(response.text)
            del sensorValue[:]

        else:
            del sensorValue[:]
            continue

        print(formData)
           
    except:
        print("오류 발생")

        
