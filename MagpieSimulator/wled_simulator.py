# wled_simulator.py
import asyncio
from aiohttp import web
import json


class WLEDSimulator:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.state = {
            "on": True,
            "bri": 128,
            "name": self.name,
        }
        self.effect = None  # Store current effect (e.g., pride)
        self.segments = [
            {"id": 0, "col": [[255, 255, 255]]},
            {"id": 1, "col": [[255, 255, 255]]},
        ]  # Simulate two segments
        self.app = web.Application()
        self.app.add_routes(
            [
                web.get("/json", self.handle_json),
                web.post("/json/state", self.handle_state),
            ]
        )

    async def handle_json(self, request):
        # Return current state, including segments and effect
        state = self.state.copy()
        state["seg"] = self.segments
        if self.effect is not None:
            state["fx"] = self.effect
        # print(f"Received GET for {self.name} state: {request}")
        return web.json_response(state)

    async def handle_state(self, request):
        data = await request.json()
        print(f"Received POST for {self.name} state: {data}")
        # Handle on/off and brightness
        if "on" in data:
            self.state["on"] = data["on"]
        if "bri" in data:
            self.state["bri"] = data["bri"]
        # Handle effect
        if "fx" in data:
            self.effect = data["fx"]
        else:
            self.effect = None
        # Handle segments/colors
        if "seg" in data:
            for seg in data["seg"]:
                seg_id = seg.get("id", 0)
                color = seg.get("col")
                if color:
                    # Update the simulated segment color
                    for s in self.segments:
                        if s["id"] == seg_id:
                            s["col"] = color
        return web.json_response({"success": True})

    async def run(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", self.port)
        await site.start()
        print(f"WLED Simulator '{self.name}' running on port {self.port}")
        while True:
            await asyncio.sleep(3600)  # Keep running
