import threading
import time
import RPi.GPIO as GPIO

class StepperMotor:
    dutySleep = 0.001

    def __init__(self, stepPin, dirPin):
        self.stepPin = stepPin
        self.dirPin = dirPin

        GPIO.setup(self.stepPin, GPIO.OUT)
        GPIO.setup(self.dirPin, GPIO.OUT)

        self.dir = 0
        self.dirLock = threading.Lock()

        self.stopping = False

        self.thread = threading.Thread(target=self.controlLoop)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stopping = True
        self.thread.join()

    def controlLoop(self):
        while not self.stopping:
            if self.dir != 0:
                GPIO.output(self.stepPin, GPIO.HIGH)
                time.sleep(self.dutySleep)
                GPIO.output(self.stepPin, GPIO.LOW)
                time.sleep(self.dutySleep)

    def up(self):
        if self.dir == 1:
            return

        self.__updateDir(self.dir + 1)

    def down(self):
        if self.dir == -1:
            return

        self.__updateDir(self.dir - 1)

    def stop(self):
        if self.dir == 0:
            return

        self.__updateDir(0)

    def __str__(self):
        dirState = 'Stopped'
        if self.dir > 0:
            dirState = 'Forward'
        elif self.dir < 0:
            dirState = 'Reverse'

        return "STEPPER(step={0},dir={1}): {2}".format(self.stepPin, self.dirPin, dirState)

    def __updateDir(self, newDir):
        with self.dirLock:
            self.dir = newDir

        if self.dir != 0:
            GPIO.output(self.dirPin, GPIO.HIGH if self.dir >= 0 else GPIO.LOW)
