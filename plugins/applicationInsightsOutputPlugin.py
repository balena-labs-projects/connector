import os

def invoke(services):
    key = os.environ.get('APPLICATION_INSIGHTS_KEY') or None
    if(key is None):
        return None
    return getConfigSection(key)    

def getConfigSection(key):
    output = """
[[outputs.application_insights]]
  instrumentation_key = "{key}"
""".format(key=key)
    return output



