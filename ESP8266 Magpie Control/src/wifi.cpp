#include <wifi.hpp>
#include <secrets.hpp>

#include <ESP8266WiFi.h>

namespace wifi
{
  void setup()
  {
    WiFi.begin(WIFI_SSID, WIFI_PSK);

    Serial.print("Connecting");
    while (WiFi.status() != WL_CONNECTED)
    {
      delay(500);
      Serial.print(".");
    }
    Serial.println();

    Serial.print("Connected, IP address: ");
    Serial.println(WiFi.localIP());
  }

  void loop()
  {
    while (WiFi.status() != WL_CONNECTED)
      ;
  }
}