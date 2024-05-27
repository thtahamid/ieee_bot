from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
import time
from time import sleep


# Adafruit servokit for arm control
arm=ServoKit (channels=16) # all 16 channel in use
servo=3 # first 3 channel in user


# Define GPIO pins for ultrasonic
GPIO_TRIGGER = 24
GPIO_ECHO = 23



# GPIO pins for IR sensors
sensor_pins = [5, 6, 13, 19, 26]
# GPIO pins for motors
enr,ra,rb,enl,la,lb = 21,16,20, 1,7,8


def pin_setup():
    global pwmr 
    global pwml
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in sensor_pins:
        GPIO.setup(pin, GPIO.IN)

    GPIO.setup(enr,GPIO.OUT)
    GPIO.setup(ra,GPIO.OUT)
    GPIO.setup(rb,GPIO.OUT)
    GPIO.setup(enl,GPIO.OUT)
    GPIO.setup(la,GPIO.OUT)
    GPIO.setup(lb,GPIO.OUT)

    # speed for left and right motor
    pwmr = GPIO.PWM(enr, 100)
    pwml = GPIO.PWM(enl, 100)

    pwmr.start(0)
    pwml.start(0)


    # Set up the GPIO pins for ultrasonic
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)





def moveF( r=0, l=0):
        pwmr.ChangeDutyCycle(r)
        pwml.ChangeDutyCycle(l)
        GPIO.output(ra,GPIO.HIGH)
        GPIO.output(rb,GPIO.LOW)
        GPIO.output(la,GPIO.HIGH)
        GPIO.output(lb,GPIO.LOW)

def moveB(r=0, l=0):
        pwmr.ChangeDutyCycle(r)
        pwml.ChangeDutyCycle(l)
        GPIO.output(ra,GPIO.LOW)
        GPIO.output(rb,GPIO.HIGH)
        GPIO.output(la,GPIO.LOW)
        GPIO.output(lb,GPIO.HIGH)

def moveR(r=0, l=0):
        pwmr.ChangeDutyCycle(r)
        pwml.ChangeDutyCycle(l)
        GPIO.output(ra,GPIO.LOW)
        GPIO.output(rb,GPIO.HIGH)
        GPIO.output(la,GPIO.HIGH)
        GPIO.output(lb,GPIO.LOW)

def moveL(r=0, l=0):
        pwmr.ChangeDutyCycle(r)
        pwml.ChangeDutyCycle(l)
        GPIO.output(ra,GPIO.HIGH)
        GPIO.output(rb,GPIO.LOW)
        GPIO.output(la,GPIO.LOW)
        GPIO.output(lb,GPIO.HIGH)

def stop(t = 10):
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

def follow_line(ir):

    if ir[2] == 0 :  # on the line so, move forward
        moveF(25,25) 
    elif ir[1] == 0:    # towards right so, turn little left
        moveF(60,10) 
    elif ir[3] == 0:    # towards left so, turn little right
        moveF(10,60)
    elif ir[1] and ir[2] == 0:  # slightly toward right so, turn slightly left
        moveF(30,10)
    elif ir[2] and ir[3] ==0:   # slightly toward left so, turn slightly right
        moveF(10,30)
    elif ir[0] and ir[1] and ir[2] and ir[4] ==1 and ir [3] == 0:
         moveF(10,50)
    # elif ir[1] and ir[2] and ir[3] ==0:
    #     moveF(25,25)
    else:
         moveF(25,25)

    # ir = read_sensor_values()
    # print_sensor_values(ir)
    # if ir[2] == 0 and ir[0]and ir[1]  ==1 : # and ir[3] and ir[4]
    #     moveF(25,25)
    # if ir[2] and ir[3]== 0 and ir[0]and ir[1] and ir[4] ==1 :
    #     moveF(10,40)
    # elif ir[3]== 0 : # and ir[0]and ir[1] and ir[2] and ir[4] ==1 :
    #     moveF(20,100)
    # elif ir[3] and ir[4]== 0 and ir[0]and ir[1] and ir[2] ==1 :
    #     moveR(20,50)
    # elif ir[4]== 0 and ir[0]and ir[1] and ir[2] and ir[3] ==1 :
    #     moveF(20,80)
    # elif ir[1]== 0 and ir[0]and ir[2] and ir[3] and ir[4] ==1 :
    #     moveF(40,10)
    # elif ir[1] and ir[2]== 0 and ir[0]and ir[3] and ir[4] ==1 :
    #     moveF(60,10)
    # elif ir[3] and ir[4]== 0 and ir[0]and ir[1] and ir[2] ==1 :
    #     moveR(50,20)
    # elif ir[0] and ir[1] and ir[2] and ir[3] and ir[4] == 0:
    #     moveF(20,20)
    
    

