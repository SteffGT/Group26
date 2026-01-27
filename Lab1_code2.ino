/***************************************************************************
* Sketch Name: Lab1_code2
*
* Original Version: 14/11/2020 (by Hakan KAYAN)
* Updated Version: 24/12/2024 (by Charith PERERA)
*
* Note: This code demonstrates how to control a servo based on a button input.
*       In an IoT context, the button press could be replaced or augmented by 
*       sensor data (e.g., PIR sensor, light sensor) to automate actions.
***************************************************************************/

// 1. Include the Servo library, which contains functions to control servo motors.
#include <Servo.h>  
#define PIR_MOTION_SENSOR 2  
// 2. Define the digital pin to which the button is connected.
//    In many IoT applications, a push button can manually trigger an event 
//    (e.g., turning on lights, opening doors, etc.).
const int buttonPin = 4;
const int ledPin = 3;    // the number of the LED pin (D3)
const int buzzerPin = 6;

// 3. Declare a variable to store the button's state (HIGH or LOW).
int buttonState;
int ledState = HIGH;       // the current state of the LED (HIGH or LOW)
int MotionState;
int buzzerState = LOW;

// 4. Create a Servo object named 'myservo'. We will use the methods inside
//    this object to control the position (angle) of the servo motor.
Servo myservo;

// 5. This variable will store the servo position (in degrees).
//    Even though we are not using 'pos' directly in the loop here, it is 
//    commonly used for incremental or sweeping movements.
int pos = 0;

void setup() {
  // 6. Attach the servo object to digital pin 5. The servo library 
  //    will internally handle the timing to position the servo.
  myservo.attach(5);

  // 7. It is best practice to specify the pin mode for the button.
  //    If your button is wired so that pressing it reads HIGH, you should 
  //    set the pin to INPUT or INPUT_PULLDOWN (depending on your board).
  //    If you have a pull-up resistor, use INPUT_PULLUP. For simplicity, 
  //    we assume you have an external pull-down resistor.
  pinMode(buttonPin, INPUT);
  pinMode(PIR_MOTION_SENSOR, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  // 5. Initialize the LED to the default state defined in ledState.
  digitalWrite(ledPin, ledState);

  // 6. Begin serial communication at 9600 bits per second.
  //    This allows you to print sensor values or states to the Serial Monitor.
  Serial.begin(9600);
}

void loop() {
  // 8. Read the current state of the button (HIGH or LOW).
  buttonState = digitalRead(buttonPin);
  MotionState = digitalRead(PIR_MOTION_SENSOR);
 

  int light = analogRead(A3);

  light = map(light, 0, 800, 0, 10);
  // 9. If the button is pressed (i.e., reads HIGH), rotate the servo to 180°.
  //    This simulates an action triggered by the button in an IoT scenario, 
  //    such as opening a lock or pointing a sensor in a certain direction.
  for (int i = 0; i <= 255; i++) {
      analogWrite(ledPin, i);  // PWM value for LED brightness
      delay(10);               // short delay for smooth fading
    }

    // 10b. Check the light level. If the mapped value is <= 5, it is relatively dark.
    if (light <= 5) {
      Serial.println("Dark");
    } else {
      Serial.println("Light");
    }
  
  if (MotionState == HIGH || light <= 5) {
    myservo.write(180);    // Move servo to 180 degrees
    Serial.println("movement");
    delay(3000);             // Short delay to give servo time to reach position
    myservo.write(0);
    digitalWrite(buzzerPin, HIGH);
    delay(100);
    digitalWrite(buzzerPin, LOW);
  } 
  // 10. Otherwise (button not pressed), rotate the servo to 0°.
  else {
      Serial.println("Watching");
      delay(100);
    }
}
