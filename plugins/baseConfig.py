import os

SERVICE_NAME = "base config"

def invoke(services):
    print("Loading {name} plugin".format(name=SERVICE_NAME))
    return getConfigSection()    

def getConfigSection():
    debug = ((os.environ.get('DEBUG') or '0') == '1')

    output = """
[agent]
debug = {debug}
""".format(debug=str(debug)).lower()
    return output


