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
    # https://github.com/influxdata/telegraf/blob/master/docs/DATA_FORMATS_INPUT.md
    format = os.environ.get('MQTT_DATA_FORMAT') or "json"
    
    output = """
[[inputs.mqtt_consumer]]
servers = ["mqtt://mqtt:1883"]
topics = [
    "sensors/#",
    "balena/#"
]

data_format = "{format}"
""".format(format=format)

    stringFields = os.environ.get('MQTT_INPUT_STRINGS_FIELDS')
    if(stringFields is not None):
      stringFieldsSection = helpers.formatStringField(stringFields)
      output = output + stringFieldsSection

    return output