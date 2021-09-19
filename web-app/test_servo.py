import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8,GPIO.OUT)

#pwm.ChangeDutyCycle(12)

servo_pwm = GPIO.PWM(8, 50)
servo_pwm.start(2.5)

def change(angle):
    servo_pwm.ChangeDutyCycle((1.0/18.0 * angle) + 2.5)
    
while True:
    angle = int(input("enter: "))
    change(angle)
