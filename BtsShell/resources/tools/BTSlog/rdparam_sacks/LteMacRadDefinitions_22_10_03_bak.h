/**
*******************************************************************************
* @file                  %PM%
* @version               %PR%
* @date                  %PRT%
* @author                %PO%
* @brief                 ?Short file presentation
*
*                        ?Detailed description
*
* PVCS Information:
*
* PVCS Product           %PP%
*
* Base Database          ?Helena
*
* Design Part            ?WCDMA:CODEC_DSP
*
* Development Workset    ?WCDMA:WN1CODECDSP_WS
*
* Item Specification     %PP%:%PI%.%PV%-%PT%
*
* Status                 %PS%
*
* Revision History:
*
* - 1.0.0 09.11.07/MKJ   First version.
*
* Copyright (c) Nokia Siemens Networks 2007. All rights reserved.
*******************************************************************************/
#ifndef _MAC_RAD_DEFINITIONS_H
#define _MAC_RAD_DEFINITIONS_H

#include <ERadSwDomain.h>


/************************** DOXYGEN GROUPS ************************************/

/**
 *  @defgroup RadLteMac          LTE MAC R&D parameters
 *  @ingroup  AaConfigSwDomain
 *
 *  Defines LTE MAC R&D parameters.
 */
/*@{*/

/************************** INCLUDED FILES ************************************/

/************************** PUBLIC DECLARATIONS *******************************/

// TODO: In future these kind of offsets should not be used in case of signed integers (using is complicated).
//       R&D switches supports also negative value by setting -1 as 0xffffffff.
#define DELTA_CQI_INI_OFFSET 100
#define DELTA_CQI_MIN_OFFSET 100


#define RAD_LTEMAC(value) RAD_SW_DOMAIN( ERadSwDomain_LteMac, value)

/************************** PUBLIC INTERFACES *********************************/

/*!
  @brief  Defines LTE Mac R&D parameters.
 */
enum ERadLteMac
{

  ERadLteMac_MaxUlTbSize     = RAD_LTEMAC(0),
    /*Maximum uplink TB size in bits.*/

  
  ERadLteMac_MaxDlPrbs       = RAD_LTEMAC(1),
	/*Maximum number of PRBs that can be allocated for the UE in DL in one TTI. Value: 1-50, if >25 only even numbers possible.*/
  
   
  
  ERadLteMac_DlMimoIndicator = RAD_LTEMAC(2),
	/* Indicates whether MIMO is used (1) or not (0). */
  

  ERadLteMac_EnableSr        = RAD_LTEMAC(3),
	/*  Enabling/disabling the use of scheduling request.*/
  

  ERadLteMac_DlTfi1          = RAD_LTEMAC(4),
	/* Indicates the transport format for a downlink TB, value: 0 to 23. */
  

  ERadLteMac_DlTfi2          = RAD_LTEMAC(5),
	/* In case of MIMO indicates the transport format for the second */
  

  ERadLteMac_TxPower         = RAD_LTEMAC(6),
/*  Transmission power per subcarrier in W, value: 0 to 1000000*/
  

  ERadLteMac_ForcedNumPrbs   = RAD_LTEMAC(7),
/*  Forced number of PRBs allocated for the transport block.*/
  

  ERadLteMac_MibTbSize   = RAD_LTEMAC(8),
/*  MIB transport block size [bits].*/
  

  ERadLteMac_MaxDlTbSizeWithoutMimo = RAD_LTEMAC(9),
/*  Default value for DL maximum TB size without mimmo*/
  

  ERadLteMac_MaxDlTbSizeWithMimo = RAD_LTEMAC(10),
	/* Default value for DL maximum TB size without mimmo */
  

  ERadLteMac_DeltaCqiIni = RAD_LTEMAC(11),
/*  Initial CQI offset for DL OLQC,*/
  

  ERadLteMac_DeltaCqiMin = RAD_LTEMAC(12),
/*  Minimum CQI offset for DL OLQC,*/
  

  ERadLteMac_DeltaCqiMax = RAD_LTEMAC(13),
/*   Maximum CQI offset for DL OLQC,*/
  

