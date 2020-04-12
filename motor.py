import RPi.GPIO as GPIO

class Motor:
    """
    Control a DC motor through PWM.
    `enablePin` is the GPIO pin number for turning the motor on. It will be PWN'd to control speed.
    `phasePin` is the GPIO pin number for controling the direction of the motor.

    Pin numbers are dependant of the current setting of `GPIO.setmode()`
    """
    def __init__(self, enablePin, phasePin):
        self.enablePin = enablePin
        self.phasePin = phasePin

        GPIO.setup(self.enablePin, GPIO.OUT)
        GPIO.setup(self.phasePin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.enablePin, 250)
        self.pwm.start(0)

        self.setSpeed(0)

    """
    Set the speed given as a float -1 to 1. Negative speed represents reverse rotation.
    The speed is projected into a useful duty value (as small duty values may not be enough
    to actually move the motor)
    """
    def setSpeed(self, speed):
        # Project the speed to the useful duty range (-1 to -0.5, 0.5 to 1 or 0 for stop)
        if speed == 0:
            self.duty = 0
        else:
            rawDuty = (abs(speed)  / 2) + 0.5
            self.duty = max(min(rawDuty, -1), 1) * 100 * (1 if speed > 0 else -1)

        GPIO.output(self.phasePin, GPIO.HIGH if self.duty >= 0 else GPIO.LOW)
        self.pwm.ChangeDutyCycle(abs(self.duty))

    """
    Get the speed given as a float -1 to 1. Similar to `setSpeed` the speed is projected back
    from the current duty value
    """
    def getSpeed(self):
        if self.duty == 0:
            return 0

        return ((abs(self.duty) / 100) - 0.5) * 2 * (1 if self.duty > 0 else -1)

    def __str__(self):
        return 'DCMOTOR(enable={0},phase={1}): speed={2:.0%}'.format(
            self.enablePin,
            self.phasePin,
            self.getSpeed()
        )
