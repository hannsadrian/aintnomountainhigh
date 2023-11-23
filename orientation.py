from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Stop
from pybricks.tools import wait

import turning

LEVEL = [130, 152]
LOW = [105, 130]
IDEAL = [80, 105]
HIGH = [0, 80]

CRAWLING_SPEED = 180
BACKING_UP_TIME = 2

LEFT = "LEFT"
CENTER = "CENTER"
RIGHT = "RIGHT"

def do_average_calculation(latest_distance_readings: [int]) -> (float, float):
    sum = 0
    for m in latest_distance_readings:
        sum += m

    average_distance = sum / len(latest_distance_readings)

    latest_distance_readings.sort()
    variance = abs(latest_distance_readings[-1]-latest_distance_readings[0])
    latest_distance_readings.clear()

    return average_distance, variance

def orientationStep(
        ev3: EV3Brick,
        left_motor: Motor, 
        right_motor: Motor, 
        lift_motor: Motor,
        ultrasonic: UltrasonicSensor, 
        horizontal_gyro: GyroSensor,
        vertical_gyro: GyroSensor) -> bool:
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
    horizontal_gyro.reset_angle(0)
    vertical_gyro.reset_angle(0)

    while True:
        left_motor.reset_angle(0)
        right_motor.reset_angle(0)
        left_motor.run(CRAWLING_SPEED)
        right_motor.run(CRAWLING_SPEED)

        latest_distance_readings = []
        average_distance = ultrasonic.distance()
        distance_variance = 0

        counter = 0
        while LEVEL[0] < average_distance < LEVEL[1] or distance_variance > 5 or abs(vertical_gyro.angle()) > 5:
            counter += 1
            latest_distance_readings.append(ultrasonic.distance())

            if counter % 50 == 0:
                average_distance, distance_variance = do_average_calculation(latest_distance_readings)
            pass

        vertical_gyro.reset_angle(0)

        # wait in order to drive a bit further for accurate measurements
        wait(100)
        
        left_motor.brake()
        right_motor.brake()
        crawled_distance = (left_motor.angle() + right_motor.angle())/2
        print("crawled distance ", crawled_distance)

        # wait in order to get the vehicle to a rest
        wait(800)

        # TODO: check for misreadings, if there are any: move slightly

        # output current state to display
        ev3.screen.clear()
        ev3.screen.draw_text(10, 10, "found step")
        ev3.screen.draw_text(10, 30,  "with height " + str(average_distance))

        if currently_exploring_angle is CENTER:
            center_step_distance = average_distance
        elif currently_exploring_angle is RIGHT:
            right_step_distance = average_distance
        elif currently_exploring_angle is LEFT:
            left_step_distance = average_distance

        if isIdealStep(average_distance):
            ev3.screen.clear()
            ev3.screen.draw_text(10, 10, "going for " + currently_exploring_angle)
            return True
        else:
            # back up and turn 90deg
            left_motor.run_angle(-CRAWLING_SPEED, crawled_distance*0.75, Stop.BRAKE, wait=False)
            right_motor.run_angle(-CRAWLING_SPEED, crawled_distance*0.75, Stop.BRAKE, wait=True)

            if currently_exploring_angle is CENTER:
                turning.turn_to(80, horizontal_gyro, left_motor, right_motor, lift_motor)
                currently_exploring_angle = RIGHT
            elif currently_exploring_angle is RIGHT:
                turning.turn_to(-180, horizontal_gyro, left_motor, right_motor, lift_motor)
                currently_exploring_angle = LEFT
            else:
                ev3.screen.clear()
                ev3.screen.draw_text(10, 10, "center: " + str(center_step_distance))
                ev3.screen.draw_text(10, 30, "right: " + str(right_step_distance))
                ev3.screen.draw_text(10, 60, "left: " + str(left_step_distance))
                while True:
                    pass
                return False
                
            


def isIdealStep(distance: int) -> bool:
    return IDEAL[0] < distance < IDEAL[1]