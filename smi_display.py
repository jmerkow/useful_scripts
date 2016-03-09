#!/usr/bin/env python

from __future__ import print_function
import re,sys
def smi_parse(in_str,return_details=False,gpu_id=-1):
    start_re=re.compile('\|\s*GPU\s*PID\s*Type\s*Process\s*name\s*Usage\s*\|')
    gpu_pid=re.compile('\|\s+(\d*)\s+(\d+)\s+(\w+)\s+(.+)\s+(\d+MiB)\s+\|')
    start=False
    pids=list()
    for line in in_str.readlines():
        if not start:
            m= start_re.search(line)
            if m: start=True
            continue
        m= gpu_pid.search(line)
        if m:
            if gpu_id<0 or m.groups()[0]==gpu_id:
                vals=m.groups()
                pids.append((int(vals[0]),int(vals[1]),int(vals[-1].strip('MiB'))))
                # print(m.groups())
    if return_details:
        return pids
    else:
        return [str(p[1]) for p in pids]
import psutil
import subprocess as sp
from StringIO import StringIO
import sys
if len(sys.argv)==2:
    trunc=int(sys.argv[1])
else:
    trunc=26
buf=StringIO(sp.check_output('nvidia-smi'))
top_buf=buf.getvalue().split('| Processes: ')[0].strip()
cool_line=top_buf.split('\n')[-1]
print(top_buf)
pids = smi_parse(buf,return_details=True)
from  datetime import datetime
fts=datetime.fromtimestamp
from tabulate import tabulate
tab=list()
#print(pids)
print("Summary")
for pid in pids:
    if psutil.pid_exists(pid[1]):
        proc=psutil.Process(pid[1])
        tm=fts(proc.create_time())
        tmstr = tm.strftime('%H:%M:%S') if tm.date() == datetime.today().date() else tm.strftime('%b-%d')
        tab.append((pid[0],proc.pid,proc.ppid(),proc.username(),str(pid[2])+'MiB',\
        tmstr,\
        ' '.join(proc.cmdline())[:trunc]))
#	print('\t'.join(map(str,tab[-1])))
print(tabulate(tab,headers=['GPU','PID','PPID','UID','GPU Mem','STime','CMD']))
print(cool_line)
