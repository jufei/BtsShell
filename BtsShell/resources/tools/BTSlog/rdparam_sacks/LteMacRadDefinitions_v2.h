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


enum ERadLteMac
{

  ERadLteMac_MaxUlTbSize     = RAD_LTEMAC(0),


  ERadLteMac_MaxDlPrbs       = RAD_LTEMAC(1),


  ERadLteMac_DlMimoIndicator = RAD_LTEMAC(2),


  ERadLteMac_EnableSr        = RAD_LTEMAC(3),


  ERadLteMac_DlTfi1          = RAD_LTEMAC(4),


  ERadLteMac_DlTfi2          = RAD_LTEMAC(5),


  ERadLteMac_TxPower         = RAD_LTEMAC(6),


  ERadLteMac_ForcedNumPrbs   = RAD_LTEMAC(7),


  ERadLteMac_MibTbSize   = RAD_LTEMAC(8),


  ERadLteMac_MaxDlTbSizeWithoutMimo = RAD_LTEMAC(9),


  ERadLteMac_MaxDlTbSizeWithMimo = RAD_LTEMAC(10),


  ERadLteMac_DeltaCqiIni = RAD_LTEMAC(11),


  ERadLteMac_DeltaCqiMin = RAD_LTEMAC(12),


  ERadLteMac_DeltaCqiMax = RAD_LTEMAC(13),


  ERadLteMac_DeltaCqiStepUp = RAD_LTEMAC(14),


  ERadLteMac_MimoOllaUsedOl = RAD_LTEMAC(15),


  ERadLteMac_MimoCqiAgeing = RAD_LTEMAC(16),


  ERadLteMac_MimoRiAgeing = RAD_LTEMAC(17),


  ERadLteMac_TtiObjectList = RAD_LTEMAC(18),


  ERadLteMac_MaxNumUeTdDl = RAD_LTEMAC(19),


  ERadLteMac_AveragingPeriod = RAD_LTEMAC(20),


  ERadLteMac_MinN = RAD_LTEMAC(21),


  ERadLteMac_McDampingFactor = RAD_LTEMAC(22),


  ERadLteMac_McFactor = RAD_LTEMAC(23),


  ERadLteMac_TaTimeMargin = RAD_LTEMAC(24),


  ERadLteMac_ForcedDlHarqAcks = RAD_LTEMAC(25),


  ERadLteMac_DlDataMaxNumOfNackSns = RAD_LTEMAC(26),


  ERadLteMac_rdDedicRaPreExpTimer = RAD_LTEMAC(27),


  ERadLteMac_MaxNumUeTdDl5 = RAD_LTEMAC(28),


  ERadLteMac_MaxNumUeTdDl10 = RAD_LTEMAC(29),


  ERadLteMac_MaxNumUeTdDl15 = RAD_LTEMAC(30),


  ERadLteMac_MaxNumUeTdDl20 = RAD_LTEMAC(31),


  ERadLteMac_MaxNumUeTdUl5 = RAD_LTEMAC(32),


  ERadLteMac_MaxNumUeTdUl10 = RAD_LTEMAC(33),


  ERadLteMac_MaxNumUeTdUl15 = RAD_LTEMAC(34),


  ERadLteMac_MaxNumUeTdUl20 = RAD_LTEMAC(35),


  ERadLteMac_PdcchAlpha = RAD_LTEMAC(36),


  ERadLteMac_DlTbsMax5  = RAD_LTEMAC(37),
  ERadLteMac_DlTbsMax10  = RAD_LTEMAC(38),
  ERadLteMac_DlTbsMax15  = RAD_LTEMAC(39),
  ERadLteMac_DlTbsMax20  = RAD_LTEMAC(40),


  ERadLteMac_DlTbsMax2c5  = RAD_LTEMAC(41),
  ERadLteMac_DlTbsMax2c10  = RAD_LTEMAC(42),


  ERadLteMac_DlTbsLimC5  = RAD_LTEMAC(43),
  ERadLteMac_DlTbsLimC10 = RAD_LTEMAC(44),
  ERadLteMac_DlTbsLimC15 = RAD_LTEMAC(45),
  ERadLteMac_DlTbsLimC20 = RAD_LTEMAC(46),


  ERadLteMac_DlTbsLimC2c5 = RAD_LTEMAC(47),
  ERadLteMac_DlTbsLimC2c10 = RAD_LTEMAC(48),


  ERadLteMac_EnDlTbsLimOpt = RAD_LTEMAC(49),


  ERadLteMac_EnDlTbsSumLim  = RAD_LTEMAC(50),


  ERadLteMac_UlPrbLim5    = RAD_LTEMAC(51),
  ERadLteMac_UlPrbLim10   = RAD_LTEMAC(52),
  ERadLteMac_UlPrbLim15   = RAD_LTEMAC(53),
  ERadLteMac_UlPrbLim20   = RAD_LTEMAC(54),
  ERadLteMac_UlPrbLim2c5  = RAD_LTEMAC(55),
  ERadLteMac_UlPrbLim2c10 = RAD_LTEMAC(56),


