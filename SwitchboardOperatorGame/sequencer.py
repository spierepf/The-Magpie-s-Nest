try:
    from time import ticks_ms, ticks_add, ticks_diff
except:
    from time import time_ns


    def ticks_ms():
        return time_ns() // 1000000


    def ticks_add(ticks, delta):
        return ticks + delta


    def ticks_diff(ticks1, ticks2):
        return ticks1 - ticks2

MILLISECOND = 1
SECOND = MILLISECOND * 1000
MINUTE = SECOND * 60
HOUR = MINUTE * 60


class Sequencer:
    def __init__(self, clock=ticks_ms, add=ticks_add, diff=ticks_diff):
        self._tasks = set()
        self._clock = clock
        self._add = add
        self._diff = diff

    def after(self, duration, unit, task):
        when = self._add(self._clock(), duration * unit)
        self._tasks.add((when, task))

    def __call__(self):
        for when, task in list(self._tasks):
            if self._diff(self._clock(), when) >= 0:
                task()
                self._tasks.remove((when, task))
