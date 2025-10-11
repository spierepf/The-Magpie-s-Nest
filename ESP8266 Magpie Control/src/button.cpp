#include <Arduino.h>
#include <WiFiUdp.h>

#include <button.hpp>

#define BUTTON_PIN 2

namespace button {
  WiFiUDP Udp;

  unsigned long next_press_threshold = 0;

  uint8_t message[24] = {
    0,          // Packet Purpose Byte
    1,          // Packet Reason - Direct Change via UI or API
    128,        // Master Brightness
    0, 0, 0,    // Primary Colour
    0,          // Nightlight running?
    0,          // Nightlight Time
    63,         // Effect Index - Pride 2015
    128,        // Effect Speed
    0,          // Primary White Value
    5,          // Version Byte - Palettes supported
    0, 0, 0, 0, // Secondary Colour (incl. white)
    128,        // Effect Intensity
    0,          // Transition Duration Upper
    0,          // Transition Duration Lower
    0,          // FastLED palette
  };

  void setup() {
    pinMode(BUTTON_PIN, INPUT_PULLUP);
  }

  void loop() {
    if(digitalRead(BUTTON_PIN) == 0) {
      unsigned long now = millis();
      if(now > next_press_threshold) {
        Serial.println("Pressed!");
        const IPAddress broadcastIP(255, 255, 255, 255);
        Udp.beginPacket(broadcastIP, 21324);
        Udp.write(message, sizeof(message));
        Udp.endPacket();
      }
      next_press_threshold = now + 10000;
    }
  }
}