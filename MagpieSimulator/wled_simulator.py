# wled_simulator.py
import asyncio
from aiohttp import web
from typing import Any, Dict
from models import WLED_EFFECTS, WLEDState, SegmentState


class WLEDSimulator:
    def __init__(self, name: str, port: int) -> None:
        self.name = name
        self.port = port
        self.state = WLEDState(
            on=True,
            bri=128,
            name=self.name,
            seg=[
                SegmentState(id=0, col=[[255, 255, 255]], fx=None),
                SegmentState(id=1, col=[[255, 255, 255]], fx=None),
            ],
            fx=None,
        )
        self.app = web.Application()
        self.app.add_routes(
            [
                web.route("*", "/{tail:.*}", self.handle_generic),
                web.get("/", self.handle_wled_autodiscover),
                web.get("/win", self.handle_wled_autodiscover),
                web.get("/json", self.handle_json),
                web.post("/json/state", self.handle_state),
                web.get("/json/info", self.handle_info),
                web.get("/json/effects", self.handle_effects),
                web.get("/json/palettes", self.handle_palettes),
            ]
        )

    async def handle_generic(self, request: web.Request) -> web.Response:
        print(f"-> Processing generic request for {self.name}")
        return web.Response(text="Not found", status=404)

    async def handle_wled_autodiscover(self, request: web.Request) -> web.Response:
        print(f"-> Processing WLED autodiscover request for {self.name}")
        # Return a simple HTML page for WLED autodiscovery
        return web.Response(
            text="""<leds>
  <on>1</on>
  <bri>128</bri>
  <transition>7</transition>
  <ps>0</ps>
  <pl>0</pl>
  <cc>16711680</cc>
  <fx>0</fx>
  <sx>128</sx>
  <ix>128</ix>
  <pal>0</pal>
  <c1>16711680</c1>
  <c2>255</c2>
  <c3>65280</c3>
  <mainseg>
    <id>0</id>
    <start>0</start>
    <stop>149</stop>
    <grp>1</grp>
    <spc>0</spc>
    <on>1</on>
    <bri>128</bri>
    <c1>16711680</c1>
    <c2>255</c2>
    <c3>65280</c3>
    <fx>0</fx>
    <sx>128</sx>
    <ix>128</ix>
    <pal>0</pal>
  </mainseg>
</leds>""",
            content_type="text/xml",
        )

    async def handle_json(self, request: web.Request) -> web.Response:
        # Return current state, including segments and effect
        # print(f"-> Processing JSON request for {self.name}")
        state_dict: Dict[str, Any] = {
            "on": self.state.on,
            "bri": self.state.bri,
            "name": self.state.name,
            "seg": [
                {"id": seg.id, "col": seg.col, "fx": seg.fx} for seg in self.state.seg
            ],
        }
        if self.state.fx is not None:
            state_dict["fx"] = self.state.fx
        return web.json_response(state_dict)

    async def handle_state(self, request: web.Request) -> web.Response:
        data = await request.json()
        print(f"Received POST for {self.name} state: {data}")
        # Handle on/off and brightness
        if "on" in data:
            self.state.on = data["on"]
        if "bri" in data:
            self.state.bri = data["bri"]
        # Handle effect
        if "fx" in data:
            self.state.fx = data["fx"]
        else:
            self.state.fx = None
        # Handle segments/colors
        if "seg" in data:
            for seg_update in data["seg"]:
                seg_id = seg_update.get("id", 0)
                color = seg_update.get("col")
                fx = seg_update.get("fx")
                for seg in self.state.seg:
                    if seg.id == seg_id:
                        seg.fx = fx
                        seg.col = [color] if color else [[0, 0, 0]]
                        break

        return web.json_response({"success": True})

    async def handle_info(self, request: web.Request) -> web.Response:
        # Return JSON with 2 segments, each with 10 RGBW LEDs
        mock_response = {
            "ver": "0.15.0",
            "vid": 2412100,
            "cn": "Kōsen",
            "release": "ESP32",
            "leds": {
                "count": 30,
                "pwr": 470,
                "fps": 2,
                "maxpwr": 850,
                "maxseg": 32,
                "bootps": 0,
                "seglc": [1],
                "lc": 1,
                "rgbw": False,
                "wv": 0,
                "cct": 0,
            },
            "str": False,
            "name": "WLED",
            "udpport": 21324,
            "simplifiedui": False,
            "live": False,
            "liveseg": -1,
            "lm": "",
            "lip": "",
            "ws": 1,
            "fxcount": 187,
            "palcount": 71,
            "cpalcount": 0,
            "maps": [{"id": 0}],
            "wifi": {
                "bssid": "78:45:58:84:62:88",
                "rssi": -62,
                "signal": 76,
                "channel": 11,
                "ap": False,
            },
            "fs": {"u": 8, "t": 983, "pmt": 0},
            "ndc": 0,
            "arch": "esp32",
            "core": "v3.3.6-16-gcc5440f6a2",
            "clock": 240,
            "flash": 4,
            "lwip": 0,
            "freeheap": 177240,
            "uptime": 300,
            "time": "1970-1-1, 00:05:00",
            "u": {
                "AudioReactive": {
                    '<button class="btn btn-xs" onclick="requestJson({AudioReactive:{enabled:true}});"><i class="icons off">&#xe08f;</i></button>': ""
                }
            },
            "opt": 79,
            "brand": "WLED",
            "product": "FOSS",
            "mac": "30aea49ccb3c",
            "ip": "10.10.10.255",
        }
        return web.json_response(mock_response)

    async def handle_effects(self, request: web.Request) -> web.Response:
        # Typical WLED effects list
        return web.json_response(WLED_EFFECTS)

    async def handle_palettes(self, request: web.Request) -> web.Response:
        # Typical WLED palettes list
        palettes = [
            "Default",
            "* Random Cycle",
            "* Color 1",
            "* Colors 1&2",
            "* Color Gradient",
            "* Colors Only",
            "Party",
            "Cloud",
            "Lava",
            "Ocean",
            "Forest",
            "Rainbow",
            "Rainbow Bands",
            "Sunset",
            "Rivendell",
            "Breeze",
            "Red & Blue",
            "Yellowout",
            "Analogous",
            "Splash",
            "Pastel",
            "Sunset 2",
            "Beach",
            "Vintage",
            "Departure",
            "Landscape",
            "Beech",
            "Sherbet",
            "Hult",
            "Hult 64",
            "Drywet",
            "Jul",
            "Grintage",
            "Rewhi",
            "Tertiary",
            "Fire",
            "Icefire",
            "Cyane",
            "Light Pink",
            "Autumn",
            "Magenta",
            "Magred",
            "Yelmag",
            "Yelblu",
            "Orange & Teal",
            "Tiamat",
            "April Night",
            "Orangery",
            "C9",
            "Sakura",
            "Aurora",
            "Atlantica",
            "C9 2",
            "C9 New",
            "Temperature",
            "Aurora 2",
            "Retro Clown",
            "Candy",
            "Toxy Reaf",
            "Fairy Reaf",
            "Semi Blue",
            "Pink Candy",
            "Red Reaf",
            "Aqua Flash",
            "Yelblu Hot",
            "Lite Light",
            "Red Flash",
            "Blink Red",
            "Red Shift",
            "Red Tide",
            "Candy2",
        ]
        return web.json_response(palettes)

    async def run(self) -> None:
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", self.port)
        await site.start()
        print(f"WLED Simulator '{self.name}' running on port {self.port}")
        while True:
            await asyncio.sleep(3600)  # Keep running