  ERadLteMac_UlPrbMax5    = RAD_LTEMAC(57),
  ERadLteMac_UlPrbMax10   = RAD_LTEMAC(58),
  ERadLteMac_UlPrbMax15   = RAD_LTEMAC(59),
  ERadLteMac_UlPrbMax20   = RAD_LTEMAC(60),
  ERadLteMac_UlPrbMax2c5  = RAD_LTEMAC(61),
  ERadLteMac_UlPrbMax2c10 = RAD_LTEMAC(62),


  ERadLteMac_EnUlPrbSumLim  = RAD_LTEMAC(63),


  ERadLteMac_UlTbsLim5    = RAD_LTEMAC(64),
  ERadLteMac_UlTbsLim10   = RAD_LTEMAC(65),
  ERadLteMac_UlTbsLim15   = RAD_LTEMAC(66),
  ERadLteMac_UlTbsLim20   = RAD_LTEMAC(67),
  ERadLteMac_UlTbsLim2c5  = RAD_LTEMAC(68),
  ERadLteMac_UlTbsLim2c10 = RAD_LTEMAC(69),


  ERadLteMac_UlTbsMax5    = RAD_LTEMAC(70),
  ERadLteMac_UlTbsMax10   = RAD_LTEMAC(71),
  ERadLteMac_UlTbsMax15   = RAD_LTEMAC(72),
  ERadLteMac_UlTbsMax20   = RAD_LTEMAC(73),
  ERadLteMac_UlTbsMax2c5  = RAD_LTEMAC(74),
  ERadLteMac_UlTbsMax2c10 = RAD_LTEMAC(75),


  ERadLteMac_EnUlTbsLimOpt = RAD_LTEMAC(76),


  ERadLteMac_EnUlTbsSumLim  = RAD_LTEMAC(77),


  ERadLteMac_UlBufferMargin  = RAD_LTEMAC(78),


  ERadLteMac_UlPrbAllocOpt  = RAD_LTEMAC(79),


  ERadLteMac_CqiAperTtiMax  = RAD_LTEMAC(80),


  ERadLteMac_rdEnSrReqAN  = RAD_LTEMAC(81),


  ERadLteMac_AbsMaxCrLimit  = RAD_LTEMAC(82),


  ERadLteMac_MaxMcsDl = RAD_LTEMAC(83),


  ERadLteMac_rdUlMacRetransmissionPolicy = RAD_LTEMAC(84),


  ERadLteMac_rdCqiAperEnable = RAD_LTEMAC(85),


  ERadLteMac_TaOffScheMarg = RAD_LTEMAC(86),


  ERadLteMac_TaCchWtMin = RAD_LTEMAC(87),


  ERadLteMac_FixWeightPusch = RAD_LTEMAC(88),


  ERadLteMac_FixWeightCch = RAD_LTEMAC(89),


  ERadLteMac_AvePeriodCch = RAD_LTEMAC(90),


  ERadLteMac_MinCountCch = RAD_LTEMAC(91),


  ERadLteMac_BlindCount = RAD_LTEMAC(92),


  ERadLteMac_TaCmdMaxRetry = RAD_LTEMAC(93),


  ERadLteMac_TaPucchEnable = RAD_LTEMAC(94),


  ERadLteMac_PrioDummyBsrUl        = RAD_LTEMAC(95),


  ERadLteMac_MinMcsDl = RAD_LTEMAC(96),


  ERadLteMac_DlPsCycleProfileEnable = RAD_LTEMAC(97),


  ERadLteMac_PrioNumPrbsUl = RAD_LTEMAC(98),


  ERadLteMac_TargetTimeOffset = RAD_LTEMAC(99),
 

  ERadLteMac_DisableAdjustUeAggregates = RAD_LTEMAC(100),


  ERadLteMac_FixedMaxInitialAggregationLevel = RAD_LTEMAC(101),


  ERadLteMac_HardcodeUeCategory = RAD_LTEMAC(102),


  ERadLteMac_TaEnable = RAD_LTEMAC(103),


  ERadLteMac_perfMonIntEnabled = RAD_LTEMAC(104),


  ERadLteMac_DiscardSearchLimit = RAD_LTEMAC(105),


  ERadLteMac_UlClPcPrintingEnable = RAD_LTEMAC(106),


  ERadLteMac_UlClPcPucchPrintingEnable = RAD_LTEMAC(107),


  ERadLteMac_UlClPcPuschPrintingEnable = RAD_LTEMAC(108),


  ERadLteMac_UlAtbPhrShift = RAD_LTEMAC(109),


  ERadLteMac_UlPrbMin = RAD_LTEMAC(110),


  ERadLteMac_TtiTraceSi = RAD_LTEMAC(111),


  ERadLteMac_DisableLomCounterUpdate = RAD_LTEMAC(112),


  ERadLteMac_TtiObjectListUl = RAD_LTEMAC(113),


  ERadLteMac_MimoOllaUsedCl = RAD_LTEMAC(114),


  ERadLteMac_UlClPcPrintIOEnable = RAD_LTEMAC(115),


  ERadLteMac_Last
};

/*@}*/

#endif /* _MAC_RAD_DEFINITIONS_H */
