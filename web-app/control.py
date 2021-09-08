###########################################################
#                        IMPORT                           #
###########################################################
import RPi.GPIO as GPIO
import Adafruit_DHT
import Adafruit_ADS1x15
from time import sleep
import time
import threading
import math
import sensor
import log
from dotenv import load_dotenv
import os

###########################################################
#                  CLASSES                                #
############################################################

################## DHT (tempreture sensor) Class ###########

class dht_worker():
    def __init__(self):
        self.sensor = Adafruit_DHT.DHT11
        self.DHT11_pin = 4                        

    def start(self):
        myThread = threading.Thread(target=self._read)
        myThread.daemon = True
        myThread.start()

    def _read(self):
        while True:
            sensor_obj_1 = sensor.sensor()
            sensor_obj_2 = sensor.sensor()
            humidity,temperature = Adafruit_DHT.read_retry(self.sensor, self.DHT11_pin)
            
            if humidity is not None and temperature is not None:
                sensor_obj_1.update_temerature(temperature)

                log_obj_1 = log.log()
                action_msg_1 = "the temperature is " + str(temperature) + " celsius"
                log_obj_1.add(action_msg_1, "sensing")       
                
                sensor_obj_2.update_humidity(humidity)
                
                log_obj_2 = log.log()
                action_msg_2 = "the humidity is " + str(humidity) + " %"
                log_obj_2.add(action_msg_2, "sensing")

#################### ADC Class ##############################

class adc_worker():
    def __init__(self):
        self.gain = 1
        self.channel = 0
        self.adc = Adafruit_ADS1x15.ADS1115()

    def start(self):
        myThread = threading.Thread(target=self._read)
        myThread.daemon = True
        myThread.start()
  
    def _read(self):
        while True:
            sleep(3)
            sensor_obj = sensor.sensor()
            value = self.adc.read_adc(self.channel, gain=self.gain)
            value = math.ceil(value * (5 / 32786))
            if value is not None:
                sensor_obj.update_adc(value)
                log_obj = log.log()
                action_msg = "the voltage reading is " + str(value)
                log_obj.add(action_msg, "sensing")


################## rpi_control Class ###########
class rpi_control_():                                      
    servo_pwm = 11                                   
    led_pwm_1 = 8                                         
    led_pwm_2 = 13
    led_pwm_3 = 15
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.servo_init()                               
        self.led_init()                                 

    #############################################################
    #   Description :  initilizatin led                         #
    #   Parametars  :  none                                     #                                                         
    #############################################################

    def led_init(self):
        GPIO.setup(self.led_pwm_1,GPIO.OUT)
        GPIO.setup(self.led_pwm_2,GPIO.OUT)
        GPIO.setup(self.led_pwm_3,GPIO.OUT)
        self.led_1_intensity = GPIO.PWM(self.led_pwm_1,100)
        self.led_2_intensity = GPIO.PWM(self.led_pwm_2,100)
        self.led_3_intensity = GPIO.PWM(self.led_pwm_3,100)
        self.led_1_intensity.start(0)
        self.led_2_intensity.start(0)
        self.led_3_intensity.start(0)
        
    #############################################################
    #   Description :  initilizatin servo                       #
    #   Parametars  :  none                                     #                                                         
    #############################################################
    def servo_init(self):
        GPIO.setup(self.servo_pwm,GPIO.OUT)
        self.servo_pwm = GPIO.PWM(self.servo_pwm, 50)
        self.servo_pwm.start(2)
        
    #############################################################
    #   Description :  Change led brightness                    #
    #   Parametars  :  brightness                               #                                                         
    #############################################################

    def change_brightness(self, brightness, id):
        if id == 1:
            self.led_1_intensity.ChangeDutyCycle(brightness)
        if id == 2:
            self.led_2_intensity.ChangeDutyCycle(brightness)
        if id == 3:
            self.led_3_intensity.ChangeDutyCycle(brightness)
        

    #############################################################
    #   Description :  Change servo angle                       #
    #   Parametars  :  angle                                    #                                                         
    #############################################################   

    def change_servo_angle(self, angle):
        self.servo_pwm.ChangeDutyCycle ( (1.0/18.0 * angle) + 2)

    #############################################################
    #   Description :  Change adc                               #
    #   Parametars  :  none                                     #   
    #   Return      :  ADC value                                #                                                       
    #############################################################   
    def on_adc_changed(self):
        self.value = self.adc.read_adc(0, gain=self.gain)
        return self.value