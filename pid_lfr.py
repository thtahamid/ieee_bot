import RPi.GPIO as GPIO
from time import sleep

# Define GPIO pins for IR sensors
IR_pins = [5, 6, 13, 19, 26]

# Initialize GPIO
def init_GPIO():
    GPIO.setmode(GPIO.BCM)
    for pin in IR_pins:
        GPIO.setup(pin, GPIO.IN)

# Read sensor values
def read_sensors():
    return [GPIO.input(pin) for pin in IR_pins]

# PID control function
def pid_control(error):
    # Placeholder for PID control
    return 0

# Control motors based on PID output
def control_motors(pid_output, motors):
    if pid_output > 0:
        # Move right
        motors.moveR(pid_output)
    elif pid_output < 0:
        # Move left
        motors.moveL(-pid_output)
    else:
        # Move forward
        motors.moveF()

# Main function
def main():
    try:
        init_GPIO()
        
        # Initialize motors
        motors = motor(21, 16, 20, 1, 7, 8)

        while True:
            # Read sensor values
            sensor_values = read_sensors()

            # Calculate error (distance from the line's center)
            error = sensor_values[2] - 0.5

            # Perform PID control
            pid_output = pid_control(error)

            # Control motors based on PID output
            control_motors(pid_output, motors)

            # Delay for stability
            sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()

# Define motor class
class motor():
    def __init__(self, Ena, In1, In2, Enb, In3, In4):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        self.Enb = Enb
        self.In3 = In3
        self.In4 = In4
        GPIO.setup([Ena, In1, In2, Enb, In3, In4], GPIO.OUT)
        self.pwma = GPIO.PWM(Ena, 30)
        self.pwmb = GPIO.PWM(Enb, 30)
        self.pwma.start(0)
        self.pwmb.start(0)

    def moveF(self, x=30, t=0):
        self.pwma.ChangeDutyCycle(x)
        self.pwmb.ChangeDutyCycle(x)
        GPIO.output(self.In1, GPIO.HIGH)
        GPIO.output(self.In2, GPIO.LOW)
        GPIO.output(self.In3, GPIO.HIGH)
        GPIO.output(self.In4, GPIO.LOW)
        sleep(t)

    def moveB(self, x=30, t=0):
        self.pwma.ChangeDutyCycle(x)
        self.pwmb.ChangeDutyCycle(x)
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.HIGH)
        GPIO.output(self.In3, GPIO.LOW)
        GPIO.output(self.In4, GPIO.HIGH)
        sleep(t)

    def moveR(self, x=100, t=0):
        self.pwma.ChangeDutyCycle(x)
        self.pwmb.ChangeDutyCycle(x - (50 * 0.4))
        GPIO.output(self.In1, GPIO.HIGH)
        GPIO.output(self.In2, GPIO.LOW)
        GPIO.output(self.In3, GPIO.LOW)
        GPIO.output(self.In4, GPIO.HIGH)
        sleep(t)

    def moveL(self, x=100, t=0):
        self.pwma.ChangeDutyCycle(x - (50 * 0.4))
        self.pwmb.ChangeDutyCycle(x)
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.HIGH)
        GPIO.output(self.In3, GPIO.HIGH)
        GPIO.output(self.In4, GPIO.LOW)
        sleep(t)

    def stop(self, t=0):
        self.pwma.ChangeDutyCycle(0)
        self.pwmb.ChangeDutyCycle(0)
        sleep(t)

if __name__ == "__main__":
    main()
