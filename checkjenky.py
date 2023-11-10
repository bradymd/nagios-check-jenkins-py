#!./checkjenky-venv/bin/python
import argparse
import sys
from jenkinsapi.jenkins import Jenkins
url = "https://jenkins:8083"
# jobs set here for testing/verification
jobs = [
    "(vcl-la-rwa03) Import notification logs",
    "(vcl-la-rwa03) Import AWS notification logs",
    "(hokey cokey)",
    "(ask) Staging wayfinding index",
]
parser = argparse.ArgumentParser()
parser.add_argument(
    "-j",
    "--jobs",
    help='"Jenkins Job name"',
    nargs="+",
    type=str,
)
parser.add_argument(
    "-u",
    "--url",
    help="default: " + url,
)
parser.add_argument(
    "--user",
    help="user, default will be guest",
)
parser.add_argument(
    "--password",
    help="password, default will be guest",
)
args = parser.parse_args()
if args.jobs == None:
    pass
else:
    jobs = args.jobs
if args.url == None:
    pass
else:
    url == args.url
if args.user == None:
    user = "guest"
if args.password== None:
    password = "guest"

try:
    J=Jenkins(url,user,password)
except:
    print(f"ERROR: Could not connect to Jenkins")
    sys.exit(1)
    
output = ""
enabled = ""
badresult=False
notfound=False
disabled=False
for jobname in jobs:
    if J.has_job(jobname):
        enabled =  J[jobname].is_enabled()
        if enabled == False:
            output = output + "DISABLED " +  ' job="' + jobname + '" is_enabled=' + str(enabled)
            disabled=True
            badresult=True
        else:
            status=J[jobname].get_last_build().get_status()
            output = output + status  +  ' job="' + jobname + '" is_enabled=' + str(enabled)
        output = output +  "\n"
    else:   
            badresult=True
            notfound=True
            output = output + "NOTFOUND" +  ' job="' + jobname  
            output=output+"\n"

if badresult == True:
    if notfound:
        print(f"CRITICAL: NOTFOUND Job: {output}")
        sys.exit(2)
    elif disabled:
        print(f"WARNING: DISABLED Job: {output}")
        sys.exit(1)
else:
    print(f"OK:{output}")
    sys.exit(0)
