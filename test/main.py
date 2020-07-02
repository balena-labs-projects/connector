import paho.mqtt.client as mqtt
import os
import random
import json
import time

def GetReading():
    return [
                {
                    'measurement': 'test',
                    'fields': {
                        'reading': int(random.randint(1,101))
                    }
                }
            ]

broker_address = os.environ.get('MQTT_ADDRESS') or "localhost" 
client = mqtt.Client("1")
client.connect(broker_address)

while(True):
    value = GetReading()
    print("Sending {value}".format(value=value))
    client.publish("sensors",json.dumps(value))
    time.sleep(5)


