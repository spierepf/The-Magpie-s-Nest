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
        self.app = web.Application()
        self.app.add_routes(
            [
                web.get("/json", self.handle_json),
            ]
        )

    async def handle_json(self, request):
        return web.json_response(self.state)

    async def run(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", self.port)
        await site.start()
        print(f"WLED Simulator '{self.name}' running on port {self.port}")
        while True:
            await asyncio.sleep(3600)  # Keep running
