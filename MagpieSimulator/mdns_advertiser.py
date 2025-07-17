# mdns_advertiser.py
# Rewritten to use the 'zeroconf' library for mDNS advertisement
import asyncio
import socket
import traceback
from zeroconf import ServiceInfo
from zeroconf.asyncio import AsyncZeroconf


class MDNSAdvertiser:
    def __init__(self, name: str, port: int) -> None:
        self.name = name
        self.port = port
        self._task = None
        self._running = False
        self.zeroconf = None
        self.service_info = None

    def _get_local_ip(self):
        # Get the LAN IP address, not loopback
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Doesn't have to be reachable
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            print(f"Local IP address: {ip}")
        except Exception:
            ip = "127.0.0.1"
            print("Failed to get local IP address, using loopback")
        finally:
            s.close()
        # return "10.10.2.36"
        return ip

    def _build_service_info(self):
        # Build the ServiceInfo object for zeroconf
        desc = {}  # Empty TXT record
        hostname = socket.gethostname()
        local_ip = self._get_local_ip()
        service_type = "_http._tcp.local."
        service_name = f"{self.name}.{service_type}"
        self.service_info = ServiceInfo(
            type_=service_type,
            name=service_name,
            addresses=[socket.inet_aton(local_ip)],
            port=self.port,
            properties=desc,
            server=f"{hostname}.local.",
        )

    async def _advertise(self):
        print("Starting mDNS advertisement with zeroconf...")
        try:
            self._build_service_info()
            if self.service_info is not None:
                print("Registering mDNS service...")
                self.zeroconf = AsyncZeroconf()
                await self.zeroconf.async_register_service(self.service_info)
        except Exception as e:
            print(f"Error during mDNS advertisement: {e}")
            traceback.print_exc()
            return
        print("Running now...")
        self._running = True
        try:
            while self._running:
                print(f"Announcing mDNS service for {self.name} on port {self.port}")
                await asyncio.sleep(60)  # Announce every 60 seconds
        finally:
            print("Unregistering mDNS service...")
            if self.service_info is not None and self.zeroconf is not None:
                await self.zeroconf.async_unregister_service(self.service_info)
                await self.zeroconf.async_close()

    async def start(self) -> None:
        if self._task is None:
            print(f"Starting mDNS advertiser for {self.name} on port {self.port}")
            self._task = asyncio.create_task(self._advertise())

    async def stop(self) -> None:
        self._running = False
        if self._task:
            await self._task
            self._task = None