  ERadLteMac_DeltaCqiStepUp = RAD_LTEMAC(14),
/* CQI offset for HARQ ACK response for DL OLQC, */
  
  
  ERadLteMac_MimoOllaUsedOl = RAD_LTEMAC(15),
/*  Enables OLLA compensation DELTA_CQI applied to Measurement Filter*/
  
  
  ERadLteMac_MimoCqiAgeing = RAD_LTEMAC(16),
/*  Ageing constant for CQI filter during times on inactivity*/
  

  ERadLteMac_MimoRiAgeing = RAD_LTEMAC(17),
/*  Ageing constant for Rank filter during times on inactivity*/

  ERadLteMac_TtiObjectList = RAD_LTEMAC(18),
/* parameter selects for different test purposes used measurement object list for TTI Trace of */
 
  ERadLteMac_MaxNumUeTdDl = RAD_LTEMAC(19),
/*  CS1 list length. Number of Ues which can be scheduled in one TTI Time domain.*/

  ERadLteMac_AveragingPeriod = RAD_LTEMAC(20),
/*Time period over which the noise power estimates for early, on-time and late  */

  ERadLteMac_MinN = RAD_LTEMAC(21),
/* Minimum required value for N, the number of valid noise power estimates received */

  ERadLteMac_McDampingFactor = RAD_LTEMAC(22),
/*  Defines a damping factor for the mass centre method to improve the variance*/
 
  ERadLteMac_McFactor = RAD_LTEMAC(23),
/* Defines the gradient of timing correction versus estimated noise power */

  ERadLteMac_TaTimeMargin = RAD_LTEMAC(24),
/*  Used to control the interval between periodic timing alignment commands being sent to the UE.*/

  ERadLteMac_ForcedDlHarqAcks = RAD_LTEMAC(25),
/* When enabled (=GLO_TRUE), Uplink Scheduler sends PucchReceiveRespD msg or */

  ERadLteMac_DlDataMaxNumOfNackSns = RAD_LTEMAC(26),
/* Maximum number of NACKs which can be stored to the NACK list without removing any. */

  ERadLteMac_rdDedicRaPreExpTimer = RAD_LTEMAC(27),
/* Timer value in microsecs) for rdDedicRaPreExpTimer Duration */

  ERadLteMac_MaxNumUeTdDl5 = RAD_LTEMAC(28),
/* Number of Ues which can be scheduled in Dl in one TTI Time domain. 5 Mhz. */
 
  ERadLteMac_MaxNumUeTdDl10 = RAD_LTEMAC(29),
/* Number of Ues which can be scheduled in Dl in one TTI Time domain. 10 Mhz. */

  ERadLteMac_MaxNumUeTdDl15 = RAD_LTEMAC(30),
/*   Number of Ues which can be scheduled in Dl in one TTI Time domain. 15 Mhz.*/

  ERadLteMac_MaxNumUeTdDl20 = RAD_LTEMAC(31),
/* Number of Ues which can be scheduled in Dl in one TTI Time domain. 20 Mhz. */

  ERadLteMac_MaxNumUeTdUl5 = RAD_LTEMAC(32),
/* Number of Ues which can be scheduled in Ul in one TTI Time domain. 5 Mhz. */

  ERadLteMac_MaxNumUeTdUl10 = RAD_LTEMAC(33),
/* Number of Ues which can be scheduled in Ul in one TTI Time domain. 10 Mhz. */

  ERadLteMac_MaxNumUeTdUl15 = RAD_LTEMAC(34),
/* Number of Ues which can be scheduled in Ul in one TTI Time domain. 15 Mhz. */

  ERadLteMac_MaxNumUeTdUl20 = RAD_LTEMAC(35),
/* Number of Ues which can be scheduled in Ul in one TTI Time domain. 20 Mhz. */
 
  ERadLteMac_PdcchAlpha = RAD_LTEMAC(36),
/* Margin for selecting highest possible aggregation for each scheduled PDCCH */

