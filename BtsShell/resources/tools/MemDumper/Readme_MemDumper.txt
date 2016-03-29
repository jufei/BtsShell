
     Getting Started with MemDumper
      -----------------------------

MemDumper is used to dump memory from all dsp boards of NSN WCDMA or LTE BTS in use. 

There are two types of dumping, dumping all memory areas defined in ini file (WHOLE DUMP) and dumping specified memory area defined in GUI (SINGLE DUMP). If the user knows which memory section is needed exactly, it is recommended to use the SINGLE DUMP since it is faster than the WHOLE DUMP and the dumped files will be smaller.

Steps:

1.Configure the IP address and port of FCM Board. Click ¡°Connect¡± button to connect. If connected, this button will change to ¡°Disconnect¡±.

For example, FCM IP:192.168.255.1, Port:15003 or 15002

2.Configure the path of ini file which defines the memory area to get from DSP board. Click ¡°Browse¡± button to select an ini file. The default value is ¡°memorydumps.ini¡± in the same directory of MemDumper.exe.

NOTE1: This step is not necessary if using SINGLE DUMP.

NOTE2: The ini file must be in accordance with the following format:
(1) For FSPB/FSPC:
[$CPU$]
$CORE$ $TARGET MEMORY START ADDRESS$:$TARGET MEMORY LENGTH$   <<$COMMENTS$
[/$CPU$]

For example:
[FARADAY1]
CORE0 02f10000:00050000         <<INT MEM
...
CORE1 11828000:000B8000         <<INT MEM
...
[/FARADAY1]

(2) For older boards:
[$BOARD TYPE$]
$CPU FUNCTION$ $TARGET MEMORY START ADDRESS$:$TARGET MEMORY LENGTH$   <<$COMMENTS$
[/$BOARD TYPE$]

For example:
[WSPC]
CODEC 00000000:00100000         <<INT MEM
...
RAKE1 00000000:00100000         <<INT MEM
...
[/WSPC]

The address must be hexadecimal format. Memory address selection depends on the corresponding map file with a product type.

3.Configure the store path of dump files. Click ¡°Browse¡± button to select a path. The default value is the same directory of MemDumper.exe .

4.Configure the details for dumping. Click the corresponding tab label of the dsp board type, Fill the board ID to select the target board. For example, 0x14 for FSM1_FSP3.

NOTE: The board ID are defined in file DSP SW sack file: Glo_bs.h

If you want a WHOLE DUMP, Click this ¡°FETCH MEMORY DUMPS BY USING VALUES FROM INI FILE¡± button to dump all memory areas defined in ini file.

If you want a SINGLE DUMP, select the target cpu and core, configure the target memory ddress and length to dump. Then Click ¡°READ SINGLE DUMP¡± button to dump the memory area specified.

NOTE: If ¡°Save single dump to file¡± check box is selected, the dump result will be saved to file within specified format. Otherwise, the dump result will be shown in the text box below.

Other functions:
You can use the GetCoreStatus function to find out if cores can be dumped, and the software can dump memory from other cores in same cpu.
 

More info about this tool can be found at WCDMA NODEB User Plane Layer1 DSP Debugging Application team Wiki Page:

http://wikis.inside.nokiasiemensnetworks.com/bin/view/WCDMA_BTS_UP_HZ_DDA/WebHome