def main():
    try:
        pin_setup()
        # arm.servo[1].angle = int(90)
        # sleep(1)
        # arm.servo[0].angle = int(180)
        # sleep(1.5)
        # arm.servo[0].angle = None
        # arm.servo[1].angle = None


        
        

        coordinate = 0
        at_intersection = False
        after_turn = False

        while True:
            dist = measure_distance()
            ir = read_sensor_values()
            print('\t'.join(map(str, ir)), f"Distance: {dist:.2f} cm\tCoordinate: {coordinate}", sep='\t')
            time.sleep(0.02)
            
            

            if ir[1] == 0 and ir[2] == 0 and ir[3] == 0:
                if not at_intersection and not after_turn:
                    moveB(25,25)
                    sleep(0.1)
                    stop(1)
                    coordinate += 1
                    at_intersection = True
            else:
                at_intersection = False
                # after_turn = False  # Reset after moving forward
            if coordinate == 4 :
                # coordinate += 1
                print("Turning left, Current Coordinate is: ", coordinate)
                moveB(27,27)
                sleep(0.15)
                stop(1)
                moveL(90,90)
                sleep(0.9)
                stop(1)
                moveF(20,20)
                sleep(0.4)
                follow_line(ir)
                
            elif coordinate == 6:
                #  coordinate += 1
                 print("Turning left, current coordinate is: ", coordinate)
                 moveB(27,27)
                 sleep(0.2)
                 stop(1)
                 moveL(90,90)
                 sleep(0.9)
                 stop(1)
                 moveF(20,20)
                 sleep(0.7)
                 follow_line(ir)
            elif coordinate == 9:
                #  coordinate += 1
                 print("Turning right, current coordinate is: ", coordinate)
                 moveB(27,27)
                 sleep(0.15)
                 stop(1)
                 moveR(90,90)
                 sleep(0.9)
                 stop(1)
                 moveF(20,20)
                 sleep(0.7)
                 follow_line(ir)
            elif coordinate == 10:
                #  coordinate += 1
                 print("Turning right, current coordinate is: ", coordinate)
                 moveB(27,27)
                 sleep(0.15)
                 stop(1)
                 moveR(90,90)
                 sleep(0.9)
                 stop(1)
                 moveF(20,20)
                 sleep(0.7)
                 follow_line(ir)
            elif coordinate == 13:
                stop(100)
                break
                #  coordinate += 1
                #  print("Turning left, current coordinate is: ", coordinate)
                #  moveB(27,27)
                #  sleep(0.15)
                #  stop(1)
                #  moveL(90,90)
                #  sleep(0.9)
                #  stop(1)
                #  follow_line(ir)

            else:
                follow_line(ir)
            # # Check for specific coordinates to make turns
            # if coordinate in {4, 5, 8, 9, 12, 13}:
                
            #     stop(0.5)

            #     if coordinate in {4, 5, 12, 13}:
            #         print("Turning left")
            #         moveL(80, 80)
            #         while read_sensor_values()[2] != 0:
            #             time.sleep(0.02)  # Small delay to prevent overloading the loop
            #         stop(0.5)
            #     elif coordinate in {8, 9}:
            #         print("Turning right")
            #         moveR(80, 80)
            #         while read_sensor_values()[2] != 0:
            #             time.sleep(0.02)  # Small delay to prevent overloading the loop
            #         stop(0.5)

            #     moveF(20, 20)  # Move forward a bit after turning
            #     time.sleep(1.0)  # Ensure it clears the intersection
            #     stop(0.5)
            #     after_turn = True  # Set the flag to prevent immediate re-detection
            #     at_intersection = False  # Ensure it's reset to detect the next intersection

            # elif coordinate == 16:
            #     moveB(20, 20)
            #     time.sleep(0.15)
            #     stop(20)
            #     break

            



                

        # while True:
            
        #     dist = measure_distance()
        #     ir = read_sensor_values()
        #     print('\t'.join(map(str, ir)), f"Distance: {dist:.2f} cm", sep='\t')
        #     time.sleep(0.02)
        #     print(coordinate)
            
        #     if ir[1] ==0 and ir[2] == 0 and ir[3] ==0:
        #         if not at_intersection:
        #              coordinate +=1
        #              at_intersection = True
        #     else:
        #         at_intersection= False
                   
        #     if coordinate == 4 or coordinate == 5:
        #         moveB(20, 20)
        #         time.sleep(0.15)
        #         stop(0.5)
        #         moveL(80, 80)
        #         time.sleep(1.3)
        #         stop(1)
        #         moveF(30,30)
        #         time.sleep(1)
        #         follow_line(ir)  # Ensure the robot continues following the line after the turn
        #     elif coordinate == 8 or coordinate == 9:
        #         moveB(20, 20)
        #         time.sleep(0.15)
        #         stop(0.5)
        #         moveR(80, 80)
        #         time.sleep(1.3)
        #         stop(1)
        #         follow_line(ir)
        #     elif coordinate == 12 or coordinate == 13:
        #         moveB(20, 20)
        #         time.sleep(0.15)
        #         stop(0.5)
        #         moveL(80, 80)
        #         time.sleep(1.3)
        #         stop(1)
        #         follow_line(ir)
        #     elif coordinate == 16:
        #         moveB(20, 20)
        #         time.sleep(0.15)
        #         stop(20)
        #         break
        #     else:
        #         follow_line(ir)
            
   
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()





# print(f"Distance: {dist:.2f} cm")
            
            # follow_line(ir)

           

            
            
            # if dist < 20 :
            #     stop(1)
            #     arm.servo[0].angle = int(105)
            #     sleep(1)
            #     arm.servo[1].angle = int(50)
            #     sleep(1.5)
            #     stop(50)
            # elif dist < 30 : 
            #      moveF(20,20)
                
                # arm.servo[1].angle = int(72)
                # sleep(1)
                # arm.servo[0].angle = int(180)
                # sleep(1.5)
                # arm.servo[0].angle = None
                # arm.servo[1].angle = None
                # stop(100)
            # elif ir[1] and ir[3] ==0:
            #      coordinate += 1
                 
                #  moveR(70,70)
                #  sleep(2)
                #  stop(20)



# test code for movement



            # moveF(25,25)
            # sleep(2)
            # stop(1)
            # moveB(25,25)
            # sleep(2)
            # stop(1)
            # moveR(90,90)
            # sleep(2)
            # stop(1)
            # moveL(90,90)
            # sleep(2)
            # stop(50)