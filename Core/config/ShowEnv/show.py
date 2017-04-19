import json
import os
import subprocess
from subprocess import Popen

# TODO if the show entity hasn't been found, should raise a custom exception and log it. Please see Jira issue


def set_show():
    with open(os.path.join(os.getenv("CYC_CORE_PATH"), "shows.json")) as data_file:
        data = json.load(data_file)

    sys_environ = dict(os.environ)
    showName = os.getenv("JOB")

    for n in data.get("active_shows"):
        if n == showName:
            print "You are now on the show: %s" % showName
            args = "C:\Program Files\Nuke9.0v7\Nuke9.0.exe"
            Popen(args, shell=True, stdout=subprocess.PIPE, env=sys_environ)
        else:
            print "Please provide an active show."
            return None


set_show()
