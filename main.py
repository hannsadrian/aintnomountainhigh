#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Image

import orientation
import climbing
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
#climbing.climbingStep(ev3, left_drive_motor, right_drive_motor, lift_motor, vertical_gyro)
""" latest_distance_readings = []
average_distance = distance_sensor.distance()
distance_variance = 0

counter = 0

while True:
    counter += 1
    latest_distance_readings.append(distance_sensor.distance())

    if counter % 50 == 0:
        average_distance, distance_variance = orientation.do_average_calculation(latest_distance_readings)

    wait(1) """
# ------------------

while not Button.DOWN in ev3.buttons.pressed():
    pass

ev3.screen.draw_text(10, 10, "waiting to start")

left_drive_motor.reset_angle(0)
right_drive_motor.reset_angle(0)
triggering_angle = 5
while left_drive_motor.angle() < triggering_angle and right_drive_motor.angle() < triggering_angle:
    pass

ev3.screen.clear()

start_off_angle = 90
left_drive_motor.run_target(180, start_off_angle, wait=False)
right_drive_motor.run_target(180, start_off_angle, wait=True)
turning.turn_to(-80, ev3, horizontal_gyro, left_drive_motor, right_drive_motor, lift_motor, vertical_gyro, distance_sensor)

climbing_step_number = 0
while climbing_step_number < 6:

    if program_state == ORIENTING_STATE:
        orientation_result = orientation.orientationStep(
            ev3, left_drive_motor, right_drive_motor, 
            lift_motor, distance_sensor, horizontal_gyro, vertical_gyro)
        if orientation_result is True:
            vertical_gyro.reset_angle(0)
            program_state = CLIMBING_STATE
        else:
            ev3.screen.clear()
            ev3.screen.draw_text(10, 10, "ERROR WHILE ORIENTING")

    
    if program_state == CLIMBING_STATE:
        climbing.climbingStep(ev3, left_drive_motor, right_drive_motor, lift_motor, vertical_gyro, distance_sensor)
        climbing_step_number += 1
        program_state = ORIENTING_STATE
            
ev3.screen.clear()
ev3.screen.draw_text(10, 10, "top reached!")
