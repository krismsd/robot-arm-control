from abc import ABC, abstractmethod
import threading

class ThreadResource(ABC):
    stopping = False
    threadException = None

    def __init__(self):
        self.thread = threading.Thread(target=self.threadTarget)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stopping = True
        self.thread.join()
        if self.threadException is not None:
            raise self.threadException

    def threadTarget(self):
        try:
            while not self.stopping:
                self.loop()
        except Exception as e:
            self.threadException = e

    @abstractmethod
    def loop(self):
        pass
