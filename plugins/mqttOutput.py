import os

SERVICE_NAME = "MQTT Push"

def invoke(services):
    url = os.environ.get('MQTT_PUSH_URL') or None
    if(url is None):
        return None
    print("Loading {name} plugin".format(name=SERVICE_NAME))
    return getConfigSection(url)    

def getConfigSection(url):
    output = """
[[outputs.mqtt]]
  servers = ["{url}"]
  data_format = "json"
""".format(url=url)

    mqtt_username = os.environ.get('MQTT_PUSH_USERNAME')
    if(mqtt_username is not None):
        mqtt_username_section = """ 
        username = "{value}" """.format(value=mqtt_username)
        output = output + mqtt_username_section

    mqtt_password = os.environ.get('MQTT_PUSH_PASSWORD')
    if(mqtt_password is not None):
        mqtt_password_section = """ 
        password = "{value}" """.format(value=mqtt_password)
        output = output + mqtt_password_section

    topic_prefix = os.environ.get('MQTT_PUSH_TOPIC_PREFIX')
    if(topic_prefix is not None):
        topic_prefix_section = """ 
        topic_prefix = "{value}" """.format(value=topic_prefix)
        output = output + topic_prefix_section

    return output


