import RPi.GPIO as GPIO
import time

# GPIO pins for IR sensors
sensor_pins = [5, 6, 13, 19, 26]

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in sensor_pins:
        GPIO.setup(pin, GPIO.IN)

def read_sensor_values():
    sensor_values = []
    for pin in sensor_pins:
        sensor_values.append(GPIO.input(pin))
    return sensor_values

def print_sensor_values(sensor_values):
    print('\t'.join(map(str, sensor_values)))

def main():
    try:
        setup()
        print("Reading IR sensor values...")
        while True:
            sensor_values = read_sensor_values()
            print_sensor_values(sensor_values)
            time.sleep(0.05)  # Adjust delay as needed
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
