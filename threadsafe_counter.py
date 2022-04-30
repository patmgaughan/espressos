"""
  threadsafe_counter.py
  Description: a threadsafe counter class

  Authors: Jackson Clayton
"""

import threading

class ThreadsafeCounter:
    """
    Monitor class for a threadsafe counter
    """
    def __init__(self, start = 0):
        self.lock = threading.Lock()
        self.count = start

    def __str__(self):
        with self.lock:
            return str(self.count)

    def add(self, i):
        with self.lock:
            self.count += i
            return self.count

    def get(self):
        with self.lock:
            return self.count

    def increment(self):
        return self.add(1)

