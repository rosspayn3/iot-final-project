# *****************************************
# Name:         Ross Payne & Jacob Baltazar
# Problem Set:  Final Project
# Due Date:     Dec 16, 2021
# *****************************************

import cherrypy, time, threading, json
from fakesensors import getFakeTemp, getFakeHumidity, getFakeDistance
from sensors import readHumidity, readTemp, readDistance, alert
from gpiozero import Button
from gyrosensor import read_word_2c
import os

humidity = 45
data = {}
alerts = {}
armed = True

button = Button(25)


def toggleArm():
    global armed
    armed = not armed

button.when_pressed = toggleArm

def fakemonitor():
    while True:
        global armed
        if armed:
            print("🔵 Monitoring...")
            distance = getFakeDistance()
            print("📏 " + str( round(distance, 3)) )
            if distance < 10:
                fakealert()
        time.sleep(0.5)

def tweet(message):
    os.system("python3 twitterbot.py " + message)

def monitor():
    while True:
        global armed
        global alerts
        if armed:
            #print("MONITORING...")
            distance = readDistance()
            gyro_xout = read_word_2c(0x43)
            gyro_yout = read_word_2c(0x45)
            gyro_zout = read_word_2c(0x47)
            #print("DISTANCE FROM SENSOR: " + str(round(distance, 2)) )
            if distance < 10:
                alerts[time.strftime("%a %b-%d-%Y %#I:%M:%S %p")] = "Distance sensor triggered"
                print("ALERT ALERT ALERT")
                print("starting beeps")
                alert(3)
                tweet("Distance sensor triggered")
#            print("gyro x: ", gyro_xout)
#            print("gyro y: ", gyro_yout)
#            print("gyro z: ", gyro_zout)

            # JACOB'S ATTEMPTED SOLUTION TO DETECTING GYRO MOVEMENT
            # if abs(x) - abs(perv_read_x) > abs(gyro_xout - 600) or abs(y) - abs(perv_read_y) > abs(gyro_yout - 600) or abs(z) - abs(perv_read_z) > abs(gyro_zout - 600):
                 # do something

            if len(str(abs(gyro_xout))) > 3 or len(str(abs(gyro_yout))) > 3 or len(str(abs(gyro_zout))) > 3:
                alerts[time.strftime("%a %b-%d-%Y %#I:%M:%S %p")] = "Monitoring device moved"
                print("ALERT BOX MOVED")
                alert(3)
                tweet("Monitoring device moved")
        time.sleep(0.1)

def fakealert():
    global alerts
    print("🟡 ALERT ALERT")
    alerts[time.strftime("%a %b-%d-%Y %#I:%M:%S %p")] = "Movement detected"

class HomeMonitor(object):
    @cherrypy.expose
    def index(self):
        return open("dashboard.html").read()

    @cherrypy.expose
    def demo(self):
        return open("dashboard-demo.html").read()

    @cherrypy.expose
    def twitter(self):
        return open("twitter.html").read()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def fakedata(self):
        global data
        global humidity
        global armed
        data["armed"] = armed
        tempc = getFakeTemp()
        data["tempC"] = str(round(tempc, 1))
        data["tempF"] = str(round((tempc * 9 / 5) + 32, 1))
        humidity = getFakeHumidity()
        data["humidity"] = str(round(humidity, 1))
        JSON = json.dumps(data)
        return JSON

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def data(self):
        global data
        global humidity
        data["armed"] = armed
        result = readHumidity()
#        print("**********************\nhumidity: ", result)
        if result:
            humidity, temp = result
            data["humidity"] = str(round(humidity, 1))
        else:
            data["humidity"] = str(round(humidity, 1))
        temp = readTemp()
        if temp != None:
            data["tempC"] = str(round(temp, 1))
            data["tempF"] = str(round( (temp * 9 / 5) + 32, 1))
        JSON = json.dumps(data)
        return JSON

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def alerts(self):
        global alerts
        JSON = json.dumps(alerts)
        return JSON

    @cherrypy.expose
    def enable(self):
        if(cherrypy.request.remote.ip in ("127.0.0.1", "::1")):
            global armed
            armed = True
            cherrypy.response.cookie['armed'] = True
            print("🟢 alerts enabled")

    @cherrypy.expose
    def disable(self):
        if(cherrypy.request.remote.ip in ("127.0.0.1", "::1")):
            global armed
            armed = False
            cherrypy.response.cookie['armed'] = False
            print("🔴 alerts disabled")

    @cherrypy.expose
    def clearalerts(self):
        if(cherrypy.request.remote.ip in ("127.0.0.1", "::1")):
            global alerts
            alerts = {}
            print("🟡 alerts cleared")



if __name__ == "__main__":
    try:
        t1 = threading.Thread(target=monitor)
        t1.daemon = True
        t1.start()
        cherrypy.quickstart(HomeMonitor())
    except Exception:
        print("exception happened")
