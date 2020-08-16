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

    headers_found = False
    headers = ""
    for env_var,env_var_value in os.environ.items():
      if env_var.startswith('EXTERNAL_HTTP_PULL_HEADER_'):
        headers_found = True
        headers = headers + "    " + env_var[26:] + " = \"" + env_var_value + "\"\n"

    if headers_found == True:
      output = output + "  [inputs.http.headers]\n"
      output = output + headers

    return output