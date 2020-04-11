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
        self.duty = 0

        self.pwm.start(0)
        self.__reflectDuty()

    """
    Increate PWM duty cycle value to change motor speed. 
    If value is negative Motor speed is abs(duty) in reverse direction.
    """
    def up(self):
        self.duty += 10
        if self.duty > 100:
            self.duty = 100

        self.__reflectDuty()

    """
    Decrease PWM duty cycle value to change motor speed. 
    If value is negative Motor speed is abs(duty) in reverse direction.
    """
    def down(self):
        self.duty -= 10
        if self.duty < -100:
            self.duty = -100
            
        self.__reflectDuty()

    """
    Set PWN duty cycle to zero, stopping the motor
    """
    def stop(self):
        self.duty = 0
        self.__reflectDuty()

    def __str__(self):
        dutyState = 'Stopped'
        if self.duty != 0:
            dutyState = "{0} - {1}%".format(('Forward' if self.duty >= 0 else 'Reverse'), str(abs(self.duty)))

        return 'DCMOTOR(enable={0},phase={1}): {2}'.format(self.enablePin, self.phasePin, dutyState)

    def __reflectDuty(self):
        GPIO.output(self.phasePin, GPIO.HIGH if self.duty >= 0 else GPIO.LOW)
        self.pwm.ChangeDutyCycle(abs(self.duty))
