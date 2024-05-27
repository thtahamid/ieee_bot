import RPi.GPIO as GPIO
from pynput.keyboard import Key, Listener

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor:
    def __init__(self, Ena, In1, In2, Enb, In3, In4):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        self.Enb = Enb
        self.In3 = In3
        self.In4 = In4
        GPIO.setup(self.Ena, GPIO.OUT)
        GPIO.setup(self.In1, GPIO.OUT)
        GPIO.setup(self.In2, GPIO.OUT)
        GPIO.setup(self.Enb, GPIO.OUT)
        GPIO.setup(self.In3, GPIO.OUT)
        GPIO.setup(self.In4, GPIO.OUT)
        self.pwma = GPIO.PWM(self.Ena, 100)
        self.pwmb = GPIO.PWM(self.Enb, 100)
        self.pwma.start(0)
        self.pwmb.start(0)

    def move_forward(self, speed=100):
        self.pwma.ChangeDutyCycle(speed)
        self.pwmb.ChangeDutyCycle(speed)
        GPIO.output(self.In1, GPIO.HIGH)
        GPIO.output(self.In2, GPIO.LOW)
        GPIO.output(self.In3, GPIO.HIGH)
        GPIO.output(self.In4, GPIO.LOW)

    def move_backward(self, speed=100):
        self.pwma.ChangeDutyCycle(speed)
        self.pwmb.ChangeDutyCycle(speed)
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.HIGH)
        GPIO.output(self.In3, GPIO.LOW)
        GPIO.output(self.In4, GPIO.HIGH)

    def turn_right(self, speed=100):
        self.pwma.ChangeDutyCycle(speed)
        self.pwmb.ChangeDutyCycle(speed * 0.6)
        GPIO.output(self.In1, GPIO.HIGH)
        GPIO.output(self.In2, GPIO.LOW)
        GPIO.output(self.In3, GPIO.LOW)
        GPIO.output(self.In4, GPIO.HIGH)

    def turn_left(self, speed=100):
        self.pwma.ChangeDutyCycle(speed * 0.6)
        self.pwmb.ChangeDutyCycle(speed)
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.HIGH)
        GPIO.output(self.In3, GPIO.HIGH)
        GPIO.output(self.In4, GPIO.LOW)

    def stop(self):
        self.pwma.ChangeDutyCycle(0)
        self.pwmb.ChangeDutyCycle(0)

motor = Motor(21, 16, 20, 1, 7, 8)

def on_press(key):
    if key == Key.up:
        motor.move_forward(100)
    elif key == Key.down:
        motor.move_backward(100)
    elif key == Key.left:
        motor.turn_left(100)
    elif key == Key.right:
        motor.turn_right(100)

def on_release(key):
    motor.stop()
    if key == Key.esc:
        return False  # Stop listener

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
