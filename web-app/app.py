###########################################################
#                    IMPORT                               #
###########################################################
from flask import Flask, request, jsonify, abort
import urllib3
import control
import action
import sensor
import actuator
import log
from dotenv import load_dotenv
from functools import wraps

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


################ The actual decorator function ######################
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        with open('api.key', 'r') as apikey:
            key=apikey.read().replace('\n', '')
            print(key)
        #if request.args.get('key') and request.args.get('key') == key:
        if request.headers.get('server-api-key') and request.headers.get('server-api-key') == key:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


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
@app.route('/sensors', methods=['GET'])
def handle_get():
   header_log = log.log()
   header_log.add(get_header_info(), "HEADER_INFO")   
      
   sensor_obj = sensor.sensor()
   return jsonify(sensor_obj.get_all())     
              
@app.route('/sensors', methods=['POST'])
@require_appkey
def handle_post():
   header_log = log.log()
   header_log.add(get_header_info(), "HEADER_INFO")  

   sensor_obj = sensor.sensor()
   sensor_name = request.form['name']
   sensor_number = request.form['number']
   sensor_discription = request.form['discription']
   sensor_isDigital = request.form['isDigital']
   return jsonify(sensor_obj.add(sensor_name, sensor_number, sensor_discription, sensor_isDigital))


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
@app.route('/actuators', methods=['GET'])
def handle_actuator_get():
   header_log = log.log()
   header_log.add(get_header_info(), "HEADER_INFO")      

   actuator_obj = actuator.actuator()
   return jsonify(actuator_obj.get_all()) 

@app.route('/actuators', methods=['POST'])
@require_appkey
def handle_actuator_post():
   header_log = log.log()
   header_log.add(get_header_info(), "HEADER_INFO")      

   actuator_obj = actuator.actuator()
   sensor_name = request.form['name']
   sensor_number = request.form['number']
   sensor_discription = request.form['discription']
   sensor_isDigital = request.form['isDigital']
   return jsonify(actuator_obj.add(sensor_name, sensor_number, sensor_discription, sensor_isDigital))                             

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
@require_appkey
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