#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <bitbar.title>Janelia LSF Jobs</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Andrew Champion</bitbar.author>
# <bitbar.author.github>aschampion</bitbar.author.github>
# <bitbar.desc>Show the status of jobs on the Janelia LSF cluster</bitbar.desc>

from collections import OrderedDict
from subprocess import PIPE, Popen


def parse_output(output):
    lines = output.splitlines()

    header = lines[0].split()
    jobs = [dict(zip(header, l.split())) for l in lines[1:]]

    return jobs


DISPLAY_GROUPS = OrderedDict([
    ("Pending", {"stat": "PEND", "icon": ":hourglass:"}),
    ("Running", {"stat": "RUN", "icon": ":running:"}),
    ("Done", {"stat": "DONE", "icon": ":checkered_flag:"}),
    ("Exited", {"stat": "EXIT", "icon": ":door:"}),
])


def group_jobs(groups, jobs):
    return OrderedDict([
        (name, [j for j in jobs if j["STAT"] == g["stat"]])
        for name, g in groups.items()
    ])


def bitbar(grouped_jobs):
    print "".join(["%i%s" % (len(jobs), DISPLAY_GROUPS[name]["icon"]) for name, jobs in grouped_jobs.items()])

    print "---"

    for name, jobs in grouped_jobs.items():
        print name
        for job in jobs:
            print "--%s %s" % (job["JOBID"], job["JOB_NAME"])


process = Popen('ssh -o ConnectTimeout=1 login1.int.janelia.org "bjobs -a"', shell=True, stdout=PIPE)
output = process.stdout.read()

if process.wait() == 0:
    bitbar(group_jobs(DISPLAY_GROUPS, parse_output(output)))
else:
    print ":red_circle:"

print "---"
print "Refresh|refresh=true"
