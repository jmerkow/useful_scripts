#!/usr/bin/env python
import re,sys
def smi_parse(in_str,return_details=False,gpu_id=-1):
    start_re=re.compile('\|\s*GPU\s*PID\s*Type\s*Process\s*name\s*Usage\s*\|')
    gpu_pid=re.compile('\|\s+(\d*)\s+(\d+)\s+(\w+)\s+([/|\.|a-z|0-9]+)\s+(\d+MiB)\s+\|')
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
#                 print(m.groups())
    if return_details:
        return pids
    else:
        return [str(p[1]) for p in pids]
if __name__ == "__main__":
    if len(sys.argv)==2:
        gpu_id=sys.argv[1]
    else:
        gpu_id=-1
    print '\n'.join(smi_parse(sys.stdin,gpu_id=gpu_id))

