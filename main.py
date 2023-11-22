#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Image

import orientation
import turning

ORIENTING_STATE = "ORIENTING_STATE"
CLIMBING_STATE = "CLIMBING_STATE"

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
program_state = ORIENTING_STATE

#kill_switch = TouchSensor(Port.S4)
distance_sensor = UltrasonicSensor(Port.S1)
vertical_gyro = GyroSensor(Port.S2)
vertical_gyro.reset_angle(0)
horizontal_gyro = GyroSensor(Port.S3)
horizontal_gyro.reset_angle(0)

left_drive_motor = Motor(Port.D)
right_drive_motor = Motor(Port.A)
lift_motor = Motor(Port.C)


# --- TEST FIELD ---
#turning.turn_to(80, horizontal_gyro, left_drive_motor, right_drive_motor, lift_motor)
#turning.turn_to(-80, horizontal_gyro, left_drive_motor, right_drive_motor, lift_motor)
# ------------------


ev3.screen.draw_text(10, 10, "waiting to start")

left_drive_motor.reset_angle(0)
right_drive_motor.reset_angle(0)
triggering_angle = 5
while left_drive_motor.angle() < triggering_angle and right_drive_motor.angle() < triggering_angle:
    pass

ev3.screen.clear()

while True:

    if program_state == ORIENTING_STATE:
        orientation_result = orientation.orientationStep(
            ev3, left_drive_motor, right_drive_motor, 
            lift_motor, distance_sensor, horizontal_gyro)
        if orientation_result is True:
            program_state = CLIMBING_STATE
        else:
            ev3.screen.clear()
            ev3.screen.draw_text(10, 10, "ERROR WHILE ORIENTING")

    
    if program_state == CLIMBING_STATE:
        #left_drive_motor.run(DRIVE_SPEED)
        #right_drive_motor.run(DRIVE_SPEED)
        pass
            
