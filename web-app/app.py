###########################################################
#                  IMPORT                                 #
###########################################################
from flask import Flask, request, jsonify
import sqlite3
import requests as req
import urllib3
import control
import action
from time import sleep
import RPi.GPIO as GPIO
from dotenv import load_dotenv
import os
import log


###############  OBJECTS  ###############################
# control = control.rpi_control_()           # Control object
dht_thread = control.dht_worker()
adc_thread = control.adc_worker()
action_thread = action.action_worker()
http = urllib3.PoolManager()
app = Flask(__name__)

################# run temperature and adc threads ####################
dht_thread.start()
adc_thread.start()
action_thread.start()

################ Load Environment variables #########################
load_dotenv()



######################################################################
#   Description :  Route for sensors                                 #
#   methods     :  Get , Post [name,number, discription,isDigitsl]   #
#                                                                    #
######################################################################

@app.route('/sensors', methods=['GET','POST'])
def handle_post():
########################### GET  REQUEST ############################
   if request.method == 'GET':
      sensor_obj = sensor.sensor()
      return jsonify(response)                  ## present data as json file 

########################### POST REQUEST ############################
   elif request.method == 'POST':
      sensor_obj = sensor.sensor()
      sensor_name = request.form['name']
      sensor_number = request.form['number']
      sensor_discription = request.form['discription']
      sensor_isDigital = request.form['isDigital']
      return sensor_obj.add(sensor_name, sensor_number, sensor_discription)

###########################################################
#   Description :  Route of sensor with ID for each one   #
#   methods     :  Get data from DB                       #
#                                                         #
###########################################################

@app.route('/sensors/<int:id_>', methods=['GET', 'DELETE'])
def get_sensor(id):                                                   ## get ID to get its data
   if request.method == 'GET':
      sensor_obj = sensor.sensor()                                                  ## cleanup
      return jsonify(sensor_obj.add_id(id)) 
   elif request.method == 'DELETE':
      sensor_obj = sensor.sensor() 
      action_msg = "the sensor with id "+ str(id) + " is deleted"                                                   ## cleanup
      return jsonify(sensor_obj.remove(id)) 
   
###########################################################
#   Description :  Route of actuators                     #
#   methods     :  Get ,post                              #
#                                                         #
###########################################################

@app.route('/actuators', methods=['POST', 'GET'])
def handle_actuator_post():
###################  GET REQUEST   #########################
   if request.method == 'GET':
      actuator_obj = actuator.actuator()
      return jsonify(actuator_obj.get_all()) 
###################  POST REQUEST  #########################
   if request.method == 'POST':
      actuator_obj = actuator.actuator()
      actuator_name = request.form['name']
      actuator_number = request.form['number']
      actuator_discription = request.form['discription']
      actuator_isDigital = request.form['isDigital']
      return (actuator_obj.add(actuator_name, actuator_number, actuator_discription, actuator_isDigital)
      
###########################################################
#   Description :  Route of actuator with ID for each one #
#   methods     :  Get data from DB                       #
#                                                         #
###########################################################
@app.route('/actuators/<int:id_>', methods=['GET', 'DELETE'])
def get_actuator(id):                                                     
   if request.method == 'GET':                                                
      actuator_obj = actuator.actuator()
      return jsonify(actuator_obj.add_id(id)) 
   elif request.method == 'DELETE':
      actuator_obj = sensor.sensor()
      return jsonify(actuator_obj.remove(id))

#############################################################
#   Description :  Route actuators (servo) with ID          #
#   methods     :  POST servo [angle]                       #
#                                                           #
#############################################################
@app.route('/actuators/set_action/<int:id_>', methods=['POST'])
def control_servo(id):                                                
   actuator_obj = actuator.actuator()    
   value = int(request.form['value'])
   action_type = request.form['action_type']

   return jsonify(actuator_obj.set_action(id, action_type, value))                                                ## present data as json file


#############################################################
#   Description :  Route of sensor_log with ID for each one #
#   methods     :  Get data from sensor_log table in DB     #
#                                                           #
#############################################################
@app.route('/system_log', methods=['GET'])
def get_sensor_log():
   if request.method == 'GET':                                
      system_log = log.log()
      return jsonify(system_log.get_())                                             

if __name__ == '__main__':
   app.run()
