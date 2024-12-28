#!/usr/bin/env python3

import time
import paho.mqtt.client as mqtt
import argparse
import signal
import logging
import json
import re
import csv
import os

from logging.handlers import TimedRotatingFileHandler
from htheatpump.htheatpump import HtHeatpump
from htheatpump.htparams import HtDataTypes, HtParams
from htheatpump.utils import Timer

from ha_sensors import *

from mqtt_homeassistant_utils import HADevice

#global Variables
loopEnabled = True
HP_DEVICE = ""
HP_BAUD = ""

MQTT_CLIENT_IDENTIFIER = ""
MQTT_TOPIC = ""
MQTT_BROKER_ADDRESS = ""
MQTT_PORT = 0
MQTT_QOS = 0
MQTT_USER = ""
MQTT_PASS = ""
HADEVICE = None

def writeCSV(data: dict) -> None:
    with open('values.csv', 'a') as f:
        w = csv.DictWriter(f,fieldnames=data.keys(), dialect='excel', delimiter=';')
        
        if os.path.getsize('values.csv') == 0:
            w.writeheader()

        w.writerow(data)   

#Read general information
def readDeviceInfo() -> HADevice:
    hp = HtHeatpump(HP_DEVICE, baudrate=HP_BAUD)
    try:
        hp.open_connection()
        hp.login()

        version = hp.get_version()
        sn = str(hp.get_serial_number())

        device = HADevice(
            manufacturer="Heliotherm", 
            model="Basic Comfort",
            name="Heliotherm Heat Pump",
            sw_version=version[0],
            identifiers=[sn]
        )

    except Exception as ex:
        device = HADevice(
            manufacturer="Heliotherm", 
            model="Basic Comfort",
            name="Heliotherm Heat Pump"
        )

    finally:
        hp.logout()  # try to logout for an ordinary cancellation (if possible)
        hp.close_connection()

    return device

def modifyStats(data: dict) -> dict:
    norm_values = {}
    for name, val in data.items():
        
        #normalize key
        new_key = re.sub(r'[^A-Za-z]', '', name).lower()


        new_val = val

        if new_key == "betriebsart":
            match new_val:
                case 0:
                    new_val = "Aus"
                case 1:
                    new_val = "Auto"
                case 2:
                    new_val = "Kühlen"
                case 3:
                    new_val = "Sommer"
                case 4:
                    new_val = "Dauerbetrieb"
                case 5:
                    new_val = "Absenken"
                case 6:
                    new_val = "Urlaub"
                case 7:
                    new_val = "Party"
                case _:
                    new_val = None

        #if it is boolean convert to string
        if isinstance(new_val, bool):
            if new_val:
                new_val = "ON"
            else:
                new_val = "OFF"

        #if it is a number and smaller then -50, then kill data
        try:
            new_val = float(new_val)
            if new_val <= -50.:
                new_val = None
        except ValueError:
            pass
        
        norm_values[new_key] = new_val

    return norm_values


#Read contents 
def readStats() -> dict:
    hp = HtHeatpump(HP_DEVICE, baudrate=HP_BAUD)
    try:
        hp.open_connection()
        hp.login()

        values = hp.query()
        return modifyStats(values)

    except Exception as ex:
        logging.exception(ex)

    finally:
        hp.logout()  # try to logout for an ordinary cancellation (if possible)
        hp.close_connection()

#push auto discovery info for home assistant
def pushMqttConfig(mqttclient: mqtt.Client, device: HADevice) -> None:
    logging.info("pushing online message and auto discovery info for home assistant")
    
    #Status/Alive Message
    mqttclient.publish(MQTT_TOPIC + "/state", "online", qos=MQTT_QOS, retain=True)

    allSensors = createSensors(MQTT_TOPIC, device, MQTT_QOS)
    for sensor in allSensors:
        sensor.publish(mqttclient)
       
def pushMqttStats(mqttclient, mydata: dict):  
    mqttclient.publish(MQTT_TOPIC + "/values", json.dumps(mydata), qos=MQTT_QOS)

def mqttOnConnect(client, userdata, flags, rc):
    if rc==0:
        logging.info('MQTT connected')
        client.connected_flag = True
        pushMqttConfig(client, HADEVICE)
    else:
        logging.info("Bad connection Returned code=",rc)
    