  ERadLteMac_DlTbsMax5  = RAD_LTEMAC(37),
  /* Defines the maximum for the PDSCH TBS sum PHY resource model  for taking into */
  ERadLteMac_DlTbsMax10  = RAD_LTEMAC(38),
  /* Defines the maximum for the PDSCH TBS sum PHY resource model  for taking into */
  ERadLteMac_DlTbsMax15  = RAD_LTEMAC(39),
  /* Defines the maximum for the PDSCH TBS sum PHY resource model  for taking into */
  ERadLteMac_DlTbsMax20  = RAD_LTEMAC(40),
/* Defines the maximum for the PDSCH TBS sum PHY resource model  for taking into */

  ERadLteMac_DlTbsMax2c5  = RAD_LTEMAC(41),
  /*  Defines the maximum for the PDSCH TBS sum PHY resource model  for taking*/
  ERadLteMac_DlTbsMax2c10  = RAD_LTEMAC(42),
/*  Defines the maximum for the PDSCH TBS sum PHY resource model  for taking*/

  ERadLteMac_DlTbsLimC5  = RAD_LTEMAC(43),
  /* Defines the coefficient for the PDSCH TBS sum PHY resource model for */
  ERadLteMac_DlTbsLimC10 = RAD_LTEMAC(44),
  /* Defines the coefficient for the PDSCH TBS sum PHY resource model for */
  ERadLteMac_DlTbsLimC15 = RAD_LTEMAC(45),
  /* Defines the coefficient for the PDSCH TBS sum PHY resource model for */
  ERadLteMac_DlTbsLimC20 = RAD_LTEMAC(46),
/* Defines the coefficient for the PDSCH TBS sum PHY resource model for */

  ERadLteMac_DlTbsLimC2c5 = RAD_LTEMAC(47),
  /*  Defines the maximum for the PDSCH TBS sum PHY resource model  for taking*/
  ERadLteMac_DlTbsLimC2c10 = RAD_LTEMAC(48),
/*  Defines the maximum for the PDSCH TBS sum PHY resource model  for taking*/

  ERadLteMac_EnDlTbsLimOpt = RAD_LTEMAC(49),
/* Enables / disables PDSCH TBS sum PHY resource model limitation optimization. */
 
  ERadLteMac_EnDlTbsSumLim  = RAD_LTEMAC(50),
/*Enables / disables PDSCH TBS sum PHY resource model  */

  ERadLteMac_UlPrbLim5    = RAD_LTEMAC(51),
  /* Defines the coefficient for the PUSCH PRB sum PHY resource model */
  ERadLteMac_UlPrbLim10   = RAD_LTEMAC(52),
  /* Defines the coefficient for the PUSCH PRB sum PHY resource model */
  ERadLteMac_UlPrbLim15   = RAD_LTEMAC(53),
  /* Defines the coefficient for the PUSCH PRB sum PHY resource model */
  ERadLteMac_UlPrbLim20   = RAD_LTEMAC(54),
  /* Defines the coefficient for the PUSCH PRB sum PHY resource model */
  ERadLteMac_UlPrbLim2c5  = RAD_LTEMAC(55),
  /* Defines the coefficient for the PUSCH PRB sum PHY resource model */
  ERadLteMac_UlPrbLim2c10 = RAD_LTEMAC(56),
/* Defines the coefficient for the PUSCH PRB sum PHY resource model */

  ERadLteMac_UlPrbMax5    = RAD_LTEMAC(57),
  /* Defines the maximum for the PUSCH PRB sum PHY resource model taking */
  ERadLteMac_UlPrbMax10   = RAD_LTEMAC(58),
  /* Defines the maximum for the PUSCH PRB sum PHY resource model taking */
  ERadLteMac_UlPrbMax15   = RAD_LTEMAC(59),
  /* Defines the maximum for the PUSCH PRB sum PHY resource model taking */
  ERadLteMac_UlPrbMax20   = RAD_LTEMAC(60),
  /* Defines the maximum for the PUSCH PRB sum PHY resource model taking */
  ERadLteMac_UlPrbMax2c5  = RAD_LTEMAC(61),
  /* Defines the maximum for the PUSCH PRB sum PHY resource model taking */
  ERadLteMac_UlPrbMax2c10 = RAD_LTEMAC(62),
/* Defines the maximum for the PUSCH PRB sum PHY resource model taking */

  ERadLteMac_EnUlPrbSumLim  = RAD_LTEMAC(63),
/*  Enables / disables PUSCH PRB sum PHY resource model*/

