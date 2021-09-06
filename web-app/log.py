from dotenv import load_dotenv
import os
import sqlite3

class log():
    def __init__(self):
        self.conn = sqlite3.connect(os.getenv('PATH_2_DB'))                                      ## connect to DB
        self.cursor = self.conn.cursor() 
        self.response = {}  

    def get_all(self):
        self.cursor.execute("select * from system_log")                              
        rows = self.cursor.fetchall()      
                     
        if len(rows) >= 1:
            cnt = 0                                                           ## counter for sensors
            for row in rows:
                self.response[cnt] = {}
                self.response[cnt]['id'] = row[0]
                self.response[cnt]['log_message'] = row[1]
                self.response[cnt]['time'] = row[2]
                self.response[cnt]['type'] = row[3]
                cnt = cnt + 1
            self.response['status_code'] = 201                                        ## if response get data return 201 
        else:
            self.response['status_code'] = 401
        return self.response
    def add(self, msg, type):
        print("sfdjbrskhf")
    def __del__(self):                                                                                                 ## if response can't get data return 401 
        self.conn.commit()                          
        self.conn.close()
