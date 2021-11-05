import sqlite3
import os

class db():
    def init_db(self):
        try:
            self.conn = sqlite3.connect(os.getenv('PATH_2_DB'))
        except Exception as ex:
           print(ex) 
    def get_cursor(self):
        return self.conn.cursor()


