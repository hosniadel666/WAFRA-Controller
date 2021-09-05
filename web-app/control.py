###########################################################
#                        IMPORT                           #
###########################################################
import RPi.GPIO as GPIO
import Adafruit_DHT
import Adafruit_ADS1x15
from time import sleep
import time
import threading
import sqlite3

PATH_2_DB = '/home/pi/Desktop/cvs_internship/web_app/cvs.db'

###########################################################
#                  CLASSES                                #
############################################################

################## DHT (tempreture sensor) Class ###########

class dht_worker():
    def __init__(self):
        self.sensor = Adafruit_DHT.DHT11
        self.DHT11_pin = 4                        ## connect tempreture sensor with pin 4
        self.dht_val_2db = "dht_1"
    ## create thread to show tempreture and humidity ##
    def start(self):
        myThread = threading.Thread(target=self._read)
        myThread.daemon = True
        myThread.start()
    ## read tempreture and humidity from sensor and print it ##
    def _read(self):
        while True:
            humidity,temperature = Adafruit_DHT.read_retry(self.sensor, self.DHT11_pin)
            ## check if tempreture and humidity data is correct ##
            if humidity is not None and temperature is not None:
                action_msg = "the dht_1 reading is " + str(temperature) + " celsius"
                conn = sqlite3.connect(PATH_2_DB)            ## connect to DB
                cursor = conn.cursor()                       ## get a cursor

                sql_1 = "UPDATE sensor SET sensor_data=(?) WHERE name=(?)"
                cursor.execute(sql_1,(temperature, self.dht_val_2db))           ## execute INSERT

                sql_2 = "INSERT INTO system_log(log_message) VALUES (?)"
                cursor.execute(sql_2, (action_msg,))  

                conn.commit()                                ## commit
                conn.close()                                 ## cleanup

#################### ADC Class ##############################

class adc_worker():

    def __init__(self):
        self.gain = 1
        self.channel = 0
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.adc_val_2db = "adc_1"

    def start(self):
        myThread = threading.Thread(target=self._read)
        myThread.daemon = True
        myThread.start()
  
    def _read(self):
        while True:
            value = self.adc.read_adc(self.channel, gain=self.gain)
            if value is not None:
                sleep(4)
                action_msg = "the adc_1 reading is " + str(value)
                conn = sqlite3.connect(PATH_2_DB)            ## connect to DB
                cursor = conn.cursor()                       ## get a cursor
                sql_1 = "UPDATE sensor SET sensor_data=(?) WHERE name=(?)"
                cursor.execute(sql_1,(value,self.adc_val_2db))           ## execute INSERT

                sql_2 = "INSERT INTO system_log(log_message) VALUES (?)"                  
                cursor.execute(sql_2, (action_msg,))  

                conn.commit()                                ## commit
                conn.close()                                 ## cleanup


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