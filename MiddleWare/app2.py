

      
      sensorValueToList = []
      #[' 34.20 %\r\n', ' 21.50 *C \r\n', '0.15 nm \r\n', '44 nV/√Hz\r\n', ' 27 voc\r\n', ' 0.13 vol\r\n', ' 1.00 ppm\r\n', ' 34.20 %\r\n', ' 21.50 *C \r\n', '0.15 nm \r\n']
      #['15 nV/√Hz\r\n', ' 24 voc\r\n', ' 0.12 vol\r\n', ' 1.00 ppm\r\n', ' 311 ug/m3\r\n', ' 312 ug/m3\r\n', ' 322 ug/m3\r\n', ' 33.80 %\r\n', ' 21.50 *C \r\n', '0.15 nm \r\n']
      for i in range(10):
          sensorValue = ser.readline().decode().split(':')[1]
          if len(sensorValue) !=10:
              break
          sensorValueToList.append(sensorValue)

      print(sensorValueToList)
        
      import requests 
      API_ENDPOINT = "http://0.0.0.0:5000/add"
      # json 파일로 저장하기 위한 데이터 저장! 
      # {} - json의 형식인 딕트형식으로 저장해줌

      formData = {
              'deviceName': "place1",
              'Humidity': sensorValueToList[0],
              'Temperature': sensorValueToList[1],
              'Fire ':sensorValueToList[2],
              'sound ': sensorValueToList[3],
              'sensorValue':sensorValueToList[4],
              'Vol ': sensorValueToList[5], 
              'ppm': sensorValueToList[6],
              'PM 1.0':sensorValueToList[7],
              'PM 2.5':sensorValueToList[8],
              'PM 10':sensorValueToList[9]
          } 
      # print(formData)

      # response = requests.post(url = API_ENDPOINT, json = formData)
      # print(response.text)

      del sensorValueToList[:]

  except KeyboardInterrupt:
      import requests 
      print('아두이노 시리얼 통신을 중단합니다.\n')
      break
