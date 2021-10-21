import os
import sys
sys.path.append(".")
sys.path.append("./plugins")
from functools import partial
from pluginbase import PluginBase
from balena import Balena
import toml
import requests

class AutoWire():
  balena = ""
  services = None

  def __init__(self, balena):
    self.balena = balena

   ### Gets the services running on the device from the release definition ###
  def GetServices(self):
    if self.services is None:
      # Use the device UUID to get the device model and check device mode
      device_id = os.environ.get('BALENA_DEVICE_UUID')
      local_mode = balena.models.device.is_in_local_mode(device_id)
      
      if local_mode:
        supervisor_address = os.environ.get('BALENA_SUPERVISOR_ADDRESS')
        r = requests.get(supervisor_address + '/v2/local/target-state')
        services = r.json()["state"]["local"]["apps"]["1"]["services"]
        self.services = {}
        for service in services:
          self.services[service.get("serviceName")] = service.get("config")
      else:
        device = self.balena.models.device.get_with_service_details(device_id, False)
        # get the commit the device is on
        commit = device["is_on__commit"]
        # use the commit to get the release the device is on
        release = self.balena.models.release.get(commit)
        # use the release to find the services configured
        self.services = release["composition"]["services"]

    return self.services

  ### Returns a default input section (device temp) if
  ### no input sections have been created by plugins.
  ### (i.e. no input sources configured or discovered) 
  def GenerateDefaultInputConfig(self, config):
    section = "[[inputs.temp]]"

    if('inputs' not in toml.loads(config).keys()):
      return section
    
    if(len(toml.loads(config)['inputs']) == 0):
      return section
    
    return None

  ### Loads the plugins and passes the service list to each one ###
  ### A plugin outputs it's config only if there is an entry in ###
  ### the list for the backend service it configures            ###
  def GetConfig(self):
    services = self.GetServices()
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
      section = plugin.invoke(services)
      if(section is not None):
        config = (config + str(section))
    
    defaultSection = self.GenerateDefaultInputConfig(config)
    if(defaultSection is not None):
      print("No data sources configured or detected. Enabling default: device temperature.")
      config = (config + str(defaultSection))

    return config

# Authenticate with balenaCloud
balena = Balena()
auth_token = os.environ.get('BALENA_API_KEY') or sys.exit("No AUTH_TOKEN device variable set. Cannot authenticate with balenaCloud")
balena.auth.login_with_token(auth_token)

# Create the autowire class
autowire = AutoWire(balena)
print("balenablocks/connector")
print("----------------------")
print('Intelligently connecting data sources with data sinks')
# Get the config and write to to the file.
config = autowire.GetConfig()
doc = toml.loads(config)
f = open('telegraf.conf', 'w')
f.write(toml.dumps(doc))
f.close()