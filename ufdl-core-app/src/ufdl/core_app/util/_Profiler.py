from time import thread_time_ns
from typing import Optional


class Profiler:
    def __init__(
            self,
            label: str
    ):
        self._label = label
        self._start = thread_time_ns()
        self._last = self._start
        self.msg("Start", self._start)

    def msg(self, message: str, time: Optional[int] = None):
        time = time if time is not None else thread_time_ns()
        print(f"[{time}] {self._label} @ {time - self._start} [+{time - self._last}]: {message}")
        self._last = time

    def end(self, message: Optional[str] = None):
        message = "End" if message is None else f"End: {message}"
        self.msg(message)
