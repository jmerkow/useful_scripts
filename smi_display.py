#!/usr/bin/env python

from __future__ import print_function
from smi_parse import smi_parse
import psutil
import subprocess as sp
from StringIO import StringIO
import sys
if len(sys.argv)==2:
    trunc=int(sys.argv[1])
else:
    trunc=50
buf=StringIO(sp.check_output('nvidia-smi'))
top_buf=buf.getvalue().split('| Processes: ')[0].strip()
cool_line=top_buf.split('\n')[-1]
print(top_buf)
pids = smi_parse(buf,return_details=True)
from  datetime import datetime
fts=datetime.fromtimestamp
from tabulate import tabulate
tab=list()
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
print(tabulate(tab,headers=['GPU','PID','PPID','UID','GPU Mem Usage','STime','CMD']))
print(cool_line)
