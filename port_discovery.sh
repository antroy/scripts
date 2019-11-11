#!/bin/bash

EXE=$1

data=`netstat -tulpn 2>/dev/null | grep "/$EXE" | sed -e 's/[[:blank:]]\+/|/g'`

pid_port=`echo "$data" | cut -d '|' -f '4,7' | uniq | cut -d '/' -f 1`

pid_list="["
first=0

for pid_port in $pid_port
do
    pid=$(echo $pid_port | sed 's/.*|//')
    port=$(echo $pid_port | sed 's/|.*//')

    if [ $first -eq 0 ]
    then
        first=1
    else
        pid_list+=", "
    fi

    exe=`ls -l /proc/$pid/exe | sed 's/.*-> \(.*\)/\1/'`
    pid_list+="('$exe', '$port')"
done

pid_list+="]"

python3 -c "
from collections import defaultdict
data=$pid_list
out=defaultdict(lambda: [])

for d in data:
    out[d[0]].append(d[1])

for exe in out:
    print('%s:\n\t%s' % (exe, '\n\t'.join(out[exe])))


"





