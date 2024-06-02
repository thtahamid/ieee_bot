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
def hard_stop():
    moveB(20, 20)
    sleep(0.11)
    stop(0.4)

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
        moveF(30, 30)
    elif ir[1] == 0:
        # moveL(70,40)
        moveF(50, 10)
    elif ir[3] == 0:
        # moveR(40,70)
        moveF(10, 50)
    elif ir[1] and ir[2] == 0:
        moveF(40, 15)
    elif ir[2] and ir[3] == 0:
        moveF(15, 40)
    elif ir[0] == 0:
        moveL(90,90)
    elif ir[4] == 0:
        moveR(90,90)

    else:
        moveF(30, 30)

def pick_object():
    arm.servo[0].angle = int(105)
    sleep(0.5)
    arm.servo[1].angle = int(40)
    sleep(0.5)

def drop_object():
    arm.servo[1].angle = int(70)
    sleep(0.4)
    arm.servo[0].angle = int(180)
    sleep(0.3)
    arm.servo[0].angle = None
    arm.servo[1].angle = None

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
                color = "red"
            elif blue_percentage > red_percentage:
                color = "blue"
            else:
                color = "None"
            
            # print(f"Detected color: {color}")
            # Add a small delay to avoid flooding the terminal
            cv2.waitKey(1000)
            return color

            

    except KeyboardInterrupt:
        print("Program interrupted by user")

    finally:
        # Release the capture and close any OpenCV windows
        cap.release()
        cv2.destroyAllWindows()


def blue1():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.2)
            stop(0.2)
            # hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 3 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveL(80,80)
            sleep(0.8)
            stop(0.2)
            drop_object()
            moveB(30,30)
            sleep(0.4)
            turnL(90,90)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 4 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnL(90,100)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 5 and n_coordinate not in g_coordinates:
            
            stop(0.3)
            print("Stopped for a sec")
            print("Turnning left")
            turnL(90,90)
            print("Turned left, back to normal traversal")
            stop(0.5)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue2():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.22)
            stop(0.3)
            # hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 2 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveF(30,30)
            sleep(0.6)
            stop(0.5)
            drop_object()
            moveB(30,30)
            sleep(1.5)
            stop(0.4)
            turnL(100,100)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
    
        elif n_coordinate == 3 and n_coordinate not in g_coordinates:
            stop(1)
            print("Stopped for a sec")
            print("Turnning left")
            turnL(90,90)
            print("Turned left, back to normal traversal")
            stop(0.5)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue3():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.2)
            stop(0.3)
            # hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            
            stop(0.3)
            # hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 3 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveR(80,80)
            sleep(0.8)
            stop(0.3)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            turnR(100,100)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
    
        elif n_coordinate == 4 and n_coordinate not in g_coordinates:
            stop(0.5)
            
            turnR(90,90)
            print("Turned left, back to normal traversal")
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 5 and n_coordinate not in g_coordinates:
            stop(0.5)
            
            turnL(90,90)
            print("Turned left, back to normal traversal")
            stop(0.5)
            g_coordinates.add(n_coordinate)
            break

        follow_line(ir)

