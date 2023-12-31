# nagios-check-jenkins-py
# checkjenky
Nagios utility for interrograting jenkins

```
git clone  https://gitlab.herts.ac.uk/nagios-check-jenkins-py
cd nagios-check-jenkins-py
python3 -m venv  checkjenky-venv
./checkjenky-venv/bin/activate
pip  install -r requirements.txt
```

##  Configuring checkjenky.py
Optionally set the url of jenkins and a jenkins user / password credentials in the program.
 
## Program checkjenky.py
Is using jenkins api for nagios.

##  with no arguments is is currently set up to run some tests

```
   ./checkjenky.py
   WARNING: DISABLED or NOTFOUND Job:
   SUCCESS job="(vcl-la-rwa03) Import notification logs" is_enabled=True
   SUCCESS job="(vcl-la-rwa03) Import AWS notification logs" is_enabled=True
   NOTFOUND job="(hokey cokey)
   DISABLED  job="(ask) Staging wayfinding index" is_enabled=False
```

##  Usage
```
usage: checkjenky.py [-h] [-j JOBS [JOBS ...]] [--url URL] [--user USER]
                     [--password PASSWORD] [--list] [--all]

optional arguments:
  -h, --help            show this help message and exit
  -j JOBS [JOBS ...], --jobs JOBS [JOBS ...]
                        "Jenkins Job name"
  --url URL             default: https://jenkins:8083
  --user USER           user, default will be guest
  --password PASSWORD   password, default will be guest
  --list                list all the jobs on your jenkins server
  --all                 will get all jobs from jenkins and report on them
```

##  Obtaining the status of the last  build ( or notification if DISABLED)
```
+ ./checkjenky.py -j '(vcl-la-rwa03) Import notification logs'
OK:
SUCCESS job="(vcl-la-rwa03) Import notification logs" is_enabled=True
```

##  Notification if no such job
```
+ ./checkjenky.py -j '(hokey cokey'
WARNING: DISABLED or NOTFOUND Job:
NOTFOUND job="(hokey cokey
```

##  Notifiication if a job is DISABLED
```
+ ./checkjenky.py -j '(ask) Staging wayfinding index,'
WARNING: DISABLED or NOTFOUND Job:
NOTFOUND job="(ask) Staging wayfinding index,
```

## Can take multiple jobs
```
+ ./checkjenky.py -j '(vcl-la-rwa03) Import notification logs' '(hokey cokey)' '(vcl-la-rwa03) Import AWS notification logs,'
WARNING: DISABLED or NOTFOUND Job:
SUCCESS job="(vcl-la-rwa03) Import notification logs" is_enabled=True
NOTFOUND job="(hokey cokey)
NOTFOUND job="(vcl-la-rwa03) Import AWS notification logs,
```

