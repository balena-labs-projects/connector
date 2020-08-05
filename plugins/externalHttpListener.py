import os

SERVICE_NAME = "External Http Listener"

def invoke(services):
    name = os.environ.get('EXTERNAL_HTTP_LISTENER_NAME')

    if(name is None):
        name = "ExternalHttpListener"
        if((os.environ.get('ENABLE_EXTERNAL_HTTP_LISTENER') or '0') != '1'):
            return None
    
    print("Loading {name} plugin".format(name=SERVICE_NAME))
    return getConfigSection(name)    

def getConfigSection(name):
    output = """
[[inputs.http_listener_v2]]
  service_address = ":8080"
  methods = ["POST"]
  path = "/"

  data_format = "json"
  name_override = "{name}"
""".format(name=name)

    json_query = os.environ.get('EXTERNAL_HTTP_LISTENER_JSON_QUERY')
    if(json_query is not None):
        jsonQuerySection = """json_query = "{value}" """.format(value=json_query)
        output = output + jsonQuerySection

    return output