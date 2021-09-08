###########################################################
#                        IMPORT                           #
###########################################################
import RPi.GPIO as GPIO
import Adafruit_DHT
import Adafruit_ADS1x15
from time import sleep
import threading
import sqlite3
import control

PATH_2_DB = '/home/pi/Desktop/cvs_internship/web-app/cvs.db'

class action_worker():
    def __init__(self):
        self.control = control.rpi_control_()

    def start(self):
        myThread = threading.Thread(target=self.act)
        myThread.daemon = True
        myThread.start()

    def act(self):
        while True:
            self.conn = sqlite3.connect(PATH_2_DB)                       
            self.cursor = self.conn.cursor()
            
            self.cursor.execute("select * from actuator")
            rows = self.cursor.fetchall()                   
            if len(rows) >= 1:                        
                for row in rows:
                    self.handle(row[0], row[5], row[6])
            
            self.conn.commit()                                
            self.conn.close()                                 

    def handle(self, id, value, type):
        if id == 1:
            if type == "UPDATE" :
                # print(value)
                self.control.change_brightness(value)
            elif type == "OFF":
                self.control.change_brightness(0)
            elif type == "ON":
                self.control.change_brightness(value)

        # elif id == 2:
        #     if type == "UPDATE" :
        #         self.control.change_brightness(value)
        #     elif type == "OFF":
        #         self.control.change_brightness(0)
        #     elif type == "ON":
        #         self.control.change_brightness(value)

        # elif id == 3:
        #     if type == "UPDATE" :
        #         self.control.change_brightness(value)
        #     elif type == "OFF":
        #         self.control.change_brightness(0)
        #     elif type == "ON":
        #         self.control.change_brightness(value)

        elif id == 4:
            if type == "UPDATE" :
                self.control.change_servo_angle(value)  
            elif type == "OFF":
                self.control.change_servo_angle(2)
            elif type == "ON":
                self.control.change_servo_angle(value)

   # def __del__(self):


