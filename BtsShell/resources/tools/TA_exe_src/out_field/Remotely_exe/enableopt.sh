#!/bin/bash 
enable129()
{
    (   
        echo "rad -pw 0xED 0"  
        sleep 5
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
        echo "rad -pw 0xED 0"  
        sleep 5
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
        echo "rad -pw 0xED 0"  
        sleep 5
        echo $1@done@
        sleep 1
        echo "exit"
        sleep 1
    ) | telnet $1 $2
}
enable141 192.168.254.141 2323
