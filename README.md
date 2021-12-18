# CS 4363: Internet of Things Developement
### Final Project
#### This lab is an extension of Problem Set 2

### Libraries used in `home-monitor.py`:
1. `cherrypy` - A web framework for Python that can be used to build a functional web server.
2. `gpiozero` - A simple interface for GPIO devices.
3. `json` - A Python module that aids in encoding and decoding JSON format data. All sensor information is sent to the web dashboard in JSON format.
4. `threading` - A Python module that provides functionality for creating and managing threads in a Python environment. In this project, it is used to spawn a new thread which runs the monitor function in home-monitor.py so that cherrypy can continue to serve data.
5. `time` - A Python module that provides various time related functions. In this project, it is used for controlling the polling rate of sensors, controlling the duration of buzzer sounds, and providing a timestamp for alert events such as detected movement from the distance sensor.


### Libraries used in `sensors.py`:
1. `gpiozero` - A simple interface for GPIO devices.
2. `os` - A Python module that facilitates various functions dealing with reading/writing files and directories.
3. `RPi.GPIO` - An interface for GPIO devices that is less abstracted than gpiozero.
4. `time` - A Python module that provides various time related functions. In this project, it is used for controlling the polling rate of sensors, controlling the duration of buzzer sounds, and providing a timestamp for alert events such as detected movement from the distance sensor.

### Libraries used in `twitterbot.py`:
1. `Twython` - A Python wrapper for the Twitter API that supports both normal and streaming Twitter APIs.

### Configuration of sensor connections
1. GPIO4 - DS18B201 temperature sensor
2. GPIO17 - Humiture sensor
3. GPIO22 - HC-SR04 ultrasonic sensor `echo`
4. GPIO23 - HC-SR04 ultrasonic sensor `trigger`
5. GPIO24 - Active buzzer
6. GPIO25 - Button
7. SDA1 - MPU-6050 Gyro Module `SDA`
8. SCL1 - MPU-6050 Gyro Module `SCL`
9. USB port - Webcam
