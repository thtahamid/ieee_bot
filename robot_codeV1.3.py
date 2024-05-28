from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
import time
from time import sleep
from collections import deque
import cv2
import numpy as np


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
    while read_sensor_values()[1] != 0:
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
    while read_sensor_values()[3] != 0:
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

def hard_stop():
    moveB(20, 20)
    sleep(0.15)
    stop(1)

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
        moveF(70, 0)
    elif ir[3] == 0:
        moveF(0, 70)
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

def detect_color():
    # Define the lower and upper boundaries for red and blue colors in the HSV color space
    red_lower = np.array([0, 120, 70])
    red_upper = np.array([10, 255, 255])
    blue_lower = np.array([94, 80, 2])
    blue_upper = np.array([126, 255, 255])

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if not ret:
                print("Failed to grab frame")
                break

            # Convert the frame to the HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create masks for red and blue colors
            red_mask = cv2.inRange(hsv, red_lower, red_upper)
            blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
            
            # Calculate the percentage of each color in the frame
            red_percentage = (cv2.countNonZero(red_mask) / (frame.size / 3)) * 100
            blue_percentage = (cv2.countNonZero(blue_mask) / (frame.size / 3)) * 100
            
            # Determine which color is dominant
            if red_percentage > blue_percentage:
                color = "Red"
            elif blue_percentage > red_percentage:
                color = "Blue"
            else:
                color = "None"
            
            # print(f"Detected color: {color}")
            return color

            # Add a small delay to avoid flooding the terminal
            cv2.waitKey(1000)

    except KeyboardInterrupt:
        print("Program interrupted by user")

    finally:
        # Release the capture and close any OpenCV windows
        cap.release()
        cv2.destroyAllWindows()



def main():
    try:
        pin_setup()
        arm.servo[1].angle = int(90)
        sleep(1)
        arm.servo[0].angle = int(180)
        sleep(1.5)
        arm.servo[0].angle = None
        arm.servo[1].angle = None
        
        coordinate = 0
        at_intersection = False
        completed_coordinates = set()
        free_coordinates = set()
        obj_coordinate = []
        while True:
            dist = measure_distance()
            ir = read_sensor_values()
            # obj_color = detect_color()
            print('\t'.join(map(str, ir)), f"Distance: {dist:.2f} cm\tCoordinate: {coordinate}", sep='\t')
            time.sleep(0.02)

            # Mark each coordinate in the variable coordinate
            if ir[1] == 0 and ir[2] == 0 and ir[3] ==0 :
                if not at_intersection:
                    coordinate += 1
                    at_intersection = True
                    free_coordinates.add(coordinate)
                    print("Coordinate: ", coordinate)
                    
                    print("Free coordinates: ", free_coordinates)
                    
            else:
                at_intersection = False

            if coordinate == 4 and coordinate not in completed_coordinates:
                hard_stop()
                print("Robot reached coordinate: ", coordinate)
                turnL(100, 100)
                print("Turned left")
                stop(1)
                print("Completed Coordinates: ", completed_coordinates)
                follow_line(ir)
                
                completed_coordinates.add(coordinate)

            elif coordinate == 5 and coordinate not in completed_coordinates:
                hard_stop()
                print("Robot reached coordinate: ", coordinate)
                turnL(100, 100)
                print("Turned left")
                stop(1)
                print("Completed Coordinates: ", completed_coordinates)
                follow_line(ir)
                completed_coordinates.add(coordinate)

            elif coordinate == 8 and coordinate not in completed_coordinates:
                hard_stop()
                print("Robot reached coordinate: ", coordinate)
                turnR(100, 100)
                print("Turned Right")
                stop(1)
                print("Completed Coordinates: ", completed_coordinates)
                follow_line(ir)
                completed_coordinates.add(coordinate)

            elif coordinate == 9 and coordinate not in completed_coordinates:
                hard_stop()
                print("Robot reached coordinate: ", coordinate)
                turnR(100, 100)
                print("Turned Right")
                stop(1)
                print("Completed Coordinates: ", completed_coordinates)
                follow_line(ir)
                completed_coordinates.add(coordinate)
                # print("Completed coordinates: ", completed_coordinates)
                
            elif coordinate == 12 and coordinate not in completed_coordinates:
                hard_stop()
                print("Robot reached coordinate: ", coordinate)
                turnL(100, 100)
                print("Turned left")
                stop(1)
                print("Completed coordinates: ", completed_coordinates)
                follow_line(ir)
                completed_coordinates.add(coordinate)
            elif coordinate == 13 and coordinate not in completed_coordinates:
                hard_stop()
                print("Robot reached coordinate: ", coordinate)
                turnL(100, 100)
                print("Turned left")
                stop(1)
                print("Completed coordinates: ", completed_coordinates)
                follow_line(ir)
                completed_coordinates.add(coordinate)
            elif coordinate == 16 and coordinate not in completed_coordinates:
                hard_stop()
                print("Robot reached coordinate: ", coordinate)
                print("Robot finished traversal`")
                stop(1)
                print("Completed coordinates: ", completed_coordinates)
                print("Object color is: ", detect_color())
                break
            elif coordinate == 7 and coordinate not in obj_coordinate:
                if dist <= 15 :
                    stop(1)
                    print("Object color is: ", detect_color())
                    arm.servo[1].angle = int(90)
                    sleep(1)
                    arm.servo[0].angle = int(120)
                    sleep(5)
                    arm.servo[0].angle = None
                    arm.servo[1].angle = None
                    break
                else: 
                    follow_line(ir)
            follow_line(ir)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
