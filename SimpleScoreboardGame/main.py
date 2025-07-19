"""
SimpleScoreboardGame main logic
- Two modes: ScoreBoard and ReactionTime
- Uses 2 player buttons (with NeoPixels), 1 main NeoPixel, 1 start button, 1 mode toggle, and 0.96" I2C OLED
- MicroPython, ESP32-C3
"""

import time
from machine import Pin, I2C
import config
from wled_controller import WLEDController

try:
    import neopixel
except ImportError:
    neopixel = None  # For code completion only

try:
    import ssd1306
except ImportError:
    ssd1306 = None  # For code completion only

# Hardware setup
player1_btn = Pin(config.PLAYER1_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
player2_btn = Pin(config.PLAYER2_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
start_btn = Pin(config.START_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
mode_switch = Pin(config.MODE_SWITCH_PIN, Pin.IN, Pin.PULL_UP)

np1 = neopixel.NeoPixel(Pin(config.PLAYER1_NEOPIXEL_PIN), 1)
np2 = neopixel.NeoPixel(Pin(config.PLAYER2_NEOPIXEL_PIN), 1)
np_main = neopixel.NeoPixel(Pin(config.MAIN_NEOPIXEL_PIN), 1)

i2c = I2C(0, scl=Pin(config.I2C_SCL_PIN), sda=Pin(config.I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Game state
game_mode = 0  # 0 = ScoreBoard, 1 = ReactionTime
scores = [0, 0]

# Add a busy color for WLED updates
BUSY_COLOR = (255, 0, 255)  # Magenta

# Initialize WLED controller
wled = WLEDController(
    wled_names=[
        "WLED-1-1",
        "WLED-1-2",
        "WLED-1-3",
        "WLED-2-1",
        "WLED-2-2",
        "WLED-2-3",
        "WLED-2-4",
        "WLED-2-5",
        "WLED-3-1",
        "WLED-3-2",
        "WLED-4-1",
        "WLED-4-2",
        "WLED-4-3",
        "WLED-4-4",
        "WLED-4-5",
        "WLED-5-1",
        "WLED-5-2",
        "WLED-5-3",
    ],
    player1_color=config.PLAYER1_COLOR,
    player2_color=config.PLAYER2_COLOR,
)


# Helper functions
def show_scores():
    oled.fill(0)
    oled.text("P1: {}".format(scores[0]), 0, 0)
    oled.text("P2: {}".format(scores[1]), 64, 0)
    oled.text("Mode: {}".format("Score" if game_mode == 0 else "React"), 0, 16)
    oled.show()


def set_neopixels():
    np1[0] = config.PLAYER1_COLOR
    np2[0] = config.PLAYER2_COLOR
    np_main[0] = config.IDLE_COLOR
    np1.write()
    np2.write()
    np_main.write()


def wait_for_start():
    oled.fill(0)
    oled.text("Press Start", 0, 32)
    oled.show()
    while start_btn.value():
        time.sleep_ms(50)


def scoreboard_mode():
    set_neopixels()
    show_scores()
    last_update = time.time()
    wled.set_busy(True)
    np_main[0] = BUSY_COLOR
    np_main.write()
    wled.set_score(scores[0], scores[1])
    wled.set_busy(False)
    np_main[0] = config.IDLE_COLOR
    np_main.write()
    while max(scores) < config.MAX_SCORE:
        updated = False
        if not player1_btn.value():
            scores[0] = min(config.MAX_SCORE, scores[0] + 1)
            show_scores()
            updated = True
            time.sleep(0.3)
        if not player2_btn.value():
            scores[1] = min(config.MAX_SCORE, scores[1] + 1)
            show_scores()
            updated = True
            time.sleep(0.3)
        if updated:
            last_update = time.time()
            wled.set_busy(True)
            np_main[0] = BUSY_COLOR
            np_main.write()
            wled.set_score(scores[0], scores[1])
            wled.set_busy(False)
            np_main[0] = config.IDLE_COLOR
            np_main.write()
        if time.time() - last_update > 10:
            wled.set_busy(True)
            np_main[0] = BUSY_COLOR
            np_main.write()
            wled.set_pride()
            wled.set_busy(False)
            np_main[0] = config.IDLE_COLOR
            np_main.write()
            last_update = time.time()  # Prevent repeated pride calls
        if not start_btn.value():
            return
    # Win state
    wled.set_busy(True)
    np_main[0] = BUSY_COLOR
    np_main.write()
    winner = 1 if scores[0] == config.MAX_SCORE else 2
    wled.blink_win(winner)
    wled.set_busy(False)
    np_main[0] = config.IDLE_COLOR
    np_main.write()
    oled.fill(0)
    oled.text("P{} Wins!".format(winner), 0, 32)
    oled.show()
    time.sleep(2)


def reaction_time_mode():
    set_neopixels()
    show_scores()
    last_update = time.time()
    wled.set_busy(True)
    np_main[0] = BUSY_COLOR
    np_main.write()
    wled.set_score(scores[0], scores[1])
    wled.set_busy(False)
    np_main[0] = config.IDLE_COLOR
    np_main.write()
    while max(scores) < config.MAX_SCORE:
        # Blink main NeoPixel 3 times
        for _ in range(3):
            np_main[0] = (255, 255, 255)
            np_main.write()
            time.sleep(0.2)
            np_main[0] = (0, 0, 0)
            np_main.write()
            time.sleep(0.2)
        # Wait random time
        delay = (
            config.REACTION_MIN_DELAY
            + (time.ticks_ms() % (config.REACTION_MAX_DELAY * 1000)) / 1000
        )
        time.sleep(delay)
        # Light main NeoPixel
        np_main[0] = (0, 255, 0)
        np_main.write()
        # Wait for first button press
        updated = False
        while True:
            if not player1_btn.value():
                scores[0] = min(config.MAX_SCORE, scores[0] + 1)
                updated = True
                break
            if not player2_btn.value():
                scores[1] = min(config.MAX_SCORE, scores[1] + 1)
                updated = True
                break
        show_scores()
        if updated:
            last_update = time.time()
            wled.set_busy(True)
            np_main[0] = BUSY_COLOR
            np_main.write()
            wled.set_score(scores[0], scores[1])
            wled.set_busy(False)
            np_main[0] = config.IDLE_COLOR
            np_main.write()
        if time.time() - last_update > 10:
            wled.set_busy(True)
            np_main[0] = BUSY_COLOR
            np_main.write()
            wled.set_pride()
            wled.set_busy(False)
            np_main[0] = config.IDLE_COLOR
            np_main.write()
            last_update = time.time()
        time.sleep(0.5)
        if not start_btn.value():
            return
    # Win state
    wled.set_busy(True)
    np_main[0] = BUSY_COLOR
    np_main.write()
    winner = 1 if scores[0] == config.MAX_SCORE else 2
    wled.blink_win(winner)
    wled.set_busy(False)
    np_main[0] = config.IDLE_COLOR
    np_main.write()
    oled.fill(0)
    oled.text("P{} Wins!".format(winner), 0, 32)
    oled.show()
    time.sleep(2)


def main():
    global game_mode, scores
    while True:
        scores = [0, 0]
        game_mode = 0 if mode_switch.value() else 1
        wait_for_start()
        if game_mode == 0:
            scoreboard_mode()
        else:
            reaction_time_mode()
        time.sleep(1)


if __name__ == "__main__":
    main()
