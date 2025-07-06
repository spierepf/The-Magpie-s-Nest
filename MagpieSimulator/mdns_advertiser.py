# mdns_advertiser.py
import asyncio
from zeroconf.asyncio import AsyncZeroconf, AsyncServiceInfo


class MDNSAdvertiser:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.zeroconf = None
        self.service_info = None

    async def start(self):
        self.zeroconf = AsyncZeroconf()
        self.service_info = AsyncServiceInfo(
            type_="_http._tcp.local.",
            name=f"{self.name}._http._tcp.local.",
            port=self.port,
            properties={},
            addresses=None,  # Use default local address
        )
        await self.zeroconf.async_register_service(self.service_info)

    async def stop(self):
        if self.zeroconf and self.service_info:
            await self.zeroconf.async_unregister_service(self.service_info)
            await self.zeroconf.async_close()
