import sys
sys.path.append(".")

import os
from helper_methods import helpers

SERVICE_NAME = "mqtt"

def invoke(services):
    if(SERVICE_NAME in services.keys()):
            print("Loading {name} plugin".format(name=SERVICE_NAME))
            return getConfigSection()

def getConfigSection():
    output = """
[[inputs.mqtt_consumer]]
servers = ["mqtt://mqtt:1883"]
topics = [
    "sensors/#",
    "balena/#"
]

data_format = "json"
"""

    stringFields = os.environ.get('MQTT_INPUT_STRINGS_FIELDS')
    if(stringFields is not None):
      stringFieldsSection = helpers.formatStringField(stringFields)
      output = output + stringFieldsSection

    return output