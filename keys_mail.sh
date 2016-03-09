#! /bin/bash
Logs=/opt/newslogs/mis_out.log
Keys="(WARN|ERROR)"
nn=/home/zhaoyingbin/misscript/222
Admin="'
    while read line
    do
        grep $line ${Logs}| egrep -iq ${Keys}
              if [ $? -eq 0 ];then
                rm -rf /home/zhaoyingbin/misscript/mis.out
               awk '/ERROR/' ${Logs} > /home/zin/misscript/mis.out
               awk '/WARN/' ${Logs} >> /home/zhao/misscript/mis.out
               fi
     done < $nn
               mail -s miserror $Admin < /home/zhn/misscript/mis.out
               rm -rf /home/zhaoyingbin/misscript/mis.out
