from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
from time import sleep
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


arm=ServoKit (channels=16)
servo=3


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



class motor():
    def __init__(self,enr,ra,rb,enl,la,lb):
        self.enr = enr
        self.ra = ra
        self.rb = rb
        self.enl = enl
        self.la = la
        self.lb = lb
        GPIO.setup(self.enr,GPIO.OUT)
        GPIO.setup(self.ra,GPIO.OUT)
        GPIO.setup(self.rb,GPIO.OUT)
        GPIO.setup(self.enl,GPIO.OUT)
        GPIO.setup(self.la,GPIO.OUT)
        GPIO.setup(self.lb,GPIO.OUT)
        self.pwmr = GPIO.PWM(self.enr, 100)
        self.pwml = GPIO.PWM(self.enl, 100)
        self.pwmr.start(0)
        self.pwml.start(0)

    def moveF(self, r=0, l=0):
        self.pwmr.ChangeDutyCycle(r)
        self.pwml.ChangeDutyCycle(l)
        GPIO.output(self.ra,GPIO.HIGH)
        GPIO.output(self.rb,GPIO.LOW)
        GPIO.output(self.la,GPIO.HIGH)
        GPIO.output(self.lb,GPIO.LOW)
        
    def moveB(self, r=0, l=0):
        self.pwmr.ChangeDutyCycle(r)
        self.pwml.ChangeDutyCycle(l)
        GPIO.output(self.ra,GPIO.LOW)
        GPIO.output(self.rb,GPIO.HIGH)
        GPIO.output(self.la,GPIO.LOW)
        GPIO.output(self.lb,GPIO.HIGH)
        # sleep(t)

    def moveR(self,r=0, l=0):
        self.pwmr.ChangeDutyCycle(r)
        self.pwml.ChangeDutyCycle(l)
        GPIO.output(self.ra,GPIO.LOW)
        GPIO.output(self.rb,GPIO.HIGH)
        GPIO.output(self.la,GPIO.HIGH)
        GPIO.output(self.lb,GPIO.LOW)
        
    def moveL(self,r=0, l=0):
        self.pwmr.ChangeDutyCycle(r)
        self.pwml.ChangeDutyCycle(l)
        GPIO.output(self.ra,GPIO.HIGH)
        GPIO.output(self.rb,GPIO.LOW)
        GPIO.output(self.la,GPIO.LOW)
        GPIO.output(self.lb,GPIO.HIGH)
        
    def stop(self):
        self.pwmr.ChangeDutyCycle(0)
        self.pwml.ChangeDutyCycle(0)
        # sleep(t)
 





def main():
    try:
        setup()
        rm = motor(21,16,20, 1,7,8)
        print("Reading IR sensor values...")
        
        # rm.moveL(80,80)
        # sleep(1)
        # rm.moveB(30,30)
        # sleep(0.2)
        while True:

            
            
            # ir = read_sensor_values()
            # print_sensor_values(ir)
            # time.sleep(0.05)  # Adjust delay as needed
            rm.moveL(100,100)
            sleep(1)
            rm.stop()
            sleep(1)
            rm.moveR(100,100)
            sleep(1)
            rm.stop()
            sleep(1)
            # rm.moveL(100,100)
            # sleep(2)
            # rm.stop(1)
            # rm.move(100,100)
            # sleep(2)
            # rm.stop(1)

            # rm.moveB(50,50)
            # # sleep(0.7)
            # rm.moveL(100,100)
            # sleep(3)
            # rm.stop()
            # sleep(0.7)
            # rm.stop()
            # sleep(0.7)
            # rm.moveL(100,100)
            # sleep(3)
            
            # if ir[2] == 0 and ir[1] and ir[3] ==1:  # on the line so, move forward
            #     rm.moveF(25,25) 
            # elif ir[1] == 0:    # towards right so, turn little left
            #     rm.moveF(70,10) 
            # elif ir[3] == 0:    # towards left so, turn little right
            #     rm.moveF(10,70)
            # elif ir[1] and ir[2] == 0:  # slightly toward right so, turn slightly left
            #     rm.moveF(50,10)
            # elif ir[2] and ir[3] ==0:   # slightly toward left so, turn slightly right
            #     rm.moveF(10,50)
            # elif ir[1] and ir[2] and ir[3] ==0:
            #     rm.stop()
                
            
            


            # if ir[2] == 0 and ir[0]and ir[1] and ir[3] and ir[4] ==1 :
            #     rm.moveF(25,25)
            # elif ir[2] and ir[3]== 0 and ir[0]and ir[1] and ir[4] ==1 :
            #     rm.moveF(10,40)
            # elif ir[3]== 0 : # and ir[0]and ir[1] and ir[2] and ir[4] ==1 :
            #     rm.moveF(20,100)
            # elif ir[3] and ir[4]== 0 and ir[0]and ir[1] and ir[2] ==1 :
            #     rm.moveR(20,50)
            # elif ir[4]== 0 and ir[0]and ir[1] and ir[2] and ir[3] ==1 :
            #     rm.moveF(20,80)
            # elif ir[1]== 0 and ir[0]and ir[2] and ir[3] and ir[4] ==1 :
            #     rm.moveF(40,10)
            # elif ir[1] and ir[2]== 0 and ir[0]and ir[3] and ir[4] ==1 :
            #     rm.moveF(60,10)
            # elif ir[3] and ir[4]== 0 and ir[0]and ir[1] and ir[2] ==1 :
            #     rm.moveR(50,20)
            # elif ir[0] and ir[1] and ir[2] and ir[3] and ir[4] == 0:
            #     rm.stop()
            
 
            # else:
            #     rm.stop()
   
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()





