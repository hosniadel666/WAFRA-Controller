###########################################################
#                    IMPORT                               #
###########################################################
from flask import Flask, request, jsonify
import sqlite3
import urllib3
import control
import action
import sensor
import actuator
import log
from dotenv import load_dotenv

###############  OBJECTS  ###############################
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

############### Extract Header Data From API Requests################
def get_header_info():
   response={}
   response['method'] = request.__dict__['environ']['REQUEST_METHOD']
   response['path'] = request.__dict__['environ']['PATH_INFO']
   response['remote_addr'] = request.__dict__['environ']['REMOTE_ADDR']
   response['host_server'] = request.__dict__['environ']['HTTP_HOST']
   header_msg = response['remote_addr'] + " " + response['method'] + " " + response['host_server'] + response['path']
   return header_msg

######################################################################
#   Description :  Route for sensors                                 #
#   methods     :  Get , Post [name,number, discription,isDigitsl]   #
#                                                                    #
######################################################################
@app.route('/sensors', methods=['GET','POST'])
def handle_post():
   header_log = log.log()
   header_log.add(get_header_info(), "HEADER_INFO")      
########################### GET  REQUEST ############################
   if request.method == 'GET':
      sensor_obj = sensor.sensor()
      return jsonify(sensor_obj.get_all())                

########################### POST REQUEST ############################
   elif request.method == 'POST':
      sensor_obj = sensor.sensor()
      sensor_name = request.form['name']
      sensor_number = request.form['number']
      sensor_discription = request.form['discription']
      sensor_isDigital = request.form['isDigital']
      return jsonify(sensor_obj.add(sensor_name, sensor_number, sensor_discription))


###########################################################
#   Description :  Route of sensor with ID for each one   #
#   methods     :  Get data from DB                       #
#                                                         #
###########################################################
@app.route('/sensors/<int:id>', methods=['GET', 'DELETE'])
def get_sensor(id): 
   header_log = log.log()  
   header_log.add(get_header_info(), "HEADER_INFO")                                              
   if request.method == 'GET':
      sensor_obj = sensor.sensor()                                                 
      return jsonify(sensor_obj.get_id(id)) 
   elif request.method == 'DELETE':
      sensor_obj = sensor.sensor() 
      action_msg = "the sensor with id "+ str(id) + " is deleted"                                                  
      return jsonify(sensor_obj.remove(id)) 

###########################################################
#   Description :  Route of actuators                     #
#   methods     :  Get ,post                              #
#                                                         #
###########################################################
@app.route('/actuators', methods=['POST', 'GET'])
def handle_actuator_post():
   header_log = log.log()
   header_log.add(get_header_info(), "HEADER_INFO")      
###################  GET REQUEST   #########################
   if request.method == 'GET':
      actuator_obj = actuator.actuator()
      return jsonify(actuator_obj.get_all()) 
###################  POST REQUEST  #########################
   elif request.method == 'POST':
      actuator_obj = actuator.actuator()
      sensor_name = request.form['name']
      sensor_number = request.form['number']
      sensor_discription = request.form['discription']
      sensor_isDigital = request.form['isDigital']
      return jsonify(actuator_obj.add(sensor_name, sensor_number, sensor_discription))                             

###########################################################
#   Description :  Route of actuator with ID for each one #
#   methods     :  Get data from DB                       #
#                                                         #
###########################################################
@app.route('/actuators/<int:id>', methods=['GET', 'DELETE'])
def get_actuator(id): 
   header_log = log.log()
   header_log.add(get_header_info(), "HEADER_INFO")                                                         
   if request.method == 'GET':                                                
      actuator_obj = actuator.actuator()
      return jsonify(actuator_obj.get_id(id)) 
   elif request.method == 'DELETE':
      actuator_obj = sensor.sensor()
      return jsonify(actuator_obj.remove(id))

#############################################################
#   Description :  Route actuators (servo) with ID          #
#   methods     :  POST servo [angle]                       #
#                                                           #
#############################################################
@app.route('/actuators/set_action/<int:id>', methods=['POST'])
def control_servo(id):  
   
   header_log = log.log()
   header_log.add(get_header_info(), "HEADER_INFO")     
    
   actuator_obj = actuator.actuator()    
   #value = int(request.form['value'])
   action_type = request.form['action_type']
   #return jsonify(actuator_obj.set_action(id, value, action_type)) 
   return jsonify(actuator_obj.set_action(id, action_type)) 

#############################################################
#   Description :  Route of sensor_log with ID for each one #
#   methods     :  Get data from sensor_log table in DB     #
#                                                           #
#############################################################
@app.route('/system_log', methods=['GET'])
def get_sensor_log():
   header_log = log.log()
   header_log.add(get_header_info(), "HEADER_INFO")      
   if request.method == 'GET':                                
      system_log = log.log()
      return jsonify(system_log.get_all())  

if __name__ == '__main__':
   app.run()