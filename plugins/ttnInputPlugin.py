import os

def invoke(services):
    if((os.environ.get('ENABLE_EXTERNAL_HTTP_LISTENER') or '0') != '1'):
        return None
    return getConfigSection()    

def getConfigSection():
    output = """
[[inputs.http_listener_v2]]
  service_address = ":8080"
  methods = ["POST"]
  path = "/"

  data_format = "json"
"""

    if((os.environ.get('EXTERNAL_HTTP_LISTENER_JSON_QUERY') or '0') is '1'):
        jsonQuerySection = """json_query = "payload_fields" """
        output = output + jsonQuerySection

    return output