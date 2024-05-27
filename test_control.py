from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
from time import sleep


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


arm=ServoKit (channels=16)
servo=3


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
 



rm = motor(21, 16, 20, 1, 7, 8)


def arm_ctl():
    
    
    
    arm.servo[0].angle = int(180)
    sleep(1)
    


# arm.servo[1].angle = int(90)
# sleep(1)
# arm.servo[0].angle = int(180)
# sleep(1.5)
# rm.moveF(25,25)
# sleep(2)
# rm.stop()
# sleep(2)
# arm.servo[0].angle = int(110)
# sleep(2)
# arm.servo[1].angle = int(30)
# sleep(1)
# rm.moveB(25,25)
# sleep(2)
# rm.stop()
# sleep(1)
# rm.moveR(60, 80)
# sleep(3)
# rm.stop()
# sleep(1)
# arm.servo[1].angle = int(90)
# sleep(1)
# arm.servo[0].angle = int(180)
# sleep(1)
# arm.servo[0].angle = None
# arm.servo[1].angle = None


rm.stop()
sleep(2)
arm.servo[1].angle = int(90)
sleep(1)
arm.servo[0].angle = int(180)
sleep(1.5)

rm.moveF(30,30)
sleep(1.7)
rm.stop()
sleep(0.5)
rm.moveL(80, 60)
sleep(1.9)
rm.moveF(30,30)
sleep(1.1)
rm.stop()
sleep(0.5)
arm.servo[0].angle = int(105)
sleep(1)
arm.servo[1].angle = int(50)
sleep(1)
rm.stop()
sleep(1)
rm.moveB(30,30)
sleep(2)
rm.stop()
sleep(0.3)
rm.moveL(80, 60)
sleep(1.8)
rm.moveF(30,30)
sleep(1.7)
rm.stop()
sleep(0.5)
arm.servo[1].angle = int(90)
sleep(1)
arm.servo[0].angle = int(180)
sleep(1)
arm.servo[0].angle = None
arm.servo[1].angle = None



# arm_ctl()













