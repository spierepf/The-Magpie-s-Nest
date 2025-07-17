# state_updater.py
import asyncio
import aiohttp
from config import BASE_PORT, WLED_NAMES
from models import WLEDState, SegmentState
from typing import List, Optional


class WLEDStateManager:
    def __init__(self) -> None:
        self.states: List[Optional[WLEDState]] = [None] * len(WLED_NAMES)
        self.names: List[str] = list(WLED_NAMES)

    async def poll_states(self, interval: float = 1.0) -> None:
        while True:
            await self._update_all_states()
            await asyncio.sleep(interval)

    async def _update_all_states(self) -> None:
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_state(session, i) for i in range(len(self.names))]
            await asyncio.gather(*tasks)

    async def _fetch_state(self, session: aiohttp.ClientSession, idx: int) -> None:
        port = BASE_PORT + idx
        url = f"http://127.0.0.1:{port}/json"
        try:
            async with session.get(url, timeout=0.5) as resp:
                data = await resp.json()
                self.states[idx] = WLEDState(
                    on=data.get("on", False),
                    bri=data.get("bri", 0),
                    name=data.get("name", self.names[idx]),
                    seg=[
                        SegmentState(id=s.get("id", 0), col=s.get("col", [[0, 0, 0]]))
                        for s in data.get("seg", [])
                    ],
                    fx=data.get("fx"),
                )
        except Exception:
            self.states[idx] = None


class StateUpdater:
    def __init__(self, state_manager: WLEDStateManager) -> None:
        self.state_manager = state_manager

    def update(self) -> None:
        # ...existing code...
        pass
