#!/usr/bin/env python3
'''Hello to the world from ev3dev.org'''

import os
import sys
from time import sleep
import datetime

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, SpeedPercent, SpeedRPM, MoveTank, MoveSteering
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button
from ev3dev2.sound import Sound

# state constants
ON = True
OFF = False

btn = Button()
sound = Sound()

slow_speed = 20
normal_speed = 40

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')


def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)


def main():
    '''The main function of our program'''

    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')

    # print something to the screen of the device
    print('Hello World!')

    # print something to the output panel in VS Code
    debug_print('Hello VS Code!')

    # wait a bit so you have time to look at the display before the program
    # exits

    leds = Leds()

    leds.set_color("LEFT", "GREEN")
    leds.set_color("RIGHT", "GREEN")

    sound.speak("I am ready")

    btn.wait_for_bump('right')

    leds.set_color("LEFT", "RED")
    leds.set_color("RIGHT", "RED")

    drive()

def drive():
    # Move the device until wall is hit, after hit, drive back and turn left and try again
    #tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
    move = MoveSteering(OUTPUT_A, OUTPUT_D)
    move.on(steering=0, speed=normal_speed)

    ts = TouchSensor(INPUT_3)
    ts2 = TouchSensor(INPUT_2)
    ultra = UltrasonicSensor(INPUT_4)

    while True:
        # 1. Check if hit a wall
        while not ts.is_pressed and not ts2.is_pressed and ultra.distance_centimeters < 50:
            sleep(0.01)

        # 2. Check if space on the right side
        if ultra.distance_centimeters > 50:
            move.on_for_degrees(steering=100, speed=slow_speed, degrees=180)
            sound.speak("Going full speed")
            move.on(steering=0, speed=normal_speed)
            continue

        move.off()

        sound.speak("Found a wall")

        # Go back a bit so enough room to turn
        move.on_for_degrees(steering=0, speed=-slow_speed, degrees=90)

        # Turn
        move.on_for_degrees(steering=100, speed=-slow_speed, degrees=180)

        sound.speak("Going full speed")
        move.on(steering=0, speed=normal_speed)



if __name__ == '__main__':
    main()
