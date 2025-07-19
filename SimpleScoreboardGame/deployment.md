# SimpleScoreboardGame Deployment Instructions

## 1. Prepare Your ESP32-C3

- Install the latest MicroPython firmware for ESP32-C3:
  - Download from https://micropython.org/download/esp32c3/
  - Use esptool to flash:
    ```
    esptool.py --chip esp32c3 erase_flash
    esptool.py --chip esp32c3 --baud 460800 write_flash -z 0x0 firmware.bin
    ```

## 2. Install Required Libraries

- Download or copy the following MicroPython libraries to your ESP32-C3:
  - `neopixel.py` (usually built-in)
  - `ssd1306.py` (get from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py)

## 3. Upload Game Files

- Copy these files to your ESP32-C3 (using ampy, Thonny, or rshell):
  - `main.py`
  - `config.py`

## 4. Wire the Hardware

- Follow the pinout in `wiring.md` for all buttons, NeoPixels, OLED, and switches.
- Double-check all GND and VCC connections.

## 5. Run the Game

- Reset or power-cycle the ESP32-C3.
- The game should start automatically.
- Use the mode switch to select game mode, then press the start button to begin.

## 6. Troubleshooting

- If the display or NeoPixels do not light up, check wiring and power.
- If buttons do not register, check for correct pull-up configuration.
- Use the REPL (serial console) for debugging output if needed.

---

For more help, see the MicroPython documentation: https://docs.micropython.org/en/latest/esp32/quickref.html
