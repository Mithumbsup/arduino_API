#include "Adafruit_Sensor.h"
#include <SoftwareSerial.h>        //RX, TX 통신 라이브러리 추가
#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT22 
DHT dht(DHTPIN, DHTTYPE);

SoftwareSerial Serial1(4,5);         //TX ,RX 핀을 4, 5번 핀으로 지정

long pmcf10=0;

long pmcf25=0;

long pmcf100=0;

long pmat10=0;

long pmat25=0;

long pmat100=0;



char buf[50];
void setup() {

  Serial.begin(9600);   // 시리얼 통신을 시작, 통신 속도는 9600
  dht.begin();
  Serial1.begin(9600);        //RX, TX 통신 시작
}


void loop() {
  float Vol, ppm;
  int sensorValue;
  float a1 = analogRead(A0);   
  float a2 = analogRead(A3);                             
  int b = analogRead(A1);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  sensorValue=analogRead(A2);
  Vol=sensorValue*4.95/1023;
  ppm = map(Vol, 0, 4.95, 1, 50); // Concentration Range: 1~50 ppm 
  int count = 0;
  unsigned char c;
  unsigned char high;

  
  
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  Serial.print(",");
  Serial.print("Humidity: ");        //습도
  Serial.print(h);
  Serial.print(" % ");
  
  Serial.print(",");
  Serial.print("Temperature: ");     //온도
  Serial.print(t);
  Serial.print(" *C ");

  Serial.print(",");
  Serial.print("Flame1:");              //Flame
  Serial.print((1/a1)*100);  
  Serial.print(" nm ");             

  Serial.print(",");
  Serial.print("Flame2:");              //Flame
  Serial.print((1/a2)*100);  
  Serial.print(" nm ");                                 
                                                                          

  Serial.print(",");
  Serial.print("Sound:");            //Sound
  Serial.print(b);
  Serial.println(" nV/√Hz "); 

  Serial.print(",");
  Serial.print("Sensor Value: ");    //VOCs
  Serial.print(sensorValue);
  Serial.print(" voc ");

  Serial.print(",");
  Serial.print("Vol: ");
  Serial.print(Vol);
  Serial.print(" vol ");

  Serial.print(",");
  Serial.print("ppm: ");
  Serial.print(ppm);
  Serial.print(" ppm ");
    
 while (Serial1.available()) {               //FineDust

    c = Serial1.read();           //RX, TX 통신을 통한 값을 c로 저장

    if((count==0 && c!=0x42) || (count==1 && c!=0x4d)){

      Serial.println("check failed");

      break;

    }
    else if(count == 4 || count == 6 || count == 8 || count == 10 || count == 12 || count == 14) {

      high = c;

    }

    else if(count == 5){             //pm1.0의 수치값 계산

      pmcf10 = 256*high + c;
      Serial.print(",");
      Serial.print("PM 1.0: ");
      Serial.print(pmcf10);
      Serial.print(" ug/m3 ");

    }

    else if(count == 7){           //pm2.5의 수치값 계산

      pmcf25 = 256*high + c;
      Serial.print(",");
      Serial.print("PM 2.5: ");
      Serial.print(pmcf25);
      Serial.print(" ug/m3 ");

    }

    else if(count == 9){           //pm 10의 수치값 계산

      pmcf100 = 256*high + c;
      Serial.print(",");
      Serial.print("PM 10: ");
      Serial.print(pmcf100);
      Serial.print(" ug/m3 ");
      Serial.print(",");

    }

    count++;
 }

  while(Serial1.available()) Serial1.read();
  
  delay(1000);     
}