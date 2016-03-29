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

/* TODO: In future these kind of offsets should not be used in case of signed integers (using is complicated).
 *      R&D switches supports also negative value by setting -1 as 0xffffffff.
 */
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

  Invalid_01 = RAD_LTEMAC(11),
  Invalid_02 = RAD_LTEMAC(12),
  Invalid_03 = RAD_LTEMAC(13),
  Invalid_04 = RAD_LTEMAC(14),

  ERadLteMac_MimoOllaUsedOl = RAD_LTEMAC(15),

  ERadLteMac_MimoCqiAgeing = RAD_LTEMAC(16),

  ERadLteMac_MimoRiAgeing = RAD_LTEMAC(17),

  ERadLteMac_TtiObjectList = RAD_LTEMAC(18),

  ERadLteMac_MaxNumUeTdDl = RAD_LTEMAC(19),

  ERadLteMac_AveragingPeriod = RAD_LTEMAC(20),

  ERadLteMac_MinN = RAD_LTEMAC(21),

  ERadLteMac_McDampingFactor = RAD_LTEMAC(22),

  ERadLteMac_McFactor = RAD_LTEMAC(23),

  ERadLteMac_PdcchOllaUsed = RAD_LTEMAC(24),

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

  ERadLteMac_TaWindow = RAD_LTEMAC(104),

  ERadLteMac_TaMinReliability = RAD_LTEMAC(105),

  ERadLteMac_TaAgingF = RAD_LTEMAC(106),

  ERadLteMac_TaBlindPeriodMax = RAD_LTEMAC(107),

  ERadLteMac_DiscardSearchLimit = RAD_LTEMAC(108),

  ERadLteMac_UlAtbPhrShift = RAD_LTEMAC(109),

  ERadLteMac_UlPrbMin = RAD_LTEMAC(110),

  ERadLteMac_TtiTraceSi = RAD_LTEMAC(111),

  ERadLteMac_perfMonIntEnabled = RAD_LTEMAC(112),

  ERadLteMac_DisableLomCounterUpdate = RAD_LTEMAC(113),


  ERadLteMac_McsReductDummy = RAD_LTEMAC(114),

  ERadLteMac_MaxMcsUl = RAD_LTEMAC(115),

  ERadLteMac_MinMcsUl = RAD_LTEMAC(116),

  ERadLteMac_CrcFailTraceRate = RAD_LTEMAC(117),

  ERadLteMac_TbPointerDeleteTimerLength = RAD_LTEMAC(118),


  ERadLteMac_PdcchCapDlSchedEnable = RAD_LTEMAC(119),

  ERadLteMac_UlTUPIfPeakRateLimit = RAD_LTEMAC(120),

 
  ERadLteMac_PdcchCapUlSchedEnable = RAD_LTEMAC(121),


  ERadLteMac_DopplerCorLag = RAD_LTEMAC(122),


  ERadLteMac_DopplerBorderFactor = RAD_LTEMAC(123),

   ERadLteMac_DopplerEstSamples = RAD_LTEMAC(124),

  ERadLteMac_BesselJ0DopplerC1 = RAD_LTEMAC(125),


  ERadLteMac_BesselJ0DopplerC2 = RAD_LTEMAC(126),


  ERadLteMac_TaTimerMargin = RAD_LTEMAC(127),


  ERadLteMac_InitSyncStateDCM = RAD_LTEMAC(128),

  ERadLteMac_DopplerEstPeriod = RAD_LTEMAC(129),


  ERadLteMac_PdcchPcBoostConstant    = RAD_LTEMAC(130),


  ERadLteMac_PdcchPcReductionConstant= RAD_LTEMAC(131),


  ERadLteMac_PdcchTraceAllPdcchUes   = RAD_LTEMAC(132),
  

  ERadLteMac_rdSrsDtxTreshold = RAD_LTEMAC(133),   

 
  ERadLteMac_rdInitSyncStateDcm = RAD_LTEMAC(134),   


  ERadLteMac_rdDopplerFreqCategoryDcm = RAD_LTEMAC(135),   


  ERadLteMac_rdOptSrioMsgInMacPhyIf = RAD_LTEMAC(136),   


  ERadLteMac_rdMaxNumUeTdDlDualCell = RAD_LTEMAC(137),   


  ERadLteMac_rdMaxNumUeTdUlDualCell = RAD_LTEMAC(138),   


  ERadLteMac_rdMaxNumUeFdDlDualCell = RAD_LTEMAC(139),   


  ERadLteMac_rdMaxNumUeFdUlDualCell = RAD_LTEMAC(140),   

 
  ERadLteMac_writeDlMacPduDumpToHB = RAD_LTEMAC(141),
  

  ERadLteMac_DlCellInterferceEn = RAD_LTEMAC(142),


  ERadLteMac_DlCellInterferceLevel = RAD_LTEMAC(143),

  ERadLteMac_DlsFdPfschFairness    = RAD_LTEMAC(144),    /* */
  ERadLteMac_DlsFdPfschMaxWeight   = RAD_LTEMAC(145),    /* */
  ERadLteMac_DlsFdActivityAvgT     = RAD_LTEMAC(146),    /* */

  #define RAD_LTE_TDD_MAC_START 147

    ERadLteMac_TtiObjectListUl = RAD_LTEMAC(RAD_LTE_TDD_MAC_START),


    ERadLteMac_UlClPcPrintingEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 1),

    ERadLteMac_UlClPcPrintIOEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 2),


    ERadLteMac_UlClPcPucchPrintingEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 3),


    ERadLteMac_UlClPcPuschPrintingEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 4),


    ERadLteMac_MimoOllaUsedCl = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 5),


    ERadLteMac_FixWeightSrs = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 6),
    

  ERadLteMac_PdcchTtiTraceEnable=RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 7),
  
 

  ERadLteMac_UlGbrEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 8),

 
  ERadLteMac_NonGBRULPRINTSWITCH  = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 9),

  ERadLteMac_SCHEDORDEREXHFD  = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 10),  



   ERadLteMac_UlsTdDelayMetricEnable   = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 11),
  
   ERadLteMac_UlsTdGbrStaticSchedulWeight = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 12),

   ERadLteMac_UlsHolEstSrFactor = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 13),
  
 
   ERadLteMac_UlsSrIntervalForSidDetection = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 14),
  

   ERadLteMac_VoicePacketIAT = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 15),


  ERadLteMac_DlsTdDelayMetricEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 16),
  ERadLteMac_DlsTdGbrStaticSchedulWeight = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 17),
  ERadLteMac_EnableGbrBufferLevelEvalDl = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 18),


  

  ERadLteMac_rdLatMeas1       = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 19),

  ERadLteMac_rdLatMeas2       = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 20),

  ERadLteMac_rdLatMeas3       = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 21),



  ERadLteMac_TRdUlsPrbGapChangeEn = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 22),

  ERadLteMac_DlLaMaxHysteresisFactor = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 24),
  ERadLteMac_RdDlCodeRateBoost = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 25), 
  ERadLteMac_RdDlLaMaxHysteresisFactor = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 30),
  ECqiAperOptimisticFullFeedbackMode = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 31),
  

  ERadLteMac_puschHoppingEnable  = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 32),
  ERadLteMac_puschHopOffset      = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 33),
  ERadLteMac_hopModePusch        = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 34),
  ERadLteMac_hopSubBwPusch       = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 35),
  ERadLteMac_hopTypePusch        = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 36),
  ERadLteMac_hopPatternExplictInfBased = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 37),

  

  ERadLteMac_UlReTxPercentage    = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 38),
  ERadLteMac_DisableLomRDCounterUpdate = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 39),   
  ERadLteMac_rdPdcchMaxCr              = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 40), 


  ERadLteMac_rdOptPhichCalcMethodTwo  = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 41),    
  ERadLteMac_rdOptPhichLogSwither  = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 42),    

  ERadLteMac_DlType1Enable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 43),
  ERadLteMac_LVRBEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 44),


  ERadLteMac_DlPsAlgType = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 45),

  
  ERadLteMac_ULTdSchAlg = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 46), 
  ERadLteMac_UlMsg3PwCtrl = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 47), 
  ERadLteMac_rdDciStatics = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 48), 
  ERadLteMac_Last
};



#endif /* _MAC_RAD_DEFINITIONS_H */
