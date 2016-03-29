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
  /*
   Maximum uplink TB size in bits.
  */
  ERadLteMac_MaxUlTbSize     = RAD_LTEMAC(0),

  /*
   Maximum number of PRBs that can be allocated for the UE in DL in
   one TTI. Value: 1-50, if >25 only even numbers possible.
  */
  ERadLteMac_MaxDlPrbs       = RAD_LTEMAC(1),

  /*
   Indicates whether MIMO is used (1) or not (0).
  */
  ERadLteMac_DlMimoIndicator = RAD_LTEMAC(2),

  /*
   Enabling/disabling the use of scheduling request. When SR is disabled,
   UEs will always be scheduled with PUSCH without considering if it needs to be scheduled.
  */
  ERadLteMac_EnableSr        = RAD_LTEMAC(3),

  /*
   Indicates the transport format for a downlink TB, value: 0 to 23.
   In MIMO case indicates the TFI for the first TB (codeWordNumber=0).
  */
  ERadLteMac_DlTfi1          = RAD_LTEMAC(4),

  /*
   In case of MIMO indicates the transport format for the second
   downlink TB (codeWordNumber=1). Value: 0 to 23.
  */
  ERadLteMac_DlTfi2          = RAD_LTEMAC(5),

  /*
   Transmission power per subcarrier in W, value: 0 to 1000000
  */
  ERadLteMac_TxPower         = RAD_LTEMAC(6),

  /*
   Forced number of PRBs allocated for the transport block. If set 0,
   normal algorithm will be used for determining this.
  */
  ERadLteMac_ForcedNumPrbs   = RAD_LTEMAC(7),

  /*
   MIB transport block size [bits].
  */
  ERadLteMac_MibTbSize   = RAD_LTEMAC(8),

  /*
   Default value for DL maximum TB size without mimmo
  */
  ERadLteMac_MaxDlTbSizeWithoutMimo = RAD_LTEMAC(9),

  /*
   Default value for DL maximum TB size without mimmo
  */
  ERadLteMac_MaxDlTbSizeWithMimo = RAD_LTEMAC(10),

  /*
    These R&D parameter IDs are invalid. These shall be kept unused for the next two months,
    so it could be reused from 1/March/2010.
  */
  Invalid_01 = RAD_LTEMAC(11),
  Invalid_02 = RAD_LTEMAC(12),
  Invalid_03 = RAD_LTEMAC(13),
  Invalid_04 = RAD_LTEMAC(14),

  /*
   Enables OLLA compensation DELTA_CQI applied to Measurement Filter,
   value:  true (1) or false (0)
  */
  ERadLteMac_MimoOllaUsedOl = RAD_LTEMAC(15),

  /*
   Ageing constant for CQI filter during times on inactivity,
   value:       80 to 100  , step size 1
   when used:  0.8 to 1    , step size 0.01
  */
  ERadLteMac_MimoCqiAgeing = RAD_LTEMAC(16),

  /*
   Ageing constant for Rank filter during times on inactivity,
   value:       80 to 100  , step size 1
   when used:  0.8 to 1    , step size 0.01
  */
  ERadLteMac_MimoRiAgeing = RAD_LTEMAC(17),

  /*
   parameter selects for different test purposes used measurement object list for TTI Trace of
   UL/DL Scheduler Browser Measurements.
   value:     0 to 3  , step size 1
             11 to 12 , step size 1
  */
  ERadLteMac_TtiObjectList = RAD_LTEMAC(18),

  /*
   CS1 list length. Number of Ues which can be scheduled in one TTI Time domain.
  */
  ERadLteMac_MaxNumUeTdDl = RAD_LTEMAC(19),

  /*
   Time period over which the noise power estimates for early, on-time and late
   shall be averaged prior to applying the mass centre method [ms].
   Min:50, Max:500, Step:1ms.
  */
  ERadLteMac_AveragingPeriod = RAD_LTEMAC(20),

  /*
   Minimum required value for N, the number of valid noise power estimates received
   for the PnEstCumulMean averages, to proceed into DelayMassCentre calculation.
   Min:1, Max:*, Step:1.
  */
  ERadLteMac_MinN = RAD_LTEMAC(21),

  /*
   Defines a damping factor for the mass centre method to improve the variance
   of calculated timing correction values. The used value here must be value*10^3.
   Min:0, Max:1000, Step:1.
  */
  ERadLteMac_McDampingFactor = RAD_LTEMAC(22),

  /*
   Defines the gradient of timing correction versus estimated noise power
   difference using the mass centre method. The used value here is value*10.
   Min:10, Max:320, Step:1.
  */
  ERadLteMac_McFactor = RAD_LTEMAC(23),

  /*
    When enabled (=GLO_TRUE), outer loop link adaptation has an influence on PDCCH LA
  */
  ERadLteMac_PdcchOllaUsed = RAD_LTEMAC(24),

  /*
   When enabled (=GLO_TRUE), Uplink Scheduler sends PucchReceiveRespD msg or
   PuschReceiveRespD msg with HARQ ACKs to Downlink Data Transfer.
  */
  ERadLteMac_ForcedDlHarqAcks = RAD_LTEMAC(25),

  /*
   Maximum number of NACKs which can be stored to the NACK list without removing any.
  */
  ERadLteMac_DlDataMaxNumOfNackSns = RAD_LTEMAC(26),

  /*
   Timer value in microsecs) for rdDedicRaPreExpTimer Duration
  */
  ERadLteMac_rdDedicRaPreExpTimer = RAD_LTEMAC(27),

  /*
   When enabled (=GLO_TRUE), Ul support saves bearer setup req and starts hold timer (2s).
  */
  /*ERadLteMac_rdDelayedConf = RAD_LTEMAC(28),*/

  /*
   Number of Ues which can be scheduled in Dl in one TTI Time domain. 5 Mhz.
  */
  ERadLteMac_MaxNumUeTdDl5 = RAD_LTEMAC(28),

  /*
   Number of Ues which can be scheduled in Dl in one TTI Time domain. 10 Mhz.
  */
  ERadLteMac_MaxNumUeTdDl10 = RAD_LTEMAC(29),

  /*
   Number of Ues which can be scheduled in Dl in one TTI Time domain. 15 Mhz.
  */
  ERadLteMac_MaxNumUeTdDl15 = RAD_LTEMAC(30),

  /*
   Number of Ues which can be scheduled in Dl in one TTI Time domain. 20 Mhz.
  */
  ERadLteMac_MaxNumUeTdDl20 = RAD_LTEMAC(31),

  /*
   Number of Ues which can be scheduled in Ul in one TTI Time domain. 5 Mhz.
  */
  ERadLteMac_MaxNumUeTdUl5 = RAD_LTEMAC(32),

  /*
   Number of Ues which can be scheduled in Ul in one TTI Time domain. 10 Mhz.
  */
  ERadLteMac_MaxNumUeTdUl10 = RAD_LTEMAC(33),

  /*
   Number of Ues which can be scheduled in Ul in one TTI Time domain. 15 Mhz.
  */
  ERadLteMac_MaxNumUeTdUl15 = RAD_LTEMAC(34),

  /*
   Number of Ues which can be scheduled in Ul in one TTI Time domain. 20 Mhz.
  */
  ERadLteMac_MaxNumUeTdUl20 = RAD_LTEMAC(35),

  /*
   Margin for selecting highest possible aggregation for each scheduled PDCCH
   from total PDCCH capacity to take into account that all capacity cannot be used
   because of UE specific search spaces.
  */
  ERadLteMac_PdcchAlpha = RAD_LTEMAC(36),

  /*
   Defines the maximum for the PDSCH TBS sum PHY resource model  for taking into
   account when deciding the total TBS sum in TTI basis.
  */
  ERadLteMac_DlTbsMax5  = RAD_LTEMAC(37),
  ERadLteMac_DlTbsMax10  = RAD_LTEMAC(38),
  ERadLteMac_DlTbsMax15  = RAD_LTEMAC(39),
  ERadLteMac_DlTbsMax20  = RAD_LTEMAC(40),

  /*
   Defines the maximum for the PDSCH TBS sum PHY resource model  for taking
   into account when deciding the total TBS sum in TTI basis. Applicable to
   dual 5/10 MHz cells in one FSP.
  */
  ERadLteMac_DlTbsMax2c5  = RAD_LTEMAC(41),
  ERadLteMac_DlTbsMax2c10  = RAD_LTEMAC(42),

  /*
   Defines the coefficient for the PDSCH TBS sum PHY resource model for
   taking into account the scheduled amount of users when deciding the total
   TBS sum in TTI basis. Applicable to 5 MHz cell.
  */
  ERadLteMac_DlTbsLimC5  = RAD_LTEMAC(43),
  ERadLteMac_DlTbsLimC10 = RAD_LTEMAC(44),
  ERadLteMac_DlTbsLimC15 = RAD_LTEMAC(45),
  ERadLteMac_DlTbsLimC20 = RAD_LTEMAC(46),

  /*
   Defines the maximum for the PDSCH TBS sum PHY resource model  for taking
   into account when deciding the total TBS sum in TTI basis. Applicable to
   dual 5/10 MHz cells in one FSP.
  */
  ERadLteMac_DlTbsLimC2c5 = RAD_LTEMAC(47),
  ERadLteMac_DlTbsLimC2c10 = RAD_LTEMAC(48),

  /*
   Enables / disables PDSCH TBS sum PHY resource model limitation optimization.
   Basically higher TBS limit for PDSCH TBS sum is got, if lower amount of Ues
   are scheduled. In over limit situation, high amount of Ues with low MCS can
   be scheduled (parameter disabled) or low amount of Ues with high MCS can be
   scheduled (parameter enabled).
  */
  ERadLteMac_EnDlTbsLimOpt = RAD_LTEMAC(49),

  /*
   Enables / disables PDSCH TBS sum PHY resource model
  */
  ERadLteMac_EnDlTbsSumLim  = RAD_LTEMAC(50),

  /*
   Defines the coefficient for the PUSCH PRB sum PHY resource model
   for taking into account the scheduled amount of users when
   deciding the total PRB sum in TTI basis
  */
  ERadLteMac_UlPrbLim5    = RAD_LTEMAC(51),
  ERadLteMac_UlPrbLim10   = RAD_LTEMAC(52),
  ERadLteMac_UlPrbLim15   = RAD_LTEMAC(53),
  ERadLteMac_UlPrbLim20   = RAD_LTEMAC(54),
  ERadLteMac_UlPrbLim2c5  = RAD_LTEMAC(55),
  ERadLteMac_UlPrbLim2c10 = RAD_LTEMAC(56),

  /*
   Defines the maximum for the PUSCH PRB sum PHY resource model taking
   into account when deciding the total PRB sum in TTI basis
  */
  ERadLteMac_UlPrbMax5    = RAD_LTEMAC(57),
  ERadLteMac_UlPrbMax10   = RAD_LTEMAC(58),
  ERadLteMac_UlPrbMax15   = RAD_LTEMAC(59),
  ERadLteMac_UlPrbMax20   = RAD_LTEMAC(60),
  ERadLteMac_UlPrbMax2c5  = RAD_LTEMAC(61),
  ERadLteMac_UlPrbMax2c10 = RAD_LTEMAC(62),

  /*
   Enables / disables PUSCH PRB sum PHY resource model
  */
  ERadLteMac_EnUlPrbSumLim  = RAD_LTEMAC(63),

  /*
   Defines the coefficient for the PUSCH TBS sum PHY resource model
   for taking into account the scheduled amount of users when
   deciding the total PRB sum in TTI basis
  */
  ERadLteMac_UlTbsLim5    = RAD_LTEMAC(64),
  ERadLteMac_UlTbsLim10   = RAD_LTEMAC(65),
  ERadLteMac_UlTbsLim15   = RAD_LTEMAC(66),
  ERadLteMac_UlTbsLim20   = RAD_LTEMAC(67),
  ERadLteMac_UlTbsLim2c5  = RAD_LTEMAC(68),
  ERadLteMac_UlTbsLim2c10 = RAD_LTEMAC(69),

  /*
   Defines the maximum for the PUSCH TBS sum PHY resource model taking
   into account when deciding the total PRB sum in TTI basis
  */
  ERadLteMac_UlTbsMax5    = RAD_LTEMAC(70),
  ERadLteMac_UlTbsMax10   = RAD_LTEMAC(71),
  ERadLteMac_UlTbsMax15   = RAD_LTEMAC(72),
  ERadLteMac_UlTbsMax20   = RAD_LTEMAC(73),
  ERadLteMac_UlTbsMax2c5  = RAD_LTEMAC(74),
  ERadLteMac_UlTbsMax2c10 = RAD_LTEMAC(75),

  /*
   Enables / disables PUSCH TBS sum PHY resource model limitation optimization.
   Basically higher TBS limit for PDSCH TBS sum is got, if lower amount of UEs
   are scheduled. In over limit situation, high amount of UEs with low MCS can
   be scheduled
  */
  ERadLteMac_EnUlTbsLimOpt = RAD_LTEMAC(76),

  /*
   Enables / disables PUSCH TBS sum PHY resource model
  */
  ERadLteMac_EnUlTbsSumLim  = RAD_LTEMAC(77),

  /*
   Defines UL buffer margin which is multiplier for the reported buffer size totally.
   The parameter is meant for example covering the bytes which will be lost
   for header information
  */
  ERadLteMac_UlBufferMargin  = RAD_LTEMAC(78),

  /*
   Defines the uplink PRB allocation optimisation for effiecient UL bandwidth usage
   (1 is the most efficient) or for the low scheduling latency of users
  */
  ERadLteMac_UlPrbAllocOpt  = RAD_LTEMAC(79),

  /*
   To limit PHY load DlScheduling shall ensure that the total number of
   aperiodic CQI requests per TTI is less or equal to this parameter;
   0 means no limit
  */
  ERadLteMac_CqiAperTtiMax  = RAD_LTEMAC(80),

  /*
   If 'enabled', SR is requested in every subframe in which UE
   is sending Ack/Nack and in which UE has no PUSCH allocation
  */
  ERadLteMac_rdEnSrReqAN  = RAD_LTEMAC(81),

  /*
   If 'enabled', SR is requested in every subframe in which UE
   is sending Ack/Nack and in which UE has no PUSCH allocation
  */
  ERadLteMac_AbsMaxCrLimit  = RAD_LTEMAC(82),

  /*
   Maximum MCS to be used in DL
   Range: 0...28, default 28
  */
  ERadLteMac_MaxMcsDl = RAD_LTEMAC(83),

  /*
   Mac retransmission policy in UL, 0: use chase combining,
   1: use redundancy version variations.
  */
  ERadLteMac_rdUlMacRetransmissionPolicy = RAD_LTEMAC(84),

  /*
   Enabling of aperiodic CQI report:
   0: aperiodic CQI report disabled, 1: aperiodic CQI report enabled.
  */
  ERadLteMac_rdCqiAperEnable = RAD_LTEMAC(85),

  /*
   Determines time alignment offset limit for the uplink
   sceduler to stop considering the UE for scheduling.
   Multiplicative factor to taMaxOffset.
   Range: 1...5, default 2
  */
  ERadLteMac_TaOffScheMarg = RAD_LTEMAC(86),

  /*
   Minimum required value of the reliability wight factor
   taPucchMeasWeight for inclusion of the corresponding time
   offset value taPucchMeasurement into the averaging calculation.
   Range: 0...1, default 0
  */
  ERadLteMac_TaCchWtMin = RAD_LTEMAC(87),

  /*
   Fixed weighting for PUSCH based TA error estimates for
   calculation of the combined PUSCH/PUCCH DelayError.
   Range: 0...1, default 1
  */
  ERadLteMac_FixWeightPusch = RAD_LTEMAC(88),

  /*
   Fixed weighting for PUCCH based TA error estimates for
   calculation of the combined PUSCH/PUCCH DelayError.
   Range: 0...1, default 1
  */
  ERadLteMac_FixWeightCch = RAD_LTEMAC(89),

  /*
   Time period over which time offset estimates from the PUCCH receiver
   will be nominally averaged prior to being used to generate a TA command.
   Note: The number of valid time offset estimates in the moving window
   for delay estimate calculation, after the initial fill of the buffer
   after previous UE timer update, will be FLOOR(rdAvePeriodCch/rrmCqiPerNp)+1.
   Thus the required nominal number of time offset estimates for the delay
   estimate calculation sets the upper bound for CQI reporting period
   rrmCqiPerNp on the UE PUCCH.
   Range: 50...490, default 390
  */
  ERadLteMac_AvePeriodCch = RAD_LTEMAC(90),

  /*
   The minimum number of valid time offset estimates from the PUCCH receiver,
   which is required in order to generate a Timing Advance Command.
   Note: This parameter does not set the typical or nominal number of
   time offset estimates included into TA error calculation, but the
   acceptable minimum. The value should be set  low enough to allow
   UE timing Advance update (1) more than rdTaTimerMargin before expiration
   of the TA Control Timer under the worst (design) case failure rate of the
   PUCCH time offset measurements, and (2) timely on crossings of the taMaxOffset
   limit for the fastest moving UEs. The value is upper bounded
   to FLOOR(rdAvePeriodCch/rrmCqiPerNp).
   Range: 10...100, default 25
  */
  ERadLteMac_MinCountCch = RAD_LTEMAC(91),

  /*
   Allowed maximum number of Time Alignment Timer periods to maintain the UE uplink
   synchronization based on the latest valid estimate of the required correction
   to the UE timing advance (DelayEstimate). Values greater than one allow a
   respective number (value - 1) of TA Command transmissions with forced zero TA
   correction to only restart the Time Alignment Timer.
   Range: 1...12,   default 1
  */
  ERadLteMac_BlindCount = RAD_LTEMAC(92),

  /*
   The number of times the Timing Advance Command will be retried before LTE MAC
   assumes the UE has gone Out-of-Synch.
   Range: 1...10,   default 1
  */
  ERadLteMac_TaCmdMaxRetry = RAD_LTEMAC(93),

  /*
   Selector to enable/disable timing error measurements on PUCCH receptions
   Range: 0...1,   default 1
  */
  ERadLteMac_TaPucchEnable = RAD_LTEMAC(94),

  /*
   Scheduling priority for dummy BSRs in UL
   range: 0..100, default 5
  */
  ERadLteMac_PrioDummyBsrUl        = RAD_LTEMAC(95),

  /*
   Maximum MCS to be used in DL
   Range: 0...28, default 0
  */
  ERadLteMac_MinMcsDl = RAD_LTEMAC(96),

  /*
   Enables DL PS runtime cycle profiling
   Range: 0 (off),1 (on)
  */
  ERadLteMac_DlPsCycleProfileEnable = RAD_LTEMAC(97),

  /*
   Factor for adding number of PRBs to UL scheduling priority of retransmissions
   Range 0.01 to 10, default 1.0, step size 0.01
  */
  ERadLteMac_PrioNumPrbsUl = RAD_LTEMAC(98),

  /*
   Time offset added to TA Commands to move the uplink transmission
   towards cyclic prefix from the reference timing of Rx.
   Range 0 to 2.5, default 1.0, step size 0.01
  */
  ERadLteMac_TargetTimeOffset = RAD_LTEMAC(99),

  /*
   Enable or disable the function AdjustUeAggregates
   Range 0 to 1, default is 0 (do not disable)
  */
  ERadLteMac_DisableAdjustUeAggregates = RAD_LTEMAC(100),

  /*
   Set the Max Initial Aggregation to a fixed value
   Range 0 to 8, default is 0 (take the one from the alpha calculated)
   1,2,4,8 are the other values
  */
  ERadLteMac_FixedMaxInitialAggregationLevel = RAD_LTEMAC(101),

  /**
   * Hardcode ueCategory value
   * Range 1 to 5, default 0(Disable hardcoding).
   */
  ERadLteMac_HardcodeUeCategory = RAD_LTEMAC(102),

  /**
   * Enable Time Alignment
   * 0=disabled, 1=enabled
   */
  ERadLteMac_TaEnable = RAD_LTEMAC(103),

  /*
  The number of consecutive averaging periods from which the measurements
  are included when calculating the weighted sum for the complex Phi
  estimate. (Window size in sliding window mechanism)
  */
  ERadLteMac_TaWindow = RAD_LTEMAC(104),

  /*
  Minimum required value of the reliability (magnitude of SumPhiTotal)
  of the measurements to calculate a valid Time Offset Estimate and
  Time Alignment Command
  */
  ERadLteMac_TaMinReliability = RAD_LTEMAC(105),

  /*
  The aging factor to be applied to measurements of the previous
  averaging periods
  */
  ERadLteMac_TaAgingF = RAD_LTEMAC(106),

  /*
  Allowed maximum time period without reliable timing offset
  estimate to maintain the UE uplink synchronization based on the
  latest valid estimate of the required correction to the UE timing
  advance.
  */
  ERadLteMac_TaBlindPeriodMax = RAD_LTEMAC(107),

  /**
   * Limit search depth for discarded SDU
   */
  ERadLteMac_DiscardSearchLimit = RAD_LTEMAC(108),

  /**
   * Offset to power headroom report
   */
  ERadLteMac_UlAtbPhrShift = RAD_LTEMAC(109),

  /**
   * UL minimum PRB limit
   */
  ERadLteMac_UlPrbMin = RAD_LTEMAC(110),
  /**
   * if not 0: trace MIB and SSI even if no UE is scheduled in tti trace
   */

  ERadLteMac_TtiTraceSi = RAD_LTEMAC(111),

  /*
   Bit index for enabling performance interval monitoring
   0          Default, all monitorings disabled
   0xFFFFFFFF All monitorings enabled
  */
  ERadLteMac_perfMonIntEnabled = RAD_LTEMAC(112),

  /**
   * if not 0: LOM counters are not updated
   */
  ERadLteMac_DisableLomCounterUpdate = RAD_LTEMAC(113),

  /**
   * MCS reduction for CS3 candidates
   */
  ERadLteMac_McsReductDummy = RAD_LTEMAC(114),

  /*
   Maximum MCS to be used in DL
   Range: 0...28, default 28
  */
  ERadLteMac_MaxMcsUl = RAD_LTEMAC(115),

  /*
   Maximum MCS to be used in DL
   Range: 0...28, default 0
  */
  ERadLteMac_MinMcsUl = RAD_LTEMAC(116),

  /**
   * CRC failure is output into trace 1 / # of failed TB's.
   *  0 = never.
   */
  ERadLteMac_CrcFailTraceRate = RAD_LTEMAC(117),

  /**
   * UL Data: length for TB pointer delete timer [ms]
   */
  ERadLteMac_TbPointerDeleteTimerLength = RAD_LTEMAC(118),

  /**
   * DL PS: rdPdcchCapDlSched
   */
  ERadLteMac_PdcchCapDlSchedEnable = RAD_LTEMAC(119),

  /**
   * UL Data: Peak rate limit on sending RLC SDUs to TUP [Mbps] 0=No limit
   */
  ERadLteMac_UlTUPIfPeakRateLimit = RAD_LTEMAC(120),

  /**
   * UL PS: rdPdcchCapUlSched
   */
  ERadLteMac_PdcchCapUlSchedEnable = RAD_LTEMAC(121),

  /**
   * Delay for concecutive channel estimations
   * used by Doppler category estimation algorithm
   */
  ERadLteMac_DopplerCorLag = RAD_LTEMAC(122),

  /**
   * A finetuning value for doppler category evaluation
   */
  ERadLteMac_DopplerBorderFactor = RAD_LTEMAC(123),

  /**
   * Number of doppler estimation covariance samples
   */
  ERadLteMac_DopplerEstSamples = RAD_LTEMAC(124),

  /**
   * Bessel J0 value calculated by using doppler
   * low frequency and ERadLteMac_DopplerEstLag.
   * The result is used for Doppler category evaluation.
   */
  ERadLteMac_BesselJ0DopplerC1 = RAD_LTEMAC(125),

  /**
   * Bessel J0 value calculated by using doppler
   * high frequency and ERadLteMac_DopplerEstLag.
   * The result is used for Doppler category evaluation.
   */
  ERadLteMac_BesselJ0DopplerC2 = RAD_LTEMAC(126),

  /**
   * Margin before timer expiry when TAC is sent to UE in ms, DCM only.
   */
  ERadLteMac_TaTimerMargin = RAD_LTEMAC(127),

  /**
   * Allows CQI disabling for test purposes, DCM only.
   */
  ERadLteMac_InitSyncStateDCM = RAD_LTEMAC(128),

  ERadLteMac_DopplerEstPeriod = RAD_LTEMAC(129),

  /* 1.96 the constant for PC boost */
  ERadLteMac_PdcchPcBoostConstant    = RAD_LTEMAC(130),

  /* 1.96 the constant for PC reduction */
  ERadLteMac_PdcchPcReductionConstant= RAD_LTEMAC(131),

  /**
  * enable tracing of unscheduled UEs with PDCCH allocation
  */
  ERadLteMac_PdcchTraceAllPdcchUes   = RAD_LTEMAC(132),
  
  /**
  * Defines the false DTX state detection rate
  */
  ERadLteMac_rdSrsDtxTreshold = RAD_LTEMAC(133),   

  /**
  * Controls to which sync state UE is put when msg3 is received
  */  
  ERadLteMac_rdInitSyncStateDcm = RAD_LTEMAC(134),   

  /**
  * Controls whether the input from the doppler frequency algorithm is used 
  * or if category is fixed to either high or low
  */  
  ERadLteMac_rdDopplerFreqCategoryDcm = RAD_LTEMAC(135),   

  /**
  * Controls whether the optimized implementation of PHY interface for 
  * certain messages is used or not
  */  
  ERadLteMac_rdOptSrioMsgInMacPhyIf = RAD_LTEMAC(136),   

  /**
  * Maximum amount of users that can be taken into DL time domain 
  * scheduling per cell from capacity restrictions point of view in 
  * case of 2 cells in the same FSP
  */  
  ERadLteMac_rdMaxNumUeTdDlDualCell = RAD_LTEMAC(137),   

  /**
  * Maximum amount of users that can be taken into UL time domain 
  * scheduling per cell from capacity restrictions point of view in 
  * case of 2 cells in the same FSP
  */  
  ERadLteMac_rdMaxNumUeTdUlDualCell = RAD_LTEMAC(138),   

  /**
  * Maximum amount of users that can be taken into DL frequency domain 
  * scheduling per cell from capacity restrictions point of view in case 
  * of 2 cells in the same FSP
  */  
  ERadLteMac_rdMaxNumUeFdDlDualCell = RAD_LTEMAC(139),   

  /**
  * Maximum amount of users that can be taken into DL frequency domain 
  * scheduling per cell from capacity restrictions point of view in case 
  * of 2 cells in the same FSP
  */  
  ERadLteMac_rdMaxNumUeFdUlDualCell = RAD_LTEMAC(140),   

  /**
  * Dl MAC PDU dump writing to History Buffer enabled
  */
  ERadLteMac_writeDlMacPduDumpToHB = RAD_LTEMAC(141),
  
    // mwfu for DlInterference begin
  /**
   * Enable Downlink cell interferce
   * 0=disabled, 1=enabled
   */
  ERadLteMac_DlCellInterferceEn = RAD_LTEMAC(142),

  /**
   * Downlink cell interferce level
   * 0=70% prbs used for interference,
   * 1=100% prbs used for interference
   */
  ERadLteMac_DlCellInterferceLevel = RAD_LTEMAC(143),

  ERadLteMac_DlsFdPfschFairness    = RAD_LTEMAC(144),    /* */
  ERadLteMac_DlsFdPfschMaxWeight   = RAD_LTEMAC(145),    /* */
  ERadLteMac_DlsFdActivityAvgT     = RAD_LTEMAC(146),    /* */

