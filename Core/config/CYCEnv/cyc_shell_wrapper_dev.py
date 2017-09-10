import os
import subprocess
import json

json_file = "/home/geoff/Dropbox/CyclopsVFX/CYC_envs.json"
os.chdir("/home/geoff/Dropbox/CyclopsVFX/")

new_dict = {}

with open(json_file) as j:
  env = json.load(j)
  cyc_env = env.get("CYC_envs")
  for key, value in cyc_env.iteritems():
    new_dict[str(key)] = str(value)
  if new_dict.get("CYC_ROOT") is not None:
    cyc_root_env = new_dict.get("CYC_ROOT")
    cyc_root_env = "C:" + cyc_root_env.replace('/', "\\")
    os.environ['PYTHONPATH'] = os.getenv("PYTHONPATH") + ";%s" % cyc_root_env
  new_dict.update(os.environ)

start_app = subprocess.call(["echo", "youyou"], shell=True, env=new_dict)
