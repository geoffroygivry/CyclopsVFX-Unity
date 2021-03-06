import os
import subprocess
import json

import show_env

grettings = """

   ___        _                __   _______  __        _        _ _
  / __|  _ __| |___ _ __ ___   \ \ / / __\ \/ /     __| |_  ___| | |
 | (_| || / _| / _ \ '_ (_-<    \ V /| _| >  <     (_-< ' \/ -_) | |
  \___\_, \__|_\___/ .__/__/     \_/ |_| /_/\_\    /__/_||_\___|_|_|
      |__/         |_|

"""
print grettings
json_file = "/home/geoff/Dropbox/CyclopsVFX/CYC_envs.json"
os.chdir("/home/geoff/Dropbox/CyclopsVFX")

show_dict = show_env.run()
new_dict = {}
if show_dict is not None:
  for key, val in show_dict.iteritems():
    new_dict[str(key)] = str(val)

  with open(json_file) as j:
    env = json.load(j)
    cyc_env = env.get("CYC_envs")
    for key, value in cyc_env.iteritems():
      new_dict[str(key)] = str(value)
    if new_dict.get("CYC_ROOT") is not None:
      cyc_root_env = new_dict.get("CYC_ROOT")
      if os.getenv("PYTHONPATH") is not None:
        os.environ['PYTHONPATH'] = os.getenv("PYTHONPATH") + "/usr/bin/python2 ;%s" % cyc_root_env
      else:
        os.environ['PYTHONPATH'] = "/usr/bin/python2; %s" % cyc_root_env

    new_dict.update(os.environ)

  start_app = subprocess.call(["nuke"], shell=True, env=new_dict)