  ERadLteMac_UlTbsLim5    = RAD_LTEMAC(64),
  /* Defines the coefficient for the PUSCH TBS sum PHY resource model */
  ERadLteMac_UlTbsLim10   = RAD_LTEMAC(65),
  /* Defines the coefficient for the PUSCH TBS sum PHY resource model */
  ERadLteMac_UlTbsLim15   = RAD_LTEMAC(66),
  /* Defines the coefficient for the PUSCH TBS sum PHY resource model */
  ERadLteMac_UlTbsLim20   = RAD_LTEMAC(67),
  /* Defines the coefficient for the PUSCH TBS sum PHY resource model */
  ERadLteMac_UlTbsLim2c5  = RAD_LTEMAC(68),
  /* Defines the coefficient for the PUSCH TBS sum PHY resource model */
  ERadLteMac_UlTbsLim2c10 = RAD_LTEMAC(69),
/* Defines the coefficient for the PUSCH TBS sum PHY resource model */

  ERadLteMac_UlTbsMax5    = RAD_LTEMAC(70),
  /*  Defines the maximum for the PUSCH TBS sum PHY resource model taking*/
  ERadLteMac_UlTbsMax10   = RAD_LTEMAC(71),
  /*  Defines the maximum for the PUSCH TBS sum PHY resource model taking*/
  ERadLteMac_UlTbsMax15   = RAD_LTEMAC(72),
  /*  Defines the maximum for the PUSCH TBS sum PHY resource model taking*/
  ERadLteMac_UlTbsMax20   = RAD_LTEMAC(73),
  /*  Defines the maximum for the PUSCH TBS sum PHY resource model taking*/
  ERadLteMac_UlTbsMax2c5  = RAD_LTEMAC(74),
  /*  Defines the maximum for the PUSCH TBS sum PHY resource model taking*/
  ERadLteMac_UlTbsMax2c10 = RAD_LTEMAC(75),
/*  Defines the maximum for the PUSCH TBS sum PHY resource model taking*/

  ERadLteMac_EnUlTbsLimOpt = RAD_LTEMAC(76),
/*  Enables / disables PUSCH TBS sum PHY resource model limitation optimization.*/

  ERadLteMac_EnUlTbsSumLim  = RAD_LTEMAC(77),
/*  Enables / disables PUSCH TBS sum PHY resource model*/

  ERadLteMac_UlBufferMargin  = RAD_LTEMAC(78),
/* Defines UL buffer margin which is multiplier for the reported buffer size totally. */

  ERadLteMac_UlPrbAllocOpt  = RAD_LTEMAC(79),
/*  Defines the uplink PRB allocation optimisation for effiecient UL bandwidth usage*/

  ERadLteMac_CqiAperTtiMax  = RAD_LTEMAC(80),
/* To limit PHY load DlScheduling shall ensure that the total number of */

  ERadLteMac_rdEnSrReqAN  = RAD_LTEMAC(81),
/* If 'enabled', SR is requested in every subframe in which UE */

  ERadLteMac_AbsMaxCrLimit  = RAD_LTEMAC(82),
/*  If 'enabled', SR is requested in every subframe in which UE*/
 
  ERadLteMac_MaxMcsDl = RAD_LTEMAC(83),
/* Maximum MCS to be used in DL */

  ERadLteMac_rdUlMacRetransmissionPolicy = RAD_LTEMAC(84),
/*  Mac retransmission policy in UL, 0: use chase combining,*/

  ERadLteMac_rdCqiAperEnable = RAD_LTEMAC(85),
/* Enabling of aperiodic CQI report: */

  ERadLteMac_TaOffScheMarg = RAD_LTEMAC(86),
/*  Determines time alignment offset limit for the uplink */

  ERadLteMac_TaCchWtMin = RAD_LTEMAC(87),
/* Minimum required value of the reliability wight factor */

  ERadLteMac_FixWeightPusch = RAD_LTEMAC(88),
/* Fixed weighting for PUSCH based TA error estimates for */

  ERadLteMac_FixWeightCch = RAD_LTEMAC(89),
/* Fixed weighting for PUCCH based TA error estimates for */

