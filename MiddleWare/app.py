
import serial

import time

time.sleep(1)

ser = serial.Serial('COM15', 9600)  # Serial(Comport,baudrate)
ser.flushInput()


#---------------------------------
# mini-batch로 저장

x = []
temp = {}
formData_list = []
key_list = ["Humidity", "Temperature", "Fire", "sound", "sensorValue", "Vol", "ppm"]

# for i in range(10):
for t in range (10): # mini-batch size == 10
    while True:
        readline_x = ser.readline().decode()
 
        if readline_x != ' \n':
            print(readline_x)
            sensor = readline_x.split()[0]
            val = readline_x.split()[1]
            unit = readline_x.split()[2]
            temp[sensor] = val+unit
            x.append([sensor, val+unit])

        if len(x)==7:
            break
    formData_list.append(x)
    x=[]


# for i in range(len(formData)):
#     print(len(formData[i]))
# 
# print(formData)
# len(formData[0])
# formData[0]
# formData[0][1][0]

formData_Dict = []
for i in range(10):
    # ppm.decode().split()
    for i,key in enumerate(formData_list[0]):
        # print(key)
        key = formData_list[0][i][0]
        val_unit = formData_list[0][i][1]
        temp[key]= val_unit
    formData_Dict.append(temp)

formData_Dict[2]
# print(formData_list)

# # 저장된 mini-batch를 수집 time interval 단위로 변환 & Request
# import requests
# API_ENDPOINT = "http://203.255.67.238:5000/add"

# for i in range(10):
#     # print(formData_Dict[i])
#     formData = formData_Dict[i]
#     response = requests.post(url=API_ENDPOINT, data=formData)
#     print(response.text)