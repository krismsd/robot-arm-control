import threading
import time
import struct

from ThreadResource import ThreadResource

class I2CEncoder(ThreadResource):
    ignoring = True
    turnValues = [0, 0]

    ioErrors = 0

    def __init__(self, bus, i2cAddress):
        super().__init__()

        self.bus = bus
        self.i2cAddress = i2cAddress

    def loop(self):
        data = None
        try:
            data = self.bus.read_i2c_block_data(self.i2cAddress, 0, 4)[:4]
        except IOError:
            self.ioErrors += 1
            return

        # Ignore the first read to ensure we're zeroed properly (since encoder holds it's value until read)
        if self.ignoring:
            self.ignoring = False
        else:
            aDelta, bDelta = struct.unpack('hh', bytes(bytearray(data)))
            self.turnValues[0] += aDelta
            self.turnValues[1] += bDelta

        time.sleep(0.1)

    def getTurns(self, idx):
        return self.turnValues[idx]