def mqttOnDisconnect(client, userdata, rc):
    logging.info("MQTT disconnected")
    client.connected_flag = False

def signalHandler(signal, frame):
    global loopEnabled
    print("Got quit signal, cleaning up...")
    loopEnabled = False

def parseArguments():
    global HP_DEVICE
    global HP_BAUD
    global MQTT_CLIENT_IDENTIFIER
    global MQTT_TOPIC
    global MQTT_BROKER_ADDRESS
    global MQTT_PORT
    global MQTT_QOS
    global MQTT_USER
    global MQTT_PASS

    parser = argparse.ArgumentParser(
            description="Reads stats from Heliotherm heat pump and push to MQTT", 
            epilog="Report bugs, comments or improvements to https://github.com/Xembalo/htmqtt",
            usage="%(prog)s [options]")
    group = parser.add_argument_group('Heat pump')
    group.add_argument("-d", "--device", default="/dev/ttyUSB0", type=str, help="serial device connection to heat pump (default: %(default)s)", metavar='device')
    group.add_argument("-b", "--baudrate", default=115200, type=int, choices=[9600, 19200, 38400, 57600, 115200], help="baudrate of serial connection (as configured on the heat pump) (default: %(default)s)", metavar='baud')

    group = parser.add_argument_group('MQTT')  
    group.add_argument("-i", "--mqtt_client_identifier", help="MQTT client identifier", metavar='identifier')
    group.add_argument("-t", "--mqtt_topic",             help="Topic for stats", metavar='topic')
    group.add_argument("-x", "--mqtt_host",              help="Host or IP of your mqtt broker (e.g. localhost)", metavar='host/ip')
    group.add_argument("-p", "--mqtt_port",              type=int, default=1883, help="port of your mqtt broker (default: %(default)s)", metavar='port')
    group.add_argument("-u", "--mqtt_user",              help="Username for your mqtt broker", metavar='username')
    group.add_argument("-k", "--mqtt_pass",              help="Password for your mqtt broker", metavar='password')
    group.add_argument("-q", "--mqtt_qos",               type=int, choices=[0, 1], default=0, help="QoS of your messages [0/1] (default: %(default)s)", metavar='qos-level')
   
    args = parser.parse_args()

    HP_DEVICE                   = args.device
    HP_BAUD                     = args.baudrate
    MQTT_CLIENT_IDENTIFIER      = args.mqtt_client_identifier
    MQTT_TOPIC                  = args.mqtt_topic
    MQTT_BROKER_ADDRESS         = args.mqtt_host
    MQTT_PORT                   = args.mqtt_port
    MQTT_USER                   = args.mqtt_user
    MQTT_PASS                   = args.mqtt_pass
    MQTT_QOS                    = args.mqtt_qos


def main():
    global HADEVICE
    
    # Logger erstellen
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = TimedRotatingFileHandler("htmqtt.log", when="midnight", interval=1, backupCount=7, encoding="utf-8")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    logging.info('Script started')

    parseArguments()

    #Signal Handler for interrupting the loop
    signal.signal(signal.SIGINT, signalHandler)

    mqtt.Client.connected_flag = False

    client = mqtt.Client(MQTT_CLIENT_IDENTIFIER)
    client.on_connect = mqttOnConnect
    client.on_disconnect = mqttOnDisconnect

    if MQTT_USER != "":
        client.username_pw_set(username=MQTT_USER,password=MQTT_PASS)

    client.will_set(MQTT_TOPIC + "/state","offline",MQTT_QOS,retain=True)

    HADEVICE = readDeviceInfo()

    try:
        logging.info("try to connect")
        client.connect(MQTT_BROKER_ADDRESS, MQTT_PORT)
        logging.info("starting the MQTT background loop")  
        client.loop_start()
    except:
        #if connection was not successful, try it in next loop again
        logging.info("connection was not successful, try it in next loop again")

    while loopEnabled:
        logging.info("main loop")

        #push to mqtt and quits connection
        if client.connected_flag: 
            data = readStats()
            pushMqttStats(client, data)
        
        #wait 60 seconds
        time.sleep(60.0 - time.time() % 60.0)

    #send last message
    client.publish(MQTT_TOPIC + "/state", "offline", qos=MQTT_QOS, retain=True)
    client.loop_stop()  
    client.disconnect() 

if __name__ == "__main__":
   main()
