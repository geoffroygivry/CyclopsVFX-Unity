import json
import os
import sys
from sys import platform as _platform

# TODO if the show entity hasn't been found, should raise a custom exception and log it. Please see Jira issue
with open(os.path.join(os.getenv("CYC_CORE_PATH"), "shows.json")) as data_file:
    data = json.load(data_file)

cl_arg = sys.argv[1]
# print cl_arg

for n in data.get("active_shows"):
    if n == cl_arg:
        print "You are now on the show: %s" % cl_arg
        return cl_arg
    else:
        print "Please provide an active show."
        return None
