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

touchSensor = TouchSensor(Port.S1)
distanceSensor = UltrasonicSensor(Port.S2)
gyroSensor = GyroSensor(Port.S3)
gyroSensor.reset_angle(0)

leftDriveMotor = Motor(Port.A)
rightDriveMotor = Motor(Port.D)

DRIVE_SPEED = 360 * 2

while True:
    d = distanceSensor.distance()
    ev3.screen.clear()
    ev3.screen.draw_text(10, 10, "ultrasonic:" + str(d))
    ev3.screen.draw_text(10, 30, "gyro-angle:" + str(gyroSensor.angle()))
    ev3.screen.draw_text(10, 60, "gyro-speed:" + str(gyroSensor.speed()))
    wait(500)

    if program_state == ORIENTING_STATE:
        leftDriveMotor.brake()
        rightDriveMotor.brake()

        if touchSensor.pressed():
            program_state = CLIMBING_STATE
    
    if program_state == CLIMBING_STATE:
        leftDriveMotor.run(DRIVE_SPEED)
        rightDriveMotor.run(DRIVE_SPEED)

        # switching to ORIENTING_STATE if not pressed
        if not touchSensor.pressed():
            program_state = ORIENTING_STATE
            
