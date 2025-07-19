# SimpleScoreboardGame Wiring Diagram

## ESP32-C3 Pinout (example, check your board for exact pin numbers)

- GPIO2 -> Player 1 Button (one side to GND, other to GPIO2)
- GPIO3 -> Player 2 Button (one side to GND, other to GPIO3)
- GPIO4 -> Player 1 NeoPixel (DIN)
- GPIO5 -> Player 2 NeoPixel (DIN)
- GPIO6 -> Main NeoPixel (DIN)
- GPIO7 -> Start Button (one side to GND, other to GPIO7)
- GPIO10 -> Mode Switch (toggle, one side to GND, other to GPIO10)
- GPIO8 -> OLED SDA
- GPIO9 -> OLED SCL
- 3V3 -> All NeoPixels VCC, OLED VCC, button/switch pullups if needed
- GND -> All NeoPixels GND, OLED GND, all button/switch GND sides

## Notes

- Use a 330Ω resistor in series with each NeoPixel DIN for signal integrity.
- Place a 1000uF capacitor across NeoPixel VCC and GND if using more than a few pixels.
- Use pull-up resistors (10kΩ) on button/switch pins if not using internal pull-ups.
- OLED is assumed to be 0.96" I2C (SDA/SCL, 3.3V).

## ASCII Diagram (simplified)

[ESP32-C3]
|-- GPIO2 --[Button1]-- GND
|-- GPIO3 --[Button2]-- GND
|-- GPIO4 --[NeoPixel1 DIN]
|-- GPIO5 --[NeoPixel2 DIN]
|-- GPIO6 --[Main NeoPixel DIN]
|-- GPIO7 --[Start Button]-- GND
|-- GPIO10 --[Mode Switch]-- GND
|-- GPIO8 --[OLED SDA]
|-- GPIO9 --[OLED SCL]
|-- 3V3 --[All VCCs]
|-- GND --[All GNDs]

# For a graphical diagram, use Fritzing or Wokwi with the above pinout.
