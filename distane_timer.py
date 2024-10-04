import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
GPIO_TRIGGER = 24
GPIO_ECHO = 23

# Set up the GPIO pins
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Function to start the stopwatch and return elapsed time
def stopwatch(start_time):
    return time.time() - start_time

# Function to measure distance
def measure_distance():
    # Send a 10us pulse to trigger the measurement
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Measure the time it takes for the echo to return
    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Calculate the time difference
    time_elapsed = stop_time - start_time
    # Sound speed in air (34300 cm/s)
    distance = (time_elapsed * 34300) / 2

    return distance

try:
    # Start the stopwatch
    stopwatch_start = time.time()

    while True:
        # Measure the distance
        dist = measure_distance()

        # Calculate the elapsed time from the stopwatch start
        elapsed_time = stopwatch(stopwatch_start)

        # Print the distance along with the stopwatch time
        print(f"Distance: {dist:.2f} cm, Stopwatch: {elapsed_time:.2f} seconds")

        # Wait for 50ms before the next measurement
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
