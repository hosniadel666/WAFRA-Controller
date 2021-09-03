###########################################################
#                  IMPORT                                 #
############################################################
import sys
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5 import uic, QtWidgets
import RPi.GPIO as GPIO
import Adafruit_DHT
import Adafruit_ADS1x15
from time import sleep
import time
import threading
import csv



class DB():
    csvFile = "sensor_readings.csv"
    def __init__(self):
       with open(self.csvFile, "r") as read_file, open(self.csvFile, "w") as output:
          csv_dict = [row for row in csv.DictReader(read_file)];
          if len(csv_dict) == 0:
              writer =  csv.writer(output, delimiter = ",", lineterminator = "\n")
              writer.writerow(["Temperature", "Humididty", "Time"])
    def store(self, data):
        with open(self.csvFile, "a") as output:
            writer =  csv.writer(output, delimiter = ",", lineterminator = "\n")
            writer.writerow(data)

class Adafruit_DHT_Worker(QtCore.QObject):
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

class HMI(QtWidgets.QMainWindow):
    temperature = 0
    humidity = 0
    SERVO_PWM_PIN = 11
    PIN_LEDPWM = 8

    def __init__(self):
        super(HMI,self).__init__()
        self.setWindowTitle("CVS HMI")
        uic.loadUi('mainwindow.ui',self)

        self.adc = Adafruit_ADS1x15.ADS1115()
        self.gain = 1
        
        self.db = DB()
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.servo_init()
        self.servoRotate_PB.clicked.connect(self.servo_rotate)
	
        self.led_init()
        self.led_brightness_slider.valueChanged.connect(self.change_brightness)

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.on_adc_changed)
        self.timer.start()
        

        self.dht_worker = Adafruit_DHT_Worker()
        self.dht_worker.valueChanged.connect(self.on_dht_changed)
        self.dht_worker.start()


    def led_init(self):
        GPIO.setup(self.PIN_LEDPWM,GPIO.OUT)
        self.led_intensity = GPIO.PWM(self.PIN_LEDPWM,100)
        self.led_intensity.start(0)
        
    def servo_init(self):
        GPIO.setup(self.SERVO_PWM_PIN,GPIO.OUT)
        self.servo_pwm = GPIO.PWM(self.SERVO_PWM_PIN, 50)
        self.servo_pwm.start(2)

    @pyqtSlot(float,float)
    def on_dht_changed(self, temperature, humidity):
        time_ = time.strftime("%I") + ":" + time.strftime("%M") + ':' + time.strftime("%S")
        data = [temperature, humidity, time_]
        self.db.store(data)
        self.lcdTemperature.display(temperature)
        self.lcdHumidity.display(humidity)
    
    @pyqtSlot()
    def servo_rotate(self):
        angle_val = float(self.servoAngle_EL.text())
        if angle_val < 0 or angle_val > 180:
            print("put angle between 0-180")
        else:
            self.servo_pwm.ChangeDutyCycle ( (1.0/18.0 * angle_val) + 2)
	
    @pyqtSlot()
    def change_brightness(self):
        led_val = int(self.led_brightness_slider.value())
        self.led_intensity.ChangeDutyCycle(led_val)
    @pyqtSlot()
    def on_adc_changed(self):
        self.value = self.adc.read_adc(0, gain=self.gain)
        self.lcdADC.display(self.value)

app = QtWidgets.QApplication(sys.argv)
w = HMI()
w.show()
app.exec_()
