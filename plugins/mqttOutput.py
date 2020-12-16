import os

SERVICE_NAME = "MQTT Push"

def invoke(services):
    server = os.environ.get('MQTT_OUTPUT_SERVER') or None
    port = os.environ.get('MQTT_OUTPUT_PORT') or '1883'
    if(server is None):
        return None
    print("Loading {name} plugin".format(name=SERVICE_NAME))
    return getConfigSection(server, port)    

def getConfigSection(server, port):
    output = """
[[outputs.mqtt]]
  servers = ["{url}:{port}"]
  topic_prefix = "balena"
  data_format = "json"
  qos = 2
""".format(url=server, port=port)

    username = os.environ.get('MQTT_OUTPUT_USERNAME')
    if(username is not None):
        usernameSection = """  username = '{value}'\n""".format(value=username)
        output = output + usernameSection
    
    password = os.environ.get('MQTT_OUTPUT_PASSWORD')
    if(password is not None):
        passwordSection = """  password = '{value}'\n""".format(value=password)
        output = output + passwordSection

    return output


