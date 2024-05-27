import RPi.GPIO as GPIO
import time
from time import sleep

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

    # speed for left and right motor
    pwmr = GPIO.PWM(enr, 100)
    pwml = GPIO.PWM(enl, 100)

    pwmr.start(0)
    pwml.start(0)

    
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
    sleep(t)

def read_sensor_values():
    sensor_values = []
    for pin in sensor_pins:
        sensor_values.append(GPIO.input(pin))
    return sensor_values

def print_sensor_values(sensor_values):
    print('\t'.join(map(str, sensor_values)))

# PID Controller for line following
def pid_line_follower(kp, ki, kd, base_speed):
    previous_error = 0
    integral = 0

    while True:
        # Read the sensor values
        sensor_values = read_sensor_values()

        # Calculate the error
        if sensor_values[1] == 1 and sensor_values[2] == 0 and sensor_values[3] == 1:
            error = 0  # on the line
        elif sensor_values[1] == 0:
            error = 1  # right of the line
        elif sensor_values[3] == 0:
            error = -1  # left of the line
            
        elif sensor_values[1] == 0 and sensor_values[2] == 0:
            error = 0.5  # slightly right
        elif sensor_values[2] == 0 and sensor_values[3] == 0:
            error = -0.5  # slightly left
            
        else:
            error = previous_error  # no line detected, use previous error

        # PID calculations
        integral += error
        derivative = error - previous_error
        correction = kp * error + ki * integral + kd * derivative

        # Adjust motor speeds
        left_speed = base_speed - correction
        right_speed = base_speed + correction

        # Ensure the speeds are within bounds
        left_speed = max(0, min(100, left_speed))
        right_speed = max(0, min(100, right_speed))

        # Move the robot
        moveF(right_speed, left_speed)

        # Update previous error
        previous_error = error

        # Print sensor values for debugging
        print_sensor_values(sensor_values)

        # Short delay
        time.sleep(0.1)


pin_setup()
pid_line_follower(kp=0.1, ki=0.01, kd=0.005, base_speed=50)
