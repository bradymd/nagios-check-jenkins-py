#!./checkjenky-venv/bin/python
import argparse
import sys
from jenkinsapi.jenkins import Jenkins
defaulturl = "https://jenkins:8083"
# jobs set here for testing/verification
jobs = [
    "(vcl-la-rwa03) Import notification logs",
    "(hokey cokey)",
    "(vcl-la-rwa03) Import AWS notification logs",
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
    "--url",
    nargs=1,
    help="default: " + defaulturl,
)
parser.add_argument(
    "--user",
    help="user, default will be guest",
)
parser.add_argument(
    "--password",
    help="password, default will be guest",
)
parser.add_argument(
    "--list",
    action="store_true",
    help="list all the jobs on your jenkins server",
)
parser.add_argument(
    "--all",
    action="store_true",
    help="will get all jobs from jenkins and report on them",
)
args = parser.parse_args()
if args.jobs == None:
    pass
else:
    jobs = args.jobs
if args.url == None:
    url = defaulturl 
else:
    url = args.url[0]
if args.user == None:
    user = "guest"
if args.password== None:
    password = "guest"

try:
    J=Jenkins(url,user,password)
except:
    print(f"ERROR: Could not connect to Jenkins {url}")
    sys.exit(1)
if args.list == True:
    print('args list being used')
    for j in J.get_jobs_list():
        print(j)
    sys.exit(0)

if args.all == True:
    jobs=J.get_jobs_list()
   
output = ""
enabled = ""
badresult=False
notfound=False
disabled=False
for jobname in jobs:
    if J.has_job(jobname):
        enabled =  J[jobname].is_enabled()
        if enabled == False:
            print ( "DISABLED " +  ' job="' + jobname + '" is_enabled=' + str(enabled))
            disabled=True
            badresult=True

        else:
            status=J[jobname].get_last_build().get_status()
            print ( str(status) + "/status"  +  ' job="' + jobname + '" is_enabled=' + str(enabled))
    else:   
            badresult=True
            notfound=True
            print( "NOTFOUND" +  ' job="' + jobname  )

if badresult == True:
    if notfound:
        print(f"CRITICAL: Job(s) NOTFOUND returncode 2")
        print("==============")
        sys.exit(2)
    elif disabled:
        print(f"WARNING: Job(s) DISABLED returncode 1")
        print("==============")
        sys.exit(1)
else:
    print(f"OK:{output}")
    sys.exit(0)