  ERadLteMac_AvePeriodCch = RAD_LTEMAC(90),
/*  Time period over which time offset estimates from the PUCCH receiver*/
 
  ERadLteMac_MinCountCch = RAD_LTEMAC(91),
/*  The minimum number of valid time offset estimates from the PUCCH receiver,*/

  ERadLteMac_BlindCount = RAD_LTEMAC(92),
/* Allowed maximum number of Time Alignment Timer periods to maintain the UE uplink */

  ERadLteMac_TaCmdMaxRetry = RAD_LTEMAC(93),
/*  The number of times the Timing Advance Command will be retried before LTE MAC*/

  ERadLteMac_TaPucchEnable = RAD_LTEMAC(94),
/* Selector to enable/disable timing error measurements on PUCCH receptions */

  ERadLteMac_PrioDummyBsrUl = RAD_LTEMAC(95),
/*  Scheduling priority for dummy BSRs in UL*/

  ERadLteMac_MinMcsDl = RAD_LTEMAC(96),
/* Maximum MCS to be used in DL */

  ERadLteMac_DlPsCycleProfileEnable = RAD_LTEMAC(97),
/* Enables DL PS runtime cycle profiling */

  ERadLteMac_PrioNumPrbsUl = RAD_LTEMAC(98),
/* Factor for adding number of PRBs to UL scheduling priority of retransmissions  */

  ERadLteMac_TargetTimeOffset = RAD_LTEMAC(99),
 /*  Time offset added to TA Commands to move the uplink transmission  */

  ERadLteMac_DisableAdjustUeAggregates = RAD_LTEMAC(100),
/*  Enable or disable the function AdjustUeAggregates*/

  ERadLteMac_FixedMaxInitialAggregationLevel = RAD_LTEMAC(101),
/* Set the Max Initial Aggregation to a fixed value */

  ERadLteMac_HardcodeUeCategory = RAD_LTEMAC(102),
/* Hardcode ueCategory value Range 1 to 5, default 0(Disable hardcoding)*/

  ERadLteMac_TaEnable = RAD_LTEMAC(103),
/*  Enable Time Alignment 0=disabled, 1=enabled*/

  ERadLteMac_perfMonIntEnabled = RAD_LTEMAC(104),
/*   Bit index for enabling performance interval monitoring   0 Default, all monitorings disabled  0xFFFFFFFF All monitorings enabled */

  ERadLteMac_DiscardSearchLimit = RAD_LTEMAC(105),
/* blank */

  ERadLteMac_UlClPcPrintingEnable = RAD_LTEMAC(106),
/*Enable Uplink close loop power control printing 0=disabled, 1=enabled */
  
  ERadLteMac_UlClPcPucchPrintingEnable = RAD_LTEMAC(107),
/*Enable Uplink close loop power control printing for PUCCH 0=disabled, 1=enabled */
  
  ERadLteMac_UlClPcPuschPrintingEnable = RAD_LTEMAC(108),
/*Enable Uplink close loop power control printing for PUSCH 0=disabled, 1=enabled */
  
  ERadLteMac_UlAtbPhrShift = RAD_LTEMAC(109),
/* Offset to power headroom report */
  
  ERadLteMac_UlPrbMin = RAD_LTEMAC(110),
/* UL minimum PRB limit */
  
  ERadLteMac_TtiTraceSi = RAD_LTEMAC(111),
/*if not 0: trace MIB and SSI even if no UE is scheduled in tti trace  */

  ERadLteMac_DisableLomCounterUpdate = RAD_LTEMAC(112),
/* if not 0: LOM counters are not updated */
  
  ERadLteMac_TtiObjectListUl = RAD_LTEMAC(113),
/*  value:     1 to 3  , step size 1  11 to 12 , step size 1 */

  ERadLteMac_MimoOllaUsedCl = RAD_LTEMAC(114),
/*  Enables OLLA compensation DELTA_CQI applied to Measurement Filter, value:  true (1) or false (0) */
  
  ERadLteMac_UlClPcPrintIOEnable = RAD_LTEMAC(115),
/*Enable Uplink close loop power control printing for I/O data  0=disabled, 1=enabled */
  
};

/*@}*/

#endif /* _MAC_RAD_DEFINITIONS_H */
