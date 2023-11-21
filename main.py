#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ORIENTING_STATE = "ORIENTING_STATE"
CLIMBING_STATE = "CLIMBING_STATE"

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
program_state = ORIENTING_STATE

kill_switch = TouchSensor(Port.S4)
distance_sensor = UltrasonicSensor(Port.S1)
gyro_sensor = GyroSensor(Port.S2)
gyro_sensor.reset_angle(0)

left_drive_motor = Motor(Port.A)
right_drive_motor = Motor(Port.D)



DRIVE_SPEED = 360 * 2

ev3.screen.draw_text(10, 10, "waiting to start")

triggering_angle = 10
while left_drive_motor.angle() < triggering_angle and right_drive_motor.angle() < triggering_angle:
    pass

ev3.screen.clear()

counter = 0
while True:
    wait(1)
    counter += 1

    if kill_switch.pressed():
        quit()

    if counter % 200 == 0:
        d = distance_sensor.distance()
        ev3.screen.clear()
        ev3.screen.draw_text(10, 10, "ultrasonic:" + str(d))
        ev3.screen.draw_text(10, 30, "gyro-angle:" + str(gyro_sensor.angle()))

    if program_state == ORIENTING_STATE:
        left_drive_motor.brake()
        right_drive_motor.brake()
    
    if program_state == CLIMBING_STATE:
        left_drive_motor.run(DRIVE_SPEED)
        right_drive_motor.run(DRIVE_SPEED)
            
