from dotenv import load_dotenv
import os
import sqlite3
from time import sleep
import log

class sensor():
    def __init__(self):
        self.conn = sqlite3.connect(os.getenv('PATH_2_DB'))                                      
        self.cursor = self.conn.cursor() 
        self.response = {} 
        self.temp_id = 1
        self.humidity_id = 2 
        self.adc_id = 3
        # self.log_obj = log.log()

    def get_all(self):
        self.cursor.execute("select * from sensor")               
        rows = self.cursor.fetchall()                                
        if len(rows) >= 1:                                      
            cnt = 0                                            
            for row in rows:
                self.response[cnt] = {}
                self.response[cnt]['id'] = row[0]
                self.response[cnt]['name'] = row[1]
                self.response[cnt]['number'] = row[2]
                self.response[cnt]['discription'] = row[3]
                self.response[cnt]['isDigital'] = row[4]
                self.response[cnt]['sensor_data'] = row[5] 
                cnt = cnt + 1    
            self.response['status_code'] = 201                         
        else:
            self.response['status_code'] = 401
        self.close()
        return self.response   

    def get_id(self, id):
        self.cursor.execute("select * from sensor where id=(?)", (id,)) 
        rows = self.cursor.fetchall()                                               

        if len(rows) == 1:
            row = rows[0]
            self.response['id'] = row[0]
            self.response['name'] = row[1]
            self.response['number'] = row[2]
            self.response['discription'] = row[3]
            self.response['isDigital'] = row[4]
            self.response['sensor_data'] = row[5]
            self.response['status_code'] = 201                                      
        else:
            self.response['status_code'] = 401   
        self.close()  
        return self.response 
    
    def add(self, name, number, discription, isDigital):
        if (name is not None and number is not None and discription is not None and isDigital is not None):                                                         
            sql = "INSERT INTO sensor (name, number, discription, isDigital) values (?,?,?,?)"
            self.cursor.execute(sql, (name, number, discription, isDigital))                                             
            self.response['status_code'] = 201
        else:
            self.response['status_code'] = 401
        self.close()
        return self.response
    
    def remove(self, id):
        action_msg = "the sensor with id "+ str(id_) + " is deleted"
        self.cursor.execute("delete from actuator where id=(?)", (id,))  
        sql = "INSERT INTO system_log(log_message, type) VALUES (?,?)"
        self.cursor.execute(sql, (action_msg, "Reading")) 
        self.response['status_code'] = 201                                 
        self.response['message'] = action_msg 
        self.close()
        return self.response
        
    def update_temerature(self, value):
        sql_statement = "UPDATE sensor SET sensor_data=(?) WHERE id=(?)"
        self.cursor.execute(sql_statement,(value, self.temp_id))          
        self.close()

    def update_humidity(self, value):
        sql_statement = "UPDATE sensor SET sensor_data=(?) WHERE id=(?)"
        self.cursor.execute(sql_statement,(value, self.humidity_id))         
        self.close()
        
    def update_adc(self, value):
        sql_statement = "UPDATE sensor SET sensor_data=(?) WHERE id=(?)"
        self.cursor.execute(sql_statement,(value,self.adc_id)) 
        self.close()         
        
    def close(self):
        self.conn.commit()                          
        self.conn.close()