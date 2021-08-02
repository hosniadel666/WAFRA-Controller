import sys
from rpi_control import rpi_control_
import sqlite3

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
               
class backend_():
    def __init__(self):
        self.control = rpi_control_()

    def store_servo_angle(self, angle):
        print("bjfkg")
        #create an object from db to store these info

    def store_led_brightness(self, brightness):
        print("bjfkg")
        #create an object from db to store these info
        
    def store_dht_data(self, temperature, humidity):
        print("bjfkg")
        #create an object from db to store these info

    def servo_handle(self, angle):
        if angle < 0 or angle > 180:
            print("put angle between 0-180")
        else:
            self.control.change_servo_angle(angle)
            self.store_servo_angle(angle)

    def brightness_handle(self, brightness):
        self.control.change_brightness(brightness)
        self.store_led_brightness(brightness)
        
    def on_adc_changed(self):
        return self.control.on_adc_changed()
    
