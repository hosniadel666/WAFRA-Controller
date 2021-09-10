import RPi.GPIO as GPIO
import Adafruit_DHT
import Adafruit_ADS1x15
from time import sleep
import time
import threading
import sensor

# Tempreture and humidity sensor thread


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
            humidity, temperature = Adafruit_DHT.read_retry(
                self.sensor, self.DHT11_pin)

            if humidity is not None and temperature is not None:
                sensor_obj_1.update_temerature(temperature)
                sensor_obj_2.update_humidity(humidity)


# ADC thread
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
            value = value * (5 / 32786)
            if value is not None:
                sensor_obj.update_adc(value)

# Control Class


class control():
    servo_pwm = 11
    led_pwm_1 = 8
    led_pwm_2 = 13
    led_pwm_3 = 15

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.servo_init()
        self.led_init()

    #-----------------------------------------------------------#
    #   Description :  Initilizatin of leds[motors]             #
    #   Parametars  :  none                                     #
    #-----------------------------------------------------------#

    def led_init(self):
        GPIO.setup(self.led_pwm_1, GPIO.OUT)
        GPIO.setup(self.led_pwm_2, GPIO.OUT)
        GPIO.setup(self.led_pwm_3, GPIO.OUT)
        self.led_1_intensity = GPIO.PWM(self.led_pwm_1, 100)
        self.led_2_intensity = GPIO.PWM(self.led_pwm_2, 100)
        self.led_3_intensity = GPIO.PWM(self.led_pwm_3, 100)
        self.led_1_intensity.start(0)
        self.led_2_intensity.start(0)
        self.led_3_intensity.start(0)

    #-----------------------------------------------------------#
    #   Description :  Initilizatin of a servo motor            #
    #   Parametars  :  none                                     #
    #-----------------------------------------------------------#
    def servo_init(self):
        GPIO.setup(self.servo_pwm, GPIO.OUT)
        self.servo_pwm = GPIO.PWM(self.servo_pwm, 50)
        self.servo_pwm.start(2)

    #-----------------------------------------------------------#
    #   Description :  Change the brightness of the given led   #
    #   Parametars  :  brightness[PWM value], id[which motor]   #
    #-----------------------------------------------------------#

    def change_brightness(self, brightness, id):
        if id == 1:
            self.led_1_intensity.ChangeDutyCycle(brightness)
        elif id == 2:
            self.led_2_intensity.ChangeDutyCycle(brightness)
        elif id == 3:
            self.led_3_intensity.ChangeDutyCycle(brightness)

    #-----------------------------------------------------------#
    #   Description :  Change the angle of the servo motor      #
    #   Parametars  :  angle of movement                        #
    #-----------------------------------------------------------#

    def change_servo_angle(self, angle):
        self.servo_pwm.ChangeDutyCycle((1.0/18.0 * angle) + 2)

    #-----------------------------------------------------------#
    #   Description :  Get the value of ADC reading             #
    #   Parametars  :  None                                     #
    #   Return      :  The value of ADC module                  #
    #-----------------------------------------------------------#
    def on_adc_changed(self):
        self.value = self.adc.read_adc(0, gain=self.gain)
        return self.value
