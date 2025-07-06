# state_updater.py
import asyncio
import aiohttp
from config import BASE_PORT, WLED_NAMES


class WLEDStateManager:
    def __init__(self):
        self.states = [False] * len(WLED_NAMES)
        self.names = list(WLED_NAMES)

    async def poll_states(self, interval=1.0):
        while True:
            await self._update_all_states()
            await asyncio.sleep(interval)

    async def _update_all_states(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_state(session, i) for i in range(len(self.names))]
            await asyncio.gather(*tasks)

    async def _fetch_state(self, session, idx):
        port = BASE_PORT + idx
        url = f"http://127.0.0.1:{port}/json"
        try:
            async with session.get(url, timeout=0.5) as resp:
                data = await resp.json()
                self.states[idx] = data.get("on", False)
        except Exception:
            self.states[idx] = False
