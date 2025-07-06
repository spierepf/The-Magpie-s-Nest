# main.py
import asyncio
import threading
from config import BASE_PORT, WLED_NAMES
from wled_simulator import WLEDSimulator
from mdns_advertiser import MDNSAdvertiser
from state_updater import WLEDStateManager
from visualizer import run_visualizer


# Indices for front and back arches (adjust as needed)
FRONT_INDICES = list(range(len(WLED_NAMES)))
BACK_INDICES = list(range(len(WLED_NAMES)))


async def start_simulator(name, port):
    wled = WLEDSimulator(name, port)
    mdns = MDNSAdvertiser(name, port)
    await mdns.start()
    await wled.run()


async def start_all_simulators():
    tasks = []
    for i, name in enumerate(WLED_NAMES):
        port = BASE_PORT + i
        tasks.append(asyncio.create_task(start_simulator(name, port)))
    await asyncio.gather(*tasks)


async def main():
    state_manager = WLEDStateManager()
    # Start polling in the background
    asyncio.create_task(state_manager.poll_states())
    # Start simulators in the background
    asyncio.create_task(start_all_simulators())
    # Run the visualizer in a thread (since pygame is blocking)
    vis_thread = threading.Thread(
        target=run_visualizer, args=(state_manager, FRONT_INDICES, BACK_INDICES)
    )
    vis_thread.start()
    vis_thread.join()


if __name__ == "__main__":
    asyncio.run(main())