// mwfu for DlInterference end
  
  // TDLTE, Yang Jia, 2010-04-23, ! change this in merge !
  #define RAD_LTE_TDD_MAC_START 147
    /** TDLTE PARAMETER
    * parameter selects for different test purposes used measurement object list for TTI Trace of
    * UL Scheduler Browser Measurements.
    * value:     1 to 3  , step size 1
    *           11 to 12 , step size 1
    */
    //New added in TDD Inc21 FB3 liiikyin 2009-11-5
    ERadLteMac_TtiObjectListUl = RAD_LTEMAC(RAD_LTE_TDD_MAC_START),

    /** TDLTE PARAMETER
     * Enable Uplink close loop power control printing
     * 0=disabled, 1=enabled
     */
      ERadLteMac_UlClPcPrintingEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 1),

    /** TDLTE PARAMETER
     * Enable Uplink close loop power control printing for I/O data
     * 0=disabled, 1=enabled
     */
    ERadLteMac_UlClPcPrintIOEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 2),

    /** TDLTE PARAMETER
     * Enable Uplink close loop power control printing for PUCCH
     * 0=disabled, 1=enabled
     */
    ERadLteMac_UlClPcPucchPrintingEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 3),

    /** TDLTE PARAMETER
     * Enable Uplink close loop power control printing for PUSCH
     * 0=disabled, 1=enabled
     */
    ERadLteMac_UlClPcPuschPrintingEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 4),

    /* TDLTE PARAMETER
     Enables OLLA compensation DELTA_CQI applied to Measurement Filter,
     value:  true (1) or false (0)
    */
    ERadLteMac_MimoOllaUsedCl = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 5),

    /*
     Fixed weighting for Srs based TA error estimates for
     calculation of the combined Srs DelayError.
     Range: 0...1, default 1
    */
    ERadLteMac_FixWeightSrs = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 6),
    
  /*
   0=disable, 1=enable //Inc23 Shufei for PDCCH LA 2010-06-07
   */
  ERadLteMac_PdcchTtiTraceEnable=RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 7),
  
  /**************************************F7&9&13_UL Start***********************************************/		   
  /* Enable Uplink Gbr
   * 0=disabled, 1=enabled
   */

  ERadLteMac_UlGbrEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 8),

  /* Modified by tpj for Non-GBR UL 2010-03-24 begin */  
  /*
  **
   * control the log .
   */
  ERadLteMac_NonGBRULPRINTSWITCH  = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 9),
  /* Modified by tpj for Non-GBR UL 2010-03-24 begin */  
  /*
  **
   * control the log .rdSchedOrderExhFd
   */
  ERadLteMac_SCHEDORDEREXHFD  = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 10),  
  /* Modified by tpj for Non-GBR UL 2010-03-24 end */  

