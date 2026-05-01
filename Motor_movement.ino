#include <SoftwareSerial.h>
SoftwareSerial BT(10, 11); // RX, TX

#include <Servo.h>

const int ledpin = 8;

Servo motorX;
Servo motorY;

int angleX = 90;
int angleY = 90;

void setup(){
  Serial.begin(9600);
  BT.begin(9600);
  motorX.attach(5);
  motorY.attach(6);

  motorX.write(angleX);
  motorY.write(angleY);
  pinMode(ledpin, OUTPUT);
}

void loop(){
  if (BT.available()>0) {
    String command = BT.readStringUntil('\n');    
    command.trim();

    if (command == "XR"){
      angleX=constrain(angleX - 90, 0, 180);
      motorX.write(angleX);
      BT.println("Motor X -> RIGHT ("+ String(angleX) + "deg)");
      
    } else if (command == "XL"){
      angleX=constrain(angleX + 90, 0, 180);
      motorX.write(angleX);
      BT.println("Motor X -> LEFT = ("+ String(angleX) + "deg)");
      
    }else if (command == "YR"){
      angleY=constrain(angleY - 90, 0, 180);
      motorY.write(angleY);
      BT.println("Motor Y -> RIGHT ("+ String(angleY) + "deg)");
    
    } else if (command == "YL"){
      angleY=constrain(angleY + 90, 0, 180);
      motorY.write(angleY);
      BT.println("Motor Y -> LEFT = ("+ String(angleY) + "deg)");
    
    }else{
      BT.println("Unkown command: " + command);
    }
    digitalWrite(ledpin, HIGH);
    delay(300);
    digitalWrite(ledpin, LOW);
  }
}
