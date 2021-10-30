import os

SERVICE_NAME = "influxdb2"

def invoke(services):
    if(SERVICE_NAME in services.keys()):
        print("Loading {name} plugin".format(name=SERVICE_NAME))
        return getConfigSection()

def getConfigSection():
    host = os.environ.get('INFLUXDB_HOST') or "http://{service}:8086".format(service=SERVICE_NAME)
    organization = os.environ.get('INFLUXDB_ORG')
    database = os.environ.get('INFLUXDB_DB') or "balena"
    timeout = os.environ.get('INFLUXDB_TIMEOUT') or "1s"

    return """
[[outputs.influxdb_v2]]
    urls = ["{url}"]
    bucket = "{db}"
    organization = "{organization}"
    timeout = "{to}"
    token = "$INFLUX_TOKEN"
    """.format(
        url=host, db=database, to=timeout, organization=organization
    )
