#!/bin/sh

if [ "$2" = "" ]
then
 clear
 echo "**************************************************************************"
 echo "*     Resetting Tool                                                     *"
 echo "*                                                                        *"
 echo "*   Resets BTS.                                                          *"
 echo "*                                                                        *"
 echo "*   Usage:                                                               *"
 echo "*       reset.sh -ne [WBTS address]                                      *"
 echo "*       reset.sh -ipfile [ipfile]                                        *"
 echo "*                                                                        *"
 echo "*    Where                                                               *"
 echo "*      -ipfile defines file name containing IP addresses of BTSs         *"
 echo "*       (one ip per line).                                               *"
 echo "*      -ne defines single IP address of one BTS.                         *"
 echo "*                                                                        *"
 echo "*   If BTS is using authentication, username and password must be        *"
 echo "*   defined as argument "-username [username] -password [password]"      *"
 echo "*   or as "-pw [username]:[password]" or in ipfile (if using -ipfile     *"
 echo "*   switch).                                                             *"
 echo "*                                                                        *"
 echo "*   Use optional parameters:                                             *"
 echo "*      -resetCoverage [bs/site] to define the coverage of the reset.     *"
 echo "*       "bs" option resets only BTS, "site" resets also transmission.    *"
 echo "*      -fullReset, this is an old parameter to imply that the reset      *"
 echo "*       is needed on site level, i.e. also transmission is reset.        *"
 echo "*      -output [output file name] to redirect reset results from         *"
 echo "*       default output to a specific file.                               *"
 echo "*                                                                        *"
 echo "*   Example: ./reset.sh -ipfile ip.txt -output out.log                   *"
 echo "*                                                                        *"
 echo "*   See README.txt for more information.                                 *"
 echo "**************************************************************************"
else
 java -classpath .:./lib/btsemappl.jar:./lib/log4j-1.2.15.jar:./lib/poseidon.jar:./lib/coreasset.jar com.nokia.em.bts.coreasset.application.CoreAssetToolApplication -op reset $*
fi
