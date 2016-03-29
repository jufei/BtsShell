/**
*******************************************************************************
* @file                  AaConfigRadDefinitions.h
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
* Design Part            WCDMA:CCS
*
* Development Workset    WCDMA:CCS_ENV_WS
*
* Item Specification     %PP%:%PI%.%PV%-%PT%
*
* Status                 %PS%
*
* Revision History:
* - 0.0.0.6   12.02.2007/TeM  Added AaSysMb definition.
* - 0.0.0.5   05.02.2007/PSa  Added domain defination for DFT.
* - 0.0.0.4   02.02.2007/PSa  Added AaProdTest definitions.
* - 0.0.0.3   16.01.2007/TeA  Added more AaMemAdapter definitions.
* - 0.0.0.2   10.01.2007/TeA  Added some AaMemAdapter definitions.
* - 0.0.0.1   14.12.2006/JuMa Created.
*
* Copyright (c) Nokia 2006. All rights reserved.
*******************************************************************************/

#ifndef _AACONFIG_RAD_DEFINITIONS_H
#define _AACONFIG_RAD_DEFINITIONS_H


#if !defined(RAD_DOMAINS_IN_BTS_SACK)
/**
 *  @defgroup RadDomain R&D Domain
 *  @ingroup  AaConfig
 *
 *  This is part of AaConfig defines Software Domains for Application Runtime 
 *  Variablity.
 */
/*@{*/

/************************** INCLUDED FILES ************************************/

/************************** PUBLIC DECLARATIONS *******************************/

#define RAD_SW_DOMAIN_BITS              16
#define RAD_SW_DOMAIN(domain, radValue) (domain << RAD_SW_DOMAIN_BITS | radValue)

/************************** PUBLIC INTERFACES *********************************/

/*!
 *  @brief  Defines AaConfig R&D parameter software domains.
 */
enum ERadSwDomain
{
    ERadSwDomain_Legacy = 0,            /* BTS old R&D parameter (sw_conf_table) */
    ERadSwDomain_Ccs    = 1,            /* CCS depended parameters */
    ERadSwDomain_Hwapi  = 2,            /* HWAPI depended parameters */
    ERadSwDomain_Dft    = 3,            /* DFT depended parameters */

    ERadSwDomain_Last                   /* Not usable value, leave allways to last! */    
};
             
/*@}*/

#endif /* RAD_DOMAINS_IN_BTS_SACK */


/************************** DOXYGEN GROUPS ************************************/

/**
 *  @defgroup RadCcs            CCS R&D parameters
 *  @ingroup  AaConfigSwDomain
 *
 *  Defines CC&S R&D parameters.
 */
/*@{*/

/************************** INCLUDED FILES ************************************/

#if defined(RAD_DOMAINS_IN_BTS_SACK)
#include <ERadSwDomain.h>
#endif

/************************** PUBLIC DECLARATIONS *******************************/

#define RAD_CCS(value) RAD_SW_DOMAIN(ERadSwDomain_Ccs, value)

/************************** PUBLIC INTERFACES *********************************/

/*!
 *  @brief  Defines CC&S R&D parameters.
 */
enum ERadCcs
{
    ERadCcs_PrintAaSysCom     = RAD_CCS(0),           /* System Internal Communication debug print */
    ERadCcs_PrintAaSysLog     = RAD_CCS(1),           /* System Logging debug print */    
    ERadCcs_PrintAaSysTime    = RAD_CCS(2),           /* System Time Service debug print */
    ERadCcs_PrintAaMem        = RAD_CCS(3),           /* Dynamic Memory Management debug print */
    ERadCcs_PrintAaPro        = RAD_CCS(4),           /* Processs Management debug print */
    ERadCcs_PrintAaSem        = RAD_CCS(5),           /* Semaphore Management debug print */    
    ERadCcs_PrintAaStartup    = RAD_CCS(6),           /* Startup Service debug print */
    ERadCcs_PrintAaFile       = RAD_CCS(7),           /* File Management debug print */
    ERadCcs_PrintAaUdpcpGen   = RAD_CCS(8),           /* UDPCP */    
    ERadCcs_PrintAaUdpcpTx    = RAD_CCS(9),           /* UDPCP */    
    ERadCcs_PrintAaUdpcpRx    = RAD_CCS(10),          /* UDPCP */    
    ERadCcs_PrintAaMemAdapter = RAD_CCS(11),          /* AaMemAdapter debug print */    
    ERadCcs_PrintAaSysComGw   = RAD_CCS(12),          /* SysCom Gw */
    ERadCcs_AaMemAdapterMasterEnable     = RAD_CCS(13),      /* AaMemAdapter master enable switch */
    ERadCcs_AaMemAdapterRtTrace          = RAD_CCS(14),      /* AaMemAdapter runtime trace enable */
    ERadCcs_AaMemAdapterRtObs            = RAD_CCS(15),      /* AaMemAdapter runtime observer enable */

    ERadCcs_AaMemAdapterRtTraceTmo       = RAD_CCS(16),      /* AaMemAdapter runtime trace timeout in secs (0 = default) */

    ERadCcs_AaMemAdapterRtObsTmo         = RAD_CCS(17),          /* AaMemAdapter runtime observer timeout in secs (0 = default) */

    ERadCcs_AaMemAdapterListenerDisable  = RAD_CCS(18),      /* AaMemAdapter listener registeration disable */

    ERadCcs_PrintAaProdTest              = RAD_CCS(19),      /* Production Testing Service debug print */

    ERadCcs_PrintAaProdTestCBist         = RAD_CCS(20),      /* Production Testing Service CBIST debug print */

    ERadCcs_AaProdTestEnable             = RAD_CCS(21),      /* Production Testing Service enable switch */
    
    ERadCcs_PrintAaSysMb                 = RAD_CCS(22),      /* System Message Broker debug print */

    ERadCcs_Last                                  /* Not usable value, do not move or touch! */    
};

/*@}*/

#endif /* _AACONFIG_RAD_DEFINITIONS_H */
