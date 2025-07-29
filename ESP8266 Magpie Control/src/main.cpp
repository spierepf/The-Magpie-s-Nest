#include <Arduino.h>
#include <WiFiUdp.h>

#include <secrets.hpp>
#include <wifi.hpp>
#include <ota.hpp>

WiFiUDP Udp;

#define BUTTON_PIN 2

unsigned long next_press_threshold = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("\n\nESP8266 Magpie Remote");
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  wifi::setup();
  ota::setup();
}

uint8_t message[24] = {
  0,          // Packet Purpose Byte
  1,          // Packet Reason - Direct Change via UI or API
  128,        // Master Brightness
  0, 0, 0,    // Primary Colour
  0,          // Nightlight running?
  0,          // Nightlight Time
  60,         // Effect Index - Pride 2015
  128,        // Effect Speed
  0,          // Primary White Value
  5,          // Version Byte - Palettes supported
  0, 0, 0, 0, // Secondary Colour (incl. white)
  128,        // Effect Intensity
  0,          // Transition Duration Upper
  0,          // Transition Duration Lower
  0,          // FastLED palette
};

void do_the_needful() {
  const IPAddress broadcastIP(255, 255, 255, 255);
  Udp.beginPacket(broadcastIP, 21324);
  Udp.write(message, sizeof(message));
  Udp.endPacket();
}

void loop() {
  // put your main code here, to run repeatedly:
  wifi::loop();
  ota::loop();

  if(digitalRead(BUTTON_PIN) == 0) {
    unsigned long now = millis();
    if(now > next_press_threshold) {
      Serial.println("Pressed!");
      do_the_needful();
    }
    next_press_threshold = now + 10000;
  }
}
