#!/bin/bash 
enable129()
{
    (   
        echo "rad -nspw VSWR_Minor_Alarm_OFF 0"  
        sleep 3
        echo "rad -nspw VSWR_Major_Alarm_OFF 0"
        sleep 3
        echo $1@done@
        sleep 1
        echo "exit"
        sleep 1
    ) | telnet $1 $2
}
enable129 192.168.254.129 2323
enable137()
{
    (   
        echo "rad -nspw VSWR_Minor_Alarm_OFF 0"  
        sleep 3
        echo "rad -nspw VSWR_Major_Alarm_OFF 0"
        sleep 3
        echo $1@done@
        sleep 1
        echo "exit"
        sleep 1
    ) | telnet $1 $2
}
enable137 192.168.254.137 2323
enable141()
{
    (   
        echo "rad -nspw VSWR_Minor_Alarm_OFF 0"  
        sleep 3
        echo "rad -nspw VSWR_Major_Alarm_OFF 0"
        sleep 3
        echo $1@done@
        sleep 1
        echo "exit"
        sleep 1
    ) | telnet $1 $2
}
enable141 192.168.254.141 2323
