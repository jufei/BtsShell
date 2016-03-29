/**
*******************************************************************************
* @file                  ERadParamIndexMacHs.h
* @version               wn4_inc6#6.1
* @date                  27-APR-2007 09:47:23
* @author                ANKOKKON
*
* Item Specification     WCDMA:A26508.A-SRC
*
* Status                 DRAFT
*
* Original author        J.Saviaro
*
* Copyright (c) Nokia 2007. All rights reserved.
*******************************************************************************/

#ifndef _ERADPARAMINDEXMACHS_H
#define _ERADPARAMINDEXMACHS_H

typedef enum ERadParamIndexMacHs
{
    ERadParamIndexMacHs_A_init                                          = 0,
    /* [dB] INT scale:0.001 min:-4000 max:13000 Initial value of outer-loop link adaptation correction. Affects only new users to setup. */

    ERadParamIndexMacHs_A_stepUp                                        = 1,
    /* [dB] INT scale:0.001 min:0 max:2000 Size of upward step in outer-loop link adaptation. */

    ERadParamIndexMacHs_A_stepDown                                      = 2,
    /* [dB] INT scale:0.001 min:0 max:250 Size of downward step in outer-loop link adaptation. */

    ERadParamIndexMacHs_A_max                                           = 3,
    /* [dB] INT scale:0.001 min:0 max:13000 Maximum value of outer-loop link adaptation correction. */

    ERadParamIndexMacHs_A_min                                           = 4,
    /* [dB] INT scale:0.001 min:-4000 max:4000 Minimum value of outer-loop link adaptation correction. */

    ERadParamIndexMacHs_P_init                                          = 5,
    /* [dB] INT scale:0.001 min:-4000 max:13000 Initial value of outer-loop HS-SCCH power control correction. */

    ERadParamIndexMacHs_P_up                                            = 6,
    /* [dB] INT scale:0.001 min:0 max:2000 Size of upward step in outer-loop HS-SCCH power control. */

    ERadParamIndexMacHs_P_down                                          = 7,
    /* [dB] INT scale:0.001 min:0 max:20 Size of downward step in outer-loop HS-SCCH power control. */

    ERadParamIndexMacHs_P_max                                           = 8,
    /* [dB] INT scale:0.001 min:0: max:13000 Maximum value of outer-loop HS-SCCH power control correction. */

    ERadParamIndexMacHs_P_min                                           = 9,
    /* [dB] INT scale:0.001 min:-4000 max:4000 Minimum value of outer-loop HS-SCCH power control correctin. */

    ERadParamIndexMacHs_C_init                                          = 10,
    /* [dB] INT scale:0.001 min:-2000 max:0 Initial value of HS-PDSCH power relative to total HSDPA power. */

    ERadParamIndexMacHs_C_up                                            = 11,
    /* [dB] INT scale:0.001 min:0 max:1000 Size of upward step in HS-PDSCH power adjustment algorithm. */

    ERadParamIndexMacHs_C_down                                          = 12,
    /* [dB] INT scale:0.001 min:0 max:1000 Size of downward step in HS-PDSCH power adjustment algorithm. */

    ERadParamIndexMacHs_C_max                                           = 13,
    /* [dB] INT scale:0.001 min:-1000 max:0 Maximum HS-PDSCH power relative to total HSDPA power. */

    ERadParamIndexMacHs_C_min                                           = 14,
    /* [dB] INT scale:0.001 min:-4000 max:0 Minumum HS-PDSCH power relative to total HSDPA power. */

    ERadParamIndexMacHs_P_hsdpaHysteresis                               = 15,
    /* [Watt] UINT scale:0.001 min:0 max:3000 Hysteresis in HS-PDSCH power adjustement algorithm. */

    ERadParamIndexMacHs_HsPdschPowerAdjustmentInterval                  = 16,
    /* [ms] UINT scale:10 min:10 max:1000 Interval between HS-PDSCH power adjustment updates. */

    ERadParamIndexMacHs_MaxNoOfTrans                                    = 17,
    /* [N/A] UINT scale:1 min:1 max:10 Maximum number of transmissions of  one MAC-hs PDU. */

    ERadParamIndexMacHs_W_tti                                           = 18,
    /* [N/A] UINT scale:1 min:1 max:1000 Forgetting factor in Proportional air scheduling algorithm. */

    ERadParamIndexMacHs_N_missedCqi                                     = 19,
    /* [N/A] UINT scale:1 min:1 max:10 Number of erroneously detected CQIs before stopping scheduling. */

    ERadParamIndexMacHs_R_init                                          = 20,
    /* [bits] UINT scale:1 min:0 max:7298 Initial value for average TB size in Proportional Fair scheduling algorithm. */

    ERadParamIndexMacHs_PktSchAlg                                       = 21,
    /* [N/A] UINT scale:1 min:0 max:1 Packet Scheduling algorithm selection, 0 = Round Robin, 1 = Propotional Fair */

    ERadParamIndexMacHs_IncRed_enable                                   = 22,
    /* [N/A] BOOL scale:1 min:0 max:1 Enable incremental redundancy and constellation rearrangement. */

    ERadParamIndexMacHs_H_SC_PC_enable                                  = 23,
    /* [N/A] BOOL scale:1 min:0 max:1 Enable HS-SCCH power control. */

    ERadParamIndexMacHs_H_SC_Pwr                                        = 24,
    /* [dBm] INT scale:0.001 min:0 max:50000 HS-SCCH power if power control disabled. Note: maximum cell power limits. */

    ERadParamIndexMacHs_H_PD_PC_enable                                  = 25,
    /* [N/A] BOOL scale:1 min:0 max:1 Enable HS-PDSCH power control. */

    ERadParamIndexMacHs_H_PD_Pwr                                        = 26,
    /* [dBm] INT scale:0.001 min:0 max:50000 HS-PDSCH power if power control disabled. Note: maximum cell power limits. */

    ERadParamIndexMacHs_AkNk_enable                                     = 27,
    /* [N/A] BOOL scale:1 min:0 max:1 Enable ACK-NACK feedback handling in MAC-hs. If disabled ACK is allways assumed. */

    ERadParamIndexMacHs_CQI_enable                                      = 28,
    /* [N/A] BOOL scale:1 min:0 max:1 Enable CQI feedback handling in MAC-hs. */

    ERadParamIndexMacHs_QAM_enable                                      = 29,
    /* [N/A] BOOL scale:1 min:0 max:1 Enable support for 16-QAM modulation. */

    ERadParamIndexMacHs_CQI_default                                     = 30,
    /* [N/A] UINT scale:1 min:0 max:30 Default CQI value used when CQI feedback is disabled, when k = 0 or when CQI has not yet been received. */

    ERadParamIndexMacHs_FinTFRC_enable                                  = 31,
    /* [N/A] BOOL scale:1 min:0 max:1 Enable final TFRC selection. */

    ERadParamIndexMacHs_PwrReductEnable                                 = 32,
    /* [N/A] BOOL scale:1 min:0 max:1 Enable HS-PDSCH power reduction. */

    ERadParamIndexMacHs_PHsPdschMin                                     = 33,
    /* [Watt] UINT scale:0.001 min:0 max:100 Minimum HS-PDSCH power allocated to a cell */

    ERadParamIndexMacHs_PHsPdschMax                                     = 34,
    /* [Watt] UINT scale:0.001 min:0 max:100 Maximum HS-PDSCH power allocated to a cell  */

    ERadParamIndexMacHs_PAlfa0                                          = 35,
    /* [N/A] UINT scale:0.001 min:0 max:1 Updating speed of emergency HS-PDSCH power reduction */

    ERadParamIndexMacHs_PAlfa1                                          = 36,
    /* [N/A] UINT scale:0.001 min:0 max:1 Updating speed of HS-PDSCH power allocation based on total cell power */

    ERadParamIndexMacHs_PAlfa2                                          = 37,
    /* [N/A] UINT scale:0.001 min:0 max:1 Updating speed of HS-PDSCH power allocation based on total HSDPA power */

    ERadParamIndexMacHs_PMargin0                                        = 38,
    /* [N/A] UINT scale:0.001 min:0.001 max:2 Power margin for emergency HS-PDSCH power reduction (0.794 = - 1dB) */

    ERadParamIndexMacHs_PMargin1                                        = 39,
    /* [N/A] UINT scale:0.001 min:0.001 max:1 Power safety margin for HS-PDSCH power allocation based on total cell power (0.631 = -2dB) */

    ERadParamIndexMacHs_PHsPdschMinCodeMux2                             = 40,
    /* [Watt] UINT scale:0.001 min:0 max:100 Minimum HS-PDSCH total power of a cell to do code multiplexing for 2 users. */

    ERadParamIndexMacHs_PHsPdschMinCodeMux3                             = 41,
    /* [Watt] UINT scale:0.001 min:0 max:100 Minimum HS-PDSCH total power of a cell to do code multiplexing for 3 users. */

    ERadParamIndexMacHs_TbsMin                                          = 42,
    /* [bits] UINT scale:1 min:365 max:7298 Minimum transport block size for allowing scheduling of a priority queue. */

    ERadParamIndexMacHs_TbsMax                                          = 43,
    /* [bits] UINT scale:1 min:7298 max:83856 Maximum sum of transport block sizes per TTI */

    ERadParamIndexMacHs_SprMax                                          = 44,
    /* [N/A] UINT scale:1 min:10 max:90 Maximum amount of spreaders per TTI */

    ERadParamIndexMacHs_MaxAmount                                       = 45
    /* Not a real R&D -parameter. Used to define the amount of R&D - parameters. */

}ERadParamIndexMacHs;

