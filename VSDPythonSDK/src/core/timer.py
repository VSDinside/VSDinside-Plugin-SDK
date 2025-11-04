import threading
import time
from typing import Dict, Callable

class Timer:
    def __init__(self):
        self._intervals: Dict[str, Dict] = {}
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
    
    def _run(self):
        while True:
            current_time = time.time()
            for uuid, data in list(self._intervals.items()):
                if current_time - data['last_run'] >= data['delay']:
                    data['callback']()
                    data['last_run'] = current_time
            time.sleep(0.1)
    
    def set_interval(self, uuid: str, delay: float, callback: Callable):
        self._intervals[uuid] = {
            'delay': delay / 1000,  # Convert ms to seconds
            'callback': callback,
            'last_run': time.time()
        }
    
    def clear_interval(self, uuid: str):
        if uuid in self._intervals:
            del self._intervals[uuid]