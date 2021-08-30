###########################################################
#                  IMPORT                                 #
###########################################################
from flask import Flask, request, jsonify
import sqlite3
import requests as req
import urllib3
from control import rpi_control_, dht_worker
from time import sleep
import RPi.GPIO as GPIO

###############  OBJECTS  ###############################
control = rpi_control_()           # Control object

#########################################################

http = urllib3.PoolManager()

PATH_2_DB = '/home/pi/Desktop/cvs_internship/web_app/cvs.db'

app = Flask(__name__)


thrd = dht_worker()
thrd.start()

###########################################################
#                                              #
###########################################################

@app.route('/sensors', methods=['GET','POST'])
def handle_post():
   if request.method == 'GET':
      response = {}
      conn = sqlite3.connect(PATH_2_DB)        ## connect to DB
      cursor = conn.cursor()                   ## get a cursor
      cursor.execute("select * from sensor")

      rows = cursor.fetchall()
      if len(rows) >= 1:
         cnt = 0
         for row in rows:
            response[cnt] = {}
            response[cnt]['id'] = row[0]
            response[cnt]['name'] = row[1]
            response[cnt]['number'] = row[2]
            response[cnt]['isDigital'] = row[3]
            cnt = cnt + 1
            
         response['status_code'] = 201
      else:
         response['status_code'] = 401

      conn.commit()  ## commit
      conn.close()   ## cleanup
      return jsonify(response)

   elif request.method == 'POST':
      sensor_name = request.form['name']
      sensor_number = request.form['number']
      sensor_discription = request.form['discription']
      sensor_isDigital = request.form['isDigital']

      if (sensor_name is not None and sensor_number is not None and sensor_discription is not None and sensor_isDigital is not None):
         conn = sqlite3.connect(PATH_2_DB)      ## connect to DB
         cursor = conn.cursor()                 ## get a cursor
         sql = "INSERT INTO sensor (name, number, discription, isDigital) values (?,?,?,?)"
         cursor.execute(sql, (sensor_name, sensor_number, sensor_discription, sensor_isDigital)) ## execute INSERT
         conn.commit()  ## commit
         conn.close()   ## cleanup
         return "POST request handled.\n"
      else:
         return "Missing info in POST request.\n"

@app.route('/sensors/<int:id_>', methods=['GET'])
def get_sensor(id_):
   if request.method == 'GET':
      response = {}

      conn = sqlite3.connect(PATH_2_DB)        ## connect to DB
      cursor = conn.cursor()                   ## get a cursor
      cursor.execute("select * from sensor where id=(?)", (id_,)) 
      rows = cursor.fetchall()
      if len(rows) == 1:
         row = rows[0]
         response['id'] = row[0]
         response['name'] = row[1]
         response['number'] = row[2]
         response['discription'] = row[3]
         response['isDigital'] = row[4]
         response['status_code'] = 201
      else:
         response['status_code'] = 401
      conn.commit()  ## commit
      conn.close()   ## cleanup
      return jsonify(response)

@app.route('/actuators', methods=['POST', 'GET'])
def handle_actuator_post():
   if request.method == 'GET':
      response = {}
      conn = sqlite3.connect(PATH_2_DB)        ## connect to DB
      cursor = conn.cursor()                   ## get a cursor
      cursor.execute("select * from actuator")

      rows = cursor.fetchall()
      if len(rows) >= 1:
         cnt = 0
         for row in rows:
            response[cnt] = {}
            response[cnt]['id'] = row[0]
            response[cnt]['name'] = row[1]
            response[cnt]['number'] = row[2]
            response[cnt]['isDigital'] = row[3]
            cnt = cnt + 1  
         response['status_code'] = 201
      else:
         response['status_code'] = 401
      conn.commit()  ## commit
      conn.close()   ## cleanup
      return jsonify(response)

   if request.method == 'POST':
      actuator_name = request.form['name']
      actuator_number = request.form['number']
      actuator_discription = request.form['discription']
      actuator_isDigital = request.form['isDigital']

      if (actuator_name is not None and actuator_number is not None and actuator_discription is not None and actuator_isDigital is not None):
         conn = sqlite3.connect(PATH_2_DB)      ## connect to DB
         cursor = conn.cursor()                 ## get a cursor
         sql = "INSERT INTO actuator (name, number, discription, isDigital) values (?,?,?,?)"
         cursor.execute(sql, (actuator_name, actuator_number, actuator_discription, actuator_isDigital)) ## execute INSERT
         conn.commit()  ## commit
         conn.close()   ## cleanup
         return "POST request handled.\n"
      else:
         return "Missing info in POST request.\n"

@app.route('/actuators/<int:id_>', methods=['GET'])
def get_actuator(id_):
   if request.method == 'GET':
      response = {}

      conn = sqlite3.connect(PATH_2_DB)        ## connect to DB
      cursor = conn.cursor()                   ## get a cursor
      cursor.execute("select * from actuator where id=(?)", (id_,)) 

      rows = cursor.fetchall()
      if len(rows) == 1:
         row = rows[0]
         response['id'] = row[0]
         response['name'] = row[1]
         response['number'] = row[2]
         response['discription'] = row[3]
         response['isDigital'] = row[4]
         response['status_code'] = 201
      else:
         response['status_code'] = 401
      conn.commit()  ## commit
      conn.close()   ## cleanup
      return jsonify(response)

@app.route('/sensor_log', methods=['GET'])
def get_sensor_log():
   if request.method == 'GET':
      response = {}
      conn = sqlite3.connect(PATH_2_DB)        ## connect to DB
      cursor = conn.cursor()                   ## get a cursor
      cursor.execute("select * from sensor_log")
      rows = cursor.fetchall()
      if len(rows) >= 1:
         cnt = 0
         for row in rows:
            response[cnt] = {}
            response[cnt]['id'] = row[0]
            response[cnt]['number'] = row[1]
            response[cnt]['time'] = row[2]
            response[cnt]['data'] = row[3]
            cnt = cnt + 1

         response['status_code'] = 201
      else:
         response['status_code'] = 401

      conn.commit()  ## commit
      conn.close()   ## cleanup
      return jsonify(response)


@app.route('/actuators/servo/<int:id_>', methods=['POST'])
def control_servo(id_):
   response = {}
   data = int(request.form['angle'])
   control.change_servo_angle(data)
   action_msg = "the servo" + str(id_) + " is rotated by " + str(data) + " degree"
   conn = sqlite3.connect(PATH_2_DB)      ## connect to DB
   cursor = conn.cursor()                 ## get a cursor
   sql = "INSERT INTO action_log (action_message) VALUES (?)"
   cursor.execute(sql, (action_msg,)) ## execute INSERT
   conn.commit()  ## commit
   conn.close()   ## cleanup
   response['action'] = action_msg
   response['status_code'] = 201
   return jsonify(response)

@app.route('/actuators/led/<int:id_>', methods=['POST'])
def control_led(id_):
   response = {}
   data = int(request.form['brightness'])
   control.change_brightness(data)
   action_msg = "the led" + str(id_) + "'s brightness is " + str(data) 

   conn = sqlite3.connect(PATH_2_DB)      ## connect to DB
   cursor = conn.cursor()                 ## get a cursor
   sql = "INSERT INTO action_log (action_message) VALUES (?)"
   cursor.execute(sql, (action_msg,)) ## execute INSERT
   conn.commit()  ## commit
   conn.close()   ## cleanup

   response['action'] = action_msg
   response['status_code'] = 201
   return jsonify(response)




if __name__ == '__main__':
   app.run()

 