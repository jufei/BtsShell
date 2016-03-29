@Echo OFF

REM Check parameters
if "%2" == "" goto :HELP

java -classpath .;./lib/btsemappl.jar;./lib/ganymed-ssh2-build251beta1.jar;./lib/log4j-1.2.15.jar;./lib/poseidon.jar;./lib/coreasset.jar com.nokia.em.bts.coreasset.application.CoreAssetToolApplication -op collectfiles %*
goto :END

REM ***************************************************************************
REM HELP procedure
REM Display brief on-line help message

:HELP
cls
echo **************************************************************************
echo *                File Collector Tool                                     *
echo *                                                                        *
echo *   Fetches several type of files from one or several BTSs and saves     *
echo *   them to zip files or directories.                                    *
echo *                                                                        *
echo *   Usage:                                                               *
echo *         collectfiles -ipfile [ipfile] [options]                        *
echo *         collectfiles -ne [btsAddress] [options]                        *
echo *                                                                        *
echo *   Where                                                                *
echo *      -ipfile defines file name containing IP addresses and credentials *
echo *      -ne defines single IP address of one BTS                          *
echo *                                                                        *
echo *   Credentials can be defined with                                      *
echo *       -pw [username]:[password],[username]:[password],...              *
echo *                                                                        *
echo *   SSH credentials can be defined with                                  *
echo *       -ssh [username]:[password]                                       *
echo *                                                                        *
echo *      Options are                                                       *
echo *                                                                        *
echo *         -zip puts fetched files into zip files named with IP address   *
echo *         -dir puts fetched files into directories named with IP address *
echo *         -all fetches all supported files (except techlogs and pm)      *
echo *         -siteconf fetches siteconfiguration file                       *
echo *         -comm fetched commissioning file                               *
echo *         -currentbd fetches SW version file                             *
echo *         -swconfig fetches swconfig.txt file                            *
echo *         -swdlrep fetches software download report file                 *
echo *         -licences fetches licence information                          *
echo *         -filedir fetches file directory                                *
echo *         -rawalarms fetches raw alarm history file                      *
echo *         -freqhistory fetches frequency history file                    *
echo *         -antennadata fetches antenna configuration file                *
echo *         -hwinfo fetches HW information file                            *
echo *         -techlogs fetches minor technical log files                    *
echo *         -fullCoverage fetches all technical log files                  *
echo *         -pm fetches PM files                                           *
echo *         -concurrent [number] maximum number of concurrent connections  *
echo *         -outDir [directory] directs output to a specific directory     *
echo *         -timeout [seconds] general timeout for operations              *
echo *                                                                        *
echo *   By default, files are fetched to working directory and filenames are *
echo *   prefixed with IP address.                                            *
echo *                                                                        *
echo *   Optional argument:                                                   *
echo *      To put informative and error messages to file instead of printing *
echo *      printing them to prompt, define output file                       *
echo *        -output [output file name]                                      *
echo **************************************************************************
goto :END

REM ***************************************************************************
REM END of this file
:END