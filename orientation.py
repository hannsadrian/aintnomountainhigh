from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Stop

LEVEL = [125, 135]
VERY_LOW = [100, 125]
LOW = [80, 100]
IDEAL = [60, 80]
HIGH = [40, 80]
VERY_HIGH = [0, 40]

CRAWLING_SPEED = 180
TURNING_SPEED = 180
BACKING_UP_TIME = 2

LEFT = "LEFT"
CENTER = "CENTER"
RIGHT = "RIGHT"

def orientationStep(
        ev3: EV3Brick,
        left_motor: Motor, 
        right_motor: Motor, 
        ultrasonic: UltrasonicSensor, 
        horizontal_gyro: GyroSensor):
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

        while LEVEL[0] < ultrasonic.distance() < LEVEL[1]:
            pass

        
        left_motor.brake()
        right_motor.brake()
        crawled_distance = (left_motor.angle() + right_motor.angle())/2

        # TODO: check for misreadings, if there are any: move slightly

        # output current state to display
        ev3.screen.clear()
        ev3.screen.draw_text(10, 10, "found step with height " + ultrasonic.distance())

        distance_reading = ultrasonic.distance()

        if currently_exploring_angle is CENTER:
            center_step_distance = distance_reading
        elif currently_exploring_angle is RIGHT:
            right_step_distance = distance_reading
        elif currently_exploring_angle is LEFT:
            left_step_distance = distance_reading

        if isIdealStep(distance_reading):
            break
        else:
            # back up and turn 90deg
            left_motor.run_angle(-CRAWLING_SPEED, crawled_distance, Stop.BRAKE)
            right_motor.run_angle(-CRAWLING_SPEED, crawled_distance, Stop.BRAKE)

            left_motor.run(TURNING_SPEED)
            right_motor.run(-TURNING_SPEED)

            while horizontal_gyro.angle() < 90:
                pass
            left_motor.brake()
            right_motor.brake()

            if currently_exploring_angle is CENTER:
                currently_exploring_angle = RIGHT
            


def isIdealStep(distance: int) -> bool:
    return IDEAL[0] < distance < IDEAL[1]