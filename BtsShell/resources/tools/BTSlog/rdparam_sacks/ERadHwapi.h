/**
*******************************************************************************
* @file                  %PM%
* @version               %PR%
* @date                  %PRT%
* @author                %PO%
* @brief
*
*
* PVCS Information:
*
* PVCS Product           %PP%
*
* Base Database          HELENA
*
* Design Part            WCDMA:HWR
*
* Development Workset    WCDMA:WN_HWR_CCS_INTEGRATION
*
* Item Specification     %PP%:%PI%.%PV%-%PT%
*
* Status                 %PS%
*
* Revision History:
*
* - 0.0.18  13.13.2007/JPi   Added ERadHwapi_BtsomStubL2MemoryConfig and
*                            ERadHwapi_BtsomStubRuntimeSwSelection
* - 0.0.17  13.11.2007/PeJ   Added ERadHwapi_PrintInetTcpTask and ERadHwapi_PrintInetUdpTask
* - 0.0.16  02.11.2007/PeJ   Added ERadHwapi_PrintSfnPoll
* - 0.0.15  31.10.2007/JSM   Added OPT Service prints
* - 0.0.14  12.10.2007/PeJ   Added ERadHwapi_PrintBrowserIf, ERadHwapi_PrintBtsLogIf, ERadHwapi_PrintTesterIf
* - 0.0.13  11.10.2007/PeJ   Added ERadHwapi_PrintTassuRouter
* - 0.0.12  26.09.2007/JaVa  ERadHwapi_PrintCasaTask added.
* - 0.0.11  17.08.2007/JaTP  ERadSwDomain_HwApi changed.... corrected
* - 0.0.10  12.06.2007/VMR   Added ERadHwapi_PrintCpuLoadMon and
*                            ERadHwapi_PrintStatisticsTriggerInd
* - 0.0.9   29.05.2007/VMR   Added ERadHwapi_StatisticsTriggerIndInterval
* - 0.0.8   25.05.2007/VMR   Added ERadHwapi_PrintSfnSync
* - 0.0.7   30.04.2007/JPi   Added init print definition
* - 0.0.6   26.04.2007/JaTP  Added several ERadHwapi_PrintXxxTask definitions
* - 0.0.5   10.04.2007/VMR   Added ERadHwapi_PrintAlarmSrv
* - 0.0.4   03.04.2007/NPu   Added SUM Service prints
* - 0.0.3   07.03.2007/ArK   Added Reset Service prints
* - 0.0.2   13.02.2007/SPo   Added Ethernet Service prints
* - 0.0.1   12.12.2006/JuMa  Created.
*
* Copyright (c) Nokia 2006. All rights reserved.
*******************************************************************************/

#ifndef _ERAD_HWAPI_H
#define _ERAD_HWAPI_H

/************************** DOXYGEN GROUPS ************************************/

/**
 *  @defgroup RadHwapi          HWAPI R&D parameters
 *  @ingroup  AaConfigSwDomain
 *
 *  Defines HWAPI R&D parameters.
 */
/*@{*/

/************************** INCLUDED FILES ************************************/

#include <AaConfigRadDefinitions.h>


/************************** PUBLIC DECLARATIONS *******************************/

#define RAD_HWAPI(value) RAD_SW_DOMAIN(ERadSwDomain_HwApi, value)

/************************** PUBLIC INTERFACES *********************************/

/*!
 *  @brief  Defines HWAPI R&D parameters.
 */
enum ERadHwapi
{
    ERadHwapi_PrintCtrlTask   = RAD_HWAPI(0),               /* Control Task debug print */
    ERadHwapi_PrintAdetTask   = RAD_HWAPI(1),               /* Autodetection Task debug print */
    ERadHwapi_PrintInetTask   = RAD_HWAPI(2),               /* Inet ctrl Task debug print */
    ERadHwapi_PrintSwdlTask   = RAD_HWAPI(3),               /* SW DL Task debug print */
    ERadHwapi_PrintBistTask   = RAD_HWAPI(4),               /* BIST Task debug print */
    ERadHwapi_PrintEthsTask   = RAD_HWAPI(5),               /* Ethernet Service task print */
    ERadHwapi_PrintResetTask  = RAD_HWAPI(6),               /* Reset Service task print */
    ERadHwapi_PrintAifTask    = RAD_HWAPI(7),               /* AIF-bus task print */
    ERadHwapi_PrintSumTask    = RAD_HWAPI(8),               /* SUM Service task print */
    ERadHwapi_PrintAlarmSrv   = RAD_HWAPI(9),               /* Alarm Service print */
    ERadHwapi_PrintGenioTask  = RAD_HWAPI(10),              /* Genio Task debug print */
    ERadHwapi_PrintCdTask     = RAD_HWAPI(11),              /* CD Task debug print */
    ERadHwapi_PrintPciTask    = RAD_HWAPI(12),              /* PCI Task debug print */
    ERadHwapi_PrintI2cTask    = RAD_HWAPI(13),              /* I2C Task debug print */
    ERadHwapi_PrintSTTask     = RAD_HWAPI(14),              /* Self Test Task debug print */
    ERadHwapi_PrintInit       = RAD_HWAPI(15),              /* Init prints */
    ERadHwapi_PrintSfnSync    = RAD_HWAPI(16),              /* SFN Sync Service print */
    ERadHwapi_StatisticsTriggerIndInterval = RAD_HWAPI(17), /* Control HWAPI statistics trigger indication testability feature */
    ERadHwapi_PrintStatisticsTriggerInd    = RAD_HWAPI(18), /* Statistics trigger indication print */
    ERadHwapi_PrintCpuLoadMon = RAD_HWAPI(19),              /* CPULoadMon print */
    ERadHwapi_PrintCasaTask   = RAD_HWAPI(20),              /* CASA Task debug print */
    ERadHwapi_PrintTassuRouter = RAD_HWAPI(21),             /* Tassu Router debug print */
    ERadHwapi_PrintBrowserIf   = RAD_HWAPI(22),             /* Browser interface debug print */
    ERadHwapi_PrintBtsLogIf   = RAD_HWAPI(23),              /* BtsLog interface debug print */
    ERadHwapi_PrintTesterIf   = RAD_HWAPI(24),              /* Tester interface debug print */
    ERadHwapi_PrintOicTask    = RAD_HWAPI(25),              /* OPT Service print */
    ERadHwapi_PrintSfnPoll    = RAD_HWAPI(26),              /* Api poll debug print */
    ERadHwapi_PrintInetTcpTask = RAD_HWAPI(27),             /* Inet TCP Task debug print */
    ERadHwapi_PrintInetUdpTask = RAD_HWAPI(28),             /* Inet UDP Task debug print */
    ERadHwapi_BtsomStubL2MemoryConfig = RAD_HWAPI(29),      /* BtsomStub flag for Faraday L2 Memory config */
    ERadHwapi_BtsomStubRuntimeSwSelection = RAD_HWAPI(30),  /* BtsomStub flag for selecting Faraday Runtime SWs*/

    ERadHwapi_Last  /* Not usable value, leave allways to last! */
};

/*@}*/

#endif /* _ERAD_HWAPI_H */
