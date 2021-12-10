# This file is intended to be run when sensors are not connected, 
# or when running in an environment without the RPi.GPIO library. 
# It uses a file that generates random numbers to represent sensor 
# data, and there is no button functionality.

import cherrypy
import time
import threading
import json
from fakesensors import getFakeTemp, getFakeHumidity, getFakeDistance, getFakeGyroX, getFakeGyroY
#from sensors import readHumidity, readTemp, readDistance, alert
from gpiozero import Button
import os

humidity = 0
gyro = [0,0]
data = {}
alerts = {}
armed = True

#button = Button(25)


def toggleArm():
    global armed
    armed = not armed

#button.when_pressed = toggleArm


def fakemonitor():
    while True:
        global armed
        global gyro
        # print(f"array values:\ngyro[0]:\t{gyro[0]}\ngyro[1]:\t{gyro[1]}\n")
        if armed:
            # print("🔵 Monitoring...")
            distance = getFakeDistance()
            # print("📏 " + str(round(distance, 3)))

            if distance < 10:
                fakealert("Movement detected")
                tweet("Movement detected")

            gyroX = getFakeGyroX()
            gyroY = getFakeGyroY()
            # print(f"new gyroX:\t{gyroX}\nnew gyroY\t{gyroY}\n")
            differenceX = abs(gyro[0] - gyroX)
            differenceY = abs(gyro[1] - gyroY)
            # print(f"gyro X difference:\t{differenceX}\ngyro Y difference:\t{differenceY}\n********************************************\n\n")
            if differenceX > 20 or differenceY > 20:
                fakealert("Monitoring device moved")
                tweet("Monitoring device moved")

            gyro[0] = gyroX
            gyro[1] = gyroY
        time.sleep(1)


def tweet(message):
    print("🟡 tweeting alert!!!", message)
    # command = f"python3 twitterbot.py '{message}'"
    #os.system(command)


# def monitor():
#     while True:
#         global armed
#         global alerts
#         if armed:
#             #print("MONITORING...")
#             distance = readDistance()
#             #print("DISTANCE FROM SENSOR: " + str(round(distance, 2)) )
#             if distance < 10:
#                 alerts[time.strftime("%a %b-%d-%Y %#I:%M:%S %p")] = "Movement detected"
#                 print("ALERT ALERT ALERT")
#                 thread = threading.Thread(target=tweet)
#                 thread.daemon = True
#                 thread.start()
#                 alert(3)
#         time.sleep(0.1)


def fakealert(message):
    global alerts
    print("🟡 ALERT ALERT", str(message))
    alerts[time.strftime("%a %b %d, %Y %#I:%M:%S %p")] = str(message)


class HomeMonitor(object):
    @cherrypy.expose
    def index(self):
        return open("dashboard-demo.html").read()

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

    # @cherrypy.expose
    # @cherrypy.tools.json_out()
    # def data(self):
    #     global data
    #     global humidity
    #     data["armed"] = armed
    #     result = readHumidity()
    #     if result:
    #         humidity, temp = result
    #         data["humidity"] = str(round(humidity, 1))
    #     temp = readTemp()
    #     if temp != None:
    #         data["tempC"] = str(round(temp, 1))
    #         data["tempF"] = str(round( (temp * 9 / 5) + 32, 1))
    #     JSON = json.dumps(data)
    #     return JSON

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
        t1 = threading.Thread(target=fakemonitor)
        t1.daemon = True
        t1.start()
        cherrypy.quickstart(HomeMonitor())
    except Exception:
        print("exception happened")
