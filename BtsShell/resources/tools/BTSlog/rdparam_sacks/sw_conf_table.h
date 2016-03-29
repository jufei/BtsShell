/*----------------------------------------------------------------------------
NET                                                    HWRelSW Module document
WCDMA SW







                        SW Configuration table
                        ----------------------



*************************************************************************************************
CONTENTS

   1 INSTRUCTION
   2 USAGE OF SW CONFIGURATION TABLE
     2.1 Flags
     2.2 DBG PRINT SETTINGS
   3 NAMING OF SW CONFIGURATION TABLE
     3.1 Naming of Flags
     3.2 Naming of Prints
   4 LOCATIONS oF SW CONFIGURATION TABLE FILES
   5 RESPONSIBILITY OF SW CONFIGURATION TABLE
   6 FOOTNOTE OF SW CONFIGURATION TABLE
   7 OPEN ISSUES
   8 VERSION HISTORY OF SW CONFIGURATION TABLE INTRUCTIONS


1 INSTRUCTION

        SW runtime functionality configuration via global configuration array and external
        configuration file is useful in SW development phase, when it is not definitely known if
        some SW functionality is, or is not needed (enable/disable), or when some SW
        implementation uses “hard coded” values (e.g. timeout values, max/min limit values…).


2 USAGE OF SW CONFIGURATION TABLE

2.1 Flags

        SW configuration table is used to define start-up-time variation of code. sw_conf_table.h
        defines structure and parameters of the SW configuration table. Default values must be
        define in init_sw_conf_tbl.c file and test-time values will be define in swconfig.txt file.

        swconfig.txt file is stored in the /rom -directory of the BTS unit and this file is read by
        BTS runtime software at startup phase. sw_conf_table.c and init_sw_conf_tbl.h are part of
        BTS SW source code and files are compiled as part of executable BTS runtime binary.

        In sw_conf_table.h file definition must be add in last line before following text
        -> "FEAT_DBG_MaxNumOfFeat".

        Note! Feature parameter must be added to both in enum structure and c string in sw_conf_table.h file.
        Note! When definition must be disable therefore value always must be zero "0" !!

        Warning! Dont't remove any parameters or code lines in sw_conf_table.h file.


2.2 DBG PRINT SETTINGS

        SW configuration table contains R&D parameters that are used to control SW printouts.
        For the dbg_print -call, caller application has to define severity, feature id
        and print text parameters.

            dbg_print(enum MON_SEVERITY severity, enum FEAT_DBG featureId, const char* format, ...)

        For the severity, this file contains four predefined severity level and these severity
        levels have to be used when dbg_print is called. The predefined severity levels are:
            MON_SEVERITY_ERROR,
            MON_SEVERITY_WARNING,
            MON_SEVERITY_INFO,and
            MON_SEVERITY_DEBUG.

        A featureId parameter contains feature flag information and this flag must be defined in
        this file.  This information is used to control DEBUG level dbg_print printouts.
        For common use of dbg_print is defined common featur flag FEAT_DBG_Generic. Anyhow it's
        recommented that applications defines own feature, system component or subsystem specifics
        flags and this feature flag is used in dbg_prints. By changing value of this feature flag
        user can control DEBUG level prints and get just those prints what are waiting.

        FEAT_DBG_PrintFilter prarameter control dbg_prints. FEAT_DBG_PrintFilter property
        has four predefined operation level:
            0 - NONE            no printouts
            1 - RAM disk,       INFO, WARNING and ERROR severity level printouts into RAM disk
                                (startup log & crashdump log)
            2 - RAM disk & UDP, same as previous but also to UDP printouts
            3 - RAM disk & UDP, same as previous but DEBUG severity printouts (depending on selected
                                feature) also included

        By changing FEAT_DBG_PrintFilter parameter value user can control printouts. When level 3
        is selected also feature flag value is notified and user get more detailled filtering for
        DEBUG level printouts.

        In sw_conf_table.h file definition must be add in last line before following text
        -> "FEAT_DBG_MaxNumOfFeat".

        Note! Print parameter must be added to both in enum structure and c string in sw_conf_table.h file.
        Note! When definition must be disable therefore value always must be zero "0" !!

        Warning! Dont't remove any parameters or code lines in sw_conf_table.h file.


3 NAMING OF SW CONFIGURATION TABLE:


3.1 Naming of Flags

        Following table describes flags naming of SW Configuration table:

        ********************************************************
        * Template       * FEAT_DBG_<SC>_<Feature>_<Optional>  *
        *----------------*-------------------------------------*
        * <SC>           * Name of System component            *
        *----------------*-------------------------------------*
        * <Feature>      * Name of Definition (Name of Feature)*
        *----------------*-------------------------------------*
        * <Optional>     * Optional naming                     *
        ********************************************************
        Example -> FEAT_DBG_BTSOM_ARIO

        Note! Remember note on a revision history what you have done to file!


3.2 Naming of Prints

        Following table describes flags naming of SW Configuration table:

        ************************************************************
        * Template       * FEAT_DBG_<SC>_<Feature>_<Optional>_PRN  *
        *----------------*-----------------------------------------*
        * <SC>           * Name of System component                *
        *----------------*-----------------------------------------*
        * <Feature>      * Name of Definition (Name of Feature)    *
        *----------------*-----------------------------------------*
        * <Optional>     * Optional naming                         *
        ************************************************************
        Example -> FEAT_DBG_BTSOM_AUTH_PRN,

        Note! Remember note on a revision history what you have done to file!


4 LOCATIONS oF SW CONFIGURATION TABLE FILES

        sw_conf_table.h and init_sw_conf_tbl.c files stores following worksets in PVCS Dimensions:

        - sw_conf_table.h -> WCDMA:HELENA_HWREL_W/src/API/MISC

        - init_sw_conf_tbl.c -> WCDMA:WN_OAM_LIBS_WS/OAM/Include_Path/swconfig


5 RESPONSIBILITY OF SW CONFIGURATION TABLE

        Principal responsibility of SW configuration table is in O&M (SCM person who is
        connections in O&M architecture team and HWrel team).


6 FOOTNOTE OF SW CONFIGURATION TABLE

        - More information usage of SW configuration table finds in PI:
           PI link: http://esdoc04nok.ntc.nokia.com/urn.htm?document_id=13-140373&version=current&id=09006c37801be6d9&DMW_DOCBASE=espoo11
           PI path: Projects/WCDMA RAN/WCDMA BTS Releases/Specification Documents/SCFS/HWRel
                 -> HELENA_SW_HWAPI_R&D_SUPPORT_SPEC

        - Another file which includes information usage of dbg_prints (note! this is draft version)
           PVCS Dimension: WCDMA:HELENA_SW_DOCS_WS -> WCDMA BTS O&M SW monitoring by logging utility


7 OPEN ISSUES

        - How to remove parameters in sw_conf_table.h file?


8 VERSION HISTORY OF SW CONFIGURATION TABLE INTRUCTIONS

        17.01.2005/Juhervas/KaarloKeskitalo  First draft.
        19.01.2005/Juhervas                  Accepted version. Made corrections after comments.

*************************************************************************************************



PVCS Product           : WCDMA

Base database          : HELENA

Design Part            : WCDMA:HWREL
Development Workset    : WCDMA:HELENA_HWREL_WS

Filename               : src\API\MISC\sw_conf_table.h

Date                   : 06-FEB-2007 14:49:42

Item Specification     : WCDMA:A5869.A-SRC

Author                 : SPORSPAK

Version                : wn#0.0.246

Status                 : DRAFT



Revision history:

VERSION DATE/AUTHORS    COMMENT

0.0.246 06.02.2007/Seppo Porspakka	Modified ethernet service mirroring parameter names. Also merge from wn_ccs branch.
0.0.245 02.02.2007/Jukka Pehkonen	Added FEAT_DBG_BTSOM_TrialPeriodTime
0.0.244 26.01.2007/Esa Kemppainen	Added FEAT_DBG_BTSOM_ALMAG_Device_Detection_Timer
0.0.243 19.12.2006/Teppo Kotikagas  Added FEAT_DBG_BTSOM_PMFreezingDisabled
0.0.242 15.12.2006/Pekka Laasonen	Added FEAT_DBG_NO_WID_CHECK
0.0.241 14.12.2006/Marko Salonpää	Added FEAT_DBG_BBTraceMaxFileSize and FEAT_DBG_HWAPI_BB_TRACE_PRN
0.0.240 13.12.2006/Mika Koivisto	Added FEAT_DBG_BTSOM_Test_Enable_Big_successLimitPromille
0.0.239 OBSOLETE
0.0.238 08.12.2006/Mika Koivisto	Added FEAT_DBG_BTSOM_Test_Set_EthTestReceivePriority,
	                                FEAT_DBG_BTSOM_Test_Set_EthTestSendPriority and FEAT_BTSOM_DBG_Test_EthernetTestPrint.
0.0.237 22.11.2006/Mikko Holappa	Added FEAT_DBG_ETH_FSPB_MIRROR_SRC_FARADAY1, FEAT_DBG_ETH_FSPB_MIRROR_SRC_FARADAY2, FEAT_DBG_ETH_FSPB_MIRROR_SRC_FARADAY3
    					FEAT_DBG_ETH_FSPB_MIRROR_SRC_FARADAY4, FEAT_DBG_ETH_FSPB_MIRROR_SRC_FARADAY5, FEAT_DBG_ETH_FSPB_MIRROR_SRC_FARADAY6
						FEAT_DBG_ETH_FSPB_MIRROR_SRC_FARADAY7, FEAT_DBG_ETH_FSPB_MIRROR_SRC_RP2, FEAT_DBG_ETH_FSPB_MIRROR_SRC_EMP
    					FEAT_DBG_ETH_FSPB_MIRROR_SRC_MCU, FEAT_DBG_ETH_FSPB_MIRROR_INGRESS_DST_PORT, FEAT_DBG_ETH_FSPB_MIRROR_EGRESS_DST_PORT
    					FEAT_DBG_BTSOMStub, FEAT_DBG_BTSOMStub_AmountOfFaradays, FEAT_DBG_BTSOMStub_TupFaradayId
0.0.236 30.10.2006/Pasi Kotaniemi	Added FEAT_DBG_BTSOM_GAIN_PRN
0.0.235 23.10.2006/Saija Sipola     Added FEAT_DBG_BTSOM_Site_Reset_Allowed
0.0.234 23.10.2006/Santtu Pousi 	Added FEAT_DBG_Test_AntennaLineTestEnabled.  This enables Antenna Line Test in Cabinet and Site Tests.
0.0.233 19.10.2006/Liisa Kostamo	Added FEAT_DBG_BTSMOM_ALMAG_ALSupervisionTimer for AL communication test polling timer 
0.0.232 13.10.2006/Teppo Kotikangas	Added FEAT_DBG_BOOTCORESWDL_ENABLED
0.0.231 14.09.2006/Sirpa Salmela	Added 	FEAT_DBG_BTSOM_ALMAG_VSWR_Threshold_Timer for increment 6
0.0.230 13.09.2006/Mani Bhowmik		Added FEAT_DBG_DisableFanControl and FEAT_DBG_DisableTempTrace
0.0.229 07.09.2006/Jari-Pekka Tuikka	Added FEAT_DBG_DisableFTMReadyCheck
0.0.228 07.09.2006/Teppo Kotikangas	Added FEAT_DBG_ForceDspDump
0.0.227 05.09.2006/H.Koskela		Added FEAT_DBG_HWAPI_Illuminator_Port
0.0.226 24.08.2006/Esa Kemppainen	Added FEAT_DBG_Conf_LicensePollingTimer and FEAT_DBG_Conf_LicenseFeatureDisabled
0.0.225 18.08.2006/Marko Salonpää	Added FEAT_DBG_Test_Enable_TxRxOptimization and FEAT_DBG_Test_Enable_FspDspOptimization
0.0.224 14.08.2006/Marko Petäjäjärvi	Added FEAT_DBG_FRresetDelayTimer. If it is not set (=0) default 6 sec timer is used for FR reset delay.
0.0.223 27.06.2006/Jouni Broman		Added FEAT_DBG_SET_FSM_MODE
0.0.222 12.06.2006/Tommi Keski-Korsu	Added FEAT_DBG_TechRep_FD_Trap_Log_Trigger(s)
0.0.221 20.03.2006/Jukka Pehkonen	Added FEAT_DBG_BTSOM_EnableAllFeatures.
0.0.220 02.03.2006/Santtu Pousi		Added FEAT_DBG_Test_Enable_MasteLoopGetAntennaHWInfoFromBBC. 
									Changed FEAT_DBG_Test_Disable_CabinetTest_Feature to FEAT_DBG_Test_Enable_CabinetTest_Feature.
0.0.219 20.02.2006/Santtu Pousi		Added FEAT_DBG_Test_CabinetTest_Print and FEAT_DBG_Test_Disable_CabinetTest_Feature for Cabinet and Site Tests
									and FEAT_DBG_TechRep_MT_SCT_Enabled for TechRep
0.0.218 18.02.2006/Mani Bhowmik		Added FEAT_DBG_CLIC_MINUTE_COUNTER and FEAT_DBG_CLIC_HOUR_COUNTER
0.0.217 17.02.2006/Jouni Broman		Added FEAT_DBG_BTSOM_ISTI_Timer_Divider for testing purposes
0.0.216 15.02.2006/Keijo Hyttinen	Added FEAT_DBG_BTSOM_Disable_Channel_Validation
0.0.215 14.02.2006/T.Väyrynen	Added FEAT_DBG_Disable_ScfFromFlash
0.0.214 08.02.2006/J.Kemppainen	Added FEAT_DBG_ProdTest_TXDigitalGain and changed FEAT_CLIC_FIXED_FAN_SPEED to
								FEAT_DBG_CLIC_FIXED_FAN_SPEED
0.0.213 02.02.2006/JHKarppinen	Added FEAT_DBG_HWAPI_INSPAP_UL_DELAY and FEAT_DBG_HWAPI_INSPAP_DL_DELAY for testing purposes only
0.0.212	30.01.2006/J.Korhonen	Added FEAT_CLIC_FIXED_FAN_SPEED.
0.0.211 27.01.2006/P.Reijonen	FEAT_DBG_HeapTracePID added again, for bs_heap PID monitoring feature.
0.0.210 27.01.2006/P.Reijonen	Added new flag FEAT_DBG_HeapTracePID, for bs_heap monitoring.
0.0.209 27.01.2006/M.Koivisto	Added new flag FEAT_DBG_Test_Enable_MasteLoop_print,
								FEAT_DBG_Test_Enable_MasteLoop_Log_files,
								FEAT_DBG_Test_MasteLoopIsBranchDualMode,
								FEAT_DBG_Test_Disable_MasteLoop_Feature,
0.0.208 24.01.2006/JMoberg		Changed the print appearances: "BTSOM_HWAPI_IF_PRN" -> "HWAPI_IF" and "BTSOM_DSP_IF"-> "DSP_IF"
0.0.207 19.01.2006/heikkiha		Added FEAT_DBG_Disable_Tup
0.0.206 16.01.2006/E.Kemppainen Added FEAT_DBG_Disp_PRN, FEAT_DBG_Led_PRN and FEAT_DBG_UhndSD_PRN
0.0.205 29.12.2005/M.Lantto     Added FEAT_DBG_BTSOM_EAC_PRN
0.0.204 16.12.2005/M.Salonpää   Added FEAT_DBG_BTSOM_TEST_PRN, FEAT_DBG_BTSOM_LOOPTEST_PRN and FEAT_DBG_BTSOM_LOOPTEST_DETAIL_PRN
0.0.203 09.12.2005/P.Laasonen   Added FEAT_DBG_ACNF for ACNF debug prints
0.0.202 08.12.2005/H.Mikkonen   Added FEAT_DBG_BTSOM_ENABLE_CLOCK_TUNING.
0.0.201 02.12.2005/PeHe         Shortened common print labels ("WARN", "I", "D") and TCOM print switches due to PR 21913ES08P,
                                added FEAT_DBG_TCOM_TcomPerfTrace
0.0.200 22.11.2005/SPo          Added Ethernet traffic monitoring features. 
0.0.199 21.11.2005/H.Mikkonen	Added FEAT_DBG_CLOCK_PRN.
0.0.198 16.11.2005/TeK			Added FEAT_DBG_DBDumpObjCounter and FEAT_DBG_DatabaseDumpTimer (pronto 20158ES09P)
0.0.197 14.11.2005/ATo          Changed comment for FEAT_DBG_PoolObs
0.0.196 08.11.2005/MPet			Added FEAT_DBG_SetCellIdIsLcrId. This is for Production test purposes due O&M generates initial cellId values. 
0.0.195 27.10.2005/TeK			Added FEAT_DBG_EthRecoResetDisabled
0.0.194 25.10.2005/SPo          Added FEAT_DBG_HWAPI_ETH_SERVICE.
0.0.193 25.10.2005/M.Pelttari	Added FEAT_DBG_BTSOM_SNTPCheckPeriod,FEAT_DBG_BTSOM_LicenceCheckPeriod,FEAT_DBG_LBA_FeatureCheckPeriod
0.0.192 19.10.2005/J.H. Karppinen Added FEAT_DBG_HWAPI_MODULE_TYPE
0.0.191 11.10.2005/V-M.Runtti   Added FEAT_DBG_HWAPI_HW_CTRL_SERVICE
0.0.190 3.10.2005/J. Moberg   Added FEAT_DBG_BTSOM_DSP_IF_PRN.
0.0.189 30.09.2005/V-M.Runtti   Added FEAT_DBG_SwRecoveryTimeout
0.0.188 29.09.2005/JuhErvas	Changed FEAT_DBG_BTSOM_SPMAG name to SPMAG inside DBG_FEATURE_STRING
0.0.187 29.09.2005/Liisa Kostamo  Added   FEAT_DBG_BTSOM_ALMAG  for ALMAG_Pkg.sbs prints       
0.0.186 22.09.2005/mivaaral     Added   FEAT_DBG_Test_EthernetTestEnabled, FEAT_DBG_Test_Ethernet_poll_waitTimeout,       
                                        FEAT_DBG_Test_EthernetTest_MT_SCT_Enabled and FEAT_DBG_Test_EthernetTestAdvancedInfoEnabled
0.0.185 13.09.2005/Riitkera     Added   FEAT_DBG_BTSOM_SPMAG_PRN 
0.0.184 01.09.2005/TTuovine     Added   FEAT_DBG_BTSOM_FUM_PRN, FEAT_DBG_BTSOM_FSM_Creator_PRN
0.0.183 31.08.2005/M.Koivisto Changed FEAT_DBG_Test_Disable_Loop_parameter_read_from_dbw 
                                --> FEAT_DBG_Test_Enable_Loop_parameter_read_from_dbw
0.0.182 30.08.2005/Juhervas  Corrected comment to FEAT_DBG_Test_Disable_Loop_parameter_read_from_dbw 
0.0.181 29.08.2005/M.Koivisto FEAT_DBG_testChannelTxPowerTestKnife,
                              FEAT_DBG_Test_Disable_Loop_parameter_read_from_dbw
0.0.180 24.08.2005/P.Kotaniemi Added FEAT_DBG_BTSOM_HWAPI_IF_PRN
0.0.179 23.08.2005/J.Mattila Added FEAT_DBG_HWAPI_TraceBufferEmptyInterval and FEAT_DBG_HWAPI_TraceBufferPacketSize.
                             Also corrected previous feature addition FEAT_DBG_TCOM_TLH.  
0.0.178 12.08.2005/MKJ       Added FEAT_DBG_TCOM_TLH.
0.0.177 26.07.2005/V.Erkkilä Added FEAT_DBG_BTSOM_WSMB_Read
0.0.176 15.06.2005/P.Moisio Added FEAT_DBG_Prof... parameters for Function Execution Logger
0.0.175 15.06.2005/T.Kotikangas CN2415: added FEAT_DBG_DspDumpCpu
0.0.174 09.06.2005/P.Rimpilainen Added FEAT_DBG_StupFDEnabled
0.0.173 07.06.2005/M.Pelttari Added FEAT_DBG_BTSOM_OPT_PRN,FEAT_DBG_BTSOM_Disable_Licence_Validation,FEAT_DBG_BTSOM_OPT_Enabled
0.0.172 31.05.2005/MHo       Added FEAT_DBG_PoolObs_Status
0.0.171 30.05.2005/J.Mattila Added FEAT_DBG_HWAPI_TraceBufferMaxSize
0.0.170 27.05.2005/P.Seppänen Added FEAT_DBG_DspTraceMaxTime, FEAT_DBG_DspTraceMinTime, FEAT_DBG_DspTraceMaxFileSize
0.0.169 13.05.2005/tovayryn  Added FEAT_DBG_EnableHeapMonitoring
0.0.168 12.05.2005/MaMe      Added FEAT_DBG_Enable_DbgPrint_to_BtsLog_PRN
0.0.167 12.05.2005/J.Moberg Added FEAT_DBG_BTSOM_BBC_MANUAL_CONF_PRN.
0.0.166 10.05.2005/M.Kallio Added FEAT_DBG_BTSCommissioned, FEAT_DBG_NoRFModules, FEAT_DBG_NoFilters and FEAT_DBG_NumberOfFSP
0.0.165 19.04.2005/H.Lantto Added FEAT_DBG_BTSOM_FDRules_Distr
0.0.164 12.04.2005/J.Moberg Added FEAT_DBG_BTSOM_BBC
0.0.163 12.04.2005/J.Mattila Added FEAT_DBG_UdpPrintAddress
0.0.162 06.04.2005/L.Eilola Added FEAT_DBG_Tune_FreqHistory_PRN and a comment for FEAT_DBG_Tune
0.0.161 06.04.2005/P.Säily  Added FEAT_DBG_PU_DWI_Enabled
0.0.160 01.04.2005/L.Kostamo  Added FEAT_DBG_PM
0.0.159 15.03.2005/P.Säily  Added FEAT_DBG_PU_DWI_PRN, FEAT_DBG_PU_TESTIFAPPL_PRN
0.0.158 10.03.2005/NPu  Added FEAT_DBG_HWAPI_ApiSumService and FEAT_DBG_HWAPI_ApiSumServiceTestMessages
0.0.157 25.02.2005/R.Juntunen Changed comment for flag FEAT_DBG_BTSOM_DUAL_BAND_SUPPORT (0=disabled)
0.0.156 24.02.2005/R.Juntunen Added flag FEAT_DBG_BTSOM_DUAL_BAND_SUPPORT
0.0.155 22.02.2005/A.Pulkkinen Changed flag FEAT_DBG_BTSOM_Enable_SoapTraceToRom to FEAT_DBG_BTSOM_Enable_SoapTrace.
                               Changed flag FEAT_DBG_BTSOM_Enable_SoapTraceToRam to FEAT_DBG_BTSOM_Enable_AlTrace.
                               Added flags FEAT_DBG_BTSOM_NbrOfOldAPWMessages and FEAT_DBG_BTSOM_APWTraceFileStoringPlace
0.0.154 18.02.2005/J. Broman Added FEAT_DBG_BTSOM_MTTester_PRN
0.0.153 07.02.2005/PeHe Added FEAT_DBG_TCOM_SdlStallInterval, _SdlStallLengt, _RlMeasTrashTreshold, 
                        _SirMeasTrashTreshold, _CmeasPrio, _DmeasPrio, _CommitCfnSfn
0.0.152 03.02.2005/HaH Added FEAT_DBG_HWAPIResetService
0.0.151 28.01.2005/jaakvanh Added FEAT_DBG_HWAPI_CASA2
0.0.150 26.01.2005/J.H.Karppinen Added FEAT_DBG_HWAPI_OIC
0.0.149 25.01.2005/A.Pulkkinen Compile errors corrected
0.0.148 25.01.2005/A.Pulkkinen Added FEAT_DBG_BTSOM_Enable_SoapTraceToRom, FEAT_DBG_BTSOM_Enable_SoapTraceToRam and
                               FEAT_DBG_BTSOM_APW
0.0.147 20.01.2005/L.Kostamo added FEAT_DBG_SWMAG for SWMAG debug prints
0.0.146 19.01.2005/H.Lantto Added FEAT_DBG_EnableAlarmReporting
0.0.145 19.01.2005/Juhervas Added SW Configuration table instruction
0.0.144 13.01.2005/A.Keränen added FEAT_DBG_ADSER
0.0.143 05.01.2005/HaH Added FEAT_DBG_HWAPI_UDPCP_Stat_Print
0.0.142 23.11.2004/J.Moberg Added FEAT_DBG_Rpmag.
0.0.141 11.11.2004/M.Pelttari Added FEAT_DBG_BTSOM_AUTH_PRN, FEAT_DBG_AUTH_DISABLED
0.0.140 04.11.2004/MaMe FEAT_DBG_Disable_HSDPA_* replaced with FEAT_DBG_Disable_RadParam_*
0.0.139 03.11.2004/MaMe Added FEAT_DBG_Disable_HSDPA_Hwapi, FEAT_DBG_Disable_HSDPA_Telecom,
                        FEAT_DBG_Disable_HSDPA_Tup, FEAT_DBG_Disable_HSDPA_DspCodec,
                        FEAT_DBG_Disable_HSDPA_DspRake, FEAT_DBG_Disable_HSDPA_DspMachs and
                        FEAT_DBG_Disable_HSDPA_ALL_SC
0.0.138 02.11.2004/pseppanen Changed FEAT_DBG_EnableDbLogistic to FEAT_DBG_EnableDbStatistics
0.0.137 01.11.2004/juhervas Added FEAT_DBG_BTSOM_ARIO
0.0.136 28.10.2004/pseppanen Added FEAT_DBG_EnableDbLogistic
0.0.135 15.10.2004/jtaskin Added FEAT_DBG_AutoTestDedicatedState
0.0.134 14.10.2004/hekomula  Added FEAT_DBG_Disable_MO_WAM_Change
0.0.133 01.10.2004/HaH Added FEAT_DBG_NMAP_GW, FEAT_DBG_UDPCP, FEAT_DBG_UDPCP_RX and
                       FEAT_DBG_UDPCP_TX
0.0.132 24.09.2004/InJu FEAT_DBG_NoRampDown_OnCellDelete
0.0.131 02.09.2004/sjuvani FEAT_DBG_BPF_CRC_DECOMPRESS_DISABLE
0.0.130 24.08.2004/InJu Added FEAT_DBG_WsmaRxDelay_Triple
0.0.127 28.07.2004/NPu Added FEAT_DBG_HWAPI_ApiTesterInterface and FEAT_DBG_HWAPI_ApiBtsLog
0.0.126 21.06.2004/Sathirve Added FEAT_DBG_Para
0.0.125 16.06.2004/InJu Appended "_Other" to WSMB RT/RR delays, i.e.
            FEAT_DBG_WsmbRt_del1_wtra_Other,FEAT_DBG_WsmbRt_del1_wtrb_Other,
            FEAT_DBG_WsmbRt_del2_wtra_Other,FEAT_DBG_WsmbRt_del2_wtrb_Other,
                FEAT_DBG_WsmbRr_del1_wtra_Other,FEAT_DBG_WsmbRr_del1_wtrb_Other,
            FEAT_DBG_WsmbRr_del2_wtra_Other,FEAT_DBG_WsmbRr_del2_wtrb_Other,
            Added:
            FEAT_DBG_WsmbRt_del1_wtra_Triple,FEAT_DBG_WsmbRt_del1_wtrb_Triple,
            FEAT_DBG_WsmbRt_del2_wtra_Triple,FEAT_DBG_WsmbRt_del2_wtrb_Triple,
            FEAT_DBG_WsmbRr_del1_wtra_Triple,FEAT_DBG_WsmbRr_del1_wtrb_Triple,
            FEAT_DBG_WsmbRr_del2_wtra_Triple,FEAT_DBG_WsmbRr_del2_wtrb_Triple
0.0.124    15.06.2004/AnKu FEAT_DBG_PoolObs inserter for Pool Observer
0.0.123    03.06.2004/HaLa FEAT_DBG_RAR_Reset_tm and 3600 and FEAT_DBG_RAR_Reset_cnt added for OAM/ROUT.
0.0.122    26.05.2004/PeHe Added for TCOM prints FEAT_DBG_TCOM_SDL_*, FEAT_DBG_TCOM_AtmCap,
                        FEAT_DBG_TCOM_DMEAS and FEAT_DBG_TCOM_CMEAS
0.0.121    20.05.2004/MPelttari    Added WTRD specific WSM delay definitions
0.0.120 24.03.2004/Sathirve  Added     FEAT_DBG_LCS_RTT_CABLE_NOMINAL_FEEDER_LOSS and FEAT_DBG_LCS_RTT_CABLE_NOMINAL_DELAY
0.0.117 23.03.2004/VMR  Added FEAT_DBG_CPULoadMon, FEAT_DBG_EthDestroyPrints,
                        FEAT_DBG_EthDestroyLocalIpAddr, FEAT_DBG_EthDestroyRemoteIpAddr,
                        FEAT_DBG_EthDestroyRxCount and FEAT_DBG_EthDestroyTxCount.
                        FEAT_DBG_LCS_RTT_CABLE_xxx defintions are missing from this
                        version.
0.0.116 09.03.2004/HTK  Commented out SW_CONF_TABLE on last line
0.0.115 19.01.2004/TaTu Added FEAT_DBG_'s for WSMA/B delay blocks, USED ALSO FOR WN21#
0.0.114 08.01.2004/tovayryn    Added FEAT_DBG_CdmaLoopTestKnife
0.0.113 28.11.2003/VMR    Added FEAT_DBG_TCP_RetransmissionCnt
0.0.112 07.11.2003/JyPu Added FEAT_DBG_HOresult_denied
0.0.111 04.11.2003/JaTP    Added FEAT_DBG_FlashStatMon
0.0.110 23.10.2003/JaTP    Added FEAT_DBG_CopyPMLogToWam
0.0.109 17.10.2003/HiMa    Added FEAT_DBG_STACK_INCREASE
0.0.108 06.08.2003/HiMa    Corrected typo, "\" was missing.
0.0.107    30.07.2003/VE   Added FEAT_DBG_WSMB_LED_control
0.0.106 27.06.2003/KoJe Added Added LCS delay definitions.
0.0.105 19.05.2003/VMR  Added FEAT_DBG_HWAPI_HWCTRL, FEAT_DBG_HWAPI_CFT,
                        FEAT_DBG_HWAPI_GPS, and FEAT_DBG_R_D_IPAddr.
0.0.104 17.04.2003/TeK Added FEAT_DBG_TechRep
0.0.103 11.04.2003/JiP Added FEAT_DBG_DisableRuntimeLog
0.0.102 07.04.2003/HaLa Added FEAT_DBG_TestDedicated
0.0.101    04.04.2003/VMR  Added FEAT_DBG_R_D_CurrentBoard
0.0.100 21.03.2003/J.Korhonen Added FEAT_DBG_POST_FAILURE
0.0.99    18.03.2003/SaBu Added FEAT_DBG_FORE_SM and FEAT_DBG_BLOC
0.0.98    12.02.2003/HiMa Added FEAT_DBG_HWInq
0.0.97    12.02.2003/J.Korhonen added FEAT_DBG_LCS
0.0.96    04.02.2003/tevaisan Added FEAT_DBG_Intelligent_Shutdown
0.0.94    30.01.2003/tovayryn Added FEAT_DBG_Disable_DSP_Loading
0.0.93    21.01.2003/InJu    sw_conf_table moved to extern "C" section (same as wn20#1.2)
0.0.92    20.01.2003/PeJ  Added FEAT_DBG_WSPC_SFNPoll_WD_disable
0.0.91    16.01.2003/S. Ojalehto Added FEAT_DBG_Widm.
0.0.90    12.12.2002/tovayryn    Added FEAT_DBG_Swmg.
0.0.89    4.12.2002/HiMa    Fixed DBG_FEATURE_STRING, missing comma.
0.0.88    3.12.2002/AHe   Added FEAT_DBG_ATM_FP
0.0.87    29.11.2002/HiMa    Added all differences from wn20# branch:
                    wn20#1.8 11.10.2002/PeJ  Added FEAT_DBG_HWAPI_POLL and fixed DBG_FEATURE_STRING
                                last value missing
                    wn20#1.5 20.11.2002/S. Ojalehto  Added FEAT_DBG_HWInfo_Timer
                    wn20#1.4 13.11.2002/Tovayryn Added FEAT_DBG_ignore_wspc_vers_check
                    wn20#1.3 22.10.2002/Tovayryn Changed FEAT_DBG_WspcProto to FEAT_DBG_overruled_wsp_type
                    wn20#1.2 21.10.2002/InJu Added FEAT_DBG_WSMB_Init_Dump
                                sw_conf_table moved to extern "C" block
                    wn20#1     25.09.2002/Tovayryn Added FEAT_DBG_WspcProto
0.0.86  26.11.2002/VMR  Added FEAT_DBG_RTM_disable, FEAT_DBG_RTM_NRT_retry_count,
                        FEAT_DBG_RTM_NRT_timeout_ms and FEAT_DBG_RTM_prints for CD53
0.0.85    25.11.2002/HiMa    Fixed DBG_FEATURE_STRING last value missing
0.0.84  20.11.2002/Utervone Added FEAT_DBG_WTRStartUpDelay_Timer
0.0.83  20.11.2002/S. Ojalehto  Added FEAT_DBG_HWInfo_Timer
0.0.82  11.11.2002/PeHe Added FEAT_DBG_TCOM_*
0.0.81  02.10.2002/JaTP Added FEAT_DBG_HWAPI_PCI
0.0.80  20.08.2002/TeHo Added FEAT_DBG_IubTrace
0.0.79  09.07.2002/RisJuntu Added FEAT_DBG_Excess
0.0.78  01.07.2002/Tovayryn Added FEAT_DBG_Disable_TurboReset
0.0.77  21.06.2002/MaMe Changed comment of FEAT_DBG_DB_Change_Log
0.0.76  18.06.2002/VMR  Added FEAT_DBG_HeapStatusPolling,
                        FEAT_DBG_HeapMaxFreeLimit and FEAT_DBG_HeapMaxBlockLimit
0.0.75  05.06.2002/hekomula Added FEAT_DBG_Disable_WsmCfg
0.0.73  31.05.2002/TiSi Added FEAT_DBG_SWBUS_crc
0.0.72  15.05.2002/Tovayryn  Added FEAT_DBG_SWBPollTimeout
0.0.72  15.05.2002/SOJ  Added FEAT_DBG_IGNORE_CRCsof_SCF_HWF
0.0.71  14.05.2002/OJAR Added FEAT_DBG_API_Tcp_Echo_Server and FEAT_DBG_API_Udp_Echo_Server
0.0.70  03.05.2002/PeJ  Added FEAT_DBG_HWAPI_COMMON
0.0.69  03.05.2002/PeJ  Added FEAT_DBG_HWAPI_BIST and FEAT_DBG_HWAPI_SELF_TEST
0.0.68  30.04.2002/VMR  Added FEAT_DBG_HWAPI_HEAP and FEAT_DBG_LogHeapReset
0.0.67  30.04.2002/Hekomula  Added FEAT_DBG_Disable_Code_Tracking
0.0.66  17.04.2002/Hekomula  Added FEAT_DBG_Unit_Tests_Without_WPAs
0.0.65  16.04.2002/VMR  Added FEAT_DBG_Disable_OAM_to_TASSU and FEAT_DBG_Disable_TCOM_to_TASSU
0.0.64  09.04.2002/VMR  Added FEAT_DBG_print_flow_high and FEAT_DBG_print_flow_low
0.0.63  27.03.2002/TiSi Added FEAT_DBG_SWB_dblk_burstlen and
                        FEAT_DBG_SWB_dblk_burstdelay
0.0.62  26.03.2002/VMR  Added FEAT_DBG_HWAPI_RP_RAM_Prints ... FEAT_DBG_HWAPI_ID_string_Prints
0.0.61  26.03.2002/PeJ  Added FEAT_DBG_HWAPI_TassuRouter ... FEAT_DBG_HWAPI_AUTO_DET
0.0.60  18.03.2002/ToVayryn Added FEAT_DBG_Disable_ATM_MUX
0.0.59  15.03.2002/PeJ  Added FEAT_DBG_TassuMonMode ... FEAT_DBG_TassuMon4
0.0.58  22.02.2002/TeHo Added SuperVisionInterval, maxTimeoutCounter and FEAT_DBG_HGW
0.0.57  20.02.2002/VMR  Changed meaning of FEAT_DBG_FaultDiagnostics according to EPi
0.0.56  20.02.2002/SJO  Added FEAT_DBG_Stup
0.0.55  18.02.2002/InJu Added FEAT_DBG_AxuPollingDisabled
0.0.54  13.02.2002/JaPu Added FEAT_DBG_SNTP
0.0.53  13.02.2002/RISJUNTU Added   FEAT_DBG_Disable_WTR_Alarms,FEAT_DBG_Disable_DSP_Alarms and FEAT_DBG_Disable_ATM_Alarms
0.0.52                  ACCEPTED
0.0.51  07.02.2002/SJO  Added FEAT_DBG_Conf
0.0.50  03.02.2002/InJu Added FEAT_DBG_AxuReconfigurationTime
0.0.49  29.01.2002/VMR  Changed meaning of FEAT_DBG_UdpPrintPort
0.0.48  25.01.2002/TeK  Added comments to FEAT_DBG_FTP_Tester.
0.0.47  25.01.2002/TeK  Added FEAT_DBG_FTP_Tester and FEAT_DBG_FTP_ADDRESS
0.0.46  24.01.2002/SJO  Changed the meaning of FEAT_DBG_STUP_RESET: 0 DO RESET, 1 DO NOT RESET
0.0.45  17.01.2002/SJO  Added FEAT_DBG_STUP_RESET to make on Master WAM reset of all other active units
0.0.44  17.01.2002/TiLe Added FEAT_DBG_Rhapsody_output.
0.0.43  10.01.2002/SJO  Added FEAT_DBG_Fldb
0.0.43  03.01.2002/TeK  Removed word "enum" from version 0.0.39 comments. It caused
                        that BSconf.exe could not load the file.
0.0.42  03.01.2002/TeK  Added FEAT_DBG_Tune_Averages and added some comments to FEAT_DBG_Tune
0.0.41  03.01.2002/JoB  Added FEAT_DBG_DB_Change_Log
0.0.40  18.12.2001/VMR  Added FEAT_DBG_DisableConfChangeToTCom to DBG_FEATURE_STRING too
0.0.39  18.12.2001/VMR  Fixed FEAT_DBG definition and added FEAT_DBG_FixedFanSpeed
                        to DBG_FEATURE_STRING too
0.0.38  18.12.2001/TiLe Added FEAT_DBG_FixedFanSpeed
0.0.37  17.12.2001/LiJu Added FEAT_DBG_DisableConfChangeToTCom
0.0.36  16.12.2001/VMR  Added FEAT_DBG_SWBUS_monitor and updated some comments
0.0.35  13.12.2001/SJO  Added FEAT_DBG_OMIT_OWEN_UPWARMING to indicate if upwarming time shall be omited
0.0.34  05.12.2001/SJO  Added FEAT_DBG_DUAL_CARRIER to indicate if there is "dual carrier" situation
0.0.33  05.12.2001/SJO  Removed FEAT_DBG_UPDATEVERSIONofWSMA because FEAT_DBG_I2C_WSMA_update indicates the same thing
0.0.32  04.12 2002/TeHo Added FEAT_DBG_AntennaLoss
0.0.31  04.12.2001/SJO  Added FEAT_DBG_UPDATEVERSIONofWSMA to indicate if updated version of WSMA is in use or not
0.0.30  27.11.2001/VMR  Changed enum MON_SEVERITY values, added enum PRINT_FILTER and
                        changed FEAT_DBG_PrintFilter meaning, added FEAT_DBG_Heap_Walking
0.0.29  23.11.2001/VMR  Added FEAT_DBG_print_task_pri
0.0.28  16.11.2001/MPet Added time out flag for CONF to wait all unit info is in Db. Default 3mins.
0.0.27  16.11.2001/TeNi Added FEAT_DBG_filter_all_but_EAC_alarms
0.0.26  15.11.2001/TeHo Added FEAT_DBG_DISABLE_NAT_ENTRIES
0.0.25  15.11.2001/VMR  Added FEAT_DBG_Performance_Monitoring and PerfMonitRegister,
                        PerfMonitStart and PerfMonitStop function prototypes
0.0.24  12.11.2001/MPet Update flag descriptions.
0.0.23  09.11.2001/VMR  Changed meaning of FEAT_DBG_HeapTrace
0.0.22  09.11.2001/TeHo Added FEAT_DBG_ENABLE_ALL_CLOCKS
0.0.21  09.11.2001/TeHo Added FEAT_DBG_HeapWaitQueueLen, FEAT_DBG_HeapWaitBlockMaxSize
                        to DBG_FEATURE_STRING too.
0.0.20  09.11.2001/InJu Added FEAT_DBG_HeapWaitQueueLen, FEAT_DBG_HeapWaitBlockMaxSize
0.0.19  09.11.2001/TeHo Added FEAT_DBG_Conn, FEAT_DBG_Polling
0.0.18  31.10.2001/Kose Added FEAT_DBG_OAM_ASSERT
0.0.17  19.10.2001/SaMe Added FEAT_DBG_I2C_WSMA_update
0.0.16  23.10.2001/PaHu Added FEAT_DBG_ISTI, FEAT_DBG_FORCED_CABINETTYPE, FEAT_DBG_MHA_CONTROL
0.0.15  22.10.2001/VMR  Added FEAT_DBG_mem_load_test_interval_ms
0.0.14  19.10.2001/TeHo Added FEAT_DBG_TPGCDisable
0.0.13  01.10.2001/TeHo Added FEAT_DBG_Clic, FEAT_DBG_CellPowerMaximum,
                        FEAT_DBG_WSP_Self_Tests_Disabled,
                        FEAT_DBG_Prod_Tests_Disabled,FEAT_DBG_Prod_Test_Monitor,
                        FEAT_DBG_FORCE_TCOM_MASTER, FEAT_DBG_FORCE_OM_MASTER
                        FEAT_DBG_FORCE_TCOM_MASTER and FEAT_DBG_Reco
0.0.12  27.09.2001/VMR  Added FEAT_DBG_FaultDiagnostics define
0.0.11  10.09.2001/VMR  Added comment: 2 - force TCOM and OM master is same WAM
0.0.10  10.09.2001/VMR  Added DBG_SEVERITY_STRING and DBG_FEATURE_STRING defines
0.0.9   06.09.2001/MPet Added Disable TCOM master MSG flag.
0.0.8   04.09.2001/HiMa Added FEAT_DBG_Tune
0.0.7   03.09.2001/VMR  Added FEAT_DBG_Disable_Automatic_WDG
0.0.6   30.08.2001/VMR  Increased size of sw_conf_table[] definition with
                        50 elements so there is no need for new HWR SW if
                        new feature is added to swconfig.bin
0.0.5   13.07.2001/VeHu Added FEAT_DBG_Start_Log_Time_In_Mins and
                        FEAT_DBG_Start_Log_Size_In_KB to enum
0.0.4   06.07.2001/VeHu LevelString[] and FeatureString[] removed
0.0.3   04.07.2001/VeHu Some comments corrected and header corrected
0.0.2   02.07.2001/Kak  More features, debug print has been taken into account
0.0.1   25.06.2001/VeHu First draft


*/