/**************************************F7&9&13_UL End***********************************************/ 
  /**
	* The parameter defines if delay based UL time domain metric for QCI=1 bearer is enabled
	*/
   ERadLteMac_UlsTdDelayMetricEnable   = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 11),
  
   /**
	* The parameter defines static Head of Line delay independent scheduling weight for
	* GBR DRB in uplink. The parameter is applicable if rdUlsTdDelayMetricEnable is false
	*/
   ERadLteMac_UlsTdGbrStaticSchedulWeight = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 12),
  
   /**
	* The parameter defines the portion of SR period exceeding 20ms that is counted as
	* Head of Line delay in case of Scheduling Request for QCI=1 bearer.
	*/
   ERadLteMac_UlsHolEstSrFactor = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 13),
  
   /**
	* The parameter defines the minimum interval between consecutive Scheduling Requests
	* to conclude silent period for QCI=1 bearer.
	*/
   ERadLteMac_UlsSrIntervalForSidDetection = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 14),
  
   /**
	* The parameter defines an interarrival time of voice packet to be taken into
	* account e.g. in UL time domain scheduling metric for QCI=1 bearer.
	* The default value corresponds to the packet interarrival time of AMR codecs
	* (for the time being (WB-) AMR as it is the only supported currently)
	* range: 1...50 ms, step 1. Default: 20 ms
	*/
   ERadLteMac_VoicePacketIAT = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 15),

  // LTE10 Huang Cheng Begin
  ERadLteMac_DlsTdDelayMetricEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 16),
  ERadLteMac_DlsTdGbrStaticSchedulWeight = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 17),
  ERadLteMac_EnableGbrBufferLevelEvalDl = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 18),
  // LTE10 Huang Cheng End

  
  /* CN4267 Add by ChenYongchu 2010-08-28 Budget Time */  
  ERadLteMac_rdLatMeas1       = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 19),
  /*
      This entry is used for CN4101 Latency measurement
      ERadLteMac_rdLatMeas1:       in general most important measurements
      */

  ERadLteMac_rdLatMeas2       = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 20),
  /*
      This entry is used for CN4101 Latency measurement
      ERadLteMac_rdLatMeas2:       in general cell specific additional measurements
      */

  ERadLteMac_rdLatMeas3       = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 21),
  /*
      This entry is used for CN4101 Latency measurement
      ERadLteMac_rdLatMeas3:       in general UE specific measurements
      */



  ERadLteMac_TRdUlsPrbGapChangeEn = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 22),
  //ECqiAperOptimisticFullFeedbackMode = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 23),//LBT1000 hunan 2010.9.1
  ERadLteMac_DlLaMaxHysteresisFactor = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 24),//LBT1000 hunan 2010.9.1
  ERadLteMac_RdDlCodeRateBoost = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 25), //LBT1000 hunan 2010.9.1
  ERadLteMac_RdDlLaMaxHysteresisFactor = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 30), //LBT1000 hunan 2010.9.1
  ECqiAperOptimisticFullFeedbackMode = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 31),//LBT1000 hunan 2010.9.1
  
  /*pusch hopping start*/
  ERadLteMac_puschHoppingEnable  = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 32),
  ERadLteMac_puschHopOffset      = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 33),
  ERadLteMac_hopModePusch        = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 34),
  ERadLteMac_hopSubBwPusch       = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 35),
  ERadLteMac_hopTypePusch        = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 36),
  ERadLteMac_hopPatternExplictInfBased = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 37),
  /*pusch hopping end*/
  
  /**
  * UL PS PreScheduler: retransmission factor
  */  
  ERadLteMac_UlReTxPercentage    = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 38),
  ERadLteMac_DisableLomRDCounterUpdate = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 39),   // liyang add 2010-11-23
  ERadLteMac_rdPdcchMaxCr              = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 40), //Zheng Xiaobai 2010-12-3

  /*
   Not usable value, do not move or touch!
  */
  //cn4088 begin
  ERadLteMac_rdOptPhichCalcMethodTwo  = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 41),    /*PHICH power method flag .0 :methed 2; 1:menthed 1 */
  ERadLteMac_rdOptPhichLogSwither  = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 42),    /*PHICH power print switcher .0 :close ; 1:open */
  //cn4088 end
  ERadLteMac_DlType1Enable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 43),
  ERadLteMac_LVRBEnable = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 44),

  //Added by Chanzhu for DL PS in MIIT Test begin
  /*
   The Alg used by Downlink PacketScheduler
   0=Qos available PF. Default
   1=RoundRonbin
   2=Max C/I
   3=Proportional Fairness
   */
  ERadLteMac_DlPsAlgType = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 45),
  //Added by Chanzhu for DL PS in MIIT Test end */ 
  
  ERadLteMac_ULTdSchAlg = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 46), 
  ERadLteMac_UlMsg3PwCtrl = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 47), //msg3 power control
  ERadLteMac_rdDciStatics = RAD_LTEMAC(RAD_LTE_TDD_MAC_START + 48), //dcistastics:0 off; >0, period 
  ERadLteMac_Last
};

/*@}*/

#endif /* _MAC_RAD_DEFINITIONS_H */
