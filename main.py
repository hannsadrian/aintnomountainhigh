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

startStopSensor = TouchSensor(Port.S4)
distanceSensor = UltrasonicSensor(Port.S1)
gyroSensor = GyroSensor(Port.S2)
gyroSensor.reset_angle(0)

leftDriveMotor = Motor(Port.A)
rightDriveMotor = Motor(Port.D)



DRIVE_SPEED = 360 * 2

ev3.screen.draw_text(10, 10, "waiting to start")

triggering_angle = 10
while leftDriveMotor.angle() < triggering_angle and rightDriveMotor.angle() < triggering_angle:
    pass

ev3.screen.clear()

counter = 0
while True:
    wait(1)
    counter += 1

    if counter % 200 == 0:
        d = distanceSensor.distance()
        ev3.screen.clear()
        ev3.screen.draw_text(10, 10, "ultrasonic:" + str(d))
        ev3.screen.draw_text(10, 30, "gyro-angle:" + str(gyroSensor.angle()))

    if program_state == ORIENTING_STATE:
        leftDriveMotor.brake()
        rightDriveMotor.brake()

        if startStopSensor.pressed():
            program_state = CLIMBING_STATE
    
    if program_state == CLIMBING_STATE:
        leftDriveMotor.run(DRIVE_SPEED)
        rightDriveMotor.run(DRIVE_SPEED)

        

        # switching to ORIENTING_STATE if not pressed
        if not startStopSensor.pressed():
            program_state = ORIENTING_STATE
            
