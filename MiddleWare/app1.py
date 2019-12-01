# pySerial API : https://pyserial.readthedocs.io/en/latest/pyserial_api.html

import serial
import time
time.sleep(2)

ser = serial.Serial('COM15', 9600) # Serial(Comport,baudrate)
ser.flushInput()

# for i in range(10000):
#    data = ser.readline()
#    print(data.decode())


while True:
   try:
      data = ser.readline()
      # temp = ser.readline()
      print(data.decode())
      # print(temp.decode())
      # Transfer data to server (DB)
      print(type(data.decode()))
      import requests

      API_ENDPOINT = "http://127.0.0.1:5000/add"

      formData = {
         'deviceName': "Python",
         'deviceData': data.decode(),
         # 'devicetemp': temp.decode()
      }

      # response = requests.post(url = API_ENDPOINT, data = formData)
      # print(response.text)


   except:
      print("Keyboard Interrupt")
      break

