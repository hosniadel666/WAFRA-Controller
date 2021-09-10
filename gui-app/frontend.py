from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5 import uic, QtWidgets
from backend import backend_
import control
import sys

class HMI(QtWidgets.QMainWindow):
    def __init__(self):
        super(HMI,self).__init__()
        self.setWindowTitle("CVS HMI")
        uic.loadUi('mainwindow.ui',self)
        self.ctrl = backend_()
        
        self.dht_worker = control.dht_worker()  
        self.dht_worker.valueChanged.connect(self.on_dht_changed) 
        self.dht_worker.start()

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.on_adc_changed)
        self.timer.start()

        self.servoRotate_PB.clicked.connect(self.servo_rotate)
        self.led_brightness_slider.valueChanged.connect(self.change_brightness)
        
    @pyqtSlot(float,float)
    def on_dht_changed(self, temperature, humidity):
        #self.ctrl.store(temperature, humidity) # Store the temp and humidity throught front end
        self.lcdTemperature.display(temperature)
        self.lcdHumidity.display(humidity)
    
    @pyqtSlot()
    def servo_rotate(self):
        angle = float(self.servoAngle_EL.text())
        self.ctrl.servo_handle(angle)
        
    @pyqtSlot()
    def change_brightness(self):
        brightness = int(self.led_brightness_slider.value())
        self.ctrl.brightness_handle(brightness)
        
    @pyqtSlot()
    def on_adc_changed(self):
        self.lcdADC.display(self.ctrl.on_adc_changed())

app = QtWidgets.QApplication(sys.argv)
w = HMI()
w.show()
app.exec_()
