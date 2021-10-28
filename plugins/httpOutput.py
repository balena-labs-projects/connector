import os

SERVICE_NAME = "Http Push"

def invoke(services):
    url = os.environ.get('HTTP_PUSH_URL') or None
    if(url is None):
        return None
    print("Loading {name} plugin".format(name=SERVICE_NAME))
    return getConfigSection(url)    

def getConfigSection(url):
    output = """
[[outputs.http]]
  url = "{url}"
  data_format = "json"
[outputs.http.headers]
  Content-Type = "application/json"
""".format(url=url)
    return output


