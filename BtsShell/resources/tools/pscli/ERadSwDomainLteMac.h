/**
*******************************************************************************
* @file                  $HeadURL$
* @version               $LastChangedRevision$
* @date                  $LastChangedDate$
* @author                $Author$
*
* Below fields are optional
* @brief                 Short file presentation
* @module                Information to which subcomponent of the system component the source file belongs
* @owner                 Information who owns (i.e. is responsible of) the source file. E.g. Scrum team
*
* Copyright 2011 Nokia Siemens Networks. All rights reserved.
*******************************************************************************/

#ifndef _ERAD_SW_DOMAIN_LTE_MAC_H
#define _ERAD_SW_DOMAIN_LTE_MAC_H

#include <ERadSwDomain.h>

typedef enum ERadSwDomainLteMac
{
    ERadSwDomainLteMac_TRdMaxUlTbSize = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 0),
    /*Maximum uplink TB size. Default value:75376*/
    ERadSwDomainLteMac_DlCqiCompHo = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 1),
    /*negative CQI compensation during HO phase for conservtive MCS.Default value:-5*/
    ERadSwDomainLteMac_TM8SwitchControl= RAD_SW_DOMAIN(ERadSwDomain_LteMac, 2),
    /*Control transmission scheme selection under TM8 for convenience of CMCC test. 0: normal, 1:only switch between SL and TxDiv 2:only switch between SL and DL.Default value:0*/
    ERadSwDomainLteMac_TRdTm8ProbibitTimerMultiplier        = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 4),
    /*Defines Multiplier for the prohibitTimerTmSwitch in TM8.Range:1...5. Default value:5*/
    ERadSwDomainLteMac_TRdTm8to3CqiThdOffset                = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 5),
    /*Defines the CQI offset for tm8to3CqiTh witch used in calculation of swithching point TM8 to TM3. Range:1...5. Default value:3*/
    ERadSwDomainLteMac_TUeBlerTriggerSwitch                 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 6),
    /*LBT1585 1 enable NackInfo collection  */
    ERadSwDomainLteMac_TRdForcedNumPrbs = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 7),
    /*Forced Number of PRBs per DL SCH user. Range:1...100. Default value: 0 (Turns off the forced PRB feature)*/
    ERadSwDomainLteMac_PacketDmaAndSrioType9Enabled = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 8),
    /* 0 = disabled, 1= enabled */
    ERadSwDomainLteMac_TRdMaxDlTbSizeWithoutMimo = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 9),
    /*Maximum downlink TB size when MIMO is not used. Range: 20...80000. Default value: 80000*/
    ERadSwDomainLteMac_TRdMaxDlTbSizeWithMimo = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 10),
    /*Maximum TB size supported when MIMO is enabled. Range: 20...80000. Default value: 80000*/
    ERadSwDomainLteMac_TRdTm4TxDivEnalbe = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 11),
    /*0: fallback to TM4 txDiv is disabled for both "Fast Adaptive CL MIMO Switch" and"Dynamic CL MIMO Switch"; 1: fallback to TM4 txDiv is disabled for "Fast Adaptive CL MIMO Switch" and enabled for"Dynamic CL MIMO Switch"; 2: fallback to TM4 txDiv is enabled for "Fast Adaptive CL MIMO Switch" and disabled for "Dynamic CL MIMO Switch"; 3: fallback to TM4 txDiv is enabled for both "Fast Adaptive CL MIMO Switch" and "Dynamic CL MIMO Switch; default value: 2"*/
   ERadSwDomainLteMac_TRdTm4TxDivFallbackTime = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 12),
    /*Meaningful in case of CL MIMO (dlMimoMode = "Closed Loop MIMO (2x2)" or "Closed Loop MIMO (4x2)") when "Fast Adaptive CL MIMO Switch" is activated (O&M actFastMimoSwitch = true). It defines the maximum time interval (in ms or TTIs) during which a PMI can be used as still reflecting the channel conditions. When PMI periodicity is set such that cqiPerNp >= rdTm4TxDivFallbackTime, (cqiPerNp+10ms) is set as maximum time interval. default value: 50*/
    ERadSwDomainLteMac_TRdCqiAperOptimisticFullFeedbackMode = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 13),
    /* CQI decoder issue. Default value: 1*/
    ERadSwDomainLteMac_TRdMimoOllaUsedOl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 15),
    /*Enables OLLA compensation DELTA_CQI applied to Measurement Filter for Open Loop MIMO. 0: disabled, 1: enabled. Default value: 1*/
    ERadSwDomainLteMac_TRdMimoCqiAgeing = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 16),
    /*Ageing constant for CQI filter during times on inactivity. Range: 0.1 ...1.0. Default vaule: 0.9*/
    ERadSwDomainLteMac_TRdMimoRiAgeing = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 17),
    /*Ageing constant for Rank filter during times on inactivity. Range: 0.1 ...1.0. Default value: 0.9*/
    ERadSwDomainLteMac_TRdTtiObjectList = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 18),
    /*TTI trace object list set. Range: 1...13 Default value: 0*/
    ERadSwDomainLteMac_TRdAveragingPeriod = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 20),
    /*Time period over which the TA measurements are summed for a partial sum. Range: 50...500. Default value: 250*/
    ERadSwDomainLteMac_PoolStatsEnable = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 21),
    /*LBT1186*/
    ERadSwDomainLteMac_TRdPdcchOllaUsed = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 24),
    /*Enables / disables OLLA/OLQC compensation for PDCCH CQI. 0: disabled, 1: enabled. Default vaule: 1*/
    ERadSwDomainLteMac_TRdForcedDlHarqAcks = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 25),
    /*Overwrites received HARQ feedback with ACK. Default vaule: False.*/
    ERadSwDomainLteMac_TRdMaxNumUeTdDl10 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 29),
    /*Maximum number of users taken to time domain scheduling in DL. Applicaple for 10 Mhz cell. Range: 1...1000. Default value: LN2.0 only: 50, Otherwise: 100*/
    ERadSwDomainLteMac_TRdMaxNumUeTdDl15 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 30),
    /*Maximum number of users taken to time domain scheduling in DL. Applicaple for 15 Mhz cell. Range: 1...1000. Default value: LN2.0 only: 50, Otherwise: 100*/
    ERadSwDomainLteMac_TRdMaxNumUeTdDl20 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 31),
    /*Maximum number of users taken to time domain scheduling in DL. Applicaple for 20 Mhz cell. Range: 1...1000. Default value: LN2.0 only: 50, Otherwise: 100*/
    ERadSwDomainLteMac_TRdMaxNumUeTdUl10 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 33),
    /*Maximum number of users taken to time domain scheduling in UL. Applicaple for 10 Mhz cell. Range: 1...1000. Default value: 100*/
    ERadSwDomainLteMac_TRdMaxNumUeTdUl15 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 34),
    /*Maximum number of users taken to time domain scheduling in UL. Applicaple for 15 Mhz cell. Range: 1...1000. Default value: 150*/
    ERadSwDomainLteMac_TRdMaxNumUeTdUl20 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 35),
    /*Maximum number of users taken to time domain scheduling in UL. Applicaple for 20 Mhz cell. Range: 1...1000. Default value: 200*/
    ERadSwDomainLteMac_TRdPdcchAlpha = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 36),
    /*The parameter defines the limit for PDCCH allocations*/
    ERadSwDomainLteMac_0To15FeatLogLevel = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 37),
    /* feature_group:every 16 aligned features in a group*/
    ERadSwDomainLteMac_16To31FeatLogLevel = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 38),
    /*feature_group:every 16 aligned features in a group*/
    ERadSwDomainLteMac_32To47FeatLogLevel = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 39),
    /*feature_group:every 16 aligned features in a group*/
    ERadSwDomainLteMac_48To63FeatLogLevel = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 40),
    /*feature_group:every 16 aligned features in a group*/
    ERadSwDomainLteMac_64To79FeatLogLevel = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 41),
    /*feature_group:every 16 aligned features in a group*/
    ERadSwDomainLteMac_80To95FeatLogLevel = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 42),
    /*feature_group:every 16 aligned features in a group*/
    ERadSwDomainLteMac_96To111FeatLogLevel = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 43),
    /*feature_group:every 16 aligned features in a group*/
    ERadSwDomainLteMac_112To127FeatLogLevel = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 44),
    /*feature_group:every 16 aligned features in a group*/
    ERadSwDomainLteMac_TRdUlPrbLimC10 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 52),
    /*Defines the coefficient for the PUSCH PRB sum PHY resource model for taking into account the scheduled amount of users when deciding the total PRB sum in TTI basis. Applicable to 10 MHz cell.. Range: -5...0. Default: 0*/
    ERadSwDomainLteMac_TRdUlPrbLimC15 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 53),
   /*Defines the coefficient for the PUSCH PRB sum PHY resource model for taking into account the scheduled amount of users when deciding the total PRB sum in TTI basis. Applicable to 15 MHz cell.. Range: -5...0. Default: 0*/
    ERadSwDomainLteMac_TRdUlPrbLimC20 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 54),
    /*Defines the coefficient for the PUSCH PRB sum PHY resource model for taking into account the scheduled amount of users when deciding the total PRB sum in TTI basis. Applicable to 20 MHz cell.. Range: -5...0. Default: 0*/
    ERadSwDomainLteMac_TRdUlPrbLimC2c10 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 56),
    /*Defines the coefficient for the PUSCH PRB sum PHY resource model for taking into account the scheduled amount of users when deciding the total PRB sum in TTI basis. Applicable to dual 10 MHz cells in one FSP. Range: -5...0. Default: 0*/
    ERadSwDomainLteMac_TRdUlPrbMax10 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 58),
   /*Defines the maximum for the PUSCH PRB sum PHY resource model for taking into account when deciding the total PRB sum in TTI basis. Applicable to 5 MHz cell. Range: 0...50. Default: 50*/
    ERadSwDomainLteMac_TRdUlPrbMax15 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 59),
    /*Defines the maximum for the PUSCH PRB sum PHY resource model for taking into account when deciding the total PRB sum in TTI basis. Applicable to 5 MHz cell. Range: 0...75. Default: 75*/
    ERadSwDomainLteMac_TRdUlPrbMax20 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 60),
    /*Defines the maximum for the PUSCH PRB sum PHY resource model for taking into account when deciding the total PRB sum in TTI basis. Applicable to 5 MHz cell. Range: 0...100. Default: 100*/
    ERadSwDomainLteMac_TRdUlPrbMax2c10 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 62),
    /*Defines the maximum for the PUSCH PRB sum PHY resource model for taking into account when deciding the total PRB sum in TTI basis. Applicable to dual 10 MHz cells in one FSP. Range: 0...50. Default: 50*/
    ERadSwDomainLteMac_TRdEnUlPrbSumLim = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 63),
    /*Enables / disables PUSCH PRB sum PHY resource model. 0: disabled, 1: enabled. Default: 0*/
    ERadSwDomainLteMac_TRdUlTbsLimC10 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 65),
    /*Defines the coefficient for the PUSCH TBS sum PHY resource model for taking into account the scheduled amount of users when deciding the total TBS sum in TTI basis. Applicable to 10 MHz cell.. Range: -3669...0. Default: 0*/
    ERadSwDomainLteMac_TRdUlTbsLimC15 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 66),
    /*Defines the coefficient for the PUSCH TBS sum PHY resource model for taking into account the scheduled amount of users when deciding the total TBS sum in TTI basis. Applicable to 15 MHz cell. Range: -3670...0. Default: 0*/
    ERadSwDomainLteMac_TRdUlTbsLimC20 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 67),
    /*Defines the coefficient for the PUSCH TBS sum PHY resource model for taking into account the scheduled amount of users when deciding the total TBS sum in TTI basis. Applicable to 15 MHz cell. Range: -3768...0. Default: 0*/
    ERadSwDomainLteMac_TRdUlTbsLimC2c10 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 69),
    /*Defines the coefficient for the PUSCH TBS sum PHY resource model for taking into account the scheduled amount of users when deciding the total TBS sum in TTI basis. Applicable to dual 10 MHz cells in one FSP. Range: -3669...0. Default: 0*/
    ERadSwDomainLteMac_TRdUlTbsMax10 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 71),
    /*Defines the maximum for the PUSCH TBS sum PHY resource model  for taking into account when deciding the total TBS sum in TTI basis. Applicable to 10 MHz cell. Range: 0...36696. Default: 36696*/
    ERadSwDomainLteMac_TRdUlTbsMax15 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 72),
    /*Defines the maximum for the PUSCH TBS sum PHY resource model   for taking into account when deciding the total TBS sum in TTI basis.  Applicable to 15 MHz cell. Range: 0...55056. Default: 55056*/
    ERadSwDomainLteMac_TRdUlTbsMax20 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 73),
    /*Defines the maximum for the PUSCH TBS sum PHY resource model   for taking into account when deciding the total TBS sum in TTI basis. Applicable to 20 MHz cell. Range: 0...75376. Default: 75376*/
    ERadSwDomainLteMac_TRdUlTbsMax2c10 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 75),
    /*Defines the maximum for the PUSCH TBS sum PHY resource model   for taking into account when deciding the total TBS sum in TTI basis.  Applicable to dual 10 MHz cells in one FSP. Range: 0...36696. Default: 36696*/
    ERadSwDomainLteMac_TRdEnUlTbsSumLim = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 77),
    /*Enables / disables PUSCH TBS sum PHY resource model. 0: disabled, 1: enabled. Default: 0*/
    ERadSwDomainLteMac_TRdUlBufferMargin = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 78),
    /*Defines UL buffer margin which is multiplier for the reported buffer size totally. Range: 1...2. Default: 1.15*/
    ERadSwDomainLteMac_TRdAbsMaxCrLimit = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 82),
    /*Absolute maximum code rate for allowing the scheduling of Secondary System Information and paging, shall not be set below rdMaxCrSibDl or rdMaxCrPgDl. Range: 0.05 ... 1.00. Default: 0.67*/
    ERadSwDomainLteMac_TRdMaxMcsDl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 83),
    /*Maximum MCS to be used in DL. Range: 0...28. Default: 28*/
    ERadSwDomainLteMac_TRdUlMacRetransmissionPolicy = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 84),
    /*0: chase combining; 1: incremental redundancy*/
    ERadSwDomainLteMac_TRdCqiAperEnable = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 85),
    /*Enables / disables aperiodic CQI / RI / PMI reporting in UE basis. Range: TRUE/FALSE. Default: TRUE*/
    ERadSwDomainLteMac_TRdFixWeightPusch = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 88),
    /*Fixed weighting for PUSCH based measurements for calculation of the weighted sum of measurements from different ch. Range: 0...1. Default: 1*/
    ERadSwDomainLteMac_TRdFixWeightCch = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 89),
    /*Fixed weighting for PUCCH based measurements for calculation of the weighted sum of measurements from different ch. Range: 0...1. Default: 1*/
    ERadSwDomainLteMac_TRdQci5SignInactivityTimer = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 90),
    /*Defines the specific inactivity timer value for QCI5 bearer with schedulType = Signalling. Range: 0...180*/
    ERadSwDomainLteMac_TRdTaPucchEnable = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 94),
    /*Selector to enable/disable timing error measurements on PUCCH receptions. Range: TRUE/FALSE. Default: TRUE*/
    ERadSwDomainLteMac_TRdMinMcsDl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 96),
    /*Minimum MCS to be used in DL. Range:0...28. Default: 0*/
    ERadSwDomainLteMac_TDlPsCycleProfileEnable = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 97),
    /*Dl PS Cycel Profile Enable. 0: disabled, 1: enabled. Default: 0*/
    ERadSwDomainLteMac_TRdPrioNumPrbsUl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 98),
    /*Increment in Scheduling Priority per PRB in the calculation of scheduling metric for UL retransmission. Range: 0.01...10. Default: 1*/
    ERadSwDomainLteMac_TRdTargetTimeOffset = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 99),
    /*Time offset subtracted from TA Commands to delay the uplink timing by this amount compared to the reference timing of Rx. Range: 0...2.5. Default: 0*/
    ERadSwDomainLteMac_TTaEnable = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 103),
    /*TA enable. 0: disabled, 1: enabled. Default: 1*/
    ERadSwDomainLteMac_TRdTaWindow = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 104),
    /*The number of consecutive averaging periods from which the measurements are included when calculating the weighted sum for the complex Phi estimate. Range: 1...10. Default: 4*/
    ERadSwDomainLteMac_TRdTaMinReliability = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 105),
    /*Minimum required value of the reliability (magnitude of SumPhiTotal) of the measurements to calculate a valid Time Offset Estimate and Time Alignment Command. Range: 0...32. Default: 1*/
    ERadSwDomainLteMac_TRdTaAgingF = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 106),
    /*The aging factor to be applied to measurements of the previous averaging periods. Range: 0...1. Default: 0.5*/
    ERadSwDomainLteMac_TRdBlindPeriodMax = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 107),
    /*Allowed maximum time period without reliable timing offset estimate to maintain the UE uplink synchronization based on the latest valid estimate of the required correction to the UE timing advance. Range: 0...5000. Default: 1000*/
    ERadSwDomainLteMac_TRdUlAtbPhrShift = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 109),
    /*Offset to the power headroom reports in order to have possibility to allow high P0 values but also to have the possibility to go down to smaller power values before number of PRBs given to the UE is reduced. Range: -50...50. Default: 15*/
    ERadSwDomainLteMac_TRdUlPrbMin = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 110),
    /*The lower limit for the number of PRBs under which the number of PRBs given to UE will not be limited by Power Headroom Reports. Range: 1...10. Default: 1*/
    ERadSwDomainLteMac_TPerfMonIntEnabled = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 112),
    /*0=disabled. Bit index for enabling, 0xFFFFFFFF all enabled*/
    ERadSwDomainLteMac_TDisableLomCounterUpdate = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 113),
    /*Disabled by default. If not 0: LOM counters are not updated*/
    ERadSwDomainLteMac_TRdMcsReductDummy = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 114),
    /*Number of MCS steps reduced from MCS recommended by link adaptation for dummy grant users. Range: 1...10. Default: 0*/
    ERadSwDomainLteMac_TRdMaxMcsUl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 115),
    /*Maximum MCS to be used in UL. Range: 0...28. Default: 28*/
    ERadSwDomainLteMac_TRdMinMcsUl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 116),
    /*Minimum MCS to be used in UL. Range: 0...28. Default: 0*/
    ERadSwDomainLteMac_TRdPdcchCapDlSched = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 119),
    /*Enables / disables checking of the PDCCH capacity during dynamic downlink scheduling. 0: disabled, 1: enabled*/
    ERadSwDomainLteMac_TRdPdcchCapUlSched = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 121),
    /*Enables / disables checking of the PDCCH capacity during uplink scheduling. 0: disabled, 1: enabled*/
    ERadSwDomainLteMac_UlMcsDownStep = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 122),
    /*downgrade mcs when send reconfigration to source enb for HO*/
    ERadSwDomainLteMac_PrintUlGrantNumber = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 123),
    /*set print ul grant information number after attach*/
    ERadSwDomainLteMac_PrintDlGrantNumber = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 124),
    /*set print dl grant information number after attach*/
    ERadSwDomainLteMac_TRdMaxNumUeTdUlDualCell = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 138),
    /*The parameter defines maximum amount of users that can be taken into UL time domain scheduling per cell from capacity restrictions point of view in case of 2 cells in the same FSP. Range: 1...1000. Default: 100*/
    ERadSwDomainLteMac_TRdMaxNumUeFdUlDualCell = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 140),
    /*The parameter defines maximum amount of users can be taken into UL frequency domain scheduling per cell from capacity restrictions point of view in case of 2 cells in the same FSP. Range:1...20*/
    ERadSwDomainLteMac_TRdUlsPrbGapChangeEn = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 147),
    /*Defines if change of PUSCH subarea (gap) is allowed to optimise the PRB allocation when adding PRBs for a UE in uplink allocation. Range: 0...2. Default: 2*/
    ERadSwDomainLteMac_TRdUlsFdLastPdcchResUseEnable = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 151),
    /*Defines if usage of the last PDCCH resources is allowed in UL FD scheduling in case PDCCH capacity left is less than required PDCCH capacity of any remaining user selected for FD scheduling*/
    ERadSwDomainLteMac_TRdUlsHolEstSrFactor = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 157),
    /*The parameter defines the portion of SR period exceeding 20ms that is counted as Head of Line delay in case of Scheduling Request for QCI=1 bearer. Range: 0...1. Default: 0.5*/
    ERadSwDomainLteMac_TRdUlsSrIntervalForSidDetection = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 158),
    /*The parameter defines the minimum interval between consecutive Scheduling Requests to conclude silent period for QCI=1 bearer. Range: 0...100. Default: 50*/
    ERadSwDomainLteMac_TRdVoicePacketIAT = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 159),
    /*The parameter defines an interarrival time of voice packet to be taken into account. Range: 1...50. Default: 20*/
    ERadSwDomainLteMac_TRdCqiAperMaxUlSchCodeRateIncreaseRatio = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 160),
    /*Defines maximum limit for UL-SCH data code rate increase due to requesting of aperiodic CQI/RI/PMI feedback. Range: 1...10. Default: 1.5*/
    ERadSwDomainLteMac_TRdUlFdSchMinRequiredTbs = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 162),
    /*Defines minimum required transport block size in UL frequency domain scheduling. Range: 0...75376. Default: 100*/
    ERadSwDomainLteMac_TRdDlCodeRateBoost = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 163),
    /*Defines code rate boost multiplier in downlink. Range: 0...2. Default: 1*/
    ERadSwDomainLteMac_TRdUlMaxCodeRate = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 164),
    /*Defines maximum allowed code rate in uplink*/
    ERadSwDomainLteMac_TRdUlReTxPercentage = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 165),
    /*Defines the percentage of UEs with possible adaptive retransmission in a TTI for which the resources are assumed to be needed when estimating the resource availability for RA msg3/ 1st scheduled UL transmission in the TTI. Range: 0...100. Default: 25*/
    ERadSwDomainLteMac_TRdDlOlqcSlowdownEnable = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 166),
    /*Enables / disables DL OLQC slowdown functionality which takes into account HARQ feedback latencies by slowing updating speed for frequently scheduled UE*/
    ERadSwDomainLteMac_TRdDlLaMaxHysteresisFactor = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 167),
    /*Defines the maximum hysteresis factor inserted to stored CQI / default CQI is FD scheduling phase. The hystersis functionality is disabled with setting 0. */
    ERadSwDomainLteMac_TRdMimoOllaUsedCI = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 168),
    /*Enables OLLA compensation DELTA_CQI applied to Measurement Filter for Closed Loop MIMO*/
    ERadSwDomainLteMac_TRdLatMeas1 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 175),
    /*The parameter defines if latency measurement for I&V purposes is enabled. With this parameter most important cell specific messages are traced. */
    ERadSwDomainLteMac_TRdLatMeas2 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 176),
    /*The parameter defines if latency measurement for I&V purposes is enabled. With this parameter most additional cell specific messages are traced.*/
    ERadSwDomainLteMac_TRdLatMeas3 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 177),
    /*The parameter defines if latency measurement for I&V purposes is enabled. With this parameter most important UE specific messages are traced.*/
    ERadSwDomainLteMac_TRdEnableMacFatalExceptionInd = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 178),
    /*This parameter defines if memory allocation failure, latency check failing, out-of-sequence error or missing of message shall cause fatal error in LTE MAC.*/
    ERadSwDomainLteMac_TRdMimoCqiAgeingDrx = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 179),
    /*Defines CQI ageing coefficient used in MIMO mode control algorithm for an UE with long DRX cycle enabled. Range: 0...1.00. Default: 0.98*/
    ERadSwDomainLteMac_TRdMimoRiAgeingDrx = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 180),
    /*Defines RI ageing coefficient used in MIMO mode control algorithm for an UE with long DRX cycle enabled. Range: 0...1.00. Default: 0.98*/
    ERadSwDomainLteMac_TRdUlsWeightDrxAct1 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 182),
    /*Defines the weighting factor used in UL TD scheduling metric for UE with remaining DRX Active Time of 1 ms. Range: 0...100. Default: 10*/
    ERadSwDomainLteMac_TRdUlsWeightDrxAct2 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 183),
    /*Defines the weighting factor used in UL TD scheduling metric for UE with remaining DRX Active Time of 2 ms. Range: 0...100. Default: 5*/
    ERadSwDomainLteMac_TRdUlsWeightDrxAct3 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 184),
    /*Defines the weighting factor used in UL TD scheduling metric for UE with remaining DRX Active Time of 3 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdUlsWeightDrxAct4 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 185),
    /*Defines the weighting factor used in UL TD scheduling metric for UE with remaining DRX Active Time of 4 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdUlsWeightDrxAct5 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 186),
    /*Defines the weighting factor used in UL TD scheduling metric for UE with remaining DRX Active Time of 5 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdUlsWeightDrxAct6 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 187),
    /*Defines the weighting factor used in UL TD scheduling metric for UE with remaining DRX Active Time of 6 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdUlsWeightDrxAct7 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 188),
    /*Defines the weighting factor used in UL TD scheduling metric for UE with remaining DRX Active Time of 7 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdUlsWeightDrxAct8 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 189),
    /*Defines the weighting factor used in UL TD scheduling metric for UE with remaining DRX Active Time of 8 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdUlsWeightDrxAct9 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 190),
    /*Defines the weighting factor used in UL TD scheduling metric for UE with remaining DRX Active Time of 9 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdUlsWeightDrxAct10 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 191),
    /*Defines the weighting factor used in UL TD scheduling metric for UE with remaining DRX Active Time of 10 ms or greater. Range: 0...100 Default: 1*/
    ERadSwDomainLteMac_TRdDlsDrxWeightActTime1 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 192),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with remaining DRX Active Time of 1 ms. Range: 0...100. Default: 10*/
    ERadSwDomainLteMac_TRdDlsDrxWeightActTime2 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 193),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with remaining DRX Active Time of 2 ms. Range: 0...100. Default: 5*/
    ERadSwDomainLteMac_TRdDlsDrxWeightActTime3 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 194),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with remaining DRX Active Time of 3 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdDlsDrxWeightActTime4 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 195),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with remaining DRX Active Time of 4 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdDlsDrxWeightActTime5 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 196),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with remaining DRX Active Time of 5 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdDlsDrxWeightActTime6 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 197),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with remaining DRX Active Time of 6 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdDlsDrxWeightActTime7 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 198),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with remaining DRX Active Time of 7 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdDlsDrxWeightActTime8 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 199),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with remaining DRX Active Time of 8 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdDlsDrxWeightActTime9 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 200),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with remaining DRX Active Time of 9 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdDlsDrxWeightActTime10 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 201),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with remaining DRX Active Time of 10 ms. Range: 0...100. Default: 1*/
    ERadSwDomainLteMac_TRdDlsDrxWeightCqiSb = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 202),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with subband CQI received during a current DRX active time. Range: 0...1. Default: 1*/
    ERadSwDomainLteMac_TRdDlsDrxWeightCqiWb = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 203),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with wideband CQI received during a current DRX active time. Range: 0...1. Default: 0.90*/
    ERadSwDomainLteMac_TRdDlsDrxWeightCqiOld = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 204),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with old CQI which is not received during a current active time and which CQI age is less than rrmDlamcTHistCqi. Range: 0...1. Default: 0.80*/
    ERadSwDomainLteMac_TRdDlsDrxWeightCqiDef = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 205),
    /*Defines the weighting factor used in DL TD scheduling metric for UE with a default CQI in use. Range: 0...1. Default: 0.70*/
    ERadSwDomainLteMac_TRdPdcchMaxPsdRedSym0 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 212),
    /*Defines the maximum allowed reduction in PDCCH EPRE (PSD) on the first OFDM symbol (symbol 0) due to configured boosting of CRS, PCFICH and/or PHICH when deciding level of PHICH boosting. CRS and PCFICH are always boosted without checking this limit. Range: 0...10. Default: 4*/
    ERadSwDomainLteMac_TRdPdcchPcMaxScalingDown = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 214),
    /*Defines the maximum power which can be scaled down in PDCCH symbol basis. Range: -40...0. Default: -40*/
    ERadSwDomainLteMac_TRdMinDrxActHOdelay = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 237),
    /*Defines the minimum time for which a UE needs to be kept in DRX active the Short Term Inactivity Timer. Range: 0...5000. Default: 0*/
    ERadSwDomainLteMac_TRdDelayDiscTimerOperInSync = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 238),
    /*Defines the safety margin between detection of TA In-Sync and DRX Active state and the indication to TUPu to resume discard timer operation. Range: 10...1000. Default: 300*/
    ERadSwDomainLteMac_TRdNoRepPdcchOrder = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 239),
    /*Defines how many times PDCCH order / preamble assignment is tried/repeated before considering PDCCH order failure. Range: 0...3. Default: 1*/
    ERadSwDomainLteMac_TRdDlsMaxNumPdcchOrderTti = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 240),
    /*Defines the maximum limit for amount of PDCCH orders in one TTI. Range: 0...50. Default: 5*/
    ERadSwDomainLteMac_TRdEnableScheduledUesPerTtiDL = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 241),
    /*MAC GEN DL print for schedules UES / TTI, 0 = disabled, > 0 = enabled (print interval in steps of 1 TTI e.g. 1000 = print every 1000 TTIs)*/
    ERadSwDomainLteMac_TRdUlsFdWrrEnable = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 245),
    /*The parameter enables / disables the Weighted Round Robin scheduler in uplink Frequency Domain scheduling. */
    ERadSwDomainLteMac_TRdPdcchOrderExpT = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 246),
    /*Defines the time for waiting completion of RA procedure which was initiated by PDCCH order before considering the corresponding PDCCH order failed and as well the time for keeping a dedicated preamble reserved for certain PDCCH order after signalling/repeating it last time on PDCCH. Range: 50...2000. Default: 450*/
    ERadSwDomainLteMac_TRdUlsMaxEstBsLcg1F = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 249),
    /*The parameter defines the upper limit for periodically increasing the estimated buffer size for LCG1 assuming constant bit rate of ulsGbrRlc after Scheduling Request has been received. Range: 1...100. Default: 2*/
    ERadSwDomainLteMac_TRdPdcchMaxCr = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 258),
    /*Pdcch MaxCr*/
    ERadSwDomainLteMac_TRdFixWeightSrs = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 259),
    /*SRS weight. range:0~1,default:1 */
    ERadSwDomainLteMac_TRdUlGbrEnable = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 267),
    /*ul GBR enable. 0=disabled, 1=enabled*/
    ERadSwDomainLteMac_TRdEnableGbrBufferLevelEvalDl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 269),
    /*Defines if GBR DRB buffer level evaluation is enabled*/
    ERadSwDomainLteMac_TRdPuschHoppingEnable = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 270),
    /*Pusch hopping enable. 0=disabled,1=enabled*/
    ERadSwDomainLteMac_TRdPuschHopOffset = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 271),
    /*Pusch hopping offset. 0--max bw*/
    ERadSwDomainLteMac_TRdHopModePusch = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 272),
    /*Pusch hopping mode. 0=inter,1=InterAndIntra*/
    ERadSwDomainLteMac_TRdHopSubBwPusch = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 273),
    /*1---N*/
    ERadSwDomainLteMac_TRdHopTypePusch = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 274),
    /*Push hopping type. 0=type1,1=type2*/
    ERadSwDomainLteMac_TRdHopPatternExplictInfBased = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 275),
    /*0=1/2(6-49),1=1/4,2=-1/4,3=1/2(50-110)*/
    ERadSwDomainLteMac_TRdOptPhichCalcMethodTwo = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 277),
    /*PHICH power method flag .0 :methed 2; 1:menthed 1*/
    ERadSwDomainLteMac_TRdOptPhichLogSwither = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 278),
    /*PHICH power print switcher .0 :close ; 1:open */
    ERadSwDomainLteMac_TPdcchPcEnableRelocation = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 280),
    /*PDCCH power control enable relocation flag */
    ERadSwDomainLteMac_TRdUlMsg3PwCtrl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 284),
    /*Ul Msg3 power control*/
    ERadSwDomainLteMac_TRdPdcchUtilThUp = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 288),
    /*Defines PDCCH utilization threshold for increasing minimum number of PDCCH symbols. Range: 0...100. Default: 80*/
    ERadSwDomainLteMac_TRdPdcchUtilThDown = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 289),
    /*Defines PDCCH utilization threshold for decreasing minimum number of PDCCH symbols. Applicable if actLdPdcch is true.Range: 0...100. Default: 60*/
    ERadSwDomainLteMac_TRdPdcchAlphaLowerSymScalingFactor = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 290),
    /*Defines the multiplier for scaling the configured PDCCH alpha (pdcchAlpha) for number of PDCCH symbols lower than the default/maximum. Range: 0.001...1.000. Default: 0.875*/
    ERadSwDomainLteMac_TRdPdcchMinNumCces = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 291),
    /*Defines minimum number of CCEs per direction in USS. Range: 1...16*/
    ERadSwDomainLteMac_TRdPdcchUlCceUsageMargin = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 292),
    /*Defines the margin to be added on top of number of CCEs used for UL PDCCH entries. Range: 0.00...0.50. Default: 0.25*/
    ERadSwDomainLteMac_TRdPdcchUlDlBalHighLimit = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 293),
    /*Defines maximum value for PDCCH capacity split between UL and DL. Range: 0.01...1.00. Default: 0.7*/
    ERadSwDomainLteMac_TRdPdcchUlDlBalLowLimit = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 294),
    /*Defines minimum value for PDCCH capacity split between UL and DL. Range: 0.00...0.99. Default: 0.3*/
    ERadSwDomainLteMac_TRdPdcchUlDlBalStepIn = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 295),
    /*Defines step size towards initial value for dynamically controlled PDCCH capacity balance between UL and DL. Range: 0.00...0.20. Default: 0.1*/
    ERadSwDomainLteMac_TRdPdcchUlDlBalUsageLever = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 296),
    /*Defines multiplier for PUSCH to PDSCH ratio when controlling PDCCH capacity between UL and DL dynamically. Range: 1...10. Default: 1*/
    ERadSwDomainLteMac_TRdEnableDynUlDlBal = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 298),
    /*Defines switch for enabling/disabling dynamic control of PDCCH resource split between UL and DL.*/
    ERadSwDomainLteMac_TRdAgingRrmPdcchMinNumOfSym = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 299),
    /*Used as a conservative way to age rrmPdcchMinNumOfSym by increase it because more delay in TDD and especially more delay caused by PRS or MBSFN sub-frames which will make the value out-of-date. Range: 5..100. Default: 15*/
    ERadSwDomainLteMac_TRdPdcchCqiShiftStepupFactor = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 300),
    /*PDCCH CQI shift stepup size (rrmPdcchCqiShiftStepup) is got by multiplying dlOlqcDeltaCqiStepup parameter by this parameterized factor. The parameter is applicable only if actOlLaPdcch has been enabled. Range: 0.5...2. Default: 1*/
    ERadSwDomainLteMac_TRdPdcchCqiShiftDtxAllTrans = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 302),
    /*Defines if DL HARQ DTX feedback for all DL transmissions is considered in PDCCH CQI shift control algorithm. */
    ERadSwDomainLteMac_TRdPdcchCombUssAllocAndPwrEnable = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 303),
    /*Enables/disables PDCCH scheduling approach for combined USS allocation and power setting.*/
    ERadSwDomainLteMac_TRdPdcchPcSoftBlockTh = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 304),
    /*Defines the power threshold for blocking PDCCH entry due to missing power. Range: 0...6. Default: 3.*/
    ERadSwDomainLteMac_TRdMimoBfUpdateInterval = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 305),
    /*Time Interval for updating the beamforming weighting vector. Default: 1000*/
    ERadSwDomainLteMac_TRdOlqcBfInitOffset = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 306),
    /*Initial CQI Offset for Beamforming Transmission Mode and Reported CQI. Range: -15 to +15, in steps of 0.1. Default: 1*/
    ERadSwDomainLteMac_TRdRfilterCoff = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 307),
    /*R_FILTER_COFF. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticWFlag = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 308),
    /*R_STATIC_WFLAG. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW0_REAL = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 309),
    /*R_STATIC_W0_REAL. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW0_IMAG = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 310),
    /*R_STATIC_W0_IMAG. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW1_REAL = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 311),
    /*R_STATIC_W1_REAL. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW1_IMAG = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 312),
    /*R_STATIC_W1_IMAG. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW2_REAL = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 313),
    /*R_STATIC_W2_REAL. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW2_IMAG = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 314),
    /*R_STATIC_W2_IMAG. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW3_REAL = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 315),
    /*R_STATIC_W3_REAL. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW3_IMAG = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 316),
    /*R_STATIC_W3_IMAG. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW4_REAL = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 317),
    /*R_STATIC_W4_REAL. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW4_IMAG = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 318),
    /*R_STATIC_W4_IMAG. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW5_REAL = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 319),
    /*R_STATIC_W5_REAL. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW5_IMAG = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 320),
    /*R_STATIC_W5_IMAG. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW6_REAL = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 321),
    /*R_STATIC_W5_REAL. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW6_IMAG = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 322),
    /*R_STATIC_W6_IMAG. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW7_REAL = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 323),
    /*R_STATIC_W7_REAL. Q15: 0.01*/
    ERadSwDomainLteMac_TRdStaticW7_IMAG = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 324),
    /*R_STATIC_W7_IMAG. Q15: 0.01*/
    ERadSwDomainLteMac_TRdLogLevelDlPs = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 328),
    /*control whether print the longTerm weight: not print:0,  print:1. */
    ERadSwDomainLteMac_TRdMimoOllaUsedBfsl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 335),
    /*control if the effect of OLLA in MIMO switch alg is truned on. 0:false, 1:true*/
    ERadSwDomainLteMac_TRdMimoOllaUsedBfdl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 336),
    /*control if the effect of OLLA in MIMO switch alg is truned on. 0:false, 1:true*/
    ERadSwDomainLteMac_TRdTraceProfileMinUes = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 360),
    /*Trace profing MinUes*/
    ERadSwDomainLteMac_TRdTMcsAvgUl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 362),
    /*Averaging constant for GBR throughput calculation what is used in UL time domain scheduling. Range: 100...1000. Default: 300*/
    ERadSwDomainLteMac_TRdUlMinNumTtiGbr = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 363),
    /*Minimum number of TTIs considered for GBR token bucket. range 0...200, default 10*/
    ERadSwDomainLteMac_TUeBlerTriggerCrnti0 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 364),
    /*LBT1585 set an invaild crnti*/
    ERadSwDomainLteMac_TUeBlerTriggerCrnti1 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 365),
    /*LBT1585 set an invaild crnti*/
    ERadSwDomainLteMac_TUeBlerTriggerCrnti2 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 366),
    /*LBT1585 set an invaild crnti*/
    ERadSwDomainLteMac_TRdCqiAvgDl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 374),
    /*Averaging constant for GBR throughput calculation what is used in DL time domain scheduling. Range: 100...1000. Default: 300.*/
    ERadSwDomainLteMac_TRdDlMinNumTtiGbr = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 375),
    /*Minimum number of TTIs considered for GBR token bucket. Range: 0...200 Default: 10*/
    ERadSwDomainLteMac_TRdGbrLoadMeasRepInterval = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 376),
    /*Defines reporting interval for GBR load related measurements. Range: 100...3000. Default: 500.*/
    ERadSwDomainLteMac_TRdPdschPrbUtilAvgT = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 377),
    /*Defines time constant for averaging function of PDSCH PRB monitoring. Range: 100...1000. Default: 300*/
    ERadSwDomainLteMac_TRdPuschPrbUtilAvgT = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 378),
    /*Defines time constant for averaging function of PUSCH PRB monitoring. Range: 100...1000*/
    ERadSwDomainLteMac_TRdPdcchCceUtilAvgTDl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 379),
    /*Defines time constant for averaging function of PDCCH CCE monitoring for DL PDCCH entries. Range: 100...1000. Default: 300*/
    ERadSwDomainLteMac_TRdPdcchCceUtilAvgTUl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 380),
    /*Defines time constant for averaging function of PDCCH CCE monitoring. Range: 100...10000*/
    ERadSwDomainLteMac_TRdDlsPdschCongDetAct = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 381),
    /*Activates PDSCH based congestion detection*/
    ERadSwDomainLteMac_TRdDlsPdschCongGbrHyst = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 382),
    /*PDSCH GBR congestion hysteresis factor. Range: 0.7...1.0. Default: 0.9*/
    ERadSwDomainLteMac_TRdDlsPdschCongT = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 383),
    /*PDSCH GBR congestion timer value. Range: 100...1000. Default: 300*/
    ERadSwDomainLteMac_TRdUlsCongIndTtt = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 384),
    /*Defines time-to-trigger value for UL congestion indications. Range: 100...1000. Default: 300*/
    ERadSwDomainLteMac_TRdUlsPuschCongDetPwrLimitAct = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 385),
    /*Activates PUSCH congestion detection for power limited users*/
    ERadSwDomainLteMac_TRdUlsPuschCongDetAct = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 386),
    /*Activates PUSCH based congestion detection*/
    ERadSwDomainLteMac_TRdUlsPuschCongGbrHyst = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 387),
    /*PUSCH GBR congestion hysteresis factor. Range: 0.7...1.0. Default: 0.9*/
    ERadSwDomainLteMac_TRdUlsPuschCongT = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 388),
    /*PUSCH GBR congestion timer value. Range: 100...1000. Default: 300*/
    ERadSwDomainLteMac_TRdPdcchCongDetActUl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 389),
    /*Activates PDCCH congestion detection in UL*/
    ERadSwDomainLteMac_TRdPdcchCongDetActDl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 390),
    /*Activates PDCCH congestion detection in DL*/
    ERadSwDomainLteMac_TRdPdcchGbrBlockAvConst = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 391),
    /*Defines time constant for averaging function of PDCCH blocking level and PDCCH GBR blocked resource monitoring. Range: 100...1000. Default: 300*/
    ERadSwDomainLteMac_TRdPdcchCongGbrCceHyst = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 392),
    /*PDCCH GBR congestion hysteresis factor. Range: 0.7...1.0. Default: 0.9*/
    ERadSwDomainLteMac_TRdPdcchCongGbrT = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 393),
    /*PDCCH GBR congestion timer value. Range: 100...1000. Default: 300*/
    ERadSwDomainLteMac_TRdPdcchCongGbrBlockLimit = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 394),
    /*PDCCH GBR blocking congestion limit. Range: 0.3...1.0. Default: 0.5*/
    ERadSwDomainLteMac_TRdPdcchCongGbrBlockHyst = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 395),
    /*PDCCH GBR blocking congestion hysteresis factor. Range: 1.0....1.5. Default: 1.3*/
    ERadSwDomainLteMac_TRdSchLoadControlConfigDl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 396),
    /*DL PS CPU margin, default is 25%, valid range is from 0 to 50*/
    ERadSwDomainLteMac_TRdMuMimoLogCtrl  = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 400),
    /*DL MuMimo log control. range 0..1*/
    ERadSwDomainLteMac_TRdIpaFlag = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 401),
    /*dScUlpc = 0,1,2*/
    ERadSwDomainLteMac_TRdIpaDummy1 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 402),
    /*domRrhWinLen = 1.5us, convert to 1500*/
    ERadSwDomainLteMac_TRdIpaDummy2 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 403),
    /*rrhSinrAvgT = 30ms*/
    ERadSwDomainLteMac_TRdIpaDummy3 = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 404),
    /*rrhSwitchSinrHys = 1.5db*/
    ERadSwDomainLteMac_TRdActivateCongBearerPrioDl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 409),
    /*Activates feature for GBR bearer de-prioritization in case of GBR congestion on PDSCH*/
    ERadSwDomainLteMac_TRdActPdcchUssAllocAndPwrBlockReduction = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 410),
    /*Activates functionality for PDCCH blocking reduction*/
    ERadSwDomainLteMac_TRdSchLoadControlConfigUl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 414),
    /*UL PS CPU margin, 0 disable, 1 enable*/
    ERadSwDomainLteMac_TRdTokenBucketLowerLimit = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 415),
    /*Defines the lower limit of the token bucket for GBR bearers in negative multiples of the delay target. Range: 1...20. Default: 2*/
    ERadSwDomainLteMac_GAP20Enable = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 416),
    /*0: disabled, 0x0007: All enabled*/
    ERadSwDomainLteMac_TRdActivateCongBearerPrioUl = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 417),
    /*Activates feature for GBR bearer de-prioritization in case of GBR congestion on PUSCH*/
    ERadSwDomainLteMac_TRdGbrIniMcsOffset = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 418),
    /*Defines MCS offset for the initial MCS (iniMcsDl) which is used in calculation of maximum initial transmission efficiency in cell. Range: 0...28. Default: 28. */
    ERadSwDomainLteMac_TRdUlMaxCodeRateForSmallPrb = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 419),
    /*UL PS: maximum UL coderate when allocate one PRB to UE, step size 0.001*/
    ERadSwDomainLteMac_TLast = RAD_SW_DOMAIN(ERadSwDomain_LteMac, 420)
    /*Last*/
} ERadSwDomainLteMac;

#endif /* _ERAD_SW_DOMAIN_LTE_MAC_H */

/**
********************************************************************************
* @enum ERadSwDomainLteMac
* Development Workset :    LTE:LTE_ENV_WS
*
* Design Part :            LTE:LTE_ENV.A;1
*
*
* Remember to put an empty line in the end of each definition file. 
* Otherwise the compiler will generate a warning. 
*******************************************************************************/
