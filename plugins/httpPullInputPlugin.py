import os

### Returns the services which expose the ###
### pull data source port                 ###
def FindPullDataSources(services):
    pullSourcePort = os.environ.get('PULL_SOURCE_PORT') or '7575'
    outputDict = {}
    for service, details in services.items():
      if "expose" in details.keys():
        portNumber = details["expose"]
        if len(portNumber) == 1:
            if portNumber[0] == pullSourcePort:
                outputDict[service] = portNumber
    
    return outputDict

### Creates a HTTP input config section for any  ###
### pull data sources found in the services list ###
def invoke(services):
    output = ""
    pullDataSources = FindPullDataSources(services)
    if len(pullDataSources) > 0:
        for service, port in pullDataSources.items():
            sourceConf = """[[inputs.http]]
    urls = [
    "http://{service}:{port}"
    ]

    timeout = "1s"
    data_format = "json"
    name_override = "{service}"
""".format(service=service, port=port[0])
            output = (output + sourceConf)

    return output