#!/usr/bin/env python3

import curses
import RPi.GPIO as GPIO
import smbus

from motor import Motor
from stepper import StepperMotor
from i2cencoder import I2CEncoder

try:
    GPIO.setmode(GPIO.BCM)

    bus = smbus.SMBus(1)

    motor1 = Motor(6, 13)
    motor2 = Motor(19, 26)

    with StepperMotor(21, 20) as stepper1, I2CEncoder(bus, 0x08) as motor1Encoder:

        def updateScreen(screen):
            screen.clear()
            screen.addstr(0, 0, str(motor1))
            screen.addstr(1, 0, str(motor2))
            screen.addstr(2, 0, str(stepper1))
            screen.addstr(3, 0, "Turns:" + str(motor1Encoder.turns))
            screen.addstr(4, 0, "Encoder thread alive? " + str(motor1Encoder.thread.is_alive()))

            screen.refresh()

        def handleInputChar(char):
            if char == ord('a'):
                motor1.up()
            elif char == ord('s'):
                motor1.stop()
            elif char == ord('d'):
                motor1.down()

            elif char == ord('z'):
                motor2.up()
            elif char == ord('x'):
                motor2.stop()
            elif char == ord('c'):
                motor2.down()

            elif char == ord('b'):
                stepper1.up()
            elif char == ord('n'):
                stepper1.stop()
            elif char == ord('m'):
                stepper1.down()

            elif char == ord(' '):
                motor1.stop()
                motor2.stop()
                stepper1.stop()

        def cursesLoop(screen):
            screen.timeout(500)

            while True:
                updateScreen(screen)

                char = screen.getch()
                if char != -1:
                    if char == ord('q'):
                        break

                    handleInputChar(char)

        curses.wrapper(cursesLoop)

finally:
    GPIO.cleanup()
