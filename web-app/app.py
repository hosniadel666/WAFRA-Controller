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


###############  OBJECTS  ###############################
<<<<<<< HEAD
# control = control.rpi_control_()           # Control object
=======
>>>>>>> 8e335bd79015d25fde53fe1a40d8729abbe730e6
dht_thread = control.dht_worker()
adc_thread = control.adc_worker()
action_thread = action.action_worker()
http = urllib3.PoolManager()
app = Flask(__name__)

################# run temperature and adc threads ####################
dht_thread.start()
adc_thread.start()
action_thread.start()

<<<<<<< HEAD
################ Database Path #########################
PATH_2_DB = '/home/pi/Desktop/cvs_internship/web-app/cvs.db'
=======
################ Load Environment variables #########################
load_dotenv()
>>>>>>> 8e335bd79015d25fde53fe1a40d8729abbe730e6



######################################################################
#   Description :  Route for sensors                                 #
#   methods     :  Get , Post [name,number, discription,isDigitsl]   #
#                                                                    #
######################################################################

@app.route('/sensors', methods=['GET','POST'])
def handle_post():
########################### GET  REQUEST ############################
   if request.method == 'GET':
      response = {}                              ## response the get request 
      conn = sqlite3.connect(os.getenv('PATH_2_DB'))          ## connect to DB
      cursor = conn.cursor()                     ## get a cursor
      cursor.execute("select * from sensor")

      rows = cursor.fetchall()                   ## get data from DB and put it in rows
      ## if rows get data of one sensor or more than one sensor , start counting and get each row in response
      if len(rows) >= 1:                        
         cnt = 0                                 ## counter for sensor
         for row in rows:
            response[cnt] = {}
            response[cnt]['id'] = row[0]
            response[cnt]['name'] = row[1]
            response[cnt]['number'] = row[2]
            response[cnt]['discription'] = row[3]
            response[cnt]['isDigital'] = row[4]
            response[cnt]['sensor_data'] = row[5]
            cnt = cnt + 1
          
         response['status_code'] = 201          ## if response get data return 201  
      else:
         response['status_code'] = 401          ## if response can't get data return 401

      conn.commit()                             ## commit
      conn.close()                              ## cleanup
      return jsonify(response)                  ## present data as json file 

########################### POST REQUEST ############################
   elif request.method == 'POST':
      sensor_name = request.form['name']
      sensor_number = request.form['number']
      sensor_discription = request.form['discription']
      sensor_isDigital = request.form['isDigital']
      ## check if data is correct and store it in DB
      if (sensor_name is not None and sensor_number is not None and sensor_discription is not None and sensor_isDigital is not None):
         conn = sqlite3.connect(os.getenv('os.getenv('PATH_2_DB')'))                                                         ## connect to DB
         cursor = conn.cursor()                                                                    ## get a cursor
         sql = "INSERT INTO sensor (name, number, discription, isDigital) values (?,?,?,?)"
         cursor.execute(sql, (sensor_name, sensor_number, sensor_discription, sensor_isDigital))   ## execute to insert data in DB
         conn.commit()                                                                             ## commit
         conn.close()                                                                              ## cleanup
         ## if data is correct and stored in DB return POST request handled
         return "POST request handled.\n"
      else:
         ## if data is not correct and stored in DB return Missing info in POST request
         return "Missing info in POST request.\n"

###########################################################
#   Description :  Route of sensor with ID for each one   #
#   methods     :  Get data from DB                       #
#                                                         #
###########################################################

@app.route('/sensors/<int:id_>', methods=['GET', 'DELETE'])
def get_sensor(id_):                                                   ## get ID to get its data
   if request.method == 'GET':
      response = {}                                                    ## response the get request 
      conn = sqlite3.connect(os.getenv('PATH_2_DB'))                                ## connect to DB
      cursor = conn.cursor()                                           ## get a cursor
      cursor.execute("select * from sensor where id=(?)", (id_,))      ## execute data with ID
      rows = cursor.fetchall()                                         ## get data from DB and put it in rows
      ## if rows get data of sensor id , start to take sensor's data
      if len(rows) == 1:
         row = rows[0]
         response['id'] = row[0]
         response['name'] = row[1]
         response['number'] = row[2]
         response['discription'] = row[3]
         response['isDigital'] = row[4]
         response['sensor_data'] = row[5]
         response['status_code'] = 201                                 ## if response get data return 201 
      else:
         response['status_code'] = 401                                 ## if response can't get data return 401 
      conn.commit()                                                    ## commit
      conn.close()                                                     ## cleanup
      return jsonify(response)                                         ## present data as json file
   elif request.method == 'DELETE':
      action_msg = "the sensor with id "+ str(id_) + " is deleted"
      response = {}                                                    ## response the get request 
      conn = sqlite3.connect(os.getenv('PATH_2_DB'))                                ## connect to DB
      cursor = conn.cursor()                                           ## get a cursor
      cursor.execute("delete from sensor where id=(?)", (id_,))        ## execute data with ID
      sql = "INSERT INTO system_log(log_message) VALUES (?)"
      cursor.execute(sql, (action_msg,)) 
      response['status_code'] = 201                                    ## if response get data return 201 
      response['message'] = action_msg 
      conn.commit()                                                    ## commit
      conn.close()                                                     ## cleanup
      return jsonify(response) 

