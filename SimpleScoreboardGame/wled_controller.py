# wled_controller.py
"""
Handles WLED network updates for SimpleScoreboardGame.
Uses HTTP JSON API to control WLED modules by mDNS hostname.
"""
import urequests as requests
import time
import config


class WLEDController:
    def __init__(self, wled_names, player1_color, player2_color):
        self.wled_names = wled_names
        self.player1_color = player1_color
        self.player2_color = player2_color
        self.busy = False

    def set_busy(self, busy=True):
        self.busy = busy
        # You can update the main status NeoPixel here if needed

    def set_pride(self, exclude=None):
        """Set all (or all except exclude) modules to pride preset (preset 1)."""
        if exclude is None:
            exclude = []
        for name in self.wled_names:
            if name in exclude:
                continue
            self._send_preset(name, 1)

    def set_score(self, p1_score, p2_score):
        """Set score display: left modules for P1, right for P2, rest pride."""
        # Define which modules are for each player
        p1_modules = [
            "WLED-1-1",
            "WLED-1-2",
            "WLED-1-3",
            "WLED-2-1",
            "WLED-2-2",
            "WLED-2-3",
            "WLED-2-4",
            "WLED-2-5",
            "WLED-3-1",
        ]
        p2_modules = [
            "WLED-5-3",
            "WLED-5-2",
            "WLED-5-1",
            "WLED-4-5",
            "WLED-4-4",
            "WLED-4-3",
            "WLED-4-2",
            "WLED-4-1",
            "WLED-3-2",
        ]
        # Light up score modules
        for i, name in enumerate(p1_modules):
            if i < p1_score:
                self._send_color(name, self.player1_color)
            else:
                self._send_preset(name, 1)
        for i, name in enumerate(p2_modules):
            if i < p2_score:
                self._send_color(name, self.player2_color)
            else:
                self._send_preset(name, 1)
        # Set all others to pride
        used = set(p1_modules[:p1_score] + p2_modules[:p2_score])
        self.set_pride(exclude=used)

    def blink_win(self, winner):
        """Blink all modules in winner's color (10 times, 0.5s on/off)."""
        color = self.player1_color if winner == 1 else self.player2_color
        for _ in range(10):
            for name in self.wled_names:
                self._send_color(name, color)
            time.sleep(0.5)
            for name in self.wled_names:
                self._send_preset(name, 1)
            time.sleep(0.5)

    def _send_color(self, name, color):
        url = f"http://{name}.local/json/state"
        payload = {"on": True, "bri": 255, "seg": [{"col": [list(color)]}]}
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"WLED {name} error: {e}")

    def _send_preset(self, name, preset):
        url = f"http://{name}.local/json/state"
        payload = {"on": True, "ps": preset}
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"WLED {name} error: {e}")
