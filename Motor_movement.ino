#include <Servo.h>
const int ledpin = 8;
Servo motorX;
Servo motorY;
int angleX = 90;
int angleY = 90;
const int STEP_DELAY = 15; // ms per degree — increase to slow down

void slowMove(Servo &servo, int &currentAngle, int targetAngle) {
    int step = (targetAngle > currentAngle) ? 1 : -1;
    while (currentAngle != targetAngle) {
        currentAngle += step;
        servo.write(currentAngle);
        delay(STEP_DELAY);
    }
}

void setup() {
    Serial.begin(9600);
    motorX.attach(5);
    motorY.attach(6);
    motorX.write(angleX);
    motorY.write(angleY);
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();

        if (command == "YR") {
            int target = constrain(angleY - 40, 0, 180);
            slowMove(motorY, angleY, target);
            Serial.println("Motor Y -> RIGHT (" + String(angleY) + "deg)");
        } else if (command == "YL") {
            int target = constrain(angleY + 40, 0, 180);
            slowMove(motorY, angleY, target);
            Serial.println("Motor Y -> LEFT = (" + String(angleY) + "deg)");
        } else if (command == "M") {
            slowMove(motorX, angleX, 90);
            Serial.println("Motor X -> MIDDLE = (" + String(angleX) + "deg)");
        } else if (command == "PLAS") {
            slowMove(motorX, angleX, 180);
            Serial.println("Motor X -> CARDBOARD = (" + String(angleX) + "deg)");
        } else if (command == "CARD") {
            slowMove(motorX, angleX, 130);
            Serial.println("Motor X -> PLASTIC = (" + String(angleX) + "deg)");
        } else if (command == "WAST") {
            slowMove(motorX, angleX, 60);
            Serial.println("Motor X -> WASTE = (" + String(angleX) + "deg)");
        } else if (command == "CAN") {
            slowMove(motorX, angleX, 0);
            Serial.println("Motor X -> CANS = (" + String(angleX) + "deg)");
        } else {
            Serial.println("Unknown command: " + command);
        }
    }
}