###########################################################
#   Description :  Route of actuators                     #
#   methods     :  Get ,post                              #
#                                                         #
###########################################################

@app.route('/actuators', methods=['POST', 'GET'])
def handle_actuator_post():
###################  GET REQUEST   #########################
   if request.method == 'GET':
      response = {}                                           ## response the get request 
      conn = sqlite3.connect(os.getenv('PATH_2_DB'))                       ## connect to DB
      cursor = conn.cursor()                                  ## get a cursor
      cursor.execute("select * from actuator")                ## execute data 
      rows = cursor.fetchall()                                ## get data from DB and put it in rows
       ## if rows get data of one actuator or more than one sensor , start counting and get each row in response
      if len(rows) >= 1:                                      
         cnt = 0                                               ## counter for actuators
         for row in rows:
            response[cnt] = {}
            response[cnt]['id'] = row[0]
            response[cnt]['name'] = row[1]
            response[cnt]['number'] = row[2]
            response[cnt]['discription'] = row[3]
            response[cnt]['isDigital'] = row[4]
            response[cnt]['value'] = row[5]
            response[cnt]['type'] = row[6]
            
            cnt = cnt + 1    
         response['status_code'] = 201                         ## if response get data return 201 
      else:
         response['status_code'] = 401                         ## if response can't get data return 401
      conn.commit()                                            ## commit
      conn.close()                                             ## cleanup
      return jsonify(response)                                 ## present data as json file
###################  POST REQUEST  #########################
   if request.method == 'POST':
      actuator_name = request.form['name']
      actuator_number = request.form['number']
      actuator_discription = request.form['discription']
      actuator_isDigital = request.form['isDigital']
       ## check if data is correct and store it in DB
      if (actuator_name is not None and actuator_number is not None and actuator_discription is not None and actuator_isDigital is not None):
         conn = sqlite3.connect(os.getenv('PATH_2_DB'))                                                                 ## connect to DB
         cursor = conn.cursor()                                                                            ## get a cursor
         sql = "INSERT INTO actuator (name, number, discription, isDigital) values (?,?,?,?)"
         cursor.execute(sql, (actuator_name, actuator_number, actuator_discription, actuator_isDigital))   ## execute INSERT
         conn.commit()                                                                                     ## commit
         conn.close()                                                                                      ## cleanup
         ## if data is correct and stored in DB return POST request handled
         return "POST request handled.\n"
      else:
         ## if data is not correct and stored in DB return Missing info in POST request
         return "Missing info in POST request.\n"

###########################################################
#   Description :  Route of actuator with ID for each one #
#   methods     :  Get data from DB                       #
#                                                         #
###########################################################

@app.route('/actuators/<int:id_>', methods=['GET', 'DELETE'])
def get_actuator(id_):                                                       ## get ID to get its data
   if request.method == 'GET':                                                
      response = {}                                                          ## response the get request 
      conn = sqlite3.connect(os.getenv('PATH_2_DB'))                                      ## connect to DB
      cursor = conn.cursor()                                                 ## get a cursor
      cursor.execute("select * from actuator where id=(?)", (id_,)) 

      rows = cursor.fetchall()                                               ## get data from DB and put it in rows
     ## if rows get data of sensor id , start to take sensor's data
      if len(rows) == 1:
         row = rows[0]
         response['id'] = row[0]
         response['name'] = row[1]
         response['number'] = row[2]
         response['discription'] = row[3]
         response['isDigital'] = row[4]
         response['status_code'] = 201                                        ## if response get data return 201 
      else:
         response['status_code'] = 401                                       ## if response can't get data return 401 
      conn.commit()                                                          ## commit
      conn.close()                                                           ## cleanup
      return jsonify(response)                                               ## present data as json file
   elif request.method == 'DELETE':
      action_msg = "the actuator with id "+ str(id_) + " is deleted"
      response = {}                                                    ## response the get request 
      conn = sqlite3.connect(os.getenv('PATH_2_DB'))                                ## connect to DB
      cursor = conn.cursor()                                           ## get a cursor
      cursor.execute("delete from actuator where id=(?)", (id_,))        ## execute data with ID
      sql = "INSERT INTO system_log(log_message) VALUES (?)"
      cursor.execute(sql, (action_msg,)) 
      response['status_code'] = 201                                    ## if response get data return 201 
      response['message'] = action_msg 
      conn.commit()                                                    ## commit
      conn.close()                                                     ## cleanup
      return jsonify(response) 




#############################################################
#   Description :  Route actuators (servo) with ID          #
#   methods     :  POST servo [angle]                       #
#                                                           #
#############################################################
@app.route('/actuators/set_action/<int:id_>', methods=['POST'])
def control_servo(id_):                                                     ## get ID to get its data
   response = {}                                                            
   value = int(request.form['value'])
   action_type = request.form['action_type']

                                          
   # control.change_servo_angle(data)                                         ## control servo to change its angle
   # action_msg = "the actuator" + str(id_) + " is rotated by " + str(data) + " degree"