def blue4():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.25)
            stop(0.3)
            # hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 2 and n_coordinate not in g_coordinates:  
            stop(0.25)
            turnL(90,90)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 4 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveR(90,90)
            sleep(0.8)
            stop(0.3)
            drop_object()
            moveB(30,30)
            sleep(0.4)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 6 and n_coordinate not in g_coordinates:  
            hard_stop()
            turnR(90,90)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 7 and n_coordinate not in g_coordinates:
            stop(0.25)
        
            turnL(90,90)
            print("Turned left, back to normal traversal")
            stop(0.5)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue5():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    turnR(90,90)
    stop(0.3)
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            
            # moveF(25,25)
            # sleep(0.22)
            # stop(0.3)
            hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        
        elif n_coordinate == 4 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveR(90,90)
            sleep(0.8)
            stop(0.3)
            drop_object()
            moveB(30,30)
            sleep(0.4)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 6 and n_coordinate not in g_coordinates:  
            hard_stop()
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 7 and n_coordinate not in g_coordinates:
            stop(0.2)
            
            # stop(0.5)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue6():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.3)
            stop(0.2)
            turnR(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate  ==  3 and n_coordinate not in g_coordinates:
            hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        
        elif n_coordinate == 4 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveR(80,80)
            sleep(0.7)
            stop(0.3)
            drop_object()
            moveB(30,30)
            sleep(0.15)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 5 and n_coordinate not in g_coordinates:  
            hard_stop()
            turnR(90,90)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 7 and n_coordinate not in g_coordinates:
            stop(0.5)
            print("Stopped for a sec")
            print("Turnning left")
            turnR(90,90)
            print("Turned left, back to normal traversal")
            stop(0.3)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue7():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.22)
            stop(0.3)
            # hard_stop()
            turnR(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 3 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveF(30,30)
            sleep(0.6)
            stop(0.5)
            drop_object()
            moveB(30,30)
            sleep(1)
            turnL(100,100)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
    
        elif n_coordinate == 5 and n_coordinate not in g_coordinates:
            stop(1)
            print("Stopped for a sec")
            print("Turnning left")
            turnR(90,90)
            print("Turned left, back to normal traversal")
            stop(0.5)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue8():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.2)
            stop(0.3)
            # hard_stop()
            turnR(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  3 and n_coordinate not in g_coordinates:
            hard_stop()
            turnL(90,90)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 4 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveR(80,80)
            sleep(0.5)
            stop(0.2)
            drop_object()
            moveB(30,30)
            sleep(0.4)
            turnR(90,90)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 5 and n_coordinate not in g_coordinates:
            hard_stop()
            turnL(90,100)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 7 and n_coordinate not in g_coordinates:
            stop()
            stop(0.1)
            print("Stopped for a sec")
            print("Turnning left")
            # turnL(90,90)
            print("Turned left, back to normal traversal")
            # stop(0.5)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue9():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    turnL(90,90)
    stop(0.3)
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        

        if n_coordinate  ==  3 and n_coordinate not in g_coordinates:
            hard_stop()
            turnR(90,90)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 4 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveL(80,80)
            sleep(0.5)
            stop(0.2)
            drop_object()
            moveB(30,30)
            sleep(0.4)
            turnL(90,90)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 5 and n_coordinate not in g_coordinates:
            hard_stop()
            turnL(90,100)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 7 and n_coordinate not in g_coordinates:
            stop()
            stop(0.3)
            print("Stopped for a sec")
            print("Turnning left")
            
            print("Turned left, back to normal traversal")
            stop(0.3)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue10():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.22)
            stop(0.3)
            # hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 4 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveF(30,30)
            sleep(0.6)
            stop(0.5)
            drop_object()
            moveB(30,30)
            sleep(1)
            turnL(100,100)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
    
        elif n_coordinate == 7 and n_coordinate not in g_coordinates:
            stop(1)
            print("Stopped for a sec")
            print("Turnning left")
            turnL(90,90)
            print("Turned left, back to normal traversal")
            stop(0.5)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue11():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    turnL(90,90)
    stop(0.3)
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.22)
            stop(0.3)
            # hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 4 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveF(30,30)
            sleep(0.6)
            stop(0.5)
            drop_object()
            moveB(30,30)
            sleep(1)
            turnL(100,100)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
    
        elif n_coordinate == 7 and n_coordinate not in g_coordinates:
            stop(1)
            print("Stopped for a sec")
            print("Turnning left")
            turnL(90,90)
            print("Turned left, back to normal traversal")
            stop(0.5)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue12():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.18)
            stop(0.3)
            # hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate  ==  4 and n_coordinate not in g_coordinates:
            
            stop(0.3)
            # hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 6 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveR(80,80)
            sleep(0.8)
            stop(0.3)
            drop_object()
            # moveB(30,30)
            # sleep(1)
            turnR(100,100)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
    
        elif n_coordinate == 8 and n_coordinate not in g_coordinates:
            stop(0.5)
            
            print("Turnning left")
            turnR(90,90)
            
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 11 and n_coordinate not in g_coordinates:
            stop(0.5)
            
            g_coordinates.add(n_coordinate)  
            break  
        


        follow_line(ir)

