import os

SERVICE_NAME = "External Http Pull"

def invoke(services):
    name = os.environ.get('EXTERNAL_HTTP_PULL_NAME') or "ExternalHttpPull"
    url = os.environ.get('EXTERNAL_HTTP_PULL_URL') or None
    if(url is None):
        return None
    print("Loading {name} plugin".format(name=SERVICE_NAME))
    return getConfigSection(url, name)    

def getConfigSection(url, name):
    output = """
[[inputs.http]]
  ## One or more URLs from which to read formatted metrics
  urls = [
    "{url}"
  ]
  method = "GET"
  data_format = "json"
  name_override = "{name}"
""".format(url=url, name=name)
    return output


