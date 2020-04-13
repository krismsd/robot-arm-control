#!/usr/bin/env python3

import curses
import RPi.GPIO as GPIO
import smbus

from motor import Motor
from stepper import StepperMotor
from i2cencoder import I2CEncoder
from ArmJoint import ArmJoint

try:
    GPIO.setmode(GPIO.BCM)

    bus = smbus.SMBus(1)

    motor1 = Motor(6, 13)
    motor2 = Motor(19, 26)

    stepper1 = StepperMotor(21, 20)

    encoderConnection = I2CEncoder(bus, 0x08)

    jointAngleRatio = 54000 * 2 * -1 # 54000 measured position manually over 1/2th of full rotation
    armJoint1 = ArmJoint(motor1, encoderConnection, 0, 180, jointAngleRatio)
    armJoint2 = ArmJoint(motor2, encoderConnection, 1, 180, jointAngleRatio)

    with stepper1, encoderConnection, armJoint1, armJoint2:

        def updateScreen(screen):
            screen.clear()
            screen.addstr(1, 0, str(stepper1))
            screen.addstr(2, 0, "Encoder thread alive? " + str(encoderConnection.thread.is_alive()) + " - " + str(encoderConnection.ioErrors) + " errors")

            screen.addstr(4, 0, str(armJoint1))
            screen.addstr(5, 0, str(armJoint2))

            screen.refresh()

        def handleInputChar(char):
            if char == ord('a'):
                armJoint1.setSpeed(1)
            elif char == ord('s'):
                armJoint1.setSpeed(0)
            elif char == ord('d'):
                armJoint1.setSpeed(-1)
            elif char == ord('f'):
                armJoint1.initCurrentAngle(90)

            if char == ord('z'):
                armJoint2.setSpeed(1)
            elif char == ord('x'):
                armJoint2.setSpeed(0)
            elif char == ord('c'):
                armJoint2.setSpeed(-1)
            elif char == ord('v'):
                armJoint2.initCurrentAngle(90)

            elif char == ord('b'):
                stepper1.up()
            elif char == ord('n'):
                stepper1.stop()
            elif char == ord('m'):
                stepper1.down()

            elif char == ord(' '):
                armJoint1.setSpeed(0)
                armJoint2.setSpeed(0)
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
