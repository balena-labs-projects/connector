import os

SERVICE_NAME = "Device Metrics"

def invoke(services):
    if((os.environ.get('ENABLE_DEVICE_METRICS') or '0') != '1'):
        return None
    print("Loading {name} plugin".format(name=SERVICE_NAME))
    return getConfigSection()    

def getConfigSection():
    output = """
[[inputs.mem]]

[[inputs.cpu]]
  percpu = true
  totalcpu = true
  collect_cpu_time = false
  report_active = false
"""
    return output


