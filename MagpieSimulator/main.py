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


def start_asyncio_tasks(state_manager):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(state_manager.poll_states())
    loop.create_task(start_all_simulators())
    loop.run_forever()


def main():
    state_manager = WLEDStateManager()
    # Start asyncio tasks in a background thread
    asyncio_thread = threading.Thread(
        target=start_asyncio_tasks, args=(state_manager,), daemon=True
    )
    asyncio_thread.start()
    # Run the visualizer in the main thread (pygame must run in main thread)
    run_visualizer(state_manager, FRONT_INDICES, BACK_INDICES)


if __name__ == "__main__":
    main()
