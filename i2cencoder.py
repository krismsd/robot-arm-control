import threading
import time
import struct

class I2CEncoder:
    def __init__(self, bus, i2cAddress):
        self.bus = bus
        self.i2cAddress = i2cAddress

        self.turns = None

        self.stopping = False
        self.thread = threading.Thread(target=self.pollLoop)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stopping = True
        self.thread.join()

    def pollLoop(self):
        while not self.stopping:
            data = self.bus.read_i2c_block_data(self.i2cAddress, 0, 2)[:2]

            # Ignore the first value to ensure we're zeroed properly (since encoder holds it's value until read)
            if not self.turns is None:
                self.turns += struct.unpack('h', bytes(bytearray(data)))[0]
            else:
                self.turns = 0
                
            time.sleep(1)