def blue13():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    turnR(90,90)
    stop(0.3)
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  4 and n_coordinate not in g_coordinates:
            
            # moveF(25,25)
            # sleep(0.22)
            # stop(0.3)
            hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        
        elif n_coordinate == 6 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveR(80,80)
            sleep(0.7)
            stop(0.3)
            drop_object()
            moveB(30,30)
            sleep(0.4)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 8 and n_coordinate not in g_coordinates:  
            hard_stop()
            turnR(90,90)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 11 and n_coordinate not in g_coordinates:
            stop(0.5)
            print("Stopped for a sec")
            print("Turnning left")
            # turnL(90,90)
            print("Turned left, back to normal traversal")
            # stop(0.5)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue14():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.3)
            stop(0.3)
            turnR(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate  ==  5 and n_coordinate not in g_coordinates:
            hard_stop()
            turnL(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        
        elif n_coordinate == 6 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveR(80,80)
            sleep(0.7)
            stop(0.3)
            drop_object()
            moveB(30,30)
            sleep(0.15)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 7 and n_coordinate not in g_coordinates:  
            hard_stop()
            turnR(90,90)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 11 and n_coordinate not in g_coordinates:
            stop(0.5)
            print("Stopped for a sec")
            print("Turnning left")
            turnR(90,90)
            print("Turned left, back to normal traversal")
            stop(0.3)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue15():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.22)
            stop(0.3)
            # hard_stop()
            turnR(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 5 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveF(30,30)
            sleep(0.6)
            stop(0.5)
            drop_object()
            moveB(30,30)
            sleep(1)
            turnL(100,100)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
    
        elif n_coordinate == 9 and n_coordinate not in g_coordinates:
            stop(1)
            print("Stopped for a sec")
            print("Turnning left")
            turnR(90,90)
            print("Turned left, back to normal traversal")
            stop(0.5)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)

def blue16():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.2)
            stop(0.2)
            # hard_stop()
            turnR(90,90)
            # moveL(90,90)
            # sleep(0.8)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  5 and n_coordinate not in g_coordinates:
            hard_stop()
            turnR(90,90)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 6 and n_coordinate not in g_coordinates:  
            hard_stop()
            moveL(80,80)
            sleep(0.8)
            stop(0.2)
            drop_object()
            moveB(30,30)
            sleep(0.4)
            turnL(90,90)
            stop(0.5)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        
        elif n_coordinate == 8 and n_coordinate not in g_coordinates:
            stop()
            stop(100)
            print("Stopped for a sec")
            print("Turnning left")
            # turnL(90,90)
            print("Turned left, back to normal traversal")
            # stop(0.5)
            g_coordinates.add(n_coordinate)
            break


        follow_line(ir)


def red1():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    turnR(100,100)
    stop(0.3)
    while True:
        ir = read_sensor_values()
        

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
                    
                    
                    # stop(0.5)
        

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  5 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 7 and n_coordinate not in g_coordinates:
            hard_stop()
            moveR(90,90)
            sleep(0.6)
            stop(0.3)
            moveF(30,30)
            sleep(0.3)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnR(90,90)
            stop(0.2)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 9 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 13 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
            break

        follow_line(ir)

def red2():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    turnR(90,90)
    stop(0.3)
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
                    
                    
                    # stop(0.5)
        

        else:
            at_intersection = False
        if n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  6 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 8 and n_coordinate not in g_coordinates:
            hard_stop()
            moveR(90,90)
            sleep(0.3)
            moveF(30,30)
            sleep(0.3)
            stop(0.2)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnR(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 10 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 14 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 15 and n_coordinate not in g_coordinates:
            stop(0.1)
            
            g_coordinates.add(n_coordinate)
            break

        follow_line(ir)

def red3():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    turnR(90,90)
    stop(0.3)
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
                    
                    
                    # stop(0.5)
        

        else:
            at_intersection = False
        if n_coordinate  ==  3 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  7 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 9 and n_coordinate not in g_coordinates:
            hard_stop()
            moveR(90,90)
            sleep(0.2)
            moveF(30,30)
            sleep(0.3)
            stop(0.2)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnR(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 11 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 15 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 17 and n_coordinate not in g_coordinates:
            stop(0.1)
            
            g_coordinates.add(n_coordinate)
            break
            
        follow_line(ir)

def red4():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
                    
                    
                    # stop(0.5)
        

        else:
            at_intersection = False
        if n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  6 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 9 and n_coordinate not in g_coordinates:
            hard_stop()
            moveL(80,80)
            sleep(0.8)
            stop(0.3)
            moveF(30,30)
            sleep(0.3)
            stop(0.1)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnL(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 12 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 16 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.2)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 17 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.2)
            g_coordinates.add(n_coordinate)
            break
            
        follow_line(ir)

def red5():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
                    
                    
                    # stop(0.5)
        

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            moveF(25,25)
            sleep(0.25)
            stop(0.1)
            turnL(90,90)
            stop(0.25)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate  ==  5 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 8 and n_coordinate not in g_coordinates:
            hard_stop()
            moveL(80,80)
            sleep(0.8)
            stop(0.1)
            moveF(30,30)
            sleep(0.3)
            stop(0.2)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnL(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 11 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 14 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 15 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnL(90,90)
            stop(0.1)
            g_coordinates.add(n_coordinate)
            break
            


        follow_line(ir)

def red6():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    turnL(90,90)
    stop(0.3)
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  5 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 8 and n_coordinate not in g_coordinates:
            hard_stop()
            moveL(80,80)
            sleep(0.8)
            stop(0.2)
            moveF(30,30)
            sleep(0.3)
            stop(0.2)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnL(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 11 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 14 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        
        elif n_coordinate == 16 and n_coordinate not in g_coordinates:
            stop(0.1)
            g_coordinates.add(n_coordinate)
            break

        follow_line(ir)

def red7():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    turnL(90,90)
    stop(0.2)
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
                    
                    
                    # stop(0.5)
        

        else:
            at_intersection = False
        if n_coordinate  == 3  and n_coordinate not in g_coordinates:
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  6 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 9 and n_coordinate not in g_coordinates:
            hard_stop()
            moveL(80,80)
            sleep(0.8)
            stop(0.1)
            moveF(30,30)
            sleep(0.3)
            stop(0.2)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnL(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 12 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 15 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        
        elif n_coordinate == 17 and n_coordinate not in g_coordinates:
            stop(0.1)
            g_coordinates.add(n_coordinate)
            break
        
        follow_line(ir)

def red8():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
        else:
            at_intersection = False
        if n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  5 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 7 and n_coordinate not in g_coordinates:
            hard_stop()
            moveR(80,80)
            sleep(0.8)
            stop(0.1)
            moveF(30,30)
            sleep(0.3)
            stop(0.2)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnR(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 9 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 12 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        
        elif n_coordinate == 13 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            break
        
        follow_line(ir)

def red9():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
                    
                    
                    # stop(0.5)
        

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate  ==  4 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)


        elif n_coordinate == 6 and n_coordinate not in g_coordinates:
            hard_stop()
            moveR(80,80)
            sleep(0.8)
            stop(0.1)
            moveF(30,30)
            sleep(0.3)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnR(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 8 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 10 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        
        elif n_coordinate == 11 and n_coordinate not in g_coordinates:
            stop(0.1)
            g_coordinates.add(n_coordinate)
            break
        
        follow_line(ir)

def red10():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    turnR(90,90)
    stop(0.3)
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
                    
                    
                    # stop(0.5)
        

        else:
            at_intersection = False
        if n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  4 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)


        elif n_coordinate == 6 and n_coordinate not in g_coordinates:
            hard_stop()
            moveR(80,80)
            sleep(0.8)
            stop(0.1)
            moveF(30,30)
            sleep(0.3)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnR(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 8 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 10 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        
        elif n_coordinate == 11 and n_coordinate not in g_coordinates:
            stop(0.1)
            g_coordinates.add(n_coordinate)
            break
        
        follow_line(ir)

def red11():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    turnR(90,90)
    stop(0.3)
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
                    
                    
                    # stop(0.5)
        

        else:
            at_intersection = False
        if n_coordinate  ==  3 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  5 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)


        elif n_coordinate == 7 and n_coordinate not in g_coordinates:
            hard_stop()
            moveR(80,80)
            sleep(0.8)
            stop(0.1)
            moveF(30,30)
            sleep(0.3)
            stop(0.2)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnR(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 9 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 11 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        
        elif n_coordinate == 13 and n_coordinate not in g_coordinates:
            stop(0.1)
            g_coordinates.add(n_coordinate)
            break
        
        follow_line(ir)

def red12():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
                    
                    
                    # stop(0.5)
        

        else:
            at_intersection = False
        if n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  4 and n_coordinate not in g_coordinates:
            hard_stop()
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 7 and n_coordinate not in g_coordinates:
            hard_stop()
            moveL(80,80)
            sleep(0.8)
            stop(0.1)
            moveF(30,30)
            sleep(0.3)
            stop(0.1)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnL(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 10 and n_coordinate not in g_coordinates:
            hard_stop()
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 12 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
        elif n_coordinate == 13 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            break
            


        follow_line(ir)

def red13():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        

        elif n_coordinate == 4 and n_coordinate not in g_coordinates:
            hard_stop()
            moveL(80,80)
            sleep(0.8)
            stop(0.1)
            moveF(30,30)
            sleep(0.3)
            stop(0.1)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnL(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 6 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        
        elif n_coordinate == 7 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.2)
            g_coordinates.add(n_coordinate)
            break
        follow_line(ir)

def red14():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)

        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        if n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 3 and n_coordinate not in g_coordinates:
            hard_stop()
            moveL(80,80)
            sleep(0.8)
            stop(0.1)
            moveF(30,30)
            sleep(0.3)
            stop(0.1)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnL(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 4 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
 
        elif n_coordinate == 5 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            break

def red15():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 2 and n_coordinate not in g_coordinates:
            hard_stop()
            moveF(30,30)
            sleep(0.3)
            stop(0.1)
            drop_object()
            moveB(30,30)
            sleep(0.5)
            stop(0.1)
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)
  
        elif n_coordinate == 3 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.2)
            g_coordinates.add(n_coordinate)
            break

def red16():
    n_coordinate = 0
    at_intersection = False
    g_coordinates = set()
    
    while True:
        ir = read_sensor_values()

        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
                if not at_intersection:
                    
                    n_coordinate += 1
                    at_intersection = True
                    
                    print("n_coordinate: ", n_coordinate)
                    print("g_coordinate: ", g_coordinates)
                    
                    
                    # stop(0.5)
        
        else:
            at_intersection = False
        if n_coordinate  ==  1 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate  ==  2 and n_coordinate not in g_coordinates:
            # hard_stop()
            stop(0.2)
            turnL(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 3 and n_coordinate not in g_coordinates:
            hard_stop()
            moveR(90,90)
            sleep(0.8)
            moveF(30,30)
            sleep(0.3)
            stop(0.1)
            drop_object()
            moveB(30,30)
            sleep(0.3)
            stop(0.2)
            turnR(90,90)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 5 and n_coordinate not in g_coordinates:
            hard_stop()
            turnR(90,90)
            stop(0.3)
            g_coordinates.add(n_coordinate)
            follow_line(ir)

        elif n_coordinate == 10 and n_coordinate not in g_coordinates:
            stop(100)
            
            g_coordinates.add(n_coordinate)
            
            break

        follow_line(ir)

def traverse_map():
    coordinate = 0
    at_intersection = False
    completed_coordinates = set()
    free_coordinates = set()
    obj_coordinate = set()
    finished_drop = set()
    while True:
        dist = measure_distance()
        ir = read_sensor_values()
        
        # obj_color = detect_color()
        print('\t'.join(map(str, ir)), f"D: {dist:.2f} cm\tCor: {coordinate}", sep='\t')
        
        time.sleep(0.02)

        # Mark each coordinate in the variable coordinate
        if (ir[1] ==0  and ir[2] == 0 and ir[3] == 0) or (ir[0] == 0 and ir[1] == 0 and ir[2] == 0) or (ir[2] == 0 and ir[3] == 0 and ir[4] == 0):
            if not at_intersection:
                
                coordinate += 1
                at_intersection = True
                free_coordinates.add(coordinate)
                print("Coordinate: ", coordinate)
                
                print("Free coordinates: ", free_coordinates)
                
                # stop(0.5)
                
        else:
            at_intersection = False
        
        # AT coordinate 1 turn left to traverse
        if coordinate == 1 and coordinate not in completed_coordinates:
            stop(0.2)
            print("Robot reached coordinate: ", coordinate)
            turnL(90, 90)
            print("Turned left")
            stop(0.3)
            print("Completed Coordinates: ", completed_coordinates)
            
                    

            follow_line(ir)
            
            completed_coordinates.add(coordinate)
        
        # At coordinate 5 turn right finish first column 
        elif coordinate == 5 and coordinate not in completed_coordinates:
            stop(0.2)
            print("Robot reached coordinate: ", coordinate)
            turnR(90, 90)
            print("Turned Right")
            stop(0.3)
            print("Completed Coordinates: ", completed_coordinates)
            follow_line(ir)
            completed_coordinates.add(coordinate)
        
        # At coordinate 6 turn right to start second column
        elif coordinate == 6 and coordinate not in completed_coordinates:
            stop(0.2)
            print("Robot reached coordinate: ", coordinate)
            turnR(100, 100)
            print("Turned right")
            stop(0.3)
            print("Completed Coordinates: ", completed_coordinates)
            follow_line(ir)
            completed_coordinates.add(coordinate)

        # At coordinate 9 turn left to finish column 2
        elif coordinate == 9 and coordinate not in completed_coordinates:
            stop(0.2)
            print("Robot reached coordinate: ", coordinate)
            turnL(100, 100)
            print("Turned left")
            stop(0.3)
            print("Completed Coordinates: ", completed_coordinates)
            follow_line(ir)
            completed_coordinates.add(coordinate)
        
        # At coordinate 10 turn left to start 3rd
        elif coordinate == 10 and coordinate not in completed_coordinates:
            stop(0.2)
            print("Robot reached coordinate: ", coordinate)
            turnL(100, 100)
            print("Turned left")
            stop(0.3)
            print("Completed Coordinates: ", completed_coordinates)
            follow_line(ir)
            completed_coordinates.add(coordinate)
            # print("Completed coordinates: ", completed_coordinates)

        # At coordinate 13 turn right to finish column    
        elif coordinate == 13 and coordinate not in completed_coordinates:
            stop(0.2)
            print("Robot reached coordinate: ", coordinate)
            turnR(100, 100)
            print("Turned Right")
            stop(0.3)
            print("Completed coordinates: ", completed_coordinates)
            follow_line(ir)
            completed_coordinates.add(coordinate)
        
        # At coordinate 14 turn right to start last column
        elif coordinate == 14 and coordinate not in completed_coordinates:
            stop(0.2)
            print("Robot reached coordinate: ", coordinate)
            turnR(100, 100)
            print("Turned right")
            stop(0.3)
            print("Completed coordinates: ", completed_coordinates)
            follow_line(ir)
            completed_coordinates.add(coordinate)

        # At the end of last column FInished traversal
        elif coordinate == 17 and coordinate not in completed_coordinates:
            hard_stop()
            print("Robot reached coordinate: ", coordinate)
            print("Robot finished traversal`")
            stop(1)
            print("Completed coordinates: ", completed_coordinates)
            print("Object color is: ", detect_color())
            break
        
        if dist < 10.5:
                hard_stop()
                detect_color()
                sleep(2)
                obj_color = detect_color()
                print("Object color: ", obj_color)
                stop(0.1)
                pick_object()
                
                if obj_color == 'red' :
                    if coordinate == 1 and coordinate not in finished_drop:
                        finished_drop.add(coordinate)
                        red1()
                    elif coordinate == 2 and coordinate not in finished_drop:
                        finished_drop.add(coordinate)
                        red2()
                    elif coordinate == 3 and coordinate not in finished_drop:
                        finished_drop.add(coordinate)
                        red3()
                    elif coordinate == 4 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        red4()
                    elif coordinate == 5 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        red5()
                    elif coordinate == 6 and coordinate not in finished_drop:
                        finished_drop.add(coordinate)
                        red6()
                    elif coordinate == 7 and coordinate not in finished_drop:
                        finished_drop.add(coordinate)
                        red7()
                    elif coordinate == 8 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        red8()
                    elif coordinate == 9 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        red9()
                    elif coordinate == 10 and coordinate not in finished_drop:
                        finished_drop.add(coordinate)
                        red10()
                    elif coordinate == 10 and coordinate not in finished_drop:
                        finished_drop.add(coordinate)
                        red10()
                    elif coordinate == 11 and coordinate not in finished_drop:
                        finished_drop.add(coordinate)
                        red11()
                    elif coordinate == 12 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        red12()
                    elif coordinate == 13 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        red13()
                    elif coordinate == 14 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        red14()
                    elif coordinate == 15 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        red15()
                    elif coordinate == 16 and coordinate not in finished_drop:
                        
                        finished_drop.add(coordinate)
                        red16()
                    
                    
                else: 
                    if coordinate == 1 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        blue1()
                    elif coordinate == 2 and coordinate not in finished_drop:
                        finished_drop.add(coordinate)
                        blue2()
                    elif coordinate == 3 and coordinate not in finished_drop:
                        coordinate +=1
                        finished_drop.add(coordinate)

                        blue3()
                    elif coordinate == 4 and coordinate not in finished_drop:
                        finished_drop.add(coordinate)
                        blue4()
                    elif coordinate == 5 and coordinate not in finished_drop:
                        finished_drop.add(coordinate)
                        blue5()
                    elif coordinate == 6 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        blue6()
                    elif coordinate == 7 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        blue7()
                    elif coordinate == 8 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        blue8()
                    elif coordinate == 9 and coordinate not in finished_drop:
                        
                        finished_drop.add(coordinate)
                        blue9()
                    elif coordinate == 10 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        blue10()
                    elif coordinate == 11 and coordinate not in finished_drop:
                        
                        finished_drop.add(coordinate)
                        blue11()
                    elif coordinate == 12 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        blue12()
                    elif coordinate == 13 and coordinate not in finished_drop:
                        
                        finished_drop.add(coordinate)
                        blue13()
                    elif coordinate == 14 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        blue14()
                    elif coordinate == 15 and coordinate not in finished_drop:
                        coordinate += 1
                        finished_drop.add(coordinate)
                        blue15()
        

           
        follow_line(ir)



def main():
    try:
        t_start = time.time()
        pin_setup()
        arm.servo[1].angle = int(70)
        sleep(1)
        arm.servo[0].angle = int(180)
        sleep(1.5)
        arm.servo[0].angle = None
        arm.servo[1].angle = None
        traverse_map()
        t_end = time.time()
        print("Total time:", t_end - t_start)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
