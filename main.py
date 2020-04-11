#!/usr/bin/env python3

import curses
import RPi.GPIO as GPIO

from motor import Motor
from stepper import StepperMotor

GPIO.setmode(GPIO.BCM)


screen = curses.initscr()
screen.nodelay(1)
curses.noecho()
curses.cbreak()

screen.keypad(True)

try:
    MOTOR1 = Motor(6, 13)
    MOTOR2 = Motor(19, 26)

    with StepperMotor(21, 20) as STEPPER:
        while True:
            screen.clear()
            screen.addstr(0, 0, str(MOTOR1))
            screen.addstr(1, 0, str(MOTOR2))
            screen.addstr(2, 0, str(STEPPER))

            screen.refresh()


            char = screen.getch()
            
            if char == ord('q'):
                break

            elif char == ord('a'):
                MOTOR1.up()
            elif char == ord('s'):
                MOTOR1.stop()
            elif char == ord('d'):
                MOTOR1.down()

            elif char == ord('z'):
                MOTOR2.up()
            elif char == ord('x'):
                MOTOR2.stop()
            elif char == ord('c'):
                MOTOR2.down()

            elif char == ord('b'):
                STEPPER.up()
            elif char == ord('n'):
                STEPPER.stop()
            elif char == ord('m'):
                STEPPER.down()

            elif char == ord(' '):
                MOTOR1.stop()
                MOTOR2.stop()
                STEPPER.stop()

finally:
    GPIO.cleanup()

    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
