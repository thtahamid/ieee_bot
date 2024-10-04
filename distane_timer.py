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

# Function to measure time elapsed (start/stop stopwatch)
def measure_time():
    return time.time()

# Function to measure distance
def measure_distance():
    # Send a 10us pulse to trigger the measurement
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Measure the time it takes for the echo to return
    start_time = measure_time()
    stop_time = measure_time()

    while GPIO.input(GPIO_ECHO) == 0:
        start_time = measure_time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = measure_time()

    # Calculate the time difference
    time_elapsed = stop_time - start_time
    # Sound speed in air (34300 cm/s)
    distance = (time_elapsed * 34300) / 2

    return distance, time_elapsed

try:
    while True:
        dist, elapsed_time = measure_distance()
        # Print both distance and time elapsed for measurement
        print(f"Distance: {dist:.2f} cm, Elapsed time: {elapsed_time:.6f} seconds")
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
