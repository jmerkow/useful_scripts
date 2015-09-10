#!/usr/bin/env python
import re,sys
if len(sys.argv)==2:
    gpu_id=sys.argv[1]
else:
    gpu_id=-1
start_re=re.compile('\|\s*GPU\s*PID\s*Type\s*Process\s*name\s*Usage\s*\|')
gpu_pid=re.compile('\|\s+(\d*)\s+(\d+)\s+(\w+)\s+([/|\.|a-z|0-9]+)\s+(\d+MiB)\s+\|')
start=False
for line in sys.stdin.readlines():
    if not start:
        m= start_re.search(line)
        if m: start=True
        continue
    m= gpu_pid.search(line)
    if m:
	if gpu_id<0 or m.groups()[0]==gpu_id:
	    print m.groups()[1]
