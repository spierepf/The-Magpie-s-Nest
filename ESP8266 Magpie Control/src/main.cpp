#include <Arduino.h>
#include <WiFiUdp.h>

#include <wifi.hpp>
#include <ota.hpp>
#include <button.hpp>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("\n\nESP8266 Magpie Remote");

  wifi::setup();
  ota::setup();
  button::setup();
}

void loop() {
  // put your main code here, to run repeatedly:
  wifi::loop();
  ota::loop();
  button::loop();
}
