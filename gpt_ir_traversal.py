import RPi.GPIO as GPIO
import time

# Define GPIO pins for IR sensors
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

def read_sensors():
    return [GPIO.input(pin) for pin in sensor_pins]

class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.grid_size = 4
        pin_setup()

    def move_forward(self):
        moveF(50, 50)
        time.sleep(1)  # Adjust timing as needed
        stop()
        self.y += 1

    def move_backward(self):
        moveB(50, 50)
        time.sleep(1)  # Adjust timing as needed
        stop()
        self.y -= 1

    def move_right(self):
        moveR(50, 50)
        time.sleep(1)  # Adjust timing as needed
        stop()
        self.x += 1

    def move_left(self):
        moveL(50, 50)
        time.sleep(1)  # Adjust timing as needed
        stop()
        self.x -= 1

    def follow_line(self):
        while True:
            sensor_values = read_sensors()
            # Simple line following logic based on sensor input
            if sensor_values == [1, 1, 0, 1, 1]:  # On track
                moveF(50, 50)
            elif sensor_values == [1, 0, 0, 1, 1]:  # Slightly left
                moveR(50, 50)
            elif sensor_values == [1, 1, 0, 0, 1]:  # Slightly right
                moveL(50, 50)
            elif sensor_values == [0, 0, 0, 1, 1]:  # Hard left
                moveR(100, 50)
            elif sensor_values == [1, 1, 0, 0, 0]:  # Hard right
                moveL(50, 100)
            else:
                stop()
            time.sleep(0.1)  # Small delay to avoid flooding the GPIO

    def traverse_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                print(f"Position ({self.x},{self.y})")
                if j < self.grid_size - 1:
                    self.move_right()
                    self.follow_line()
            if i < self.grid_size - 1:
                self.move_forward()
                self.follow_line()
                if i % 2 == 0:
                    self.move_left()
                    self.follow_line()
                else:
                    self.move_right()
                    self.follow_line()

if __name__ == "__main__":
    robot = Robot()
    robot.traverse_grid()
