# wled_simulator.py
import asyncio
from aiohttp import web
from typing import Any, Dict
from models import WLEDState, SegmentState


class WLEDSimulator:
    def __init__(self, name: str, port: int) -> None:
        self.name = name
        self.port = port
        self.state = WLEDState(
            on=True,
            bri=128,
            name=self.name,
            seg=[
                SegmentState(id=0, col=[[255, 255, 255]]),
                SegmentState(id=1, col=[[255, 255, 255]]),
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
            "seg": [{"id": seg.id, "col": seg.col} for seg in self.state.seg],
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
                if color:
                    for seg in self.state.seg:
                        if seg.id == seg_id:
                            seg.col = color
        return web.json_response({"success": True})

    async def run(self) -> None:
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", self.port)
        await site.start()
        print(f"WLED Simulator '{self.name}' running on port {self.port}")
        while True:
            await asyncio.sleep(3600)  # Keep running
