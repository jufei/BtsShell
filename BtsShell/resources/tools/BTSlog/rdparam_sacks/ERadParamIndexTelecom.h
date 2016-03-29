/***********************************************************************
*                  Copyright (c) 2005 Nokia Networks
*                  All rights reserved
*
* FILENAME    : ERadParamIndexTelecom.h ver. wn3_inc2#2.13
* DATE        : 08-DEC-2006 11:12:16
* AUTHOR      : ANKOKKON
* STATUS      : DRAFT
*
************************************************************************/


#ifndef _E_RAD_PARAM_INDEX_TELECOM_H
#define _E_RAD_PARAM_INDEX_TELECOM_H


typedef enum ERadParamIndexTelecom
{
    ERadParamIndexTelecom_MeasWspWaitTime                          = 0,
    /* [ms] i32 scale:1 min:0 max:1000000   Measurement-WSP message wait time  */

    ERadParamIndexTelecom_RRI_Supported                            = 1,
    /* [boolean] BOOL scale:1 min:0 max:1   Are the RRI measurements supported */

    ERadParamIndexTelecom_CCHHWspRespWaitTime                      = 2,
    /* [ms] i32 scale:1 min:0 max:1000000   CCHH Wsp resp wait time */

    ERadParamIndexTelecom_RLHWSPWaitTime                           = 3,
    /* [ms] i32 scale:1 min:0 max:1000000   RLH-Wsp wait time */

    ERadParamIndexTelecom_RLHRMWaitTime                            = 4,
    /* [ms] i32 scale:1 min:0 max:1000000   RLH-RM wait time  */

    ERadParamIndexTelecom_MaxTxPwrHysteresisVal                    = 5,
    /* [mW] i32 scale:1 min:0 max:1000000   Max TX Power Hysteresis Value */

    ERadParamIndexTelecom_HsdpaAtmEmulation                        = 6,
    /* [boolean] BOOL scale:1 min:0 max:1000000 HSDPA ATM emulation, Don't send HS_Setup to ATM */

    ERadParamIndexTelecom_RlhHsResponseWaitTime                    = 7,
    /* [ms] i32 scale:1 min:0 max:1000000   RLH HS Response Wait time */

    ERadParamIndexTelecom_RlhHsResponseComCancWaitTime             = 8,
    /* [ms] i32 scale:1 min:0 max:1000000   RLH HS Response Commit Cancellation Wait Time */

    ERadParamIndexTelecom_LrmWspWaitTime                           = 9,
    /* [ms] i32 scale:1 min:0 max:1000000   LRM res Setup Wait Time */

    ERadParamIndexTelecom_RlhSyncWaitTime                          = 10,
    /* [ms] i32 scale:1 min:0 max:1000000   RLH-Synchronization wait time */

    ERadParamIndexTelecom_CchhResFromRMWaitTime                    = 11,
    /* [ms] i32 scale:1 min:0 max:1000000   CCHH resource resp from RM wait time */

    ERadParamIndexTelecom_CchhDeleteCallRMWaitTime                 = 12,
    /* [ms] i32 scale:1 min:0 max:1000000   CCHH expanded resource resp wait time, when RM makes space for CCHs */

    ERadParamIndexTelecom_CchhHsdpaResponseWaitTime                = 13,
    /* [ms] i32 scale:1 min:0 max:1000000   CCHH HSDPA response wait time, Master waiting Slave to response */

    ERadParamIndexTelecom_BchSenderSysInfoFilter                   = 14,
    /* [SFN-prime] u32 scale:1 min:0 max:2047, System Info filtering, Sysinfo sent every Nth SFN-prime (i.e. every N*20 ms) by BchSender  */

    ERadParamIndexTelecom_RMUserPlaneOverloadCancel                = 15,
    /* [ms] u32 scale:1 min:0 max:1000000, RM UserPlane Overload Cancel timer.  */

    ERadParamIndexTelecom_ToamTPGCnotActiveFixedGainValue          = 16,
    /* [N/A] u32 scale:1 min:0 max:2047, When TPGC has not been activated in TOAM, for testing purposes some fixed value is needed */

    ERadParamIndexTelecom_ToamMaxNbrOfMissedPwrReports             = 17,
    /* [N/A] u32 scale:1 min:0 max:4000000000, Maximum number of missed power reports in TPGC before restarts measurements. */

    ERadParamIndexTelecom_CMeasCellPwrInfoDelivery                 = 18,
    /* [boolean] BOOL scale:1 min:0 max:1, CMeas Cell power information delivery to other WAMs, 0=No sending. */

    ERadParamIndexTelecom_RmHwPlatformType                         = 19,
    /* 0 (default) = Normal HW_Rel function used. 1 = RM forced for Flexi (in Nora hw, SCT) */

    ERadParamIndexTelecom_CtrlRncDelayingTime                      = 20,
    /* 0 (default). Delay time of Deletion Response messages (0-4s).Value 0 means that the delay is not in the use.Step = 1s. */

    ERadParamIndexTelecom_LengthOfSdlMsgQueue                      = 21,
    /* 0 (default). Length of the SDL message queue. Value 0 means that parameter is not in use.*/

    ERadParamIndexTelecom_CMeasMaxAllowedSfnDelayForReport         = 22,
    /* CMeas: Maximum Delay for measurement reports. If delay is longer, report is not delivered to RNC. Unit in SFNs */

    ERadParamIndexTelecom_DMeasMaxAllowedSfnDelayForReport         = 23,
    /* DMeas: Maximum Delay for measurement reports. If delay is longer, report is not delivered to RNC. Unit in SFNs */

    ERadParamIndexTelecom_CMeasMsgQueueWaitTime                    = 24,
    /* CMeas: Time between writing the message queue statistics to the file, in minutes. 0 disables the log printing  */

    ERadParamIndexTelecom_DMeasMsgQueueWaitTime                    = 25,
    /* DMeas: Time between writing the message queue statistics to the file, in minutes. 0 disables the log printing  */

    ERadParamIndexTelecom_HsdpaPowerMin                            = 26,
    /* Minimum HSDPA total power in case HSDPA total power is not given from RNC
       step:1, Unit: milliWatt*/

    ERadParamIndexTelecom_HsdpaPowerMax                            = 27,
    /* Maximum HSDPA total power in case HSDPA total power is not given from RNC.
       step:1, Unit: milliWatt*/

    ERadParamIndexTelecom_HsdpaPowerMargin                         = 28,
    /* Power safety margin for allocation of HSDPA power.
       step:1 Unit: milliWatt*/

    ERadParamIndexTelecom_HsdpaPowerDeltaUpMax                     = 29,
    /* Maximum relative increase in the allocated HSDPA power from one allocation period to the next.
       step:1 Unit: milliWatt*/

    ERadParamIndexTelecom_MaxNbrHsdpaUes                           = 30,
    /* Maximum number of HSDPA UEs per MAC-hs entity, step:1 */

    ERadParamIndexTelecom_CmccHsdpaTrialSupported                  = 31,
    /* CMCC HSDPA trial on/off */

    ERadParamIndexTelecom_LicenseStatusCheckPeriod                 = 32,
    /* TLH: Period for checking licese status, unit: seconds */

    ERadParamIndexTelecom_NbapOverload                             = 33,
     /* Overload in NBAP. Dedicated measurement period will be doubled and GRM does not allocate RLs to a slave wam which has NbapOverload*/

    ERadParamIndexTelecom_NbapHeavyOverload                        = 34,
    /*  Heavy overload in NBAP.  Dedicated measurements will be terminated and new dedicated measurements and RL setups will be rejected*/

    ERadParamIndexTelecom_MeasStallTime                            = 35,
    /* [ms] u32 scale:1 min:0 max:1000000   DMeas stall time (delay) after each message sent to RNC */

    ERadParamIndexTelecom_RmDspHoldAlarmTime                       = 36,
    /* [s] RM DspHoldAlarm timer. (1200s = 20min) Alarm sent, if DSP put in hold three times one after the other within this time window. */

    ERadParamIndexTelecom_ToamEnableCellRespTimeout                = 37,
    /* [ms] u32 scale:1 min:0 max:1000000   Timeout used when waiting for message EnableCellResponse from CCHH in TOAM */

    ERadParamIndexTelecom_EnableDynamicPowerControl                = 38,
    /* [boolean] BOOL scale:1 min:0 max:1, CMCC - Enable Dynamic Power Control, 1 = Enble, 0 = Disable. */

    ERadParamIndexTelecom_CellAndConnectionBasedMeasurementFiltering = 39,
    /* [boolean] BOOL scale:1 min:0 max:1, Cell and connection based measurement(3GPP Iub) filtering 1 = Enble, 0 = Disable. */

    ERadParamIndexTelecom_DMeasReportStatusPrintPeriod              = 40,
    /* [SFN] min:0, DMeas report status print timeout  (0 = Disable, X Delay between prints in SFN). */

    ERadParamIndexTelecom_CchhResFromToamWaitTime                   = 41,
    /* [ms] i32 scale:1 min:0 max:1000000   CCHH resource resp from TOAM wait time */

    ERadParamIndexTelecom_CchhHsupaResponseWaitTime                 = 42,
    /* [ms] i32 scale:1 min:0 max:1000000   CCHH HSUPA response wait time, Master waiting Slave to response */

    ERadParamIndexTelecom_RlReconfigPreMaxQueueingTime              = 43,
    /* [ms] u32 scale:1 min:0 max:1000000   Queueing time for RlReconfigPrepare messages */

    ERadParamIndexTelecom_MaxNbrOfParallelRlReconfigPrepareReqs     = 44,
    /* [N/A] u32 scale:1 min:0 max:4000000000  Maximum number of parallel RlReconfigPrepare messages */

    ERadParamIndexTelecom_CchhLtxResponseWaitTime                   = 45,
    /* [ms] u32 scale:1 min:0 max:1000000   CCHH LTX response wait time */

    ERadParamIndexTelecom_RlhRlReconfigPrepareBufferingTime         = 46,
    /* [ms] u32 scale:1 min:1 max:1000000   Time for RLH to buffer one RlReconfigPrepare message in Rl buffer process*/

    ERadParamIndexTelecom_RlDeletionMaxQueueingTime                 = 47,
    /* [ms] u32 scale:1 min:0 max:1000000   Queueing time for RlReconfigPrepare messages */

    ERadParamIndexTelecom_MaxNbrOfParallelRlDeletionReqs            = 48,
    /* [N/A] u32 scale:1 min:0 max:4000000000  Maximum number of parallel RlReconfigPrepare messages */

    ERadParamIndexTelecom_RlhRlDeletionBufferingTime                = 49,
    /* [ms] u32 scale:1 min:1 max:1000000   Time for RLH to buffer one RlReconfigPrepare message in Rl buffer process*/

    ERadParamIndexTelecom_HsdpaPowerAlfa0                           = 50,
    /* Updating speed of emergency HS-PDSCH power reduction, step:1 */

    ERadParamIndexTelecom_HsdpaPowerAlfa1                           = 51,
    /* Updating speed of HS-PDSCH power allocation based on total cell power, step:1 */

    ERadParamIndexTelecom_HsdpaPowerMargin0                         = 52,
    /* Power margin for emergency HS-PDSCH power reduction, step:1 */

    ERadParamIndexTelecom_HsdpaPowerMargin1                         = 53,
    /* Power safety margin for HS-PDSCH power allocation based on total cell power, step:1 */

    ERadParamIndexTelecom_CESoftThreshold                           = 54,
    /* When CEs drop below this value resources are requested back from HSUPA if possible */

    ERadParamIndexTelecom_CEStepMargin                              = 55,
    /* When CEs are above SoftThreshold + StepMargin then HSUPA can have more resourses */

    ERadParamIndexTelecom_ToamRequestInitialCalibGainWaitTime       = 56,
     /* [ms] u32 scale:1 min:0 max:1000000   Time for TOAM to wait for message InitialCalibrationGainResp from OAM */

    ERadParamIndexTelecom_MaxRlSetupNmbr                            = 57,
    /* Maximum number of parallel NBAP RL Setup procedures handled in RLH. Min: 0, default: 7, max: 20. */

    ERadParamIndexTelecom_MaxHsdpaNmbr                              = 58,
    /* Maximum number of parallel HSRlSetup/HSRlReconfig/HSRlAddition -processes in RLH. Min: 0, default: 10, max: 20. */

    ERadParamIndexTelecom_MaxHsupaSetupNmbr                         = 59,
    /* Maximum number of parallel HsupaRlSetup -processes in RLH. Min: 0, default: 10, max: 20. */

    ERadParamIndexTelecom_MaxDchUserRlReconfigNmbr                  = 60,
    /* Maximum number of parallel 3gRlReconfig -processes in RLH. Min: 0, default: 10, max: 20. */

    ERadParamIndexTelecom_MaxHsupaUserRlReconfigNmbr                = 61,
    /* Maximum number of parallel HsupaRlReconfig -processes in RLH. Min: 0, default: 10, max: 20. */

    ERadParamIndexTelecom_MaxRlAdditionNmbr                         = 62,
    /* Maximum number of parallel NBAP RL Addition procedures in RLH. Min: 0, default: 10, max: 20. */

    ERadParamIndexTelecom_MaxHsupaUserRlAdditionNmbr                = 63,
    /* Maximum number of parallel HsupaRlAddition -processes in RLH. Min: 0, default: 10, max: 20. */

    ERadParamIndexTelecom_MaxRlDeletionNmbr                         = 64,
    /* Maximum number of parallel NBAP RL Deletion procedures handled in RLH. Min: 0, default: 10. */

    ERadParamIndexTelecom_RmMaximumNumberOfClusterFractions         = 65,
    /* Maximum number of cluster fractions in LRM. */

    ERadParamIndexTelecom_ToamWtrTxPowerLevelLimitChecking          = 66,
    /* TOAM: WTR TX power level limit checking (enabled=1, disabled=0) */

    ERadParamIndexTelecom_ToamWtrTxPowerLevelLowerLimit             = 67,
    /* TOAM: WTR TX power level lower limit (tenths of dBm) */

    ERadParamIndexTelecom_ToamWtrTxPowerLevelUpperLimit             = 68,
    /* TOAM: WTR TX power level upper limit (tenths of dBm) */

    ERadParamIndexTelecom_ToamCellMaxPowerLevelForWtrTxPowerLevelChecking = 69,
    /* TOAM: WTR TX power level limit checking enabled for cells with maximum power above this value (tenths of dBm) */
    
    ERadParamIndexTelecom_LocalReleaseTimerDuration                 = 70,
    /* RLH: Duration for local release timer. [ms] i32 scale:1 min:0 max:1000000. Default: 500. */

    ERadParamIndexTelecom_CellULDCHReportPeriod                 = 71,
    /* GRM: Duration for Cell UL DCH Report Period timer. [ms] i32 scale:1 min:0 max:1000000. Default: 50. */

    ERadParamIndexTelecom_MinimumCEforDCHAvailable                 = 72,
    /* GRM: Minimum CE for DCH Available. Default: 32. */

    ERadParamIndexTelecom_SoftRequestTimerDuration                 = 73,
    /* LRM: Duration for Soft Request timer. [ms] i32 scale:1 min:0 max:1000000. Default: 200. */

    ERadParamIndexTelecom_NbrOfParameters
    /* Keep this at last line */

} ERadParamIndexTelecom;


#endif /* _E_RAD_PARAM_INDEX_TELECOM_H */


/***********************************************************************
*
* SW Block            : Nora BTS / BS Env
*
* Development Workset : WCDMA:BS_ENV_WS
*
* Description : Index enumeration for Telecom related R&D parameter.
*
* Reference   : BTS R&D Tools Interface Specification
*               - version 2.2, paragraph 4.1.5 (PI)
*
* Parameters  :
*
* Provider : Telecom / Mika Järvi
*
* Remember to put an empty line in the end of each definition
* file. Otherwise the compiler will generate a warning.
***********************************************************************/
