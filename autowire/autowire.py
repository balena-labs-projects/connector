import os
import sys
from functools import partial
from pluginbase import PluginBase
from balena import Balena
from http.server import HTTPServer, BaseHTTPRequestHandler

class AutoWire():
  balena = ""
  services = None

  def __init__(self, balena):
    self.balena = balena

  def GetConfig(self):
    config = self.GetInputConfig()
    config = (config + self.GetOutputConfig())
    return config

  ### Gets the services running on the device from the release definition ###
  def GetServices(self):
    if self.services is None:
      # Use the device UUID to get the device model
      device_id = os.environ.get('BALENA_DEVICE_UUID')
      device = self.balena.models.device.get_with_service_details(device_id, False)
      # get the commit the device is on
      commit = device["is_on__commit"]
      # use the commit to get the release the device is on
      release = self.balena.models.release.get(commit)
      # use the release to find the services configured
      self.services = release["composition"]["services"]

    return self.services

  def FindPullDataSources(self):
    outputDict = {}

    if self.services is None:
      self.GetServices()
    
    for service, details in self.services.items():
      if "expose" in details.keys():
        outputDict[service] = details["expose"]
    
    return outputDict

  ### Loads the plugins and passes the service list to each one ###
  ### A plugin outputs it's config only if there is an entry in ###
  ### the list for the backend service it configures            ###
  def GetOutputConfig(self):
    config = ""
    # Use PluginBase to find the plugins
    here = os.path.abspath(os.path.dirname(__file__))
    get_path = partial(os.path.join, here)
    plugin_base = PluginBase(package='plugins')
    plugin_source = plugin_base.make_plugin_source(searchpath=[get_path('plugins')])

    # Call each plugin and pass in the list of services
    for plugin_name in plugin_source.list_plugins():
      plugin = plugin_source.load_plugin(plugin_name)
      # Add each plugin output to the config string we're building
      config = (config + str(plugin.invoke(self.GetServices().keys())))
    
    return config

  ### Get the input config ###
  def GetInputConfig(self):
    output = """
  [[inputs.mqtt_consumer]]
    topics = [
      "sensors/#",
    ]

    data_format = "json"
    """

    pullDataSources = self.FindPullDataSources()
    if len(pullDataSources) > 0:
      for service, port in pullDataSources.items():
        sourceConf = """
  [[inputs.http]]
  urls = [
    "http://{service}:{port}"
  ]

  timeout = "1s"
  data_format = "json"
      """.format(service=service, port=port[0])
        output = (output + sourceConf)

    return output

### HTTP server for telegraf config endpoint ###
class balenaHTTP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        config = autowire.GetConfig()
        print(config)
        self.wfile.write(config.encode('UTF-8'))

    def do_HEAD(self):
        self._set_headers()


# Authenticate with balenaCloud
balena = Balena()
auth_token = os.environ.get('AUTH_TOKEN') or sys.exit("No AUTH_TOKEN device variable set. Cannot authenticate with balenaCloud")
balena.auth.login_with_token(auth_token)

# Create the autowire class for the HTTP server to use
autowire = AutoWire(balena)

# Run the HTTP server on a specific port
while True:
  server_address = ('', 9099)
  httpd = HTTPServer(server_address, balenaHTTP)
  print('Telegraf config HTTP endpoint running')
  httpd.serve_forever()