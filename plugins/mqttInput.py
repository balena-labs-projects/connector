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

    return output