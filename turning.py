from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, GyroSensor, UltrasonicSensor)
from pybricks.parameters import Stop
from pybricks.tools import wait

import climbing

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

def calculate_average_angular_speed(samples: [int]) -> float:
    intervals = 0
    for index, value in enumerate(samples):
        if index < len(samples)-1:
            intervals += abs(samples[index+1]-samples[index])
    
    return intervals/(len(samples)-1)*100

TURNING_SPEED = 180

def turn_to(angle: int, ev3: EV3Brick, horizontal_gyro: GyroSensor, left: Motor, right: Motor, lift: Motor, vertical_gyro: GyroSensor, ultrasonic: UltrasonicSensor):
    wait(100)
    lift.reset_angle(0)
    horizontal_gyro.reset_angle(0)
    vertical_gyro.reset_angle(0)
    wait(100)

    lift.run_target(1000, 90, Stop.HOLD, wait=False)

    gyro_samples = []
    angular_speed = 0

    counter = 0
    while abs(horizontal_gyro.angle()) < abs(angle) and vertical_gyro.angle() < 3:
        counter += 1
        # this code is ran
        # gyro.angle()/angle = 0-1
        ratio = abs(horizontal_gyro.angle())/abs(angle)
        #ratio = (ratio*0.5)+0.25

        gyro_samples.append(horizontal_gyro.angle())
        if counter % 50 == 0:
            angular_speed = calculate_average_angular_speed(gyro_samples)
            gyro_samples.clear()

        inner_boost = 0
        if angular_speed < 6:
            inner_boost = TURNING_SPEED*1.5

        if angle > 0:
            left.run(TURNING_SPEED*ratio+inner_boost*0.5)  #
            right.run(-(TURNING_SPEED*(1-ratio) + inner_boost))
        elif angle < 0:
            left.run(-(TURNING_SPEED*(1-ratio) + inner_boost))
            right.run(TURNING_SPEED*ratio+inner_boost*0.5)   #

        pass

    left.brake()
    right.brake()
    lift.run_target(1000, 0, Stop.BRAKE, wait=True)

    if vertical_gyro.angle() > 2:
        climbing.climbingStep(ev3, left, right, lift, 
                              vertical_gyro, ultrasonic, is_in_save_mode=True)

        turn_to(angle-horizontal_gyro.angle(), ev3, horizontal_gyro, left, right, lift, vertical_gyro, ultrasonic)

    
    