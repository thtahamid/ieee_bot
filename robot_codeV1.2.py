from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
import time
from time import sleep
from collections import deque

# Adafruit servokit for arm control
arm = ServoKit(channels=16)
servo = 3

# Define GPIO pins for ultrasonic
GPIO_TRIGGER = 24
GPIO_ECHO = 23

# GPIO pins for IR sensors
sensor_pins = [5, 6, 13, 19, 26]
# GPIO pins for motors
enr, ra, rb, enl, la, lb = 21, 16, 20, 1, 7, 8

def pin_setup():
    global pwmr
    global pwml
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in sensor_pins:
        GPIO.setup(pin, GPIO.IN)

    GPIO.setup(enr, GPIO.OUT)
    GPIO.setup(ra, GPIO.OUT)
    GPIO.setup(rb, GPIO.OUT)
    GPIO.setup(enl, GPIO.OUT)
    GPIO.setup(la, GPIO.OUT)
    GPIO.setup(lb, GPIO.OUT)

    pwmr = GPIO.PWM(enr, 100)
    pwml = GPIO.PWM(enl, 100)

    pwmr.start(0)
    pwml.start(0)

    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

def moveF(r=0, l=0):
    pwmr.ChangeDutyCycle(r)
    pwml.ChangeDutyCycle(l)
    GPIO.output(ra, GPIO.HIGH)
    GPIO.output(rb, GPIO.LOW)
    GPIO.output(la, GPIO.HIGH)
    GPIO.output(lb, GPIO.LOW)

def moveB(r=0, l=0):
    pwmr.ChangeDutyCycle(r)
    pwml.ChangeDutyCycle(l)
    GPIO.output(ra, GPIO.LOW)
    GPIO.output(rb, GPIO.HIGH)
    GPIO.output(la, GPIO.LOW)
    GPIO.output(lb, GPIO.HIGH)


def moveR(r=0, l=0):
    pwmr.ChangeDutyCycle(r)
    pwml.ChangeDutyCycle(l)
    GPIO.output(ra, GPIO.LOW)
    GPIO.output(rb, GPIO.HIGH)
    GPIO.output(la, GPIO.HIGH)
    GPIO.output(lb, GPIO.LOW)


def turnR(r=0, l=0):

    while read_sensor_values()[4] != 0:
        pwmr.ChangeDutyCycle(r)
        pwml.ChangeDutyCycle(l)
        GPIO.output(ra, GPIO.LOW)
        GPIO.output(rb, GPIO.HIGH)
        GPIO.output(la, GPIO.HIGH)
        GPIO.output(lb, GPIO.LOW)
    while read_sensor_values()[3] != 0:
        pwmr.ChangeDutyCycle(r)
        pwml.ChangeDutyCycle(l)
        GPIO.output(ra, GPIO.LOW)
        GPIO.output(rb, GPIO.HIGH)
        GPIO.output(la, GPIO.HIGH)
        GPIO.output(lb, GPIO.LOW) 
    while read_sensor_values()[2] != 0:
        pwmr.ChangeDutyCycle(r)
        pwml.ChangeDutyCycle(l)
        GPIO.output(ra, GPIO.LOW)
        GPIO.output(rb, GPIO.HIGH)
        GPIO.output(la, GPIO.HIGH)
        GPIO.output(lb, GPIO.LOW)


def moveL(r=0, l=0):
    pwmr.ChangeDutyCycle(r)
    pwml.ChangeDutyCycle(l)
    GPIO.output(ra, GPIO.HIGH)
    GPIO.output(rb, GPIO.LOW)
    GPIO.output(la, GPIO.LOW)
    GPIO.output(lb, GPIO.HIGH)


