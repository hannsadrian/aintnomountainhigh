from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Stop
from pybricks.tools import wait

from orientation import LEVEL

CLIMBING_SPEED = 720

def climbingStep(
        ev3: EV3Brick, 
        left_motor: Motor, 
        right_motor: Motor, 
        lift_motor: Motor,
        vertical_gyro: GyroSensor,
        ultrasonic: UltrasonicSensor):
    vertical_gyro.reset_angle(0)

    lift_motor.run(-360)
    wait(500)
    lift_motor.brake()
    lift_motor.reset_angle(0)
    left_motor.run(CLIMBING_SPEED)
    right_motor.run(CLIMBING_SPEED)

    while vertical_gyro.angle() < 10:
        pass

    counter = 0
    while vertical_gyro.angle() > 3 or ultrasonic.distance() > LEVEL[1]:
        counter += 1
        if counter == 1000:
            lift_motor.run_target(1000, 90, then=Stop.COAST, wait=False)
        if counter == 2000:
            lift_motor.run_target(1000, 0, Stop.COAST, wait=False)
            counter = 0
        pass

    wait(100)

    left_motor.brake()
    right_motor.brake()

    wait(1000)