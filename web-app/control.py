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


PATH_2_DB = '/home/pi/Desktop/cvs_internship/web-app/cvs.db'

###########################################################
#                  CLASSES                                #
############################################################

################## DHT (tempreture sensor) Class ###########

class dht_worker():
    def __init__(self):
        self.sensor = Adafruit_DHT.DHT11
        self.DHT11_pin = 4                        

    ## create thread to show tempreture and humidity ##
    def start(self):
        myThread = threading.Thread(target=self._read)
        myThread.daemon = True
        myThread.start()
    ## read tempreture and humidity from sensor and print it ##
    def _read(self):
        while True:
            sensor_obj_1 = sensor.sensor()
            sensor_obj_2 = sensor.sensor()
            humidity,temperature = Adafruit_DHT.read_retry(self.sensor, self.DHT11_pin)
            ## check if tempreture and humidity data is correct ##
            if humidity is not None and temperature is not None:
                sensor_obj_1.update_temerature(temperature)

                # log_obj = log.log()
                # sql_statement = "UPDATE sensor SET sensor_data=(?) WHERE id=(?)"
                # self.cursor.execute(sql_statement,(value, self.temp_id))           ## execute INSERT
                
                sensor_obj_2.update_humidity(humidity)
                # log_obj2 = log.log()
                # action_msg2 = "the humidity is " + str(value) + " celsius"
                # log_obj2.add(action_msg2, "sensing")

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
            sleep(1)
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
    SERVO_PWM_PIN = 11                                     ## connect servo with pin 11
    PIN_LEDPWM = 8                                         ## connect led with pin 11
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.servo_init()                                 ## call initilizatin servo function
        self.led_init()                                   ## call initilizatin led function

    #############################################################
    #   Description :  initilizatin led                         #
    #   Parametars  :  none                                     #                                                         
    #############################################################

    def led_init(self):
        GPIO.setup(self.PIN_LEDPWM,GPIO.OUT)
        self.led_intensity = GPIO.PWM(self.PIN_LEDPWM,100)
        self.led_intensity.start(0)
    #############################################################
    #   Description :  initilizatin servo                       #
    #   Parametars  :  none                                     #                                                         
    #############################################################
    def servo_init(self):
        GPIO.setup(self.SERVO_PWM_PIN,GPIO.OUT)
        self.servo_pwm = GPIO.PWM(self.SERVO_PWM_PIN, 50)
        self.servo_pwm.start(2)
        
    #############################################################
    #   Description :  Change led brightness                    #
    #   Parametars  :  brightness                               #                                                         
    #############################################################

    def change_brightness(self, brightness):
        self.led_intensity.ChangeDutyCycle(brightness)

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
        # store in DATABASE
        self.value = self.adc.read_adc(0, gain=self.gain)
        return self.value