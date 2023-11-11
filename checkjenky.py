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
    "--jobs",
    help='"Jenkins Job name"',
    nargs="+",
    type=str,
)
parser.add_argument(
    "--url",
    nargs=1,
    help="Jenkins URL (default:" + defaulturl + ")",
)
parser.add_argument(
    "--user",
    help="Jenkins user login name, (default=guest)",
)
parser.add_argument(
    "--password",
    help="password, (default=guest)",
)
parser.add_argument(
    "--list",
    action="store_true",
    help="list all the jobs on your jenkins server",
)
parser.add_argument(
    "--all",
    action="store_true",
    help="list and report on all jobs from jenkins",
)
args = parser.parse_args()
if args.jobs == None:
    pass
else:
    jobs = args.jobs
if args.url == None:
    url = defaulturl 
else:
    url = args.url[0] #one item but in a list  
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
    for j in J.get_jobs_list():
        print(j)
    sys.exit(0)

if args.all == True:
    jobs=J.get_jobs_list()

# Nagios wants return codes  0(good),1(warning),2(critical)  
# The first line is visible in thruk so we need the first line summarise
# So that means accumulating the output
output = ""
enabled = ""
badresult=False
notfound=False
disabled=False
for jobname in jobs:
    if J.has_job(jobname):
        enabled =  J[jobname].is_enabled()
        if enabled == False:
            output = output +  "DISABLED" +  ', job="' + jobname + \
                '" is_enabled=' + str(enabled) + "\n"
            disabled=True
            badresult=True

        else:
            status=J[jobname].get_last_build().get_status()
            if status == None:
                if J[jobname].is_running() == True:
                    status = "RUNNING"
            output = output +  str(status) + ', job="' + jobname + '" is_enabled=' + str(enabled) + "\n"
    else:   
            badresult=True
            notfound=True
            output = output +  "NOTFOUND" +  ', job="' + jobname  + "\n"

if badresult == True:
    if notfound:
        print(f"CRITICAL: Job(s) NOTFOUND returncode 2")
        print("==============")
        print(output)
        sys.exit(2)
    elif disabled:
        print(f"WARNING: Job(s) DISABLED returncode 1")
        print("==============")
        print(output)
        sys.exit(1)
else:
    print(f"OK returncode 0")
    print("==============")
    print(output)
    sys.exit(0)

