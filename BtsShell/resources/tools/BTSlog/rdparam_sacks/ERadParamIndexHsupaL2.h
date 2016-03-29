/**
*******************************************************************************
* @file                  ERadParamIndexHsupaL2.h
* @version               wn4_inc6#6.5
* @date                  27-APR-2007 09:47:22
* @author                ANKOKKON
*
* Item Specification     WCDMA:A32158.A-SRC
*
* Status                 DRAFT
*
* Original author        Kari Korvela
*
* Copyright (c) Nokia 2007. All rights reserved.
******************************************************************************/

#ifndef _E_RAD_PARAM_INDEX_HSUPA_L2_H
#define _E_RAD_PARAM_INDEX_HSUPA_L2_H

typedef enum ERadParamIndexHsupaL2
{
    ERadParamIndexHsupaL2_HsupaMinorOverloadCounterLimit                    = 0,
    /* [n/a] UINT scale:1 min:1 max:50 HSUPA minor overload counter limit */

    ERadParamIndexHsupaL2_MacEControlReportTriggerCheckingPeriod            = 1,
    /* [ms] UINT scale:1 min:1 max:50 MAC-e control report trigger checking period */

    ERadParamIndexHsupaL2_MacEMeasurementReportReportingPeriod              = 2,
    /* [ms] UINT scale:1 min:10 max:100 MAC-e measurement report reporting period (range: 10, 25, 50, 100) */

    ERadParamIndexHsupaL2_HsupaDynamicDlPowerControl                        = 3,
    /* [n/a] BOOL scale:1 min:0 max:1 HSUPA dynamic DL power control */

    ERadParamIndexHsupaL2_HsupaEHichStaticTxPower                           = 4,
    /* [dB] INT scale:0.1 min:-500 max:500 HSUPA E-HICH static tx power */

    ERadParamIndexHsupaL2_HsupaEAgchPowerOffset                             = 5,
    /* [dB] INT scale:0.1 min:-100 max:100 HSUPA E-AGCH power offset */

    ERadParamIndexHsupaL2_HsupaERgchPowerOffset                             = 6,
    /* [dB] INT scale:0.1 min:-100 max:100 HSUPA E-RGCH power offset */

    ERadParamIndexHsupaL2_ResourceReqFreqCounter                            = 7,
    /* [n/a] UINT scale:1 min:1 max:100 DSP RM resource request frequency counter */

    ERadParamIndexHsupaL2_LowUtilizationForgettingFactor                    = 8,
    /* [n/a] UINT scale:0.1 min:0 max:10 Low utilization forgetting factor */

    ERadParamIndexHsupaL2_PsLowUtilizationThreshold                         = 9,
    /* [n/a] UINT scale:0.01 min:0 max:99 PS low utilization threshold */

    ERadParamIndexHsupaL2_PsLowUtilizationCounter                           = 10,
    /* [n/a] UINT scale:1 min:1 max:100 PS low utilization counter */

    ERadParamIndexHsupaL2_EDchPsUpgradeCounter                              = 11,
    /* [n/a] UINT scale:1 min:1 max:100 E-DCH PS upgrade counter */

    ERadParamIndexHsupaL2_EDchPsDowngradeCounter                            = 12,
    /* [n/a] UINT scale:1 min:1 max:100 E-DCH PS downgrade counter */

    ERadParamIndexHsupaL2_EDchPsPeriod                                      = 13,
    /* [ms] UINT scale:1 min:1 max:100 E-DCH PS period */

    ERadParamIndexHsupaL2_PsCongestIndDowngradeCounterForDelayBuildUp       = 14,
    /* [n/a] UINT scale:1 min:1 max:100 PS congestion indication downgrade counter for delay build-up */

    ERadParamIndexHsupaL2_PsCongestIndDowngradeCounterForFrameLoss          = 15,
    /* [n/a] UINT scale:1 min:1 max:100 PS congestion indication downgrade counter for frame loss */

    ERadParamIndexHsupaL2_PsCongestIndHoldCounter                           = 16,
    /* [n/a] UINT scale:1 min:1 max:100 PS congestion indication hold counter */

    ERadParamIndexHsupaL2_PsCongestIndReserveCounter                        = 17,
    /* [n/a] UINT scale:1 min:1 max:100 PS congestion indication reserve counter */

    ERadParamIndexHsupaL2_EDchInitialBitRate                                = 18,
    /* [n/a] UINT scale:1 min:0 max:6 E-DCH initial bit rate */

    ERadParamIndexHsupaL2_LoadOffsetOfNodeB                                 = 19,
    /* [n/a] UINT scale:0.001 min:0 max:999 Load offset of Node-B */

    ERadParamIndexHsupaL2_MinorLoadOffsetOfNodeB                            = 20,
    /* [n/a] UINT scale:0.001 min:0 max:999 Minor load offset of Node-B */

    ERadParamIndexHsupaL2_MaxCFUse                                          = 21,
    /* [n/a] UINT scale:1 min:1 max:10 HSUPA maximum CF use */

    ERadParamIndexHsupaL2_NonHWLimitedUEsPerSingleClusterFrac               = 22,
    /* [n/a] UINT scale:1 min:1 max:10 HSUPA non HW limited UEs per single cluster fraction */

    ERadParamIndexHsupaL2_NonHWLimitedMaxNumOfUEsPerClusterFrac             = 23,
    /* [n/a] UINT scale:1 min:1 max:10 HSUPA non HW limited maximum number of UEs per single cluster fraction */

    ERadParamIndexHsupaL2_HWLimitedMaxNumOfUEsPerClusterFrac                = 24,
    /* [n/a] UINT scale:1 min:1 max:16 HSUPA HW limited UEs per single cluster fraction */

    ERadParamIndexHsupaL2_DspRmSoftResourceRemovalLimit                     = 25,
    /* [n/a] UINT scale:1 min:1 max:100 DSP RM soft resource removal limit */

    ERadParamIndexHsupaL2_NumberOfSoftRemovalReqsLimit1                     = 26,
    /* [n/a] UINT scale:1 min:1 max:100 DSP RM number of soft removal requests limit 1 */

    ERadParamIndexHsupaL2_NotUsed1                                          = 27,
    /* Spare, not used */

    ERadParamIndexHsupaL2_CFoutOfResourcesCounterLimit                      = 28,
    /* [n/a] UINT scale:1 min:0 max:1000 Cluster fraction out of resources counter limit */

    ERadParamIndexHsupaL2_PenaltyCounterLimit                               = 29,
    /* [n/a] UINT scale:1 min:0 max:1000 Penalty counter limit */

    ERadParamIndexHsupaL2_CFNoResourceIncreaseCounterLimit                  = 30,
    /* [n/a] UINT scale:1 min:0 max:1000 Cluster fraction no resource increase counter limit */

    ERadParamIndexHsupaL2_TargetUEsPerCluster                               = 31,
    /* [n/a] UINT scale:1 min:1 max:100 HSUPA target UEs per cluster */

    ERadParamIndexHsupaL2_HsupaMaxNumberOfRetrans                           = 32,
    /* [n/a] UINT scale:1 min:1 max:12 HSUPA maximum number of retransmissions */

    ERadParamIndexHsupaL2_HsupaRetransmissionETfci                          = 33,
    /* [n/a] UINT scale:1 min:1 max:255 HSUPA retransmission E-TFCI */

    ERadParamIndexHsupaL2_HsupaMaxBitRateByEAgch                            = 34,
    /* [n/a] UINT scale:1 min:0 max:7 HSUPA maximum bit rate by E-AGCH */

    ERadParamIndexHsupaL2_HsupaMaxBitRateEAgchDuringDTX                     = 35,
    /* [n/a] UINT scale:1 min:0 max:7 HSUPA maximum bit rate E-AGCH during DTX */

    ERadParamIndexHsupaL2_HsupaCellLoadIncreaseLimit                        = 36,
    /* [n/a] UINT scale:0.001 min:0 max:1000 HSUPA cell load increase limit */

    ERadParamIndexHsupaL2_HsupaCellLoadDecreaseLimit                        = 37,
    /* [n/a] UINT scale:0.001 min:0 max:1000 HSUPA cell load decrease limit */

    ERadParamIndexHsupaL2_HsupaUeMinimumHwReservation                       = 38,
    /* [n/a] UINT scale:1 min:0 max:7 HSUPA UE minimum HW reservation (range: 0-7, 255) */

    ERadParamIndexHsupaL2_MaxAmount                                         = 39
    /* Not a real R&D parameter. Used to define the amount of R&D parameters. 
     * Keep this always the last one! */
}ERadParamIndexHsupaL2;

