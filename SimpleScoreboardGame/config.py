# SimpleScoreboardGame - MicroPython for ESP32-C3
# Hardware Pin Assignments
PLAYER1_BUTTON_PIN = 2  # GPIO2
PLAYER2_BUTTON_PIN = 3  # GPIO3
PLAYER1_NEOPIXEL_PIN = 4  # GPIO4
PLAYER2_NEOPIXEL_PIN = 5  # GPIO5
MAIN_NEOPIXEL_PIN = 6  # GPIO6
START_BUTTON_PIN = 7  # GPIO7
MODE_SWITCH_PIN = 10  # GPIO10 (toggle switch)
I2C_SCL_PIN = 9  # GPIO9 (OLED SCL)
I2C_SDA_PIN = 8  # GPIO8 (OLED SDA)

# Game Settings
MAX_SCORE = 10
REACTION_MIN_DELAY = 1  # seconds
REACTION_MAX_DELAY = 15  # seconds

# Player Colors
PLAYER1_COLOR = (255, 200, 0)  # Yellow
PLAYER2_COLOR = (0, 100, 255)  # Blue
WIN_COLOR = (0, 255, 0)  # Green
LOSE_COLOR = (255, 0, 0)  # Red
IDLE_COLOR = (20, 20, 20)  # Dim white

# Add more config as needed