def turnL(r=0, l=0):
    while read_sensor_values()[0] != 0:
        pwmr.ChangeDutyCycle(r)
        pwml.ChangeDutyCycle(l)
        GPIO.output(ra, GPIO.HIGH)
        GPIO.output(rb, GPIO.LOW)
        GPIO.output(la, GPIO.LOW)
        GPIO.output(lb, GPIO.HIGH)
    while read_sensor_values()[1] != 0:
        pwmr.ChangeDutyCycle(r)
        pwml.ChangeDutyCycle(l)
        GPIO.output(ra, GPIO.HIGH)
        GPIO.output(rb, GPIO.LOW)
        GPIO.output(la, GPIO.LOW)
        GPIO.output(lb, GPIO.HIGH)
    while read_sensor_values()[2] != 0:
        pwmr.ChangeDutyCycle(r)
        pwml.ChangeDutyCycle(l)
        GPIO.output(ra, GPIO.HIGH)
        GPIO.output(rb, GPIO.LOW)
        GPIO.output(la, GPIO.LOW)
        GPIO.output(lb, GPIO.HIGH)

def stop(t=10):
    pwmr.ChangeDutyCycle(0)
    pwml.ChangeDutyCycle(0)
    sleep(t)

def read_sensor_values():
    sensor_values = []
    for pin in sensor_pins:
        sensor_values.append(GPIO.input(pin))
    return sensor_values

def print_sensor_values(sensor_values):
    print('\t'.join(map(str, sensor_values)))

def measure_distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2

    return distance

def follow_line(ir):
    if ir[2] == 0:
        moveF(25, 25)
    elif ir[1] == 0:
        moveF(60, 10)
    elif ir[3] == 0:
        moveF(10, 60)
    elif ir[1] and ir[2] == 0:
        moveF(30, 10)
    elif ir[2] and ir[3] == 0:
        moveF(10, 30)
    elif ir[0] == 0:
        moveL(80,80)
    elif ir[4] == 0:
        moveR(80,80)
    # elif ir[0] and ir[1] and ir[2] and ir[4] == 1 and ir[3] == 0:
    #     moveF(10, 50)
    else:
        moveF(25, 25)





def main():
    try:
        pin_setup()

        coordinate = 0
        at_intersection = False
        completed_coordinates = set()

        while True:
            dist = measure_distance()
            ir = read_sensor_values()
            print('\t'.join(map(str, ir)), f"Distance: {dist:.2f} cm\tCoordinate: {coordinate}", sep='\t')
            time.sleep(0.02)

            # Mark each coordinate in the variable coordinate
            if ir[1] == 0 and ir[2] == 0 and ir[3] == 0:
                if not at_intersection:
                    coordinate += 1
                    at_intersection = True
                    print("Coordinate: ", coordinate)
            else:
                at_intersection = False

            if coordinate == 4 and coordinate not in completed_coordinates:
                moveB(25, 25)
                sleep(0.1)
                stop(1)
                print("Robot reached coordinate: ", coordinate)
                turnL(100, 100)
                print("Turned left")
                stop(1)
                follow_line(ir)
                
                completed_coordinates.add(coordinate)

            elif coordinate == 5 and coordinate not in completed_coordinates:
                moveB(25, 25)
                sleep(0.1)
                stop(1)
                print("Robot reached coordinate: ", coordinate)
                turnL(100, 100)
                print("Turned left")
                stop(1)
                follow_line(ir)
                completed_coordinates.add(coordinate)

            elif coordinate == 8 and coordinate not in completed_coordinates:
                moveB(25, 25)
                sleep(0.1)
                stop(1)
                print("Robot reached coordinate: ", coordinate)
                turnR(100, 100)
                print("Turned `Right`")
                stop(1)
                follow_line(ir)
                completed_coordinates.add(coordinate)

            elif coordinate == 9 and coordinate not in completed_coordinates:
                moveB(25, 25)
                sleep(0.1)
                stop(1)
                print("Robot reached coordinate: ", coordinate)
                turnR(100, 100)
                print("Turned R")
                stop(1)
                follow_line(ir)
                completed_coordinates.add(coordinate)
                # print("Completed coordinates: ", completed_coordinates)
                
            
            follow_line(ir)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
