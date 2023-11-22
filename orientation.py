from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Stop

import turning

LEVEL = [110, 135]
LOW = [100, 110]
IDEAL = [70, 100]
HIGH = [0, 70]

CRAWLING_SPEED = 360
BACKING_UP_TIME = 2

LEFT = "LEFT"
CENTER = "CENTER"
RIGHT = "RIGHT"

def orientationStep(
        ev3: EV3Brick,
        left_motor: Motor, 
        right_motor: Motor, 
        lift_motor: Motor,
        ultrasonic: UltrasonicSensor, 
        horizontal_gyro: GyroSensor) -> bool:
    # slowly move forward
    # if the distance changes: (check for misreadings)
    #   1) save it (not ideal or a step down)
    #   2) it's ideal -> exit orientation and climb

    # if it's not ideal go backwards
    # turn right 90deg
    # start again

    left_step_distance = None
    center_step_distance = None
    right_step_distance = None

    crawled_distance = 0
    currently_exploring_angle = CENTER

    while True:
        left_motor.reset_angle(0)
        right_motor.reset_angle(0)
        left_motor.run(CRAWLING_SPEED)
        right_motor.run(CRAWLING_SPEED)

        counter = 0
        while LEVEL[0] < ultrasonic.distance() < LEVEL[1]:
            counter += 1
            if counter % 200 == 0:
                ev3.screen.clear()
                ev3.screen.draw_text(10, 10, "dist: " + str(ultrasonic.distance()))
            pass

        
        left_motor.brake()
        right_motor.brake()
        crawled_distance = (left_motor.angle() + right_motor.angle())/2
        print("crawled distance ", crawled_distance)

        # TODO: check for misreadings, if there are any: move slightly

        # output current state to display
        ev3.screen.clear()
        ev3.screen.draw_text(10, 10, "found step")
        ev3.screen.draw_text(10, 30,  "with height " + str(ultrasonic.distance()))

        distance_reading = ultrasonic.distance()

        if currently_exploring_angle is CENTER:
            center_step_distance = distance_reading
        elif currently_exploring_angle is RIGHT:
            right_step_distance = distance_reading
        elif currently_exploring_angle is LEFT:
            left_step_distance = distance_reading

        if isIdealStep(distance_reading):
            ev3.screen.clear()
            ev3.screen.draw_text(10, 10, "going for " + currently_exploring_angle)
            return True
        else:
            # back up and turn 90deg
            left_motor.run_angle(-CRAWLING_SPEED, crawled_distance*0.5, Stop.BRAKE, wait=False)
            right_motor.run_angle(-CRAWLING_SPEED, crawled_distance*0.5, Stop.BRAKE, wait=True)

            if currently_exploring_angle is CENTER:
                turning.turn_to(80, horizontal_gyro, left_motor, right_motor, lift_motor)
                currently_exploring_angle = RIGHT
            elif currently_exploring_angle is RIGHT:
                turning.turn_to(-180, horizontal_gyro, left_motor, right_motor, lift_motor)
                currently_exploring_angle = LEFT
            else:
                # TODO: find ideal step and take it.
                return False
                
            


def isIdealStep(distance: int) -> bool:
    return IDEAL[0] < distance < IDEAL[1]