import itertools
import logging

log = logging.getLogger(__name__)


class GameController:
    def __init__(self, node_pairs):
        self._node_pairs = list(node_pairs)
        for node_pair in self._node_pairs:
            log.info(f'Configured pair: {node_pair}')
        self._hint_cycle = itertools.cycle(self._node_pairs)

    def poll(self):
        incomplete = False
        for node_pair in self._node_pairs:
            incomplete |= node_pair.poll()
        return incomplete

    def give_hint(self):
        for count, hint_pair in zip(itertools.count(), self._hint_cycle):
            if count >= len(self._node_pairs):
                log.info("All pairs connected, no hint needed.")
                return
            if hint_pair.is_connected() != True:
                log.info(f"Providing hint: {hint_pair}")
                hint_pair.give_hint()
                return