#endif  /* _E_RAD_PARAM_INDEX_HSUPA_L2_H */

/******************************************************************************
* @enum ERadParamIndexHsupaL2
* Development Workset : WCDMA:BS_ENV_WS
*
* Design Part         : WCDMA:BS_ENV.A;1
*
* Description         : Index enumeration for HSUPA L2 related R&D parameter.
*                       Used as a parameter index when handling following
*                       messages in HSUPA L2 subsystem:
*                       - GetRadParamsResp.h
*                       - SetRadParamsReq.h
*
* Reference           : BTS R&D Tools Interface Specification,
*                       location PI;
*                       HSUPA requirements,
*                       location Doors
*
* @param ERadParamIndexHsupaL2_HsupaMinorOverloadCounterLimit : 
*        Default value: 3; Range: 1 - 50; Step: 1;
*        HSUPA minor overload counter limit.
*        In minor overload state this parameters defines how often overload
*        actions are done.
* @param ERadParamIndexHsupaL2_MacEControlReportTriggerCheckingPeriod :
*        Default value: 3 ms; Range: 1 ms - 50 ms; Step: 1 ms;
*        MAC-e control report trigger checking period.
*        Parameter defines how ofter MAC-e report triggers should be checked.
* @param ERadParamIndexHsupaL2_MacEMeasurementReportReportingPeriod :
*        Default value: 50 ms; Range: 10 ms, 25 ms, 50 ms, 100 ms; Step: -;
*        MAC-e measurement report reporting period.
*        Parameter defines the sending period for MAC-e measurement report.
* @param ERadParamIndexHsupaL2_HsupaDynamicDlPowerControl :
*        Default value: Enabled; Range: Enabled/Disabled; Step: -;
*        HSUPA dynamic DL power control.
*        If set to Disabled, DL channels shall use static powers that are 
*        defined by R&D parameters. If set to enabled, DL powers shall be set
*        according to normal procedure. 
* @param ERadParamIndexHsupaL2_HsupaEHichStaticTxPower :
*        Default value: -10.0 dB; Range: -50.0 - +50.0 dB; Step: 0.1 dB;
*        HSUPA E-HICH static tx power. Defines the E-HICH transmission power
*        relative to P-CPICH in case HSUPA dynamic DL power control is 
*        disabled.
* @param ERadParamIndexHsupaL2_HsupaEAgchPowerOffset :
*        Default value: 1.0 dB; Range: -10.0 - +10.0 dB; Step: 0.1 dB;
*        HSUPA E-AGCH power offset. Defines the E-AGCH transmission power 
*        relative to E-HICH transmission power.
* @param ERadParamIndexHsupaL2_HsupaERgchPowerOffset :
*        Default value: 0.1 dB; Range: -10.0 - +10.0 dB; Step: 0.1 dB;
*        HSUPA E-RGCH power offset. Defines the E-RGCH transmission power
*        relative to E-HICH transmission power.
* @param ERadParamIndexHsupaL2_ResourceReqFreqCounter :
*        Default value: 20; Range: 1 - 100; Step: 1;
*        DSP RM Resource Request Frequency Counter.
*        Defines the frequency, how often HSUPA resource request may be
*        retried after unsuccessfull request. Counts scheduling periods.
* @param ERadParamIndexHsupaL2_LowUtilizationForgettingFactor :
*        Default value: 0.9; Range: 0.0 - 1.0; Step: 0.1;
*        Low utilization forgetting factor.
*        Parameter defines forgetting factor for utilization calculation.
* @param ERadParamIndexHsupaL2_PsLowUtilizationThreshold :
*        Default value: 0.75; Range: 0.00 - 0.99; Step: 0.01;
*        PS Low utilization Threshold.
*        Parameter defines utilization threshold for low utilization state.
* @param ERadParamIndexHsupaL2_PsLowUtilizationCounter :
*        Default value: 3; Range: 1 - 100; Step: 1;
*        PS Low utilization counter.
*        Parameter defines the period that utilization needs to be below PS
*        low utilization threshold before the UE is identified as low 
*        utilization UE.
* @param ERadParamIndexHsupaL2_EDchPsUpgradeCounter :
*        Default value: 5; Range: 1 - 100; Step: 1;
*        E-DCH PS Upgrade counter.
*        Parameter defines the period for which the UE specific grant is not
*        allowed to be increased. Counts PS scheduling periods.
* @param ERadParamIndexHsupaL2_EDchPsDowngradeCounter :
*        Default value: 4; Range: 1 - 100; Step: 1;
*        E-DCH PS Downgrade counter.
*        Parameter defines the period for which the UE specific grant is not
*        allowed to be decreased due overload situation. Counts PS scheduling
*        periods.
* @param ERadParamIndexHsupaL2_EDchPsPeriod :
*        Default value: 10 ms; Range: 1 ms - 100 ms; Step: 1 ms;
*        E-DCH PS Period. This parameter defines the packet scheduling
*        decision period.
* @param ERadParamIndexHsupaL2_PsCongestIndDowngradeCounterForDelayBuildUp :
*        Default value: 5; Range: 1 - 100; Step: 1;
*        PS Congestion Indication Downgrade counter for delay build-up.
*        During the activation of congestion indication downgrade counter,
*        the packet scheduler is not allowed to give the upgrading grants
*        to MAC-d flow on which the congestion indication was received.
* @param ERadParamIndexHsupaL2_PsCongestIndDowngradeCounterForFrameLoss :
*        Default value: 4; Range: 1 - 100; Step: 1;
*        PS Congestion Indication Downgrade counter for frame loss.
*        During the activation of congestion indication downgrade counter,
*        the packet scheduler is not allowed to give the upgrading grants
*        to MAC-d flow on which the congestion indication was received.
* @param ERadParamIndexHsupaL2_PsCongestIndHoldCounter :
*        Default value: 3; Range: 1 - 100; Step: 1;
*        PS Congestion Indication Hold counter.
*        During the activation of congestion indication hold counter,
*        the packet scheduler is not allowed to give the upgrading grants
*        to MAC-d flow on which the congestion indication was received.
* @param ERadParamIndexHsupaL2_PsCongestIndReserveCounter :
*        Default value: 5; Range: 1 - 100; Step: 1;
*        PS Congestion Indication Reserve counter.
*        During the activation of congestion indication reserve counter,
*        the packet scheduler shall not free the reserved load for other UEs, 
*        but it may be used by the UE it was reserved for.
* @param ERadParamIndexHsupaL2_EDchInitialBitRate :
*        Default value: 0; Range: 0 - 6; Step: 1;
*        E-DCH initial bit rate. This parameter defines the initial bit rate
*        for a new UE.
* @param ERadParamIndexHsupaL2_LoadOffsetOfNodeB :
*        Default value: 0.100; Range: 0.000 - 0.999; Step: 0.001;
*        Load offset of Node-B. This parameter indicates a safety margin to 
*        prevent the overload.
* @param ERadParamIndexHsupaL2_MinorLoadOffsetOfNodeB :
*        Default value: 0.100; Range: 0.000 - 0.999; Step: 0.001;
*        Load offset of Node-B. This parameter indicates a safety margin to 
*        prevent the overload.
* @param ERadParamIndexHsupaL2_MaxCFUse :
*        Default value: 3; Range: 1 - 10; Step: 1;
*        HSUPA maximum CF use. Defines the maximum number of cluster fractions
*        that HSUPA DSP resource manager tries to allocate.
* @param ERadParamIndexHsupaL2_NonHWLimitedUEsPerSingleClusterFrac :
*        Default value: 4; Range: 1 - 10; Step: 1;
*        HSUPA non HW limited UEs per single cluster fraction. 
*        Defines the maximum number of UEs that can be allocated into a single
*        cluster fractions, when the cluster fraction only contains UEs from
*        same cell and UEs will not get HW limited (so the UE bitrates will not
*        get limited by HW reservation, but rather by air interference).
* @param ERadParamIndexHsupaL2_NonHWLimitedMaxNumOfUEsPerClusterFrac :
*        Default value: 3; Range: 1 - 10; Step: 1;
*        HSUPA non HW limited maximum number of UEs per single cluster fraction.
*        Defines the maximum number of UEs that can be allocated into a single
*        cluster fractions, when the cluster fraction contains UEs from
*        several cells and UEs will not get HW limited (so the UE bitrates will
*        not get limited by HW reservation, but rather by air interference).
* @param ERadParamIndexHsupaL2_HWLimitedMaxNumOfUEsPerClusterFrac :
*        Default value: 8; Range: 1 - 16; Step: 1;
*        HSUPA HW limited UEs per single cluster fraction. 
*        Defines the maximum number of UEs that can be allocated into a single
*        cluster fractions, when UEs will get HW limited (so the UE bitrates 
*        will propably get limited by HW reservation, because the CF is not
*        able to support high bitrates to all UE simultaneously).
* @param ERadParamIndexHsupaL2_DspRmSoftResourceRemovalLimit :
*        Default value: 50; Range: 1 - 100; Step: 1;
*        DSP RM Soft Resource Removal Limit.
*        Defines the counter limit after which DSP RM state is set to normal,
*        if there was no resource removal requests. Counts PS scheduling 
*        periods.
* @param ERadParamIndexHsupaL2_NumberOfSoftRemovalReqsLimit1 :
*        Default value: 5; Range: 1 - 100; Step: 1;
*        DSP RM Number of Soft Removal Requests limit 1.
*        Defines the amount of consecutive resource removal requests with Soft
*        priority that causes DSP RM to start active measures by moving users 
*        to make free resources. 
* @param ERadParamIndexHsupaL2_NotUsed1 :
*        Spare, not used. 
* @param ERadParamIndexHsupaL2_CFoutOfResourcesCounterLimit :
*        Default value: 50; Range: 0 - 1000; Step: 1;
*        Cluster Fraction out of resources counter limit.
*        If the number of consecutive failed HW allocation increase attemps
*        (due insufficient resources in CF) is above this limit, then DSP RM
*        proposes PS to decrease highest allocation UE to balance the load in
*        CF.
* @param ERadParamIndexHsupaL2_PenaltyCounterLimit :
*        Default value: 10; Range: 0 - 1000; Step: 1;
*        Penalty counter limit.
*        If the number of PS periods that a UE has had penalty (HW allocation
*        increase is not allowed), is above this limit, then UE penalty shall 
*        be removed. 
* @param ERadParamIndexHsupaL2_CFNoResourceIncreaseCounterLimit :
*        Default value: 5; Range: 0 - 1000; Step: 1;
*        Cluster Fraction no resource increase counter limit.
*        If the number of consecutive PS periods without HW allocation increase
*        requests in a CF is above this limit, then the PenaltyCounter of all 
*        UEs in the cluster fraction shall be stopped.
* @param ERadParamIndexHsupaL2_TargetUEsPerCluster :
*        Default value: 9; Range: 1 - 100; Step: 1;
*        HSUPA target UEs per cluster.
*        If the total number of UEs in the resource pool is below or equal to
*        this limit, then UEs must are allocated into first cluster and other
*        clusters shall not be taken into account (even if the resources were
*        reserved from second cluster).
* @param ERadParamIndexHsupaL2_HsupaMaxNumberOfRetrans :
*        Default value: 4; Range: 1-12; Step: 1;
*        HSUPA maximum number of retransmissions.
*        Defines the maximum number of retransmissions that is allowed for
*        certain bitrates, before forced ACK is sent to the UE regardles of CRC
*        result.
* @param ERadParamIndexHsupaL2_HsupaRetransmissionETfci :
*        Default value: 27; Range: 1-255; Step: 1;
*        HSUPA retransmission E-TFCI.
*        Defines the E-TFCI after which the number of retransmissions is 
*        restricted.
* @param ERadParamIndexHsupaL2_HsupaMaxBitRateByEAgch :
*        Default value: 5; Range: 0-7; Step: 1;
*        HSUPA maximum bit rate by E-AGCH.
*        This parameter indicates a maximum bit rate that PS is allowed to 
*        allocate to a UE by using E-AGCH in fast bit rate ramp-up procedure.
* @param ERadParamIndexHsupaL2_HsupaMaxBitRateEAgchDuringDTX :
*        Default value: 4; Range: 0-7; Step: 1;
*        HSUPA maximum bit rate E-AGCH during DTX.
*        This parameter indicates a threshold value. If the bit allocation for
*        the same HARQ process in the previous TTI exceeds the threshold and 
*        DTX occurs for the same HARQ process in the current TTI, the E-AGCH
*        is considered to decrease the bit allocation.
* @param ERadParamIndexHsupaL2_HsupaCellLoadIncreaseLimit :
*        Default value: 0.300; Range: 0.000 - 1.000; Step: 0.001;
*        HSUPA cell load increase limit.
*        This parameter indicates the allowed maximum cell load increase in
*        Node-B packet scheduling period.
* @param ERadParamIndexHsupaL2_HsupaCellLoadDecreaseLimit :
*        Default value: 0.100; Range: 0.000 - 1.000; Step: 0.001;
*        HSUPA cell load decrease limit.
*        This parameter indicates the allowed maximum cell load decrease in
*        Node-B packet scheduling period.
* @param ERadParamIndexHsupaL2_HsupaUeMinimumHwReservation :
*        Default value: 0; Range: 0 - 7, 255; Step: 1;
*        HSUPA UE minimum HW reservation.
*        This parameter defines the minimum HW reservation for a HSUPA UE. 
*        DSP RM is not allowed to decrease the allocation below this limit.
* @param ERadParamIndexHsupaL2_MaxAmount :
*        Default value: N/A; Range: N/A; Step: N/A;
*        Maximum amount of R&D parameters/indices.
*
* Additional Information : - 
*
* Definition Provided by : DSP
* 
* Remember to put an empty line in the end of each definition file.
* Otherwise the compiler will generate a warning.
******************************************************************************/

