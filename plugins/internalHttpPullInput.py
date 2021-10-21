import os
import sys
sys.path.append(".")
from helper_methods import helpers

### Returns the services which expose the ###
### pull data source port                 ###
def FindPullDataSources(services):
    pullSourcePort = os.environ.get('PULL_SOURCE_PORT') or '7575'
    outputDict = {}
    for service, details in services.items():
      if "expose" in details.keys():
        portNumber = details["expose"]
        if len(portNumber) == 1:
            if portNumber[0].split('/')[0] == pullSourcePort:
                outputDict[service] = portNumber
    
    return outputDict

### Creates a HTTP input config section for any  ###
### pull data sources found in the services list ###
def invoke(services):
    output = ""
    pullDataSources = FindPullDataSources(services)
    if len(pullDataSources) > 0:
        timeout = os.environ.get('INTERNAL_HTTP_TIMEOUT') or '2'
        for service, port in pullDataSources.items():
            print("Adding {service} internal HTTP source".format(service=service))
            sourceConf = """[[inputs.http]]
    urls = [
    "http://{service}:{port}"
    ]

    timeout = "{timeout}s"
    data_format = "json"
    name_override = "{service}"
""".format(service=service, port=port[0].split('/')[0], timeout=timeout)
            output = (output + sourceConf)

    stringFields = os.environ.get('INTERNAL_HTTP_PULL_STRINGS_FIELDS')
    if(stringFields is not None):
        stringFieldsSection = helpers.formatStringField(stringFields)
        output = output + stringFieldsSection

    return output