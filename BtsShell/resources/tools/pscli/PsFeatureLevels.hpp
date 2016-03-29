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
#ifndef MAC_FEATURELEVELS_H_
#define MAC_FEATURELEVELS_H_

/**********************************************************************************
*  FEATURE level enum  * description                         * default * default *
*                      *                                     * on/off  * on/off  *
*                      *                                     * HB      * syslog  *
**********************************************************************************/
FID(  FID_LTEMAC_GENERAL,       "000: Avoid using this" ,                                                 Vip , Warning )
FID(  FID_MGMT,                        "General management"    ,                                              Vip , Warning )
FID(  FID_MGMT_STARTUP,          "Management SW startup" ,                                            Vip , Warning )
FID(  FID_MGMT_ROUTING,          "Routing and multiplexing of messages",                          Vip , Warning )
FID(  FID_MGMT_ADDRCONFIG,    "Address configuration",                                                  Vip , Warning )
FID(  FID_MGMT_CELL,                "Cell management"       ,                                                 Vip , Warning )
FID(  FID_MGMT_UE,                   "UE management"         ,                                                 Info , Warning )
FID(  FID_MGMT_RB,                   "RB management"         ,                                                 Vip , Warning )
FID(  FID_IF_ULPHY,                   "Interface between MAC and UL PHY",                                Vip , Warning )
FID(  FID_IF_DL_PS_DATA,         "Internal interface between DL packet scheduler and data",     Vip , Warning )
FID(  FID_DLDATA,                       "DL data general"       ,                                                    Info , Warning )
FID(  FID_DLDATA_BUFFER_STATUS,     "DL data buffer status",                                              Vip , Warning )
FID(  FID_DLDATA_HARQ,          "DL data HARQ",                                                                  Vip , Warning )
FID(  FID_ULDATA,           "UL data general",                                                                        Vip , Warning )
FID(  FID_ULDATA_MAC_BSR,   "UL data MAC BSR",                                                                Vip , Warning )
FID(  FID_ULDATA_BUFFER_STATUS,   "UL data buffer status",                                                Vip , Warning )
FID(  FID_ULRA,             "UL random access",                                                                       Vip , Warning )
FID(  FID_DLPS,             "DL packet scheduler",                                                                    Vip , Warning )
FID(  FID_DLPS_TD,          "DL packet scheduler time domain",                                                Vip , Warning )
FID(  FID_DLPS_FD,          "DL packet scheduler frequency domain",                                         Vip , Warning )
FID(  FID_DLPC,             "DL power control",                                                                         Vip , Warning )
FID(  FID_ULPS,             "UL packet scheduler",                                                                     Vip , Warning )
FID(  FID_ULPS_TD,          "UL packet scheduler time domain",                                                Vip , Warning )
FID(  FID_ULPS_FD,          "UL packet scheduler frequency domain",                                         Vip , Warning )
FID(  FID_ULPC,             "UL power control",                                                                         Vip , Warning )
FID(  FID_DLBBMEAS,         "DL BB measurements",                                                                Vip , Warning )
FID(  FID_MGMT_MESSAGES,    "Trace all messages" ,                                                              Vip , Warning )
FID(  FID_DOPPLER_ESTIMATION,   "Doppler estimation" ,                                                        Vip , Warning )
FID(  FID_DL_MIMOCQI,           "DL CQI MIMO selection" ,                                                        Vip , Warning )
FID(  FID_PDCCH_LA,             "PDCCH link adaptation" ,                                                          Vip , Warning )
FID(  FID_SS_TEST_MODEL,    "SS Test Model" ,                                                                      Vip , Warning )
FID(  FID_RAD_PARAMS,       "RAD Parameters" ,                                                                     Vip , Warning )
FID(  FID_DRX,              "LTE42 DRX and LTE473 Extend DRX" ,                                                Vip , Warning )
FID(  FID_DLHARQ,           "DL Harq" ,                                                                                   Vip , Warning )
FID(  FID_ULHARQ,           "UL Harq" ,                                                                                   Vip , Warning )
FID(  FID_ULPS_PRESCHEDULE, "UL Pre-Schedule" ,                                                                 Vip , Warning )
FID(  FID_DLPS_PRESCHEDULE, "DL Pre-Schedule" ,                                                                 Vip , Warning )
FID(  FID_DLPS_COMMONCHANEL_SRB0, "DL common channel and srb0 schedule" ,                      Vip , Warning )
FID(  FID_PDSCH_LA,         "DL PDSCH Link adaption" ,                                                            Vip , Warning )
FID(  FID_PUSCH_LA,         "DL PUSCH Link adaption" ,                                                            Vip , Warning )
FID(  FID_UL_DUMMY_GRANT,   "UL dummy grant" ,                                                                Vip , Warning )
FID(  FID_ULATB,            "UL ATB" ,                                                                                     Vip , Warning )
FID(  FID_BEAMFORMING,      "Beamforming" ,                                                                       Vip , Warning )
FID(  FID_CQI,              "CQI" ,                                                                                           Vip , Warning )
FID(  FID_TA,               "Time alignment" ,                                                                            Vip , Warning )
FID(  FID_RLF,              "Radio link failure" ,                                                                          Vip , Warning )
FID(  FID_TESTIABLITY,      "Testiablity" ,                                                                              Vip , Warning )
FID(  FID_CAP,              "Capacity and performance" ,                                                             Vip , Warning )
FID(  FID_ULSRS,            "UL SRS" ,                                                                                     Vip , Warning )
FID(  FID_PUSCHHOPPING,     "PUSCH Hopping",                                                                   Vip , Warning )
FID(  FID_ULPS_MEAS,        "UL measurement" ,                                                          Vip , Warning )
FID(  FID_DLPS_MEAS,        "DL measurements" ,                                                                  Vip , Warning )
FID(  FID_PUCCH,            "Uplink control channel" ,                                                                  Vip , Warning )
FID(  FID_PDCCH,            "Downlink control channel" ,                                                                  Vip , Warning )                                                            
FID(  FID_ULPS_POSTSCHEDULE, "UL Post-Schedule" ,                                                                 Vip , Warning )
FID(  FID_ULPS_CHANNELAWARE,        "UL Channel aware" ,                                                   Vip , Warning )
FID(  FID_SUPERCELL,        "Super Cell" ,                                                                 Vip , Warning )
FID(  FID_UL_CONGESTION,    "UL Pusch/Pdcch congestion" ,                                                  Vip , Warning )

#endif  // MAC_FEATURELEVELS_H_