/*
    This file includes definitions for sw configuration purposes. sw_conf_table is initialized
    to zero and if the binary setup file exist it will be read and the contents of the file
    overwrites the default values.
    Setup values for the sw_conf_table will be read from file "/rom/swconfig.bin".
*/
#ifndef SW_CONF_TABLE
#define SW_CONF_TABLE


/* Include files */
#include "glo_def.h"

enum MON_SEVERITY
{
    MON_SEVERITY_ERROR = 2,
    MON_SEVERITY_WARNING = 3,
    MON_SEVERITY_INFO = 4,
    MON_SEVERITY_DEBUG = 5
};

#define DBG_SEVERITY_STRING { "????", "????", "ERROR", "WARN", "I", "D" }

enum FEAT_DBG
{
    /* Feature Id for configuring SW functionality (CONF) and debug prints(DBG)
       Default value is zero that means final release functionality
       NOTE: Update also DBG_FEATURE_STRING define below when adding some feature
       to enum FEAT_DBG
       ------------------------------------------------------------------------ */
    FEAT_DBG_Generic,       /* DBG: 1- enable non classified feature DBG, id for functions without any specific feature */
    FEAT_DBG_OAM,           /* CONF:1- disable O&M SW start-up for L3/Tassu tests */
    FEAT_DBG_TCom,          /* CONF:1- disable TCOM start-up */
    FEAT_DBG_UdpPrintPort,  /* 0 = Default UDP print port (51000) */
                            /* 1 = Unique UDP print ports to every WAM/WTR/WPA in BS (51000 + last digit in board's IP address) */
                            /* 49152 ... 65535 = User defined UDP print port */
    FEAT_DBG_HeapTrace,     /* DBG: 0 - Disable heap trace */
                            /* DBG: Positive value - Time in minutes to print out heap trace info */
                            /* DBG: Negative value - Time in minutes to print out heap trace info and to collect heap statistics to file */
    FEAT_DBG_RawAlarm,      /* DBG: 1- Raw Alarms are printed */
    FEAT_DBG_PrintFilter,   /* DBG: 0 - NONE, 1 - RAM disk, 2 - RAM disk & UDP, 3 - RAM disk & UDP (debug prints included) */
    FEAT_DBG_Sw_dl,         /* DBG: 1- enable SW download prints */
    FEAT_DBG_Init,          /* DBG: 1- enable Init prints */
    FEAT_DBG_Adet,          /* DBG: 1- enable Autodetection prints */
    FEAT_DBG_Start_Log_Time_In_Mins, /* DBG: 0- don't gather start up prints to log, else time when to stop*/
    FEAT_DBG_Start_Log_Size_In_KB,   /*DBG: Size of buffer to be used in ramdisk when start up prints are gathered */
    FEAT_DBG_Disable_Automatic_WDG,  /* CONF: 1 - Disable automatic start of watchdog */
    FEAT_DBG_Tune,                   /* DBG: 1- enable Tune prints, 2 - enable sample prints, 3 - enable sample prints and disable DACword update */
                                     /* 4 - disable DACword update, 5- enable extra Frequency History prints */
    FEAT_DBG_Disable_TCOM_MSTR_MSG_TO_AXU, /* 1 - Disable TCOM master indication to AXU */
                                     /* 2 - Force TCOM and OM master in one message to AXU*/
    FEAT_DBG_FaultDiagnostics,       /* DBG: 1 - enable Fault Diagnostics prints */
                                     /* 2 - FD Tracing */
                                     /* 8 - Raw alarm history disabled */
                                     /* 9 - FD disabled */
    FEAT_DBG_Clic,                   /* DBG: 1 - enable climate control prints*/
    FEAT_DBG_CellPowerMaximum,       /* CONF: cellPowerMaximum value. 0 --> O&M Calculates or hardcode default: depends on O&M version*/
    FEAT_DBG_FORCE_TCOM_MASTER,      /* VALUE = MASTER UNIT e.g. 0x20 -> WAM_20 is Master, 0 -> SW decide */
    FEAT_DBG_FORCE_OM_MASTER,        /* VALUE = MASTER UNIT e.g 0x10 -> WAM_10 is Master, 0 -> O&M decide */
    FEAT_DBG_WSP_Self_Tests_Disabled,/* 0 = FALSE, 1 = TRUE */
    FEAT_DBG_Prod_Tests_Disabled,    /* 0 = FALSE, 1 = TRUE */
    FEAT_DBG_Prod_Test_Monitor,      /* 0 = Disable, 1 = Enable */
    FEAT_DBG_Reco,                   /* 1- enable Recovery prints, 2, 3, 4 = more and more prints */
    FEAT_DBG_TPGCDisable,            /* TPGC: 0: Enabled, 1: Disabled  */
    FEAT_DBG_mem_load_test_interval_ms, /* 0 = No heap memory load test, otherwise interval of heap memory tests in ms */
    FEAT_DBG_ISTI,                   /* 0 = ISTI enabled, Prints disabled */
                                     /* 1 = ISTI enabled, Prints enabled */
                                     /* 2 = ISTI disabled, Prints disabled */
    FEAT_DBG_FORCED_CABINETTYPE,     /* 0x0 = Force cabinet type disabled (Read from WID/WCC) */
                                     /* 0x1 = SUPREME_INDOOR */
                                     /* 0x2 = SUPREME_OUTDOOR */
                                     /* 0x3 = OPTIMA_INDOOR */
                                     /* 0x4 = OPTIMA_OUTDOOR */
                                     /* 0x5 = TRIPLE_MODE_INDOOR */
                                     /* 0x6 = TRIPLE_MODE_OUTDOOR */
                                     /* 0x7 = OPTIMA_COMPACT_INDOOR_IBBU */
                                     /* 0x8 = OPTIMA_COMPACT_INDOOR_RF_EXT */
                                     /* 0x9 = OPTIMA_COMPACT_OUTDOOR_IBBU */
                                     /* 0xA = OPTIMA_COMPACT_OUTDOOR_RF_EXT */
                                     /* 0xB = NOZOMI_INDOOR */
                                     /* 0xC = NOZOMI_OUTDOOR */
    FEAT_DBG_MHA_CONTROL,            /* 0 = MHA control disable */
    FEAT_DBG_I2C_WSMA_update,        /* CONF: 0- Default value: older WSMA. */
                                     /*       1- Update: Enable support for WSMA update */
    FEAT_DBG_OAM_ASSERT,             /* 0 - Default value */
                                     /* 1 - stopped current process */
    FEAT_DBG_Conn,                   /* DBG: 0: Prints disabled, 1: Prints enabled */
    FEAT_DBG_Polling,                /* DBG: 0: Prints disabled, 1: Prints enabled */
    FEAT_DBG_HeapWaitQueueLen,       /* Specifies size for user blocks in wait queue */
    FEAT_DBG_HeapWaitBlockMaxSize,   /* Specifies maximum size of a user block kept in wait queue */
    FEAT_DBG_ENABLE_ALL_CLOCKS,      /* 1 force clock signals to all units / subracks */
    FEAT_DBG_Performance_Monitoring, /* 0 -Disable performance monitoring feature */
                                     /* Otherwise time in minutes to collect perf mon info to file */
    FEAT_DBG_DISABLE_NAT_ENTRIES,    /* 1 - Disable NAT Entries sending */
    FEAT_DBG_filter_all_but_EAC_alarms, /* 1 - all but EAC alarms disabled, apply to all units */
    FEAT_DBG_TCOM_CONF_DELAY,        /* 0:Disabled, 1:Default 3mins, other value is delay value */
                                     /* Is used for wait all the unit & cell info to be available from Db. */
    FEAT_DBG_print_task_pri,         /* Priority definition for API_PRINT_TASK, 0: default (31) */
                                     /* 1 - 30: priority (1=highest, 30=lowest) less than 10 not recommended */
                                     /* > 31: default (31) */
    FEAT_DBG_Heap_Walking,           /* 0 - Disabled, 1 - Waitinglist, 2 - Allocatedlist, >= 3 Both lists heap walking */
    FEAT_DBG_AntennaLoss,            /* 0 - use calculated values, else sets value in FEAT_DBG_AntennaLoss */
    FEAT_DBG_DUAL_CARRIER,           /* 0 = NOT dual carrier situation, 1 = THERE IS dual carrier situation */
    FEAT_DBG_OMIT_OWEN_UPWARMING,    /* 0 = NOT (normal ), 1 = do not wait normal upwarming time */
    FEAT_DBG_SWBUS_monitor,          /* Monitor SW BUS, 0 = NONE, 1 = FATAL, 2 = ERROR, 3 = DEBUG INFO */
    FEAT_DBG_DisableConfChangeToTCom,/* 1- disabled, 0 - not disabled*/
    FEAT_DBG_FixedFanSpeed,          /* CLIC control normally if 0, else define fixed fan speed */
    FEAT_DBG_DB_Change_Log,          /* 0 = Disabled, 1 = Enabled storing DB changes into ram file, */
                                     /* 2 = Enabled storing DB changes into ram file and UDP print */
    FEAT_DBG_Tune_Averages,          /* 0 = default value (420), else sets the number of averages used in normal tuning */
    FEAT_DBG_Fldp,                   /* DBG: 1 enable, 0 disable FLDP (FlashDump) prints */
    FEAT_DBG_Rhapsody_output,        /* 1- notify error, >1, notify output from rhapsody */
    FEAT_DBG_STUP_RESET,             /* 0 = Master WAM resets first all other active units, 1 = No that reseting */
    FEAT_DBG_FTP_Tester,             /* 0 = FTP tester not started, 1 = loop forever, 2 = stop if error in getFile, */
                                     /* 4 = stop if crc error, 6 = stop on any error */
    FEAT_DBG_FTP_ADDRESS,            /* 0 = FTP tester not started, else FTP server IP address */
    FEAT_DBG_AxuReconfigurationTime, /* Specifies timeout in minutes for how often AXU will be reconfigured */
                                     /* 0 disables automatic reconfiguration*/
    FEAT_DBG_Conf,                   /* DBG: 0: Prints disabled, 1: Prints enabled */
    FEAT_DBG_Disable_WTR_Alarms,     /* 1= WTR alarms are disabled */
    FEAT_DBG_Disable_DSP_Alarms,     /* 1= DSP alarms are disabled */
    FEAT_DBG_Disable_ATM_Alarms,     /* 1= ATM alarms are disabled */
    FEAT_DBG_SNTP,                   /* DBG: 1 enable SNTP prints */
    FEAT_DBG_AxuPollingDisabled,     /* 0 = AXU polling is enabled, otherwise AXU polling disabled */
    FEAT_DBG_Stup,                   /* DBG: 0: Prints disabled, 1: Prints enabled */
    FEAT_DBG_SupervisionInterval,    /* 0 - disable CR104. 1-60 enables, means Supervision poll timeout in sec. */
    FEAT_DBG_maxTimeoutCounter,      /* CR104, 1-10 defines timeOut (SupervisionInterval*maxTimeoutCounter) */
                                     /* for RNC to wait superVision poll message */
    FEAT_DBG_HGW,                    /* 1 - enables HGW debug prints */
    FEAT_DBG_TassuMonMode,           /* 0=None 1=All 2=TxOnly 3=RxOnly - */
                                     /* Byte 1 for TassuMon1 - */
                                     /* Byte 2 for TassuMon2 - */
                                     /* Byte 3 for TassuMon3 - */
                                     /* Byte 4 for TassuMon4 - */
                                     /* E.g. 0x03020001 */
    FEAT_DBG_TassuMon1,              /* sigNo: message to be monitored in HWAPI (printed out) */
    FEAT_DBG_TassuMon2,              /* sigNo: message to be monitored in HWAPI (printed out) */
    FEAT_DBG_TassuMon3,              /* sigNo: message to be monitored in HWAPI (printed out) */
    FEAT_DBG_TassuMon4,              /* sigNo: message to be monitored in HWAPI (printed out) */
    FEAT_DBG_Disable_ATM_MUX,        /* 0 = enables ATM_MUX support, 1 = disabled */
    FEAT_DBG_HWAPI_TassuRouter,      /* DBG: 1- enable Tassu Router task prints */
    FEAT_DBG_HWAPI_ApiBrowser,       /* DBG: 1- enable Api Browser task prints */
    FEAT_DBG_HWAPI_SW_DL,            /* DBG: 1- enable Api SW DL task prints */
    FEAT_DBG_HWAPI_AIF,              /* DBG: 1- enable Api AIF task prints */
    FEAT_DBG_HWAPI_Init,             /* DBG: 1- enable Api early start-up prints */
    FEAT_DBG_HWAPI_GENIO,            /* DBG: 1- enable Api GENIO task prints */
    FEAT_DBG_HWAPI_I2C,              /* DBG: 1- enable Api I2C task prints */
    FEAT_DBG_HWAPI_INET,             /* DBG: 1- enable Api INET tasks prints */
    FEAT_DBG_HWAPI_CD,               /* DBG: 1- enable Api CD task prints */
    FEAT_DBG_HWAPI_CTRL,             /* DBG: 1- enable Api CTRL task prints */
    FEAT_DBG_HWAPI_AUTO_DET,         /* DBG: 1- enable Api AUTO DET task prints */
    FEAT_DBG_HWAPI_RP_RAM_Prints,    /* DBG: 1- enable Api RP RAM feature related dbg prints */
    FEAT_DBG_HWAPI_Perf_Mon_prints,  /* DBG: 1- enable Api performance monitoring feature related dbg prints */
    FEAT_DBG_HWAPI_ID_string_Prints, /* DBG: 1- enable Api ID strings related dbg prints */
    FEAT_DBG_SWB_dblk_burstlen,      /* 0 = default value (10000 bytes), else user defined */
    FEAT_DBG_SWB_dblk_burstdelay,    /* 0 = default value (400 ms), else user defined */
    FEAT_DBG_print_flow_high,        /* 0 = default value (400), else user defined print flow controlling high watermark value */
    FEAT_DBG_print_flow_low,         /* 0 = default value (200), else user defined print flow controlling low watermark value */
    FEAT_DBG_Disable_OAM_to_TASSU,   /* 0 = Route OAM messages to TASSU if OAM SW is NOT enabled, else no routing */
    FEAT_DBG_Disable_TCOM_to_TASSU,  /* 0 = Route TCOM messages to TASSU if TCOM SW is NOT enabled, else no routing */
    FEAT_DBG_Unit_Tests_Without_WPAs,/* 0 = WPAs are equipped normally, 1 = Enable unit tests without WPA units */
    FEAT_DBG_Disable_Code_Tracking,  /* 0 = Enables Code Tracking mode setting from BTSManager. 1 = disabled*/
    FEAT_DBG_HWAPI_HEAP,             /* DBG: 1- enable Heap monitoring related dbg prints */
    FEAT_DBG_LogHeapReset,           /* 0 = Disables heap log file generation to /rom before heap exhaust reset */
                                     /* otherwise generate heap log file */
    FEAT_DBG_HWAPI_BIST,             /* DBG: 1- enable Api BIST task prints */
    FEAT_DBG_HWAPI_SELF_TEST,        /* DBG: 1- enable Api SELF TEST task prints */
    FEAT_DBG_HWAPI_COMMON,           /* DBG: 1- enable Api COMMON prints */
    FEAT_DBG_Tcp_Echo_Server,        /* DBG: 1- enable api_tcp_echo_server, */
                                     /* DBG: 2- enable TCP_ECHO_SERVER_DEBUG,   */
                                     /* DBG: 3- enable TCP_ECHO_SERVER_PRINTS   */
                                     /* DBG: 4- enable TCP_ECHO_SERVER_DEBUG and PRINTS */
    FEAT_DBG_Udp_Echo_Server,        /* DBG: 1- enable api_udp_echo_server, */
                                     /* DBG: 2- enable UDP_ECHO_SERVER_DEBUG,   */
                                     /* DBG: 3- enable UDP_ECHO_SERVER_PRINTS   */
                                     /* DBG: 4- enable UDP_ECHO_SERVER_DEBUG and PRINTS */
    FEAT_DBG_IGNORE_CRCsof_SCF_HWF,  /* 0 - normal: in the StartUp CRCs of SCF and HWF and correctness of those files are checked  */
                                     /* 1 - checking ignored, this is for developing, testing purposes  */
                                     /* DBG: 2- enable UDP_ECHO_SERVER_DEBUG,   */
    FEAT_DBG_SWBPollTimeout,         /* Give SWBus polling timeout in seconds, 0 = SW decides */
    FEAT_DBG_SWBUS_crc,              /* 0 = default, feature OFF (compatible with 082 or older), 1 feature ON */
    FEAT_DBG_Disable_WsmCfg,         /* 1 = Configure WSM normally, 0 = Enable WSM bus even when unit on bus is faulty */
    FEAT_DBG_HeapStatusPolling,      /* 0 = Disable heap status polling, otherwise heap status polling interval in ms */
    FEAT_DBG_HeapMaxFreeLimit,       /* Free heap limit in bytes for heap status polling reset */
    FEAT_DBG_HeapMaxBlockLimit,      /* Max free heap block size limit in bytes for heap status polling reset */
    FEAT_DBG_Disable_TurboReset,     /* 0 = Enables BTS turbo reset, 1 = Disabled */
    FEAT_DBG_Excess,                 /* 1 = Enable excessive prints */
    FEAT_DBG_IubTrace,               /* 1 - Enable o&m iub trace */
    FEAT_DBG_HWAPI_PCI,              /* DBG: 1- enable Api PCI task prints */
    FEAT_DBG_TCOM_Basic,             /* 0 - Basic TCOM prints (SDL-message names) disabled */
    FEAT_DBG_TCOM_RrInd,             /* 0 - No Radio Resource Ind msgs printed */
    FEAT_DBG_TCOM_RlMeas,            /* 0 - No RlMeasurement msgs printed */
    FEAT_DBG_TCOM_Sfn,               /* 0 - No SFN msgs printed */
    FEAT_DBG_TCOM_BchInfo,           /* 0 - No BcchInfo and ConformanceTestData msgs printed */
    FEAT_DBG_TCOM_PowerRep,          /* 0 - No WtrPowerReport msgs printed */
    FEAT_DBG_TCOM_UlSir,             /* 0 - No UplinkSir msgs printed */
    FEAT_DBG_TCOM_FaultIndPars,      /* 0 - No FaultInd parameters printed */
    FEAT_DBG_TCOM_MsgPars,           /* 0 - Most important message parameters not printed */
    FEAT_DBG_TCOM_SdlAlloc,          /* 0 - SDL-model memory allocs not printed */
    FEAT_DBG_TCOM_BsEnvNames,        /* 0 - BS_ENV msg names not printed */
    FEAT_DBG_TCOM_CcCount,           /* 0 - Communication context count disabled */
    FEAT_DBG_TCOM_NbapCodec,         /* 0 - NBAP Codec error prints disabled */
    FEAT_DBG_HWInfo_Timer,           /* 0 not specified, default value 60 used */
                                     /*   other values time in seconds between the recreation  of the HWInformation.xml */
                                     /*   For example 60 means new Hwinformation.xml is created always after 60 sec */
    FEAT_DBG_WTRStartUpDelay_Timer,  /* 120 = default value in seconds. User can define other values in sec. */
    FEAT_DBG_RTM_disable,            /*  0 = enable RTM, otherwise disable RTM */
    FEAT_DBG_RTM_NRT_retry_count,    /*  0 = default RTM retry count 5, otherwise RTM retry count value */
    FEAT_DBG_RTM_NRT_timeout_ms,     /*  0 = default RTM timeout 200 ms, otherwise RTM timeout value in ms */
    FEAT_DBG_RTM_prints,             /*  1 = Enable RTM debug prints */
    FEAT_DBG_overruled_wsp_type,     /* 0 = WSPC type is checked from HW_SW_ID, 0x10=16=WSPC prototype, 0x20=32=WSPC 0-series, three RAKE's */
    FEAT_DBG_WSMB_Init_Dump,         /* 1 - enables WSMB init to dump conf and clipping messages to /ram */
    FEAT_DBG_ignore_wspc_vers_check, /* 1 = O&M ignores WSPC SW version check results, WSPC runs with whatever SW */
    FEAT_DBG_HWAPI_POLL,             /* DBG: 1- enable Api POLL task prints */
    FEAT_DBG_ATM_FP,                 /* DBG: 1- enable FP prints */
    FEAT_DBG_Swmg,                   /* DBG: 0: Prints disabled, 1: Prints enabled */
    FEAT_DBG_Widm,                   /* DBG: 0: Prints disabled, 1: Prints enabled */
    FEAT_DBG_WSPC_SFNPoll_WD_disable,/* CONF: nonzero = disable WSPC WSP_MCU SFN Poll reset WatchDog */
    FEAT_DBG_Disable_DSP_Loading,    /* Give WSP ID which DSP loading is disabled in O&M (e.g. 18=0x12=WSP_10) */
    FEAT_DBG_Intelligent_Shutdown,   /* DBG: 0: Prints disabled, 1: Prints enabled */
    FEAT_DBG_LCS,                    /* 0 Prints disabled, 1 Prints enabled*/
    FEAT_DBG_HWInq,                  /* 0 = HW Inquiry disabled, 1 = enabled, 2+ = debug prints */
    FEAT_DBG_BLOC,                   /* DBG: 0: Prints disabled, 1: Prints enabled */
    FEAT_DBG_FORE_SM,                /* DBG: 0: Prints disabled, 1: Prints enabled */
    FEAT_DBG_POST_FAILURE,           /*    Post definitions for testing purposes 0;Disabled, !=0 possible failure values*/
    FEAT_DBG_R_D_CurrentBoard,       /* 0 = Detect current board from HW, != 0 -> Current board from swconfig (e.g. value 0x10 = WAM_10 etc). This is for LMU R&D, DON'T USE!!! */
    FEAT_DBG_TestDedicated,          /* 1 = fd's recovery reset disabled */
    FEAT_DBG_DisableRuntimeLog,      /* DBG: 1: Logging disabled, 0: Logging enabled */
    FEAT_DBG_TechRep,                /* 1 = printing enabled */
    FEAT_DBG_HWAPI_HWCTRL,           /* 150 DBG: 1- enable Api unit HW ctrl task prints */
    FEAT_DBG_HWAPI_CFT,              /* DBG: 1- enable Api CFT task prints */
    FEAT_DBG_HWAPI_GPS,              /* DBG: 1- enable Api GPS task prints */
    FEAT_DBG_R_D_IPAddr,             /* 0 = Default IP address, 1 - 255 = Last digit of IP address (192.168.255.xxx). This is for LMU R&D, DON'T USE!!! */
    FEAT_DBG_LCS_WSMA_WTRA_DELAY,    /* LCS Unit delay for Supreme and Optima,must be defined in ns*/
    FEAT_DBG_LCS_WSMA_WSMA_WTRA_DELAY,/*    LCS Unit delay for Supreme and Optima(in ns)*/
    FEAT_DBG_LCS_WSMB_WTRA_DELAY,    /* LCS Unit delay for Supreme and Optima(in ns)*/
    FEAT_DBG_LCS_WSMB_WTRB_DELAY,    /* LCS Unit delay for Supreme and Optima(in ns)*/
    FEAT_DBG_LCS_TM_WSMA_WTRA_DELAY, /* LCS Unit delay for TripleMode(in ns)*/
    FEAT_DBG_LCS_TM_WSMB_WTRA_DELAY, /* LCS Unit delay for TripleMode(in ns)*/
    FEAT_DBG_LCS_TM_WSMB_WTRB_DELAY, /* LCS Unit delay for TripleMode(in ns)*/
    FEAT_DBG_LCS_WSMB_WTRC_DELAY,    /* LCS Unit delay for WTRC(in ns)*/
    FEAT_DBG_WSMB_LED_control,       /* Identifier of WSMB where LED control is disabled (HW control), 0 = enabled (default): All WSMB LEDs controlled by SW */
    FEAT_DBG_STACK_INCREASE,         /* Value in bytes defines how much default stack in Rhapsody OXF is increased. For example: 0 = no increase, 1024 = increase by 1kbyte */
    FEAT_DBG_CopyPMLogToWam,         /* DBG: 1- enable automatic post mortem log file copying from "slave"-unit to subrack master WAM */
    FEAT_DBG_FlashStatMon,           /* DBG: 1 - enable Flash Statistics Monitoring, 16MSB bits are for monitoring period (seconds) if 0 default period is 60sec */
    FEAT_DBG_HOresult_denied,        /* Give CELL id which HO result is changed to EHoRequestResult_RequestDenied for OAM testing of BTS Block */
    FEAT_DBG_TCP_RetransmissionCnt,  /* TCP retransmission count */
    FEAT_DBG_CdmaLoopTestKnife,      /* 0 = Disabled, 1 = Special CDMA loop test knife settings are used */
    FEAT_DBG_WsmaRxDelay,            /*Value range = 5, 6, 7, 8, 0 - delay disabled. This parameter is used on non-triple cabinets*/
    FEAT_DBG_WsmbRt_del1_wtra_Other,       /*Value range: -1...6 cycles, any other value disables, 0 = default*/
    FEAT_DBG_WsmbRt_del1_wtrb_Other,       /*Value range: -1...6 cycles, any other value disables, 0 = default*/
    FEAT_DBG_WsmbRt_del2_wtra_Other,       /*Value range: 1...16 cycles, 0 means disabled,15 = default*/
    FEAT_DBG_WsmbRt_del2_wtrb_Other,       /*Value range: 1...16 cycles, 0 means disabled,15 = default*/
    FEAT_DBG_WsmbSt_del2_wtra_Triple,/*Value range = 1...16 cycles. 0 means disabled,1 = default*/
    FEAT_DBG_WsmbSt_del2_wtrb_Triple,/*Value range = 1...16 cycles. 0 means disabled,1 = default*/
    FEAT_DBG_WsmbSt_del2_wtra_Other, /*Value range = 1...16 cycles. 0 means disabled,0 = default*/
    FEAT_DBG_WsmbSt_del2_wtrb_Other, /*Value range = 1...16 cycles. 0 means disabled,0 = default*/
    FEAT_DBG_WsmbRr_del1_wtra_Other,       /*Value range = 1...64 cycles. 0 means disabled,30 = default*/
    FEAT_DBG_WsmbRr_del1_wtrb_Other,       /*Value range = 1...64 cycles. 0 means disabled,30 = default*/
    FEAT_DBG_WsmbRr_del2_wtra_Other,       /*Value range = 1...64 cycles. 0 means disabled,12 = default*/
    FEAT_DBG_WsmbRr_del2_wtrb_Other,       /*Value range = 1...64 cycles. 0 means disabled,12 = default*/
    FEAT_DBG_WsmbSrdel_wtra_Triple,  /*Value range = 1...64 cycles. 0 means disabled,0 = default*/
    FEAT_DBG_WsmbSrdel_wtrb_Triple,  /*Value range = 1...64 cycles. 0 means disabled,0 = default*/
    FEAT_DBG_WsmbSrdel_wtra_Other,   /*Value range = 1...64 cycles. 0 means disabled,0 = default*/
    FEAT_DBG_WsmbSrdel_wtrb_Other,   /*Value range = 1...64 cycles. 0 means disabled,0 = default*/
    FEAT_DBG_CPULoadMon,             /* CPU Load Monitoring 0 = disabled 1 = enabled in startup */
    FEAT_DBG_EthDestroyPrints,       /* 0 = disable ethernet packet destroying printouts, 1 = print only plain ethernet data, 2 = print only decoded IP/TCP/UDP headers,  3 = print both ethernet data and decoded IP/TCP/UDP headers */
    FEAT_DBG_EthDestroyLocalIpAddr,  /* 0 = destroy packets from all local IP addresses, 1 ... MAX_UNITS = destroy packets only from unit specific local IP addr (see glo_bs.h), MAX_UNITS ... 0xFFFFFFFF = local IP address for destroying eth packets */
    FEAT_DBG_EthDestroyRemoteIpAddr, /* 0 = destroy packets to all destination IP addresses, 1 ... MAX_UNITS = destroy packets only to unit specific IP addr (see glo_bs.h), MAX_UNITS ... 0xFFFFFFFF = remote IP address for destoying eth packets */
    FEAT_DBG_EthDestroyTxCount,      /* 0 = disable ethernet TX packet destroying, -1 = print only (don't destroy), else destroy every x eth TX packet */
    FEAT_DBG_EthDestroyRxCount,      /* 0 = disable ethernet RX packet destroying, -1 = print only (don't destroy), else destroy every x eth RX packet */
    FEAT_DBG_LCS_RTT_CABLE_NOMINAL_FEEDER_LOSS, /*LCS RTT cable nominal feeder loss for RTT delay calculation in 100*db/m (-> value 1 means 0.01db/m...)*/
    FEAT_DBG_LCS_RTT_CABLE_NOMINAL_DELAY,       /*LCS RTT cable nominal signal propagation delay in the feeder for RTT delay calculation in 10*ns/m (-> value 12 means 1.2ns/m...)*/

