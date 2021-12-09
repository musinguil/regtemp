#!/usr/bin/python3
# coding : utf-8

import os
import json
import time

json_path = "/var/log/sensors.log"
service_list = ["networking", "ssh", "apache2"]
# service_state True mean the services are up
service_state = True

def callSensors():
    os.system("sensors -j > " + json_path)

def getTemp():
    file = open(json_path, "r")
    data = json.load(file)
    file.close()
    return data["cpu_thermal-virtual-0"]["temp1"]["temp1_input"]

while 1:
    callSensors()
    temperature = getTemp()
    if temperature >= 70 and service_state is True:
        for service in service_list:
            os.system("systemctl stop " + service)
        service_state = False
    elif temperature < 50 and service_state is False:
        for service in service_list:
            os.system("systemctl start " + service)
        service_state = True
    time.sleep(10)