#endif  /* _ERADPARAMINDEXMACHS_H */

/***********************************************************************
* @enum ERadParamIndexMacHs
* Development Workset : WCDMA:BS_ENV_WS
*
* Design Part         : WCDMA:BS_ENV.A;1
*
* Description : Index enumeration for MAC-hs related R&D parameter.
*               Used as a parameter index when handling following
*               messages in MAC-hs Packet Scheduler:
*               - GetRadParamsResp.h
*               - SetRadParamsReq.h
*
* Reference   : BTS R&D Tools Interface Specification
*               - version 5.0, paragraph 4.1.5 (PI)
*               HSDPA EFS
*               - version 9.0, paragraph 3.13.2 (PI)
*
* @param ERadParamIndexMacHs_A_init:
*       Initial value of outer-loop link adaptation correction. Affects only new users to setup.
*
* @param ERadParamIndexMacHs_A_stepUp:
*       Size of upward step in outer-loop link adaptation.
*
* @param ERadParamIndexMacHs_A_stepDown:
*       Size of downward step in outer-loop link adaptation.
*
* @param ERadParamIndexMacHs_A_max:
*       Maximum value of outer-loop link adaptation correction.
*
* @param ERadParamIndexMacHs_A_min:
*       Minimum value of outer-loop link adaptation correction.
*
* @param ERadParamIndexMacHs_P_init:
*       Initial value of outer-loop
*       HS-SCCH power control correction.
*
* @param ERadParamIndexMacHs_P_up:
*       Size of upward step in outer-loop HS-SCCH power control.
*
* @param ERadParamIndexMacHs_P_down:
*       Size of downward step in outer-loop HS-SCCH power control.
*
* @param ERadParamIndexMacHs_P_max:
*       Maximum value of outer-loop HS-SCCH power control correction.
*
* @param ERadParamIndexMacHs_P_min:
*       Minimum value of outer-loop HS-SCCH power control correctin.
*
* NOTE: Following ones not in use in WBTS4.0 
* -----> 
*
* @param ERadParamIndexMacHs_C_init:
*       Initial value of HS-PDSCH power relative to total HSDPA power.
*
* @param ERadParamIndexMacHs_C_up:
*       Size of upward step in HS-PDSCH power adjustment algorithm.
*
* @param ERadParamIndexMacHs_C_down:
*       Size of downward step in HS-PDSCH power adjustment algorithm.
*
* @param ERadParamIndexMacHs_C_max:
*       Maximum HS-PDSCH power relative to total HSDPA power.
*
* @param ERadParamIndexMacHs_C_min:
*       Minumum HS-PDSCH power relative to total HSDPA power.
*
* @param ERadParamIndexMacHs_P_hsdpaHysteresis:
*       Hysteresis in HS-PDSCH power adjustement algorithm.
*
* @param ERadParamIndexMacHs_HsPdschPowerAdjustmentInterval:
*       Interval between HS-PDSCH power adjustment updates.
*
* <----- 
* NOTE: Previous ones not in use in WBTS4.0
*
* @param ERadParamIndexMacHs_MaxNoOfTrans:
*       Maximum number of transmissions of one MAC-hs PDU.
*
* @param ERadParamIndexMacHs_W_tti:
*       Forgetting factor in Proportional Fair scheduling algorithm.
*
* @param ERadParamIndexMacHs_N_missedCqi:
*       Number of erroneously detected CQIs before stopping scheduling.
*
* @param ERadParamIndexMacHs_R_init:
*       Initial value for average TB size in Proportional Fair scheduling algorithm.
*
* @param ERadParamIndexMacHs_PktSchAlg:
*       Packet Scheduling algorithm selection, 0 = Round Robin, 1 = Propotional Fair
*
* @param ERadParamIndexMacHs_IncRed_enable:
*       Enable incremental redundancy and constellation rearrangement.
*
* @param ERadParamIndexMacHs_H_SC_PC_enable:
*       Enable HS-SCCH power control.
*
* @param ERadParamIndexMacHs_H_SC_Pwr:
*       HS-SCCH power if power control disabled. Note: maximum cell power limits.
*
* @param ERadParamIndexMacHs_H_PD_PC_enable:
*       Enable HS-PDSCH power control.
*
* @param ERadParamIndexMacHs_H_PD_Pwr:
*       HS-PDSCH power if power control disabled. Note: maximum cell power limits.
*
* @param ERadParamIndexMacHs_AkNk_enable:
*       Enable ACK-NACK feedback handling in MAC-hs. If disabled ACK is allways assumed.
*
* @param ERadParamIndexMacHs_CQI_enable:
*       Enable CQI feedback handling in MAC-hs.
*
* @param ERadParamIndexMacHs_QAM_enable:
*       Enable support for 16-QAM modulation.
*
* @param ERadParamIndexMacHs_CQI_default:
*       Default CQI value used when CQI feedback is disabled, when k = 0 or when CQI has not yet been received.
*
* NOTE: Following ones not in use in WBTS4.0 
* -----> 
*
* @param ERadParamIndexMacHs_FinTFRC_enable:
*       Enable final TFRC selection.
*
* @param ERadParamIndexMacHs_PwrReductEnable:
*       Enable HS-PDSCH power reduction.
*
* <----- 
* NOTE: Previous ones not in use in WBTS4.0
*
* @param ERadParamIndexMacHs_PHsPdschMin:
*       Minimum HS-PDSCH power allocated to a cell 
*
* @param ERadParamIndexMacHs_PHsPdschMax:
*       Maximum HS-PDSCH power allocated to a cell 
*
* @param ERadParamIndexMacHs_PAlfa0:
*       Updating speed of emergency HS-PDSCH power reduction 
*
* @param ERadParamIndexMacHs_PAlfa1:
*       Updating speed of HS-PDSCH power allocation based on total cell power 
*
* @param ERadParamIndexMacHs_PAlfa2:
*       Updating speed of HS-PDSCH power allocation based on total HSDPA power
*
* @param ERadParamIndexMacHs_PMargin0:
*       Power margin for emergency HS-PDSCH power reduction (0.794 = - 1dB)
*
* @param ERadParamIndexMacHs_PMargin1:
*       Power safety margin for HS-PDSCH power allocation based on total cell power (0.631 = -2dB)
* 
* @param ERadParamIndexMacHs_PHsPdschMinCodeMux2:
*       Minimum HS-PDSCH total power of a cell to do code multiplexing for 2 users.
*
* @param ERadParamIndexMacHs_PHsPdschMinCodeMux3:
*       Minimum HS-PDSCH total power of a cell to do code multiplexing for 3 users.
*
* @param ERadParamIndexMacHs_TbsMin:
*       Minimum transport block size for allowing scheduling of a priority queue.
* 
* @param ERadParamIndexMacHs_TbsMax:
*       Maximum sum of transport block sizes per TTI
* 
* @param ERadParamIndexMacHs_SprMax:
*       Maximum amount of spreaders per TTI
* 
* @param ERadParamIndexMacHs_MaxAmount:
*       Not a real R&D -parameter. Used to define the amount of R&D -
*       parameters.
*
* Additional Information : 
*
* Definition Provided by : DSP, MAC-hs
* 
* Remember to put an empty line in the end of each definition file.
* Otherwise the compiler will generate a warning.
***********************************************************************/