    FEAT_DBG_WsmbRt_del1_wtrd,       /*Value range: -1...6 cycles, any other value disables, 0 = default*/
    FEAT_DBG_WsmbRt_del2_wtrd,       /*Value range: 1...16 cycles, 0 means disabled,15 = default*/
    FEAT_DBG_WsmbSt_del2_wtrd_Triple,/*Value range = 1...16 cycles. 0 means disabled,1 = default*/
    FEAT_DBG_WsmbSt_del2_wtrd_Other, /*Value range = 1...16 cycles. 0 means disabled,0 = default*/
    FEAT_DBG_WsmbRr_del1_wtrd,       /*Value range = 1...64 cycles. 0 means disabled,30 = default*/
    FEAT_DBG_WsmbRr_del2_wtrd,       /*Value range = 1...64 cycles. 0 means disabled,12 = default*/
    FEAT_DBG_WsmbSrdel_wtrd_Triple,  /* Value range = 1...64 cycles. 0 means disabled,0 = default*/
    FEAT_DBG_WsmbSrdel_wtrd_Other,   /*Value range = 1...64 cycles. 0 means disabled,0 = default*/

    FEAT_DBG_TCOM_SDL_CTRL,          /* 0 - SDL/CTRL prints off */
    FEAT_DBG_TCOM_SDL_GRM,           /* 0 - SDL/GRM prints off */
    FEAT_DBG_TCOM_SDL_CCHH,          /* 0 - SDL/CCHH prints off */
    FEAT_DBG_TCOM_SDL_RLH,           /* 0 - SDL/RLH prints off */
    FEAT_DBG_TCOM_SDL_RM,            /* 0 - SDL/RM prints off */
    FEAT_DBG_TCOM_SDL_TTM,           /* 0 - SDL/TTM prints off */
    FEAT_DBG_TCOM_AtmCap,            /* 0 - SDL AtmCapacityInd prints off */
    FEAT_DBG_TCOM_DMEAS,             /* 0 - Dedicated measurement trace not printed */
    FEAT_DBG_TCOM_CMEAS,             /* 0 - Common measurement trace not printed */
    FEAT_DBG_RAR_Reset_tm,           /* time in seconds after which recovery reset counter is cleared. default is 3600. */
    FEAT_DBG_RAR_Reset_cnt,          /* allowed recovery reset count. default is 3. */
    FEAT_DBG_PoolObs,                /* This start Pool Observer task when value is 1 or more */

    FEAT_DBG_WsmbRt_del1_wtra_Triple,       /*Value range: -1...6 cycles, any other value disables, 0 = default*/
    FEAT_DBG_WsmbRt_del1_wtrb_Triple,       /*Value range: -1...6 cycles, any other value disables, 0 = default*/
    FEAT_DBG_WsmbRt_del2_wtra_Triple,       /*Value range: 1...16 cycles, 0 means disabled,15 = default*/
    FEAT_DBG_WsmbRt_del2_wtrb_Triple,       /*Value range: 1...16 cycles, 0 means disabled,15 = default*/
    FEAT_DBG_WsmbRr_del1_wtra_Triple,       /*Value range = 1...64 cycles. 0 means disabled,30 = default*/
    FEAT_DBG_WsmbRr_del1_wtrb_Triple,       /*Value range = 1...64 cycles. 0 means disabled,30 = default*/
    FEAT_DBG_WsmbRr_del2_wtra_Triple,       /*Value range = 1...64 cycles. 0 means disabled,12 = default*/
    FEAT_DBG_WsmbRr_del2_wtrb_Triple,       /*Value range = 1...64 cycles. 0 means disabled,12 = default*/
    FEAT_DBG_Para,                    /*For PARA and Dummy PARA prints*/
    FEAT_DBG_HWAPI_ApiTesterInterface,       /* DBG: 1- enable Api Tester Interface task prints */
    FEAT_DBG_HWAPI_ApiBtsLog,        /* DBG: 1- enable Api Bts Log task prints */

    FEAT_DBG_WsmaRxDelay_Triple,     /* Value range = 0, 5, 6, 7, 8 */
    FEAT_DBG_BPF_CRC_DECOMPRESS_DISABLE,    /*Disables CRC checking and file decompressing of BPF file*/
    FEAT_DBG_NoRampDown_OnCellDelete,   /* 1 - Ramp remains up on Cell Delete, Default 0 (ramp is down on cell delete) */
    FEAT_DBG_NMAP_GW,                /* 1 = enable NMAP GW prints */
    FEAT_DBG_UDPCP,                  /* 1 = enable UDPCP common prints */
    FEAT_DBG_UDPCP_RX,               /* 1 = enable UDPCP RX prints */
    FEAT_DBG_UDPCP_TX,               /* 1 = enable UDPCP TX prints */
    FEAT_DBG_Disable_MO_WAM_Change,  /* 0 = enable Master WAM change in O&M, 1 = disable Master WAM change in O&M */
    FEAT_DBG_AutoTestDedicatedState, /* 1 = autonomous start-up to test dedicated state is active, 0 = not active */
    FEAT_DBG_EnableDbStatistics,     /* 1 = prints DB operations counter (units not separated), 2 = prints DB operations counter (units separated)*/

    FEAT_DBG_BTSOM_ARIO,                /* ARIO features, 0 = disable ARIO features in O&M and 1 = enable ARIO features in O&M */
    FEAT_DBG_Disable_RadParam_Hwapi,    /* 0 - enable inquiry of HWAPI R&D parameters in BTS startup */
    FEAT_DBG_Disable_RadParam_Telecom,  /* 0 - enable inquiry of Telecom R&D parameters in BTS startup */
    FEAT_DBG_Disable_RadParam_Tup,      /* 0 - enable inquiry of TUP R&D parameters in BTS startup */
    FEAT_DBG_Disable_RadParam_DspCodec, /* 0 - enable inquiry of DSP Codec R&D parameters in BTS startup */
    FEAT_DBG_Disable_RadParam_DspRake,  /* 0 - enable inquiry of DSP Rake R&D parameters in BTS startup  */
    FEAT_DBG_Disable_RadParam_DspMachs, /* 0 - enable inquiry of DSP Machs R&D parameters in BTS startup */
    FEAT_DBG_Disable_RadParam_All_SC,   /* 0 - enable inquiry of R&D parameters of all system components in BTS startup */
    FEAT_DBG_BTSOM_AUTH_PRN,            /* 1 - enable AUTH prints,2-More detailed prints */
    FEAT_DBG_AUTH_DISABLED,             /* 0- feature enabled, 1- feature disabled */
    FEAT_DBG_Rpmag,                     /* 1 = enable RPMAG prints */
    FEAT_DBG_HWAPI_UDPCP_Stat_Print,    /* 0 = No UDPCP statistics print, otherwise interval of UDPCP statistics print in ms */
    FEAT_DBG_ADSER,                     /* 1 = enable ADSER prints */
    FEAT_DBG_EnableAlarmReporting,      /* 1 = enable alarm reporting immediately, 0 = (defaul) SNTP enables alarm reporting */
    FEAT_DBG_SWMAG,                     /* 1 = enable SWMAG debug prints */
    FEAT_DBG_BTSOM_Enable_SoapTrace,    /* 0 = (defaul) trace file is not created. Else this flag describes max size of trace file */
    FEAT_DBG_BTSOM_Enable_AlTrace,      /* 0 = (defaul) trace file is not created. Else this flag describes max size of trace file */
    FEAT_DBG_BTSOM_APW,                 /* 1 = enable APW debug prints 0 = (defaul) APW debug prints are not printed*/
    FEAT_DBG_HWAPI_OIC,                 /* 1 = enable R&D msg, 2 Opt service Trace, 3 OIC drv trace  */
    FEAT_DBG_HWAPI_CASA2,               /* 1 = Enable CASA2 prints. */
    FEAT_DBG_HWAPIResetService,         /* 1 = Enable HWAPI Reset Service prints. */

    FEAT_DBG_TCOM_SdlStallInterval,     /* 0 = off, n = the interval after how many received msgs SDL-task is stalled */
    FEAT_DBG_TCOM_SdlStallLengt,        /* SDL-task stall length in ms */
    FEAT_DBG_TCOM_RlMeasTrashTreshold,  /* RlMeasurement trashing treshold value for msg count in msg queue */
    FEAT_DBG_TCOM_SirMeasTrashTreshold, /* MeasuredUplinkSirMsg trashing treshold value for msg count in msg queue */
    FEAT_DBG_TCOM_CmeasPrio,            /* Cmeas task priority when configurable */
    FEAT_DBG_TCOM_DmeasPrio,            /* Dmeas task priority when configurable */
    FEAT_DBG_TCOM_CommitCfnSfn,         /* 0 - RlReconfigCommit CFN-SFN transformation not printed */
    FEAT_DBG_BTSOM_MTTester_PRN,        /* 0 = disabled 1 = enabled */
    FEAT_DBG_BTSOM_NbrOfOldAPWMessages, /* Describes number of old messages copied from old APW trace file to new trace file */
    FEAT_DBG_BTSOM_APWTraceFileStoringPlace, /* 0 = (default) APW trace files are stored to RAM, 1 = APW trace files are stored to ROM*/
    FEAT_DBG_BTSOM_DUAL_BAND_SUPPORT,   /* 0 - feature disabled, 1 = feature enabled */
    FEAT_DBG_HWAPI_ApiSumService,       /* 1 = enable ApiSumService debug prints 0 = disable */
    FEAT_DBG_HWAPI_ApiSumServiceTestMessages,    /* 1 = enable ApiSumServiceTestMessages  0 = disable */
    FEAT_DBG_PU_DWI_PRN,                /* 1 = enable DWI prints */
    FEAT_DBG_PU_TESTIFAPPL_PRN,         /* 1 = enable Test IF Application prints */
    FEAT_DBG_PM,                        /* 0 = disabled, 1 = enable PM prints */
    FEAT_DBG_PU_DWI_Enabled,            /* 0 = disabled 1 = enabled */
    FEAT_DBG_Tune_FreqHistory_PRN,      /* 0 = disabled 1 -> enabled to control the period of Frequency History saving for FLSH */
    FEAT_DBG_UdpPrintAddress,           /* Udp print address, unicast address A.B.C.D format 0xAABBCCDD */
    FEAT_DBG_BTSOM_BBC,                 /* 0 = disabled (default value), 1 = enable BBC prints. */
    FEAT_DBG_BTSOM_FDRules_Distr,       /* 1 = FDU asks rule file directly from FLSH, 0 = FDU asks rules from FDM */
    FEAT_DBG_BTSCommissioned,           /* 1=BTS is considered as commissioned (CDM uses fixed values and SCF is not needed).*/
    FEAT_DBG_NoRFModules,               /* 1=No RF Modules installed (e.g. BTSOM does not need to ready check RF modules).*/ 
    FEAT_DBG_NoFilters,                 /* 1=RF modules contain no Filters (e.g. BTSOM does not need to ready check Filters).*/
    FEAT_DBG_NumberOfFSP,               /* If not 0 then gives the number of FSPs installed (e.g. BTSOM does not need to ready check other FSPs).*/
    FEAT_DBG_BTSOM_BBC_MANUAL_CONF_PRN, /* 0 = BBC manual config prints disabled (default), 1 = prints enabled*/
    FEAT_DBG_Enable_DbgPrint_to_BtsLog_PRN,  /* 0 = debug prints to BtsLog disabled (default), 1 = debug prints enabled (only in MT/SCT) */
    FEAT_DBG_EnableHeapMonitoring,      /* 0 = BTS heap monitoring bs_heap disabled (default), 1 = heap monitoring enabled */
    FEAT_DBG_DspTraceMaxTime,           /* Default value 120 seconds */
    FEAT_DBG_DspTraceMinTime,           /* Default value 10 seconds */
    FEAT_DBG_DspTraceMaxFileSize,       /* Default value 3000 KBytes */
    FEAT_DBG_HWAPI_TraceBufferMaxSize,  /* 0 = default max value, -1 = disable Trace Buffer, x = max size of Trace Buffer in kB */
    FEAT_DBG_PoolObs_Status,            /* Pool status printing interval */ 
    FEAT_DBG_BTSOM_OPT_PRN,             /* 1 - enable Lic.Opt Mgmt prints */
    FEAT_DBG_BTSOM_Disable_Licence_Validation, /* 1- disable licence file signature validation */ 
    FEAT_DBG_BTSOM_OPT_Enabled,         /* 1 -enable Licence and Option Management feature */
    FEAT_DBG_StupFDEnabled,             /* 1 = FD Enabling in Nora start-up, 0 default NOT Enabling */
    FEAT_DBG_DspDumpCpu,                /* DSP processor used in memory dump, default = codec_1 = 5 */
    FEAT_DBG_Prof_Enable,             /* Enables profile data handling */
    FEAT_DBG_Prof_Monitored_PID1,     /* PID of the monitored process for Function Execution Logger or 0, if all */
    FEAT_DBG_Prof_Monitored_PID2,     /* PID of the monitored process for Function Execution Logger */
    FEAT_DBG_Prof_Monitored_PID3,     /* PID of the monitored process for Function Execution Logger */
    FEAT_DBG_Prof_Monitored_PID4,     /* PID of the monitored process for Function Execution Logger */
    FEAT_DBG_Prof_IPAddr,             /* IP-address for Function Execution Logger where to send UDP-frames */
    FEAT_DBG_Prof_Port,               /* IP-port for Function Execution Logger where to send UDP-frames */
    FEAT_DBG_Prof_trans_task_pri,     /* Priority of transmission task */
    FEAT_DBG_Prof_RingBufferSize,     /* Size of ring buffer in bytes */
    FEAT_DBG_BTSOM_WSMB_Read,         /* 1 = enable reading and printing of WSMB registers */
    FEAT_DBG_TCOM_TLH,                  /* 0 - Telecom License Handler trace not printed */
    FEAT_DBG_HWAPI_TraceBufferEmptyInterval, /* 0 = default value, x = empty interval in ms  */
    FEAT_DBG_HWAPI_TraceBufferPacketSize,    /* 0 = default value, x = packet size in bytes */
    FEAT_DBG_BTSOM_HWAPI_IF_PRN,             /* 0 = disabled 1 = enabled */
    FEAT_DBG_testChannelTxPowerTestKnife,/*-500 ... 500 */
    FEAT_DBG_Test_Enable_Loop_parameter_read_from_dbw, /* 0 = disable CDMA Loop parameter read from DBW change in O&M   */ 
                                                       /* 1 = enable CDMA Loop parameter read from DBW change in O&M   */
    FEAT_DBG_BTSOM_FUM_PRN,             /* 0 = disabled 1 = enabled */
    FEAT_DBG_BTSOM_FSM_Creator_PRN,     /* 0 = disabled 1 = enabled */
    FEAT_DBG_BTSOM_SPMAG_PRN,           /* 0 = disabled (default value), 1 = enabled*/
    FEAT_DBG_Test_EthernetTestEnabled,             /* 0 = disabled 1 = enabled */
    FEAT_DBG_Test_Ethernet_poll_waitTimeout,       /* Default value 15 ms */
    FEAT_DBG_Test_EthernetTest_MT_SCT_Enabled,     /* 0 = disabled 1 = enabled */
    FEAT_DBG_Test_EthernetTestAdvancedInfoEnabled, /* 0 = disabled 1 = enabled */
    FEAT_DBG_BTSOM_ALMAG,                          /* 1 = enable ALMAG prints   */
    FEAT_DBG_SwRecoveryTimeout,         /* Timeout in seconds for clearing SW recovery retry counter, 0 = default */
    FEAT_DBG_BTSOM_DSP_IF_PRN,          /* 0 = disabled (default value), 1 =enabled */
    FEAT_DBG_HWAPI_HW_CTRL_SERVICE,     /* 1 = Enable HWAPI HW Control Service prints. */
    FEAT_DBG_HWAPI_MODULE_TYPE,         /* 0x10 = System module, 0x20 Extension module 1 and 0x30 Extension module 2 */             
    FEAT_DBG_BTSOM_SNTPCheckPeriod,     /* Lic.Mgmt SNTP-check period, If 0 then EFS default value is used */ 
    FEAT_DBG_BTSOM_LicenceCheckPeriod,  /* Lic.Mgmt Licence-check period, If 0 then EFS default value is used */
    FEAT_DBG_LBA_FeatureCheckPeriod,    /* LBA feature check period, If 0 then EFS default value is used */
    FEAT_DBG_HWAPI_ETH_SERVICE,         /* 1 = enable ethernet service prints */
    FEAT_DBG_EthRecoResetDisabled,      /* 1 = disable ethernet jamming recovery reset in O&M */
    FEAT_DBG_SetCellIdIsLcrId,          /* 1 = Set CellId to be same as LcrId defined in commission file. For Production test purposes.*/
    FEAT_DBG_DBDumpObjCounter,          /* Number of db object print to dump file before keeping 1ms delay */
    FEAT_DBG_DatabaseDumpTimer,         /* 0 = database dump disabled, else db dump enabled and value is timer in seconds */ 
    FEAT_DBG_CLOCK_PRN,                 /* 0=disabled(default), 1=enabled */
    FEAT_DBG_ETH_MirrorSrcPort1,        /* Source port of first mirroring pair (see EL2XPort.h). */
    FEAT_DBG_ETH_MirrorDestPort1,       /* Destination port of first mirroring pair (see EL2XPort.h). */
    FEAT_DBG_ETH_MirrorDirection1,      /* Traffic direction of first mirroring pair, 0 = Ingress, 1 = Egress. */
    FEAT_DBG_ETH_MirrorSrcPort2,        /* Source port of second mirroring pair (see EL2XPort.h). */
    FEAT_DBG_ETH_MirrorDestPort2,       /* Destination port of second mirroring pair (see EL2XPort.h). */
    FEAT_DBG_ETH_MirrorDirection2,      /* Traffic direction of second mirroring pair, 0 = Ingress, 1 = Egress. */
    FEAT_DBG_TCOM_TcomPerfTrace,        /* 0 - TCOM performance monitoring feature disabled */
    FEAT_DBG_BTSOM_ENABLE_CLOCK_TUNING, /* 0=disabled(default), 1=enables OCXO clock tuning in Flexi */
    FEAT_DBG_ACNF,                      /* 1 = enable ACNF debug prints */
    FEAT_DBG_BTSOM_TEST_PRN,            /* 1 = enable common Test prints */
    FEAT_DBG_BTSOM_LOOPTEST_PRN,        /* 1 = enable CDMA Loop Test prints */
    FEAT_DBG_BTSOM_LOOPTEST_DETAIL_PRN, /* 1 = enable CDMA Loop Test detailed prints */
    FEAT_DBG_BTSOM_EAC_PRN,             /* 1 = EAC prints enabled */
    FEAT_DBG_Disp_PRN,                  /* 1 = enable DISP prints */
    FEAT_DBG_Led_PRN,                   /* 1 = enable LED prints */
    FEAT_DBG_UhndSD_PRN,                /* 1 = enable UHND_StatusDisplay prints */
    FEAT_DBG_Disable_Tup,               /* 1- disable Tup start-up */
	FEAT_DBG_Test_Enable_MasteLoop_print,/* 1 = enable MasterLoop prints 2 = Extra Print */  
	FEAT_DBG_Test_Enable_MasteLoop_Extra_print, /* 1 = enable MasterLoop Extra Print */  
    FEAT_DBG_Test_Enable_MasteLoop_Log_files,/* 1 = enable Log files*/
	FEAT_DBG_Test_MasteLoopIsBranchDualMode,/* Bit 0 = 1 ->RFM1 Branch1 is Dual mode ... Bit 5 = 1 ->RFM3 Branch2 is Dual mode*/
	FEAT_DBG_Test_Disable_MasteLoop_Feature,/* 0 = Eanble Master Loop and 1 = Diasable Master Loop*/
	FEAT_DBG_HeapTracePID,              /*At runtime this flag can be set with BTSlog tool. Full monitor mode is set for this pid*/
	FEAT_DBG_CLIC_FIXED_FAN_SPEED,      /* != 0 fans are assigned to fixed speed defined here, value(1-255)*/
    FEAT_DBG_HWAPI_INSPAP_UL_DELAY,     /* Used only in plain HWAPI sw when no O&M in package. Inspap uplink delay value. */
    FEAT_DBG_HWAPI_INSPAP_DL_DELAY,     /* Used only in plain HWAPI sw when no O&M in package. Inspap downlink delay value. */
	FEAT_DBG_ProdTest_TXDigitalGain,    /* TXDigitalGain value for production testing*/
	FEAT_DBG_Disable_ScfFromFlash,      /* 1 = Disable commissioning file backup writing and reading from flash */
	FEAT_DBG_BTSOM_Disable_Channel_Validation, /* 1 = Disable frequency channel validation */
	FEAT_DBG_BTSOM_ISTI_Timer_Divider,  /* value > 1 decreases ISTI an hour counter value(e.g. value 60 -> ISTI an hour timer expires in every minute)*/
	FEAT_DBG_CLIC_MINUTE_COUNTER,       /*value > 0, e.g. value=20 means 20 minutes =~ simulated CLIC one hour)*/
	FEAT_DBG_CLIC_HOUR_COUNTER,         /*value > 0, e.g. value=5 means (5*FEAT_DBG_CLIC_MINUTE_COUNTER) minutes =~ simulated CLIC one day)*/
    FEAT_DBG_TechRep_MT_SCT_Enabled,    /* 0 = disabled 1 = enabled */
	FEAT_DBG_Test_CabinetTest_Prints,   /* enable Cabinet and Site Test debug prints */
	FEAT_DBG_Test_Enable_CabinetTest_Feature, /* 0 = disabled 1 = enabled*/
	FEAT_DBG_Test_Enable_MasteLoopGetAntennaHWInfoFromBBC, /* 1 = disabled 0 = enabled*/
	FEAT_DBG_BTSOM_EnableAllFeatures,      /* 1 = Enable all optional features */
    FEAT_DBG_TechRep_FD_Trap_Log_Trigger1, /* 0 = triggering off, != 0 raw alarm id which triggers log */
    FEAT_DBG_TechRep_FD_Trap_Log_Trigger2, /* 0 = triggering off, != 0 raw alarm id which triggers log */
    FEAT_DBG_TechRep_FD_Trap_Log_Trigger3, /* 0 = triggering off, != 0 raw alarm id which triggers log */
    FEAT_DBG_TechRep_FD_Trap_Log_Trigger4, /* 0 = triggering off, != 0 raw alarm id which triggers log */
    FEAT_DBG_TechRep_FD_Trap_Log_Trigger5, /* 0 = triggering off, != 0 raw alarm id which triggers log */
    FEAT_DBG_SET_FSM_MODE,                 /* 1 = master ; 2 = extension1 ; 4 = extension2 ; 	*/
    FEAT_DBG_FRresetDelayTimer,            /* If flag is not set (=0) default 6 sec timer is used for FR reset delay.*/
    FEAT_DBG_Test_Enable_TxRxOptimization,   /* 0 = disabled; 1 = enabled */
    FEAT_DBG_Test_Enable_FspDspOptimization, /* 0 = disabled; 1 = enabled */
	FEAT_DBG_Conf_LicensePollingTimer,     /* 0 = use default timer value, != 0 timer value in seconds */
	FEAT_DBG_Conf_LicenseFeatureDisabled,  /* 0 = License Feature Enabled, 1 = License Feature Disabled */
	FEAT_DBG_HWAPI_Illuminator_Port,	   /* 0 = dbgserver disabled, != 0 specifies illuminator port and starts ose_dbgserver */
	FEAT_DBG_ForceDspDump,				   /* 0 = dsp memory dump is not done if files exists (=normal behavior), 1 = dump is done even if files already exists */
    FEAT_DBG_DisableFTMReadyCheck,		   /* 0 = FTM Ready check is done, 1 = FTM Ready Check is skipped*/
	FEAT_DBG_DisableFanControl,		       /* val>1 Disables Fan test and fan control,1=Disable Fan Control,0(default)=Normal Temperature Management Operations*/
	FEAT_DBG_DisableTempTrace,			   /* 1 = Disables,Temperature Trace, 0(default) = Enables,Temperature Trace */ 
	FEAT_DBG_BTSOM_ALMAG_VSWR_Threshold_Timer,	/*VSWR Threshold Timer; resoulution minutes, e.g.30=30minutes*/
	FEAT_DBG_BOOTCORESWDL_ENABLED,			/* 0=disabled=BC will not be downloaded to FSPA/WSPC, 1=BC downloading enabled */
	FEAT_DBG_BTSMOM_ALMAG_ALSupervisionTimer, /* value is in milliseconds, for example 5000. Value must be different than 0*/
	FEAT_DBG_Test_AntennaLineTestEnabled, /*0=disabled, 1=enabled*/
	FEAT_DBG_BTSOM_Site_Reset_Allowed,      /* 1 = site reset is allowed, 0 = site reset is not allowed*/
	FEAT_DBG_BTSOM_GAIN_PRN,				/* 1 = enable GAIN debug prints */
    FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT0, /* 0 = mirroring disabled, 1 = mirror egress only, 2 = mirror ingress only, 3 = mirror both */
    FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT1, /* 0 = mirroring disabled, 1 = mirror egress only, 2 = mirror ingress only, 3 = mirror both */
    FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT2, /* 0 = mirroring disabled, 1 = mirror egress only, 2 = mirror ingress only, 3 = mirror both */
    FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT3, /* 0 = mirroring disabled, 1 = mirror egress only, 2 = mirror ingress only, 3 = mirror both */
    FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT4, /* 0 = mirroring disabled, 1 = mirror egress only, 2 = mirror ingress only, 3 = mirror both */
    FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT5, /* 0 = mirroring disabled, 1 = mirror egress only, 2 = mirror ingress only, 3 = mirror both */
    FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT6, /* 0 = mirroring disabled, 1 = mirror egress only, 2 = mirror ingress only, 3 = mirror both */
    FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT7, /* 0 = mirroring disabled, 1 = mirror egress only, 2 = mirror ingress only, 3 = mirror both */
    FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT8, /* 0 = mirroring disabled, 1 = mirror egress only, 2 = mirror ingress only, 3 = mirror both */
    FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT9, /* 0 = mirroring disabled, 1 = mirror egress only, 2 = mirror ingress only, 3 = mirror both */
    FEAT_DBG_ETH_HCSM_MIRROR_INGRESS_DST_PORT,/* Destination port number for mirrored ingress data */
    FEAT_DBG_ETH_HCSM_MIRROR_EGRESS_DST_PORT, /* Destination port number for mirrored egress data */
    FEAT_DBG_BTSOMStub,                     /* HCSM BTSOMStub prints*/
    FEAT_DBG_BTSOMStub_AmountOfFaradays,    /* HCSM BTSOMStub configuration - Amount of Faradays */
    FEAT_DBG_BTSOMStub_TupFaradayId,        /* HCSM BTSOMStub configuration - Faraday CHIP ID */
	FEAT_DBG_BTSOM_Test_Set_EthTestReceivePriority,/*Ethernet Test Receive prosess priority*/
	FEAT_DBG_BTSOM_Test_Set_EthTestSendPriority,   /* Ethernet Test  sender prosess priority*/
	FEAT_DBG_BTSOM_Test_EthernetTestPrint,	       /* 0 = disabled 1 = enabled */
	FEAT_DBG_BTSOM_Test_Enable_Big_successLimitPromille, /* 0 = disabled 1 = enabled */
    FEAT_DBG_BBTraceMaxFileSize,             /* Default value 3000 KBytes */
    FEAT_DBG_HWAPI_BB_TRACE_PRN,             /* 1 = Enable BB Trace prints */
	FEAT_DBG_NO_WID_CHECK,					/* 0 = disabled 1 = enabled */
	FEAT_DBG_BTSOM_PMFreezingDisabled,		/* 0 = default = PM freezing enabled, 1 = PM freezing disabled */
	FEAT_DBG_BTSOM_ALMAG_Device_Detection_Timer,	/* 0 = default, != 0 timer value in milliseconds */
	FEAT_DBG_BTSOM_TrialPeriodTime,			 /* Trial period time value in seconds. */
	FEAT_DBG_MaxNumOfFeat                    /* Keep this at last line */	
};


/* DBG_FEATURE_STRING define used in OAM dbg_prints. Remember to update this to
    match enum FEAT_DBG above. */
#define DBG_FEATURE_STRING { "GEN", "OAM", "TCOM", "UDPPRINTPORT", "HEAP_TRACE", \
                        "RAW_ALARM", "PRINTFILTER", "SW_DL", "INIT", "ADET", \
                        "STARTLOG_TIME", "STARTLOG_SIZE", "WDOG", "TUNE", "TCOM_MASTER", \
                        "FAULT", "CLIC", "CELLPOWERMAX", "TCOM_MASTER_VALUE", \
                        "OM_MASTER_VALUE", "WSP_SELFTEST", "PROD_TEST", \
                        "PROD_TEST_MONI", "RECO", "TPGC", "MEM_LOAD_TEST", "ISTI", \
                        "FORCED_CABINETTYPE","MHA_CONTROL", "WSMA", "ASSERT", \
                        "CONN", "POLL", "HEAPLEN", "HEAPSIZE", "CLOCKS", "PERF_MONIT", \
                        "NAT", "FILT_NONEAC", "TCOM_CONFIGURATION_DELAY", "PRINT_PRI", \
                        "HEAPWALK", "ANTENNALOSS", "DUAL_CARRIER", "OMIT_UPWARMING", \
                        "SWB_MON", "DISABLE_CONF_CHANGE_TO_TCOM", "FIXED_FANS", "DB_CHANGE_LOG", \
                        "TUNE_AVG", "FLDP", "RHAPSODY_FW", "STUP_RESET", "FTP_TESTER", "FTP_ADDR", \
                        "AXU_RECONFIG_TIME", "CONF", "DISABLE_WTR_AL", "DISABLE_DSP_AL", "DISABLE_ATM_AL", "SNTP", \
                        "AXU_POLLING_DISABLED", "STUP", "CR104", "CR104", "HGW", "TASSUMONMODE", \
                        "TASSUMON1", "TASSUMON2", "TASSUMON3", "TASSUMON4", "ATMUX", "TR", "BR", \
                        "SW_DL", "AIF", "INIT", "GENIO", "I2C", "INET", "CD", "CTRL", "AUTO_DET", \
                        "RP_RAM", "PERF_M", "ID_S", \
                        "SWB_DBLK_BURSTLEN", "SWB_DBLK_BURSTDELAY", "PRINT_HIGH_WATERMARK", \
                        "PRINT_LOW_WATERMARK", "OAM_MSG_TO_TASSU", "TCOM_MSG_TO_TASSU", \
                        "UNIT_TESTS_WITHOUT_WPAS", "CODE_TRACKING", "HEAP", "LOG_HEAP_RESET", \
                        "BIST", "SELF_TEST", "COMMON","TCP_ECHO_SERVER","UDP_ECHO_SERVER", \
                        "IGNORE_CRCS", "SWBPOLL", "FEAT_DBG_SWBUS_CRC", "DISABLE_WSMCFG", \
                        "HEAP_POLL", "HEAP_FREE_LIMIT", "HEAP_BLOCK_LIMIT", "TURBO_RESET", "EXCESS", "IUB", \
                        "PCI", \
                        "B", "RRI", "RLM", "SFN", "BCI", "PWR", "USI", \
                        "FPA", "P", "XA", "E", "CC", "NC", "HWINFO", "START-UP_TIMER", \
                        "RTM_DISABLE", "RTM_RETRY", "RTM_TMO", "RTM", "WSPC_TYPE", "WSMB_INIT_DUMP", "WSPC_CHECK", \
                        "SFN_POLL", "ATM_FP", "SWMG", "WIDM", "WSPC_SFNPOLL_WD_DISABLE", "DSP_LOAD_DISABLE", "INTELLIGENT_SHUTDOWN",    \
                        "FEAT_DBG_LCS", "HWINQ","BLOC","FORE_SM","FEAT_DBG_POST_FAILURE", "BOARD", "TEST_DEDICATED", "RUNTIME_LOG", "TECHREP", \
                        "HWCTRL", "CFT", "GPS", "IPADDR","LCS_DELAY1","LCS_DELAY2","LCS_DELAY3", \
                        "LCS_DELAY4","LCS_DELAY5","LCS_DELAY6","LCS_DELAY7","LCS_DELAY8", "WSMB_LED_CTRL", "STACK_INCREASE", \
                        "COPY_PM_LOG_TO_WAM", "FLASH_STAT_MON", "HO_RESULT_DENIED", "TCP_RETRY", "CDMA_LOOP_KNIFE","WSMA_RX_DELAY", \
                        "WSMB_RT_DEL1_WTRA", "WSMB_RT_DEL1_WTRB", "WSMB_RT_DEL2_WTRA", "WSMB_RT_DEL2_WTRB", \
                        "WSMB_ST_DEL2_WTRA_TRIPLE", "WSMB_ST_DEL2_WTRB_TRIPLE", "WSMB_ST_DEL2_WTRA_OTHER", "WSMB_ST_DEL2_WTRB_OTHER", \
                        "WSMB_RR_DEL1_WTRA", "WSMB_RR_DEL1_WTRB", "WSMB_RR_DEL2_WTRA", "WSMB_RR_DEL2_WTRB", "WSMB_SR_DEL_WTRA_TRIPLE", "WSMB_SR_DEL_WTRB_TRIPLE", \
                        "WSMB_SR_DEL_WTRA_OTHER", "WSMB_SR_DEL_WTRB_OTHER", "CPU_LOAD_MON", \
                        "ETH_DESTROY", "ETH_DESTROY_LOCAL_ADDR", "ETH_DESTROY_REMOTE_ADDR", "ETH_DESTROY_TX_CNT", "ETH_DESTROY_RX_CNT","LCS_RTT_NFLOSS", "LCS_RTT_NDELAY",\
                        "WSMB_RT_DEL1_WTRD","WSMB_RT_DEL2_WTRD","WSMB_ST_DEL2_WTRD_TRIPLE","WSMB_ST_DEL2_WTRD_OTHER",\
                        "WSMB_RR_DEL1_WTRD","WSMB_RR_DEL2_WTRD","WSMB_SR_DEL_WTRD_TRIPLE","WSMB_SR_DEL_WTRD_OTHER",\
                        "CT", "G", "CH", "R", "RM", "T", "AC", "DM", "CM", "RAR_RESET_TM", "RAR_RESET_CNT", "POOL_OBSERVER",\
                        "WSMB_RT_DEL1_WTRA_TRIPLE", "WSMB_RT_DEL1_WTRB_TRIPLE", "WSMB_RT_DEL2_WTRA_TRIPLE", "WSMB_RT_DEL2_WTRB_TRIPLE",\
                        "WSMB_RR_DEL1_WTRA_TRIPLE", "WSMB_RR_DEL1_WTRB_TRIPLE", "WSMB_RR_DEL2_WTRA_TRIPLE", "WSMB_RR_DEL2_WTRB_TRIPLE", "PARA", "TESTER_INTERFACE", "BTS_LOG",\
                        "WSMA_RX_DELAY_TRIPLE", "BPF_DISABLE", "NO_RAMP_DOWN_ON_CELL_DELETE", "NMAP_GW", "UDPCP", "UDPCP_RX", "UDPCP_TX",\
                        "DISABLE_MO_CHANGE", "AUTOTEST_DEDICATED_STATE", "ENABLE_DB_STATISTICS", "BTSOM_ARIO","Disable_RadParam_Hwapi","Disable_RadParam_Telecom","Disable_RadParam_Tup",\
                        "Disable_RadParam_DspCodec","Disable_RadParam_DspRake","Disable_RadParam_DspMachs","Disable_RadParam_All_SC","BTSOM_AUTH","AUTH_DISABLED","RPMAG",\
                        "HWAPI_UDPCP_Stat_Print","ADSER","EnableAlarmReporting","SWMAG", "Enable_SoapTrace", "Enable_AlTrace", "APW", "OIC_TASK", "CASA2_TASK",\
                        "HWAPIResetService", "SDL_STALL_INT", "SDL_STALL_LENGTH", "RLM_TRASH_TRESH", "SIR_TRASH_TRESH", "CMEAS_PRIO", "DMEAS_PRIO", "COMMIT_CFN_SFN", "MTTester", "NbrOfOldAPWMessages", "APWTraceFileStoringPlace",\
                        "DUAL_BAND_SUPPORT", "SUM_SERVICE", "SUM_SERVICE_TEST_MESSAGES", "DWI", "TESTIFAPPL", "PM", "ENABLE_DWI","Tune_FreqHistory","UDP_PRINT_ADDRESS","BBC","FDRules_Distr",\
                        "FEAT_DBG_BTSCommissioned", "FEAT_DBG_NoRFModules", "FEAT_DBG_NoFilters", "FEAT_DBG_NumberOfFSP","BTSOM_BBC_MANUAL_CONF", "Enable_DbgPrint_to_BtsLog", "HEAP_MONITORING",\
                        "DspTraceMaxTime", "DspTraceMinTime", "DspTraceMaxFileSize", "TRACE_BUFFER_MAX_SIZE", "POOL_STATUS_INTERVAL","OPT","Disable_Licence_Validation","Enable_Lic&Opt_Mgmt", "EnablingFD", "DSPDump",\
                        "PROF_ENABLED","MONITORED_PID1","MONITORED_PID2","MONITORED_PID3","MONITORED_PID4","PROF_IP_ADDRESS","PROF_PORT", "TRANS_TASK_PRI","RING_BUFFER_SIZE","WSMB_Register_Read",\
                        "TLH", "TRACE_BUFFER_EMPTY_INTERVAL","TRACE_BUFFER_PACKET_SIZE", "HWAPI_IF","Test_Channel_TxPower","Enable_CDMA_loop_param_read_from_dbw","FUM", "FSM_Creator", "SPMAG",\
                        "FEAT_DBG_Test_EthernetTestEnabled", "FEAT_DBG_Test_Ethernet_poll_waitTimeout", "FEAT_DBG_Test_EthernetTest_MT_SCT_Enabled", "FEAT_DBG_Test_EthernetTestAdvancedInfoEnabled","ALMAG",\
                        "SW_RECOVERY_TIMEOUT","DSP_IF", "HW_CTRL_SERVICE", "MODULE_TYPE","SNTPCheckPeriod","LicenceCheckPeriod","FeatureCheckPeriod", "ETH_SERVICE", "EthRecoReset", "CDM", "DBDumpObjCount", "DBDumpTimer",\
                        "CLOCK", "MIRRORSRC1", "MIRRORDST1", "MIRRORDIR1", "MIRRORSRC2", "MIRRORDST2", "MIRRORDIR2", "TPT", "CLOCK_TUNING", "ACNF", "Test", "LoopTest", "LoopTest_Detail", "EAC", "DISP", "LED", "UHNDSD",\
                        "DISABLE_TUP","Enable_MasteLoop_print","Enable_ExtraMasteLoop_print","Enable_MasteLoop_Log_files","Enable_MasteLoop_Dual_Branch","Disable_MasteLoop_Feature", "HeapTracePID","ClicFixedFanSpeed",\
                        "INSPAP_UL_DELAY", "INSPAP_DL_DELAY", "ProdTest_TXDigitalGain", "Disable_ScfFromFlash", "Disable_Channel_Validation", "ISTI_Timer_Divider", "ClicMinuteCounter", "ClicHourCounter",\
                        "FEAT_DBG_TechRep_MT_SCT_Enabled", "CabinetTest_debug_prints", "FEAT_DBG_Test_Enable_CabinetTest_Feature","FEAT_DBG_Test_Enable_MasteLoopGetAntennaHWInfoFromBBC","EnableAllFeatures",\
                        "TechRep_FD_Trap_Log_Trigger1", "TechRep_FD_Trap_Log_Trigger2", "TechRep_FD_Trap_Log_Trigger3", "TechRep_FD_Trap_Log_Trigger4", "TechRep_FD_Trap_Log_Trigger5", "SET_FSM_MODE",\
                        "FEAT_DBG_FRresetDelayTimer", "FEAT_DBG_Test_Enable_TxRxOptimization", "FEAT_DBG_Test_Enable_FspDspOptimization", "FEAT_DBG_Conf_LicensePollingTimer", "FEAT_DBG_Conf_LicenseFeatureDisabled",\
						"Illuminator_Port", "ForceDspDump", "DisableFTMReadyCheck", "DisableFanControl", "DisableTempTrace", "ALMAG_VSWR_Threshold_Timer", "BootCoreSWDL", "ALSupervisionTimer", "AntennaLineTestEnabled",\
						"Site_Reset_Allowed", "GAIN", "FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT0", "FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT1", "FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT2", "FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT3", \
                        "FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT4", "FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT5", "FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT6", \
 						"FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT7", "FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT8", "FEAT_DBG_ETH_HCSM_MIRROR_SRC_PORT9", "FEAT_DBG_ETH_HCSM_MIRROR_INGRESS_DST_PORT", "FEAT_DBG_ETH_HCSM_MIRROR_EGRESS_DST_PORT",\
 						"BTSOMStub", "BTSOMStub_AmounfOfFaradays", "BTSOMStub_TupFaradayId", "FEAT_DBG_Test_Set_EthTestReceivePriority", "FEAT_DBG_Test_Set_EthTestSendPriority", "FEAT_DBG_Test_EthernetTestPrint",\
						"FEAT_DBG_BTSOM_Test_Enable_Big_successLimitPromille", "BBTraceMaxFileSize", "BB_TRACE", "NO_WID_CHECK", "PMFREEZE", "BTSOM_ALMAG_Device_Detection_Timer", "TrialPeriodTime"} 


/* Enumeration for interpreting FEAT_DBG_PrintFilter in sw_conf_table.
   Note: severity level filtering is supported only at higher level application printing */
enum PRINT_FILTER
{
    PRINT_FILTER_NONE = 0,  /* no log data to UPD port & RAM disk - default */
    PRINT_FILTER_RAMDISK,   /* INFO, WARNING and ERROR severity level printouts
                               into RAM disk (startup log & crashdump log) */
    PRINT_FILTER_UDP_INFO,  /* same as previous but also to UDP printouts */
    PRINT_FILTER_UDP_DBG    /* same as previous but DEBUG severity printouts
                               (depending on selected feature) also included */
};


#ifdef __cplusplus
extern "C" {
#endif

/* sw_conf_table size is FEAT_DBG_MaxNumOfFeat + 50 -> there is no need for
new HWR SW when some new feature is added to swconfig.bin */
extern u32 sw_conf_table[FEAT_DBG_MaxNumOfFeat + 50];

extern void  dbg_print(enum MON_SEVERITY severity, enum FEAT_DBG featureId, const char* format, ...);

extern i32 PerfMonitRegister(const char *description);
extern void PerfMonitStart(i32 id);
extern void PerfMonitStop(i32 id);
#ifdef __cplusplus
}
#endif

#endif /* SW_CONF_TABLE */
