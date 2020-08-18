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
  urls = ["{url}"]
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

    json_query = os.environ.get('EXTERNAL_HTTP_PULL_JSON_QUERY')
    if(json_query is not None):
        jsonQuerySection = """ json_query = "{value}" """.format(value=json_query)
        output = output + jsonQuerySection
    
    string_fields = os.environ.get('EXTERNAL_HTTP_PULL_STRINGS_FIELDS')
    splitFields = string_fields.split(",")
    fields = ""
    fieldList = ""

    for field in splitFields:
      field = field.strip().strip('\"')
      field = "\"" + field + "\","

      fieldList = fieldList + field

      string_fields = fieldList

    if(string_fields is not None):
        stringFieldsSection = """ json_string_fields = [{value}] """.format(value=string_fields)
        output = output + stringFieldsSection

    return output