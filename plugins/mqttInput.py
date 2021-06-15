import os

SERVICE_NAME = "mqtt"

def invoke(services):
    if(SERVICE_NAME in services.keys()):
            print("Loading {name} plugin".format(name=SERVICE_NAME))
            return getConfigSection()

def getConfigSection():
    output = """
[[inputs.mqtt_consumer]]
servers = ["mqtt:1883"]
topics = [
    "sensors/#",
]

data_format = "json"
"""

    string_fields = os.environ.get('MQTT_INPUT_STRINGS_FIELDS')
    if(string_fields is not None):
      splitFields = string_fields.split(",")
      fieldList = ""

      for field in splitFields:
        field = field.strip().strip('\"')
        field = "\"" + field + "\","

        fieldList = fieldList + field

        string_fields = fieldList
      
      stringFieldsSection = """  json_string_fields = [{value}]\n""".format(value=string_fields)
      output = output + stringFieldsSection

    return output