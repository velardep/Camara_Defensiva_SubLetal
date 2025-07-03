#include <Arduino.h>
#include <ESP32Servo.h>

Servo servoX;
Servo servoY;

String input = "";
int pinX = 13;  // Servo horizontal
int pinY = 14;  // Servo vertical
int pinDisparo = 17; // ⚠️ Pin que controla el MOSFET

void setup() {
  Serial.begin(115200);

  pinMode(pinDisparo, OUTPUT);  // Configurar pin de disparo
  digitalWrite(pinDisparo, LOW); // Inicialmente apagado

  servoX.setPeriodHertz(50);
  servoY.setPeriodHertz(50);
  servoX.attach(pinX);
  servoY.attach(pinY);
  servoX.write(90);
  servoY.write(90);

  Serial.println("Servos centrados en 90°");
  Serial.println("Esperando coordenadas...");
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      input.trim();

      if (input.startsWith("X:") && input.indexOf("Y:") != -1) {
        int x = input.indexOf("X:");
        int y = input.indexOf("Y:");
        int angX = input.substring(x + 2, y).toInt();
        int angY = input.substring(y + 2).toInt();
        angX = constrain(angX, 0, 180);
        angY = constrain(angY, 0, 180);
        servoX.write(angX);
        servoY.write(angY);
        Serial.printf("Servo X: %d | Servo Y: %d\n", angX, angY);
      } 
      else if (input == "DISPARO") {
        digitalWrite(pinDisparo, HIGH);  // Encender motor
        Serial.println("DISPARO activado");
      } 
      else if (input == "OFF") {
        digitalWrite(pinDisparo, LOW);   // Apagar motor
        Serial.println("DISPARO desactivado");
      }

      input = "";
    } else {
      input += c;
    }
  }
}
