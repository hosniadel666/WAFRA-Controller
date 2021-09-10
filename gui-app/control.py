import RPi.GPIO as GPIO
import Adafruit_DHT
import Adafruit_ADS1x15
from time import sleep
import threading
from PyQt5 import QtCore

class dht_worker(QtCore.QObject):
    sensor = Adafruit_DHT.DHT11
    DHT11_pin = 4
    valueChanged = QtCore.pyqtSignal(float, float)

    def start(self):
        myThread = threading.Thread(target=self._read)
        myThread.daemon = True
        myThread.start()

    def _read(self):
        while True:
            humidity,temperature = Adafruit_DHT.read_retry(self.sensor, self.DHT11_pin)
            if humidity is not None and temperature is not None:
                self.valueChanged.emit(temperature, humidity)
    
class control():
    temperature = 0
    humidity = 0
    SERVO_PWM_PIN = 11
    PIN_LEDPWM = 8
    def __init__(self):
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.gain = 1
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.servo_init()
        
        self.led_init()
        
        
    def led_init(self):
        GPIO.setup(self.PIN_LEDPWM,GPIO.OUT)
        self.led_intensity = GPIO.PWM(self.PIN_LEDPWM,100)
        self.led_intensity.start(0)
        
    def servo_init(self):
        GPIO.setup(self.SERVO_PWM_PIN,GPIO.OUT)
        self.servo_pwm = GPIO.PWM(self.SERVO_PWM_PIN, 50)
        self.servo_pwm.start(2)
        
    def change_brightness(self, brightness):
        self.led_intensity.ChangeDutyCycle(brightness)
        
    def change_servo_angle(self, angle):
        self.servo_pwm.ChangeDutyCycle ( (1.0/18.0 * angle) + 2)
        
    def on_adc_changed(self):
        self.value = self.adc.read_adc(0, gain=self.gain)
        return self.value
    