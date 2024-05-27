import cv2
import numpy as np
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
import time

# Initialize Adafruit ServoKit for arm control
arm = ServoKit(channels=16)  # all 16 channels in use
servo = 3  # first 3 channels in use

# Define GPIO pins for ultrasonic
GPIO_TRIGGER = 24
GPIO_ECHO = 23

# GPIO pins for IR sensors
sensor_pins = [5, 6, 13, 19, 26]
# GPIO pins for motors
enr, ra, rb, enl, la, lb = 21, 16, 20, 1, 7, 8

# Pin setup
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

    # Speed for left and right motor
    pwmr = GPIO.PWM(enr, 100)
    pwml = GPIO.PWM(enl, 100)

    pwmr.start(0)
    pwml.start(0)

    # Set up the GPIO pins for ultrasonic
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

def moveL(r=0, l=0):
    pwmr.ChangeDutyCycle(r)
    pwml.ChangeDutyCycle(l)
    GPIO.output(ra, GPIO.HIGH)
    GPIO.output(rb, GPIO.LOW)
    GPIO.output(la, GPIO.LOW)
    GPIO.output(lb, GPIO.HIGH)

def stop(t=10):
    pwmr.ChangeDutyCycle(0)
    pwml.ChangeDutyCycle(0)
    time.sleep(t)

# Color detection
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
            
            print(f"Detected color: {color}")
            return color

            # Add a small delay to avoid flooding the terminal
            cv2.waitKey(1000)

    except KeyboardInterrupt:
        print("Program interrupted by user")

    finally:
        # Release the capture and close any OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

# Coordinate system
class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.grid_size = 5
        self.grid = [['' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        pin_setup()

    def move_to(self, direction):
        if direction == "forward":
            moveF(50, 50)
        elif direction == "backward":
            moveB(50, 50)
        elif direction == "right":
            moveR(50, 50)
        elif direction == "left":
            moveL(50, 50)
        time.sleep(1)
        stop()

    def update_position(self, direction):
        if direction == "forward":
            self.y += 1
        elif direction == "backward":
            self.y -= 1
        elif direction == "right":
            self.x += 1
        elif direction == "left":
            self.x -= 1

    def traverse_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = detect_color()
                self.grid[i][j] = color
                print(f"Position ({i},{j}): Detected {color}")
                if j < self.grid_size - 1:
                    self.move_to("right")
                    self.update_position("right")
            if i < self.grid_size - 1:
                self.move_to("forward")
                self.update_position("forward")
                self.move_to("left" if i % 2 == 0 else "right")
                self.update_position("left" if i % 2 == 0 else "right")

if __name__ == "__main__":
    robot = Robot()
    robot.traverse_grid()
