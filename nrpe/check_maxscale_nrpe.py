#!/usr/bin/python
#
# Galera check using MaxScale for nrpe
# Written by: Michel Hoogervorst <michel@highking.nl>
# Date: 12/07/2016
#
from subprocess import Popen, PIPE
import json

# Define the maxadmin-command, the username and the password to use.
maxadmin='maxadmin'
username='admin'
password='mariadb'

# Ask maxadmin for the status
p = Popen('%s -u%s -p%s show serversjson' % (maxadmin, username, password), stdout=PIPE, shell=True)
out,err = p.communicate()
if p.returncode != 0:
  print "ERROR: problem running %s" % maxadmin
  exit(3)

# Read json data and put it in the status list:
status = json.loads(out)

# Initialize some vars
output=""
problems=0

# Loop through all servers
for server in status:
  ss = list(reversed(server['status'].split()))
  if 'Down' in ss[0]:
    problems+=1
    output += "Server %s is DOWN! " % server['server']
  elif len(ss) < 2 or not 'Synced' in ss[1]:
    problems+=1
    output += "Server %s is NOT in sync! " % server['server']

if problems == len(status):
  state=2
elif problems > 0:
  state=1
else:
  state=0
  output="OK: All %s servers are up and running!" % len(status)

print output
exit(state)
