import os

SERVICE_NAME = "base config"

def invoke(services):
    print("Loading {name} plugin".format(name=SERVICE_NAME))
    return getConfigSection()    

def getConfigSection():
    debug = ((os.environ.get('DEBUG') or '0') == '1')
    interval = os.environ.get('PULL_INTERVAL', '10s')

    output = """
    [agent]
    debug = {debug}
    interval = "{interval}"
    """.format(debug=str(debug), interval=interval).lower()

    return output
