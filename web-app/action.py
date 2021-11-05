from time import sleep
import threading
import control
import db 


class action_worker():
    def __init__(self):
        self.control = control.control()
        self.database = db.db()
        self.cursor = self.database.get_cursor()

    def start(self):
        myThread = threading.Thread(target=self.act)
        myThread.daemon = True
        myThread.start()

    def act(self):
        while True:
            self.cursor.execute("select * from actuator")
            rows = self.cursor.fetchall()
            if len(rows) >= 1:
                for row in rows:
                    self.handle(row[0], row[5], row[6])

            self.conn.commit()


    def handle(self, id, value, type):
        if id == 1:
            if type == "UPDATE":
                self.control.change_brightness(value, id)
            elif type == "OFF":
                self.control.change_brightness(value, id)
            elif type == "ON":
                self.control.change_brightness(value, id)

        elif id == 2:
            if type == "UPDATE":
                self.control.change_brightness(value, id)
            elif type == "OFF":
                self.control.change_brightness(value, id)
            elif type == "ON":
                self.control.change_brightness(value, id)

        elif id == 3:
            if type == "UPDATE":
                self.control.change_brightness(value, id)
            elif type == "OFF":
                self.control.change_brightness(value, id)
            elif type == "ON":
                self.control.change_brightness(value, id)

        elif id == 4:
            if type == "UPDATE":
                self.control.change_servo_angle(value)
            elif type == "OFF":
                self.control.change_servo_angle(0)
            elif type == "ON":
                self.control.change_servo_angle(90)
        elif id == 6:
            if type == "UPDATE":
                self.control.change_relay_status(value)
            elif type == "OFF":
                self.control.change_relay_status(0)
            elif type == "ON":
                self.control.change_relay_status(100)