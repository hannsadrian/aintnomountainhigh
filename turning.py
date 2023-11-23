from pybricks.ev3devices import (Motor, TouchSensor, GyroSensor)
from pybricks.parameters import Stop
from pybricks.tools import wait

def turning_test(left: Motor, right: Motor, lift: Motor, button: TouchSensor):
    lift.reset_angle(0)

    while True:
        if button.pressed():
            lift.run_target(1000, 90, Stop.HOLD)
            left.run(180)
            right.run(-180)
        else:
            lift.run_target(1000, 0, Stop.BRAKE)
            left.brake()
            right.brake()

TURNING_SPEED = 180

def turn_to(angle: int, gyro: GyroSensor, left: Motor, right: Motor, lift: Motor):
    lift.reset_angle(0)
    gyro.reset_angle(0)
    wait(100)

    lift.run_target(1000, 90, Stop.HOLD, wait=False)

    while abs(gyro.angle()) < abs(angle):
        # this code is ran
        # gyro.angle()/angle = 0-1
        ratio = abs(gyro.angle())/abs(angle)
        #ratio = (ratio*0.5)+0.25

        if angle > 0:
            left.run(TURNING_SPEED*ratio)
            right.run(-TURNING_SPEED*(1-ratio))
        elif angle < 0:
            left.run(-TURNING_SPEED*(1-ratio))
            right.run(TURNING_SPEED*ratio)

        pass

    left.brake()
    right.brake()
    lift.run_target(1000, 0, Stop.BRAKE, wait=True)
    