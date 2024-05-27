import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class motor():
    def __init__(self,Ena,In1,In2,Enb,In3,In4):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        self.Enb = Enb
        self.In3 = In3
        self.In4 = In4
        GPIO.setup(self.Ena,GPIO.OUT)
        GPIO.setup(self.In1,GPIO.OUT)
        GPIO.setup(self.In2,GPIO.OUT)
        GPIO.setup(self.Enb,GPIO.OUT)
        GPIO.setup(self.In3,GPIO.OUT)
        GPIO.setup(self.In4,GPIO.OUT)
        self.pwma = GPIO.PWM(self.Ena, 100)
        self.pwmb = GPIO.PWM(self.Enb, 100)
        self.pwma.start(0)
        self.pwmb.start(0)

    def moveF(self,x=100,t=0):
        self.pwma.ChangeDutyCycle(x)
        self.pwmb.ChangeDutyCycle(x)
        GPIO.output(self.In1,GPIO.HIGH)
        GPIO.output(self.In2,GPIO.LOW)
        GPIO.output(self.In3,GPIO.HIGH)
        GPIO.output(self.In4,GPIO.LOW)
        sleep(t)

    def moveB(self,x=100,t=0):
        self.pwma.ChangeDutyCycle(x)
        self.pwmb.ChangeDutyCycle(x)
        GPIO.output(self.In1,GPIO.LOW)
        GPIO.output(self.In2,GPIO.HIGH)
        GPIO.output(self.In3,GPIO.LOW)
        GPIO.output(self.In4,GPIO.HIGH)
        sleep(t)

    def moveR(self,x=100,t=0):
        self.pwma.ChangeDutyCycle(x)
        self.pwmb.ChangeDutyCycle(x - (50 * 0.4))
        GPIO.output(self.In1,GPIO.HIGH)
        GPIO.output(self.In2,GPIO.LOW)
        GPIO.output(self.In3,GPIO.LOW)
        GPIO.output(self.In4,GPIO.HIGH)
        sleep(t)

    def moveL(self,x=100,t=0):
        self.pwma.ChangeDutyCycle(x - (50 * 0.4))
        self.pwmb.ChangeDutyCycle(x)
        GPIO.output(self.In1,GPIO.LOW)
        GPIO.output(self.In2,GPIO.HIGH)
        GPIO.output(self.In3,GPIO.HIGH)
        GPIO.output(self.In4,GPIO.LOW)
        sleep(t)

    def stop(self,t=0):
        self.pwma.ChangeDutyCycle(0)
        self.pwmb.ChangeDutyCycle(0)
        sleep(t)
 
rmotor = motor(21,16,20, 1,7,8)


rmotor.moveF(100, 2)
rmotor.stop(1)













# # declare the pins for motorA
# ena,in1,in2 = 17, 27, 22

# enb, in3, in4 = 11, 9, 10

# # set the pin modes
# GPIO.setup(ena, GPIO.OUT)
# GPIO.setup(in1, GPIO.OUT)
# GPIO.setup(in2, GPIO.OUT)

# GPIO.setup(enb, GPIO.OUT)
# GPIO.setup(in3, GPIO.OUT)
# GPIO.setup(in4, GPIO.OUT)

# # set pwm pin 
# pwma = GPIO.PWM(ena, 100)
# pwma.start(0)

# pwmb = GPIO.PWM(enb, 100)
# pwmb.start(0)

# while True:

#     GPIO.output(in1, GPIO.LOW)
#     GPIO.output(in2, GPIO.HIGH)
#     pwma.ChangeDutyCycle(50)
#     print('left motor running')
#     sleep(2)
#     pwma.ChangeDutyCycle(0)

#     GPIO.output(in3, GPIO.LOW)
#     GPIO.output(in4, GPIO.HIGH)
#     pwmb.ChangeDutyCycle(50)
#     print('right motor running')
#     sleep(2)
#     pwmb.ChangeDutyCycle(0)
 