<<<<<<< HEAD
   conn = sqlite3.connect(PATH_2_DB)                                        ## connect to DB
=======
   conn = sqlite3.connect(os.getenv('PATH_2_DB'))                                        ## connect to DB
>>>>>>> 8e335bd79015d25fde53fe1a40d8729abbe730e6
   cursor = conn.cursor()      

   sql_1 = "INSERT INTO system_log(log_message) VALUES (?)"
   sql_2 = "UPDATE actuator SET value=(?), type=(?) WHERE id=(?)"

   # cursor.execute(sql_1, (action_msg,))
   cursor.execute(sql_2, (value, action_type, id_))                                      ## execute INSERT
   
   conn.commit()                                                           ## commit
   conn.close()                                                            ## cleanup
   # response['action'] = action_msg
   response['status_code'] = 201                                           ## if response get data return 201 
   return jsonify(response)                                                ## present data as json file


# #############################################################
# #   Description :  Route actuators (servo) with ID          #
# #   methods     :  POST servo [angle]                       #
# #                                                           #
# #############################################################
# @app.route('/actuators/servo/<int:id_>', methods=['POST'])
# def control_servo(id_):                                                     ## get ID to get its data
#    response = {}                                                            
#    data = int(request.form['value'])                                        ## take servo angle and store it in data variable
#    control.change_servo_angle(data)                                         ## control servo to change its angle
#    action_msg = "the servo" + str(id_) + " is rotated by " + str(data) + " degree"
<<<<<<< HEAD
#    conn = sqlite3.connect(PATH_2_DB)                                        ## connect to DB
=======
#    conn = sqlite3.connect(os.getenv('PATH_2_DB'))                                        ## connect to DB
>>>>>>> 8e335bd79015d25fde53fe1a40d8729abbe730e6
#    cursor = conn.cursor()                                                   ## get a cursor
#    sql = "INSERT INTO system_log(log_message) VALUES (?)"
#    cursor.execute(sql, (action_msg,))                                      ## execute INSERT
#    conn.commit()                                                           ## commit
#    conn.close()                                                            ## cleanup
#    response['action'] = action_msg
#    response['status_code'] = 201                                           ## if response get data return 201 
#    return jsonify(response)                                                ## present data as json file
 

# #############################################################
# #   Description :  Route of Actuators (LED) with ID         #
# #   methods     :  POST led [brightness]                    #
# #   URL         :  /actuators/led/<int:id_>                 #
# #############################################################

# @app.route('/actuators/led/<int:id_>', methods=['POST'])
# def control_led(id_):                                                    ## get ID to get its data
#    response = {}
#    data = int(request.form['value'])                                ## take led brightness and store it in data variable
#    control.change_brightness(data)
#    action_msg = "the led" + str(id_) + "'s brightness is " + str(data) 

<<<<<<< HEAD
#    conn = sqlite3.connect(PATH_2_DB)                                     ## connect to DB
=======
#    conn = sqlite3.connect(os.getenv('PATH_2_DB'))                                     ## connect to DB
>>>>>>> 8e335bd79015d25fde53fe1a40d8729abbe730e6
#    cursor = conn.cursor()                                                ## get a cursor
#    sql = "INSERT INTO system_log(log_message) VALUES (?)"
#    cursor.execute(sql, (action_msg,))                                    ## execute INSERT
#    conn.commit()                                                         ## commit
#    conn.close()                                                          ## cleanup

#    response['action'] = action_msg
#    response['status_code'] = 201                                         ## if response get data return 201
#    return jsonify(response)                                              ## present data as json file



#############################################################
#   Description :  Route of sensor_log with ID for each one #
#   methods     :  Get data from sensor_log table in DB     #
#                                                           #
#############################################################
@app.route('/system_log', methods=['GET'])
def get_sensor_log():
   if request.method == 'GET':                                               ## get ID to get its data
      response = {}                                                          ## response the get request 
      conn = sqlite3.connect(os.getenv('PATH_2_DB'))                                      ## connect to DB
      cursor = conn.cursor()                                                 ## get a cursor
      cursor.execute("select * from system_log")                             ## execute data 
      rows = cursor.fetchall()                                               ## get data from DB and put it in rows
      ## if rows get data of one sensor or more than one sensor , start counting and get each row in response             
      if len(rows) >= 1:
         cnt = 0                                                           ## counter for sensors
         for row in rows:
            response[cnt] = {}
            response[cnt]['id'] = row[0]
            response[cnt]['log_message'] = row[1]
            response[cnt]['time'] = row[2]
            response[cnt]['type'] = row[3]
            cnt = cnt + 1
         response['status_code'] = 201                                        ## if response get data return 201 
      else:
         response['status_code'] = 401                                       ## if response can't get data return 401 
      conn.commit()                                                          ## commit
      conn.close()                                                           ## cleanup
      return jsonify(response)                                               ## present data as json file


if __name__ == '__main__':
   app.run()