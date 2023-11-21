#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import orientation

ORIENTING_STATE = "ORIENTING_STATE"
CLIMBING_STATE = "CLIMBING_STATE"

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
program_state = ORIENTING_STATE

kill_switch = TouchSensor(Port.S4)
distance_sensor = UltrasonicSensor(Port.S1)
vertical_gyro = GyroSensor(Port.S2)
vertical_gyro.reset_angle(0)
horizontal_gyro = GyroSensor(Port.S3)
horizontal_gyro.reset_angle(0)

left_drive_motor = Motor(Port.A)
right_drive_motor = Motor(Port.D)



DRIVE_SPEED = 360 * 2

ev3.screen.draw_text(10, 10, "waiting to start")

triggering_angle = 10
while left_drive_motor.angle() < triggering_angle and right_drive_motor.angle() < triggering_angle:
    pass

ev3.screen.clear()

while True:

    if kill_switch.pressed():
        quit()

    if program_state == ORIENTING_STATE:
        orientation.orientationStep()
        program_state = CLIMBING_STATE
    
    if program_state == CLIMBING_STATE:
        left_drive_motor.run(DRIVE_SPEED)
        right_drive_motor.run(DRIVE_SPEED)
            
