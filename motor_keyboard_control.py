import RPi.GPIO as GPIO
from time import sleep
import keyboard

# Motor pin definitions
enr, ra, rb, enl, la, lb = 21, 16, 20, 1, 7, 8

# Function to set up the GPIO pins and PWM
def pin_setup():
    global pwmr 
    global pwml
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
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

# Motor control functions
def moveF(r=100, l=100):
    pwmr.ChangeDutyCycle(r)
    pwml.ChangeDutyCycle(l)
    GPIO.output(ra, GPIO.HIGH)
    GPIO.output(rb, GPIO.LOW)
    GPIO.output(la, GPIO.HIGH)
    GPIO.output(lb, GPIO.LOW)

def moveB(r=100, l=100):
    pwmr.ChangeDutyCycle(r)
    pwml.ChangeDutyCycle(l)
    GPIO.output(ra, GPIO.LOW)
    GPIO.output(rb, GPIO.HIGH)
    GPIO.output(la, GPIO.LOW)
    GPIO.output(lb, GPIO.HIGH)

def moveR(r=100, l=100):
    pwmr.ChangeDutyCycle(r)
    pwml.ChangeDutyCycle(l)
    GPIO.output(ra, GPIO.LOW)
    GPIO.output(rb, GPIO.HIGH)
    GPIO.output(la, GPIO.HIGH)
    GPIO.output(lb, GPIO.LOW)

def moveL(r=100, l=100):
    pwmr.ChangeDutyCycle(r)
    pwml.ChangeDutyCycle(l)
    GPIO.output(ra, GPIO.HIGH)
    GPIO.output(rb, GPIO.LOW)
    GPIO.output(la, GPIO.LOW)
    GPIO.output(lb, GPIO.HIGH)

def stop(t=0):
    pwmr.ChangeDutyCycle(0)
    pwml.ChangeDutyCycle(0)
    sleep(t)

# Set up the GPIO pins
pin_setup()

# Function to control the robot with keyboard
def control_robot():
    try:
        print("Press arrow keys to move the robot. Press 'q' to quit.")
        while True:
            if keyboard.is_pressed('up'):
                print("Moving Forward")
                moveF()
            elif keyboard.is_pressed('down'):
                print("Moving Backward")
                moveB()
            elif keyboard.is_pressed('left'):
                print("Turning Left")
                moveL()
            elif keyboard.is_pressed('right'):
                print("Turning Right")
                moveR()
            elif keyboard.is_pressed('q'):
                print("Quitting")
                break
            else:
                stop()
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

# Run the control function
control_robot()
