/***********************************************************************
*                  Copyright (c) 2002 Nokia Networks
*                  All rights reserved
*
* FILENAME    : sw_conf_table.h
* VERSION     : flexibts#1.45
* DATE        : 08-MAY-2006 09:50:41
* AUTHOR      : ARNIKULA
* STATUS      : ACCEPTED
*
***********************************************************************/
/*

Revision history:

VERSION   DATE/AUTHORS        COMMENT
1.45      04.05.2006/TiVi     Changed FEAT_DBG_RD_Parser to FEAT_DBG_EnablePostMortem.
                              FEAT_DBG_UdpPrintPort comment default print port 51000->50011.
1.44      15.03.2006/Ojar     Added DAPD R&D SWITCH
1.43      09.02.2006/Ojar     Bug correcions, added "," to line end
1.42      07.02.2006/Ojar     Renamed FEAT_DBG_Heap_Monitoring to FEAT_DBG_EnableHeapMonitoring.
                              Added FEAT_DBG_HeapTracePID.
							  		RX_TEMPERATURE_FACTOR
							  		RX_CALIB_TEMPERATURE	
1.41      16.12.2005/Ojar     Change comments for UOAM_fault and correct FEAT_DGB_TX_Disable_Protection 
                              ->FEAT_DBG_TX_Disable_Protection
1.40      29.11.2005/Ojar     Changed macro Get_RAD_param to point function and
                              added macro Get_RAD_param_nowait for print usage.
1.39      25.11.2005/Ojar     added FEAT_DGB_TX_Disable_Protection
1.38      19.09.2005/Ojar     Added FEAT_DBG_Oic_PI_Delay 
1.37      01.09.2005/Ojar     Remove space character to Line 346 end 
1.36      31.08.2005/Ojar     Update failure
1.35      30.08.2005/Ojar     Added FEAT_DBG_UOAM_Fault_DisableFaultHistory and 
									FEAT_DBG_UOAM_Fault_EnableLoadTestPrints
1.34      29.08.2005/Ojar     Added FEAT_DBG_UOAM_CreateEventSender 
									FEAT_DBG_UOAM_DataStorage
1.33      24.08.2005/Ojar     Add "/" to line 334 end
1.32      22.08.2005/Ojar     Added FEAT_DBG_HWREL_FaultHandler and 
									FEAT_DBG_UOAM_Disable_Fan_Ctrl 
1.31      02.08.2005/Ojar     Added FEAT_DBG_UOAM_Fault_AcksNotChecked 
1.30      15.07.2005/Ojar     Added FEAT_DBG_HWREL_SCT
1.29      19.05.2005/Ojar     Added FEAT_DBG_UOAM_DefaultGW, UOAM_Mask
							  UOAM_CreateLoggingDataService	
1.28      02.05.2005/OjAr     Added FEAT_DBG _UOAM_EthernetPortMonitoring , 
							  _UOAM_Disable_TemperatureMngr
							  _Prof_Enable , _Prof_Monitored_PID1,
							  _Prof_Monitored_PID2, _Prof_Monitored_PID3,
							  _Prof_Monitored_PID4, _Prof_IPAddr,        
							  _Prof_Port, _Prof_trans_task_pri,
							  _Prof_RingBufferSize, _HWAPI_SELF_TEST								 
1.27      18.04.2005/AhJa     Added FEAT_DBG_UOAM _IpAddress, _MacAddress_UpperBytes,
                              MacAddress_LowerBytes, _PropertyFileReader, _MTPropertyFile
1.26      12.04.2005/Ojar     Added FEAT_DBG_UOAM  _Fault_Op_Disabled,
									 _LoggingDataService , _Temperature ,_Disable_PrintClimateInfo,
								     _ClimateControl, _Enable_RD_Fan_Ctrl, _MaxFanSpeed,             
								     _MinFanSpeed, _FanTxTemperature,_FanStartTemperature,     
								     _FanStopTemperature, _FanMaxTemperature, _FanDefaultSpeed
1.25      11.04.2005/ARNIKULA Header updated
1.24      24.03.2005/Ojar     Added CLM_Pid and DftKey
1.23      02.03.2005/OjAr     Added Kernel_Error_Handler , PowerSupply and DAPD_VD
1.22      15.02.2005/OjAr     Added Oic R&D switchs		 
1.21      24.01.2005/OjAr     Added PRINT_FILTER_SERIAL to enum PRINT_FILTER and 
                              FEAT_DBG
                              RFREL_INTERPROCESSOR , RFREL_SYSTEM ,    
                              RFREL_MANAGER , RFREL_PROPAGATION_DELAY_MONITOR ,
                              RFREL_POWER_MONITOR , RFREL_ANTENNA_CARRIER_RESOURCE ,
                              RFREL_ANTENNA_CARRIER_API
1.20      04.01.2005/OjAr     Added FEAT_DBG_UOAM_SOAP_GW_OP_MODE
1.19      29.12.2004/AhJa     Added FEAT_DBG_UOAM_MTPolling
1.18      13.12.2004/Ojar     Added FEAT_DBG  CLM_Period and Statistic_Logging  
1.17      29.11.2004/Ojar	  Added FEAT_DBG_ CreateReset, CreateSOAPGW, CreateFaultMngr,		
											  CreateStateSender, CreateLedMngr, CreateMtpMngr,			
											  CreatePolling, CreateSwMngr, CreateUpdateIsti,		
											  CreatePropertyFileRead	  
1.16      29.11.2004/Ojar	  Added FEAT_DBG_ BTSLogHandler, Middleware,TroubleShootingData,XMLParser,
							                  CLM_Print and CLM			
1.15      16.11.2004/Ojar     Added FEAT_DBG_Statistic_Service --> FEAT_DBG_HeapAlarmMaxBlockLimit 
1.14      11.10.2004/Ojar	  Added FEAT_DBG_UOAM_MTP_Manager, FEAT_DBG_UOAM_ResetHander
1.13      28.09.2004/Ojar     Added FEAT_DBG_UDPCP, FEAT_DBG_UDPCP_TX, FEAT_DBG_UDPCP_RX
							  FEAT_DBG_TX_VD, FEAT_DBG_RX_VD
1.12      13.09.2004/Ojar     Added FEAT_DBG_UOAM_Fault, FEAT_DBG_BtsTrace
          10.09.2004/Ojar     Added FEAT_DBG_UOAM_Bbb. Changed FEAT_DBG_UOAM_Soap_GW_Print_Level
							  to FEAT_DBG_UOAM_Soap_Gw_Prints
							  Added FEAT_DBG_UOAM_ModuleReadyIndCollector,
                              FEAT_DBG_UOAM_ModuleReadyIndSender and 
                              FEAT_DBG_UOAM_StateSender.
          08.09.2004/Ojar     Added FEAT_DBG_UOAM_Slave_Startup and 
                              FEAT_DBG_UOAM_Unit_startup prints
    	  30.08.2004/Ojar     Added "RFCtrl_VD" and "PlatformUtilitiesCtrl" DBG_FEATURE_STRING  
1.11      27.08.2004/Ojar     Added flag for Connection Manager and I2cApp  prints
1.10      17.08.2004/Ojar     Added flag for DFT tests, Logging Service and
							  Tassu Router prints							   
1.9       09.08.2004/JyPu     Added FEAT_DBG_UOAM_SWDL
1.8       03.08.2004/KSi      Added FEAT_DBG_RFCtrl_Vd and FEAT_DBG_PlatformUtilitiesCtrl
                              Removed old Helena time comments.
1.7       03.08.2004/ARNIKULA Updates based version 1.5 added
1.6       16.07.2004/Ojar     Added FEAT_DBG_PlatformUtilitiesCtrl
1.5       16.06.2004/MeVi     Added FEAT_DBG_Heap_Monitoring and 
                              FEAT_DBG_Allocation_Monitoring.
1.4       11.06.2004/JeBa     Added FEAT_DBG_SNS_Prints, FEAT_DBG_SNS_SLP_Prints
                              FEAT_DBG_RD_Parser and FEAT_DBG_UdpPrintIpAddr.
1.3       27.05.2004/JeBa     Added SNS configuration parameters.
                              Added UOAM specific parameters.
1.2       11.03.2004/OjAr     Added Get_RAD_param makro
1.1       09.03.2004/OjAr     Removed the defintion of the WN product
1.0       20.05.2003/TeA      Imported from Helena
// Old Helena time comments removed. Can found from older revision

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
#include <glo_def.h>

enum MON_SEVERITY
{
  MON_SEVERITY_ERROR    = 2,
  MON_SEVERITY_WARNING  = 3,
  MON_SEVERITY_INFO     = 4,
  MON_SEVERITY_DEBUG    = 5
};

#define DBG_SEVERITY_STRING { "????", "????", "ERROR", "WARNING", "INFO", "DEBUG" }

enum FEAT_DBG
{
  /* Feature Id for configuring SW functionality (CONF) and debug prints(DBG) 
     Default value is zero that means final release functionality
     NOTE: Update also DBG_FEATURE_STRING define below when adding some feature
     to enum FEAT_DBG             
     ------------------------------------------------------------------------ */
  FEAT_DBG_Generic,                      /* DBG: 1- enable non classified feature DBG, id for functions without any specific feature */
  FEAT_DBG_UdpPrintPort,                 /* 0 = Default UDP print port (50011) */                                         
                                         /* 49152 ... 65535 = User defined UDP print port */
  FEAT_DBG_HeapTrace,                    /* DBG: 0 - Disable heap trace */
                                         /* DBG: Positive value - Time in minutes to print out heap trace info */
                                         /* DBG: Negative value - Time in minutes to print out heap trace info and to collect heap statistics to file */
  
  FEAT_DBG_PrintFilter,                  /* DBG: 0 - NONE, 1 - RAM disk, 2 - RAM disk & UDP, 3 - RAM disk & UDP (debug prints included) */
  FEAT_DBG_Start_Log_Time_In_Mins,       /* DBG: 0- don't gather start up prints to log, else time when to stop*/
  FEAT_DBG_Start_Log_Size_In_KB,         /*DBG: Size of buffer to be used in ramdisk when start up prints are gathered */
  FEAT_DBG_Disable_Automatic_WDG,        /* CONF: 1 - Disable automatic start of watchdog */
  FEAT_DBG_mem_load_test_interval_ms,    /* 0 = No heap memory load test, otherwise interval of heap memory tests in ms */
  FEAT_DBG_HeapWaitQueueLen,             /* Specifies size for user blocks in wait queue */
  FEAT_DBG_HeapWaitBlockMaxSize,         /* Specifies maximum size of a user block kept in wait queue */
  FEAT_DBG_Heap_Walking,                 /* NOT USED !!! */
  FEAT_DBG_HWAPI_HEAP,                   /* DBG: 1- enable Heap monitoring related dbg prints */
  FEAT_DBG_LogHeapReset,                 /* 0 = Disables heap log file generation to /rom before heap exhaust reset */
  FEAT_DBG_HeapStatusPolling,            /* 0 = Disable heap status polling, otherwise heap status polling interval in ms */
  FEAT_DBG_HeapMaxFreeLimit,             /* Free heap limit in bytes for heap status polling reset */
  FEAT_DBG_HeapMaxBlockLimit,            /* Max free heap block size limit in bytes for heap status polling reset */
  FEAT_DBG_Mcu_Vd,                       /* 1- enable Mcu virtual device prints */ 
  FEAT_DBG_BootloaderBus_Vd,             /* 1- enable BootloaderBus virtual device prints */ 
  FEAT_DBG_Clk_B_Vd,                     /* 1- enable Clk_B virtual device prints */ 
  FEAT_DBG_Dsp_Vd,                       /* 1- enable Dsp virtual device prints */      
  FEAT_DBG_Eeprom_Vd,                    /* 1- enable Eeprom virtual device prints */ 
  FEAT_DBG_Fan_Vd,                       /* 1- enable Fan virtual device prints */ 
  FEAT_DBG_Flash_Vd,                     /* 1- enable Flash virtual device prints */ 
  FEAT_DBG_FrameNumberServer_Vd,         /* 1- enable FrameNumberServer virtual device prints */ 
  FEAT_DBG_I2cCtrl_Vd,                   /* 1- enable I2cCtrl virtual device prints */
  FEAT_DBG_I2cSwitch_Vd,                 /* 1- enable I2cSwitch virtual device prints */ 
  FEAT_DBG_InSpap_Vd,                    /* 1- enable InSpap virtual device prints */
  FEAT_DBG_IpStackCtrl_Vd,               /* 1- enable IpStackCtrl virtual device prints */
  FEAT_DBG_Led_Vd,                       /* 1- enable Led virtual device prints */
  FEAT_DBG_Mci_Vd,                       /* 1- enable Mci virtual device prints */
  FEAT_DBG_Mea_Vd,                       /* 1- enable Mea virtual device prints */
  FEAT_DBG_Mfe_Vd,                       /* 1- enable Mfe virtual device prints */
  FEAT_DBG_Msu_Vd,                       /* 1- enable Msu virtual device prints */
  FEAT_DBG_Predistortion_Vd,             /* 1- enable Predistortion virtual device prints */
  FEAT_DBG_RFTestLoop_Vd,                /* 1- enable RFTestLoop virtual device prints */
  FEAT_DBG_Thermometer_Vd,               /* 1- enable Thermometer virtual device prints */
  FEAT_DBG_Watchdog_Vd,                  /* 1- enable Watchdog virtual device prints */
  FEAT_DBG_XBlock_Vd,                    /* 1- enable XBlock virtual device prints */
  FEAT_DBG_SNS_Config_DA_Find,           /* SNS wait interval between repeating active DA (P-SNS) discovery: 1-10s */
  FEAT_DBG_SNS_Config_DA_Beat,           /* SNS DA (P-SNS) heartbeat so that SAs (L-SNS) passively detect new DAs (P-SNS): 1s-1day */
  FEAT_DBG_SNS_Config_Retry,             /* SNS wait interval before initial retransmission of multicast or unicast request: 1-10s */
  FEAT_DBG_SNS_Config_Retry_Max,         /* SNS max time to unicast request retransmission: 1s-1hrs */
  FEAT_DBG_SNS_Config_MC_Max,            /* SNS Max wait time for multicast query response: 1s-1hrs */
  FEAT_DBG_SNS_Config_Refresh_Limit,     /* SNS Minimum time between registration refreshments: 1s-18hrs */
  FEAT_DBG_UOAM_Soap_Log_Enable,         /* Soap Log Enable/Disable: >0 Enable, else Disable */
  FEAT_DBG_UOAM_Soap_Gw_Prints,		     /* 1- Enable Soap Gateway prints*/
  FEAT_DBG_SNS_Prints,                   /* 1- enable SNS prints */
  FEAT_DBG_SNS_SLP_Prints,               /* 1- enable SNS SLP prints */
  FEAT_DBG_EnablePostMortem,             /* 1- enable Post Mortem creation with all except Power resets */
  FEAT_DBG_UdpPrintIpAddr,               /* User defined UDP print IP address in Dec 4 format */
  FEAT_DBG_EnableHeapMonitoring,         /* 0 = BTS heap monitoring bs_heap disabled (default), 1 = heap monitoring enabled */
  FEAT_DBG_Allocation_Monitoring,        /* 1- enable allocation monitoring test */
  FEAT_DBG_PlatformUtilitiesCtrl,        /* 1- enable PlatformUtilitiesCtrl prints */
  FEAT_DBG_UOAM_Gateway,                 /* 1- enable Gateway prints */
  FEAT_DBG_UOAM_UpdateIsti,              /* 1- enable UpdateIsti */
  FEAT_DBG_UOAM_Led,                     /* 1- enable Led*/
  FEAT_DBG_UOAM_SWDL,                    /* 1 -enable SW DL prints */
  FEAT_DBG_DftCommonTests,               /* Common flag for DFT tests (1- enable) */
  FEAT_DBG_DftLTXTests,                  /* 1- enable LTX prints */
  FEAT_DBG_DftTM,                        /* 1- enable TestManager prints */
  FEAT_DBG_DftDWI,                       /* 1- enable DWI prints */
  FEAT_DBG_DftDWS,                       /* 1- enable DWS prints */
  FEAT_DBG_Logging_Service,              /* 1- enable Logging Service prints */ 
  FEAT_DBG_Tassu_Router,                 /* 1- enable Tassu Router prints */
  FEAT_DBG_UOAM_CMa,                     /* 1- enable Connection Manager prints */
  FEAT_DBG_I2cApp,                       /* 1- enable I2cApp prints */
  FEAT_DBG_RFCtrl_Vd,				     /* 1- enable RFCtrl virtual device prints */
  FEAT_DBG_UOAM_Slave_Startup,           /* 1- enable Slave Startup prints */
  FEAT_DBG_UOAM_Unit_startup,            /* 1- enable Unit Startup prints*/
  FEAT_DBG_UOAM_ModuleReadyIndCollector, /* 1- enable ModuleReadyIndCollector prints */
  FEAT_DBG_UOAM_ModuleReadyIndSender,    /* 1- enable ModuleReadyIndSender prints */
  FEAT_DBG_UOAM_StateSender, 		     /* 1- enable StateSender prints */
  FEAT_DBG_UOAM_Bbb,                     /* 1- enable UOAM_Bbb prints */
  FEAT_DBG_UOAM_Fault,                   /* see alarm_config.h for further details */
  FEAT_DBG_BtsTrace,                     /* 1- enable message tracing prints */
  FEAT_DBG_UDPCP,						 /* 1- enable UDPCP prints */
  FEAT_DBG_UDPCP_TX,					 /* 1- enable UDPCP_TX prints */
  FEAT_DBG_UDPCP_RX,					 /* 1- enable UDPCP_RX prints */
  FEAT_DBG_TX_VD,						 /* 1- enable TX_VD prints */
  FEAT_DBG_RX_VD,						 /* 1- enable RX_VD prints */
  FEAT_DBG_UOAM_MTP_Manager,             /* 1- enable MTP Manager prints*/
  FEAT_DBG_UOAM_ResetHandler,            /* 1- enable ResetHandler prints*/
  FEAT_DBG_Statistic_Service,            /* 1- enable Statistic Service */
  FEAT_DBG_Statistic_PollCylce,          /* Statistic Service Poll Cycle timeout ms */
  FEAT_DBG_Statistic_Print,              /* 1- enable Statistic Service prints */   
  FEAT_DBG_Statistic_FileCycle,          /* Statistic Service File Cycle timeout ms */ 
  FEAT_DBG_Statistic_FileCount,          /* Statistic Service File Count */ 
  FEAT_DBG_HeapAlarm,                    /* 1- enable Heap Alarms */ 
  FEAT_DBG_HeapAlarmMaxFreeLimit,        /* Free heap limit in bytes for heap status polling alarm */
  FEAT_DBG_HeapAlarmMaxBlockLimit,       /* Max free heap block size limit in bytes for heap status polling alarm */
  FEAT_DBG_CLM_Print,					 /* 1- enable Cpu load monitoring prints */
  FEAT_DBG_CLM,							 /* 1- enable Cpu loads measurement */
  FEAT_DBG_BTSLogHandler,				 /* 1- enable BTS Log handler prints*/
  FEAT_DBG_Middleware,					 /* 1- enable Middleware prints*/
  FEAT_DBG_TroubleShootingData, 		 /* 1- enable TroubleShootingData prints*/
  FEAT_DBG_XMLParser,					 /* 1- enable XML-parser prints*/
  FEAT_DBG_UOAM_CreateReset,			 /* 1- disable creating ResetHandler */
  FEAT_DBG_UOAM_CreateSOAPGW,			 /* 1- disable creating SOAP_GW */
  FEAT_DBG_UOAM_CreateFaultMngr,		 /* 1- disable creating FaultManagement */
  FEAT_DBG_UOAM_CreateStateSender,		 /* 1- disable creating StateSender */
  FEAT_DBG_UOAM_CreateLedMngr,			 /* 1- disable creating LedManagement */
  FEAT_DBG_UOAM_CreateMtpMngr,			 /* 1- disable creating FaultManagement */
  FEAT_DBG_UOAM_CreatePolling,			 /* 1- disable creating Polling */
  FEAT_DBG_UOAM_CreateSwMngr,			 /* 1- disable creating SwMngr */
  FEAT_DBG_UOAM_CreateUpdateIsti,		 /* 1- disable creating UpdateIsti */
  FEAT_DBG_UOAM_CreatePropertyFileRead,	 /* 1- disable creating PropertyFileReader */
  FEAT_DBG_CLM_Period,                   /* Cpuload Monitoring reporting period (min) */
  FEAT_DBG_Statistic_Logging,            /* 1- enable Statistic Service statistic UDP prints and log file creations*/ 
  FEAT_DBG_UOAM_MTPolling,               /* 1- MT on */
  FEAT_DBG_UOAM_SOAP_GW_OP_MODE,         /* 0=Normal, 1=TestMode (Accept all messages)*/
  FEAT_DBG_RFREL_INTERPROCESSOR,         /* 1- enable interprocessor prints */
  FEAT_DBG_RFREL_SYSTEM,    			 /* 1- enable rfrel sysytem prints*/
  FEAT_DBG_RFREL_MANAGER,				 /* 1- enable rfrel manager prints*/
  FEAT_DBG_RFREL_PROPAGATION_DELAY_MONITOR, /* 1- enable propagation delay monitoring prints*/
  FEAT_DBG_RFREL_POWER_MONITOR,			    /* 1- enable power monitor prints*/
  FEAT_DBG_RFREL_ANTENNA_CARRIER_RESOURCE,	/* 1- enable antenna carrier resource prints*/
  FEAT_DBG_RFREL_ANTENNA_CARRIER_API,		/* 1- enable antenna carrier api prints*/
  FEAT_DBG_Oic_RM_ID,						/* Test RM ID */
  FEAT_DBG_Oic_Vd,							/* 1- enable oic vd prints*/
  FEAT_DBG_Oic_RD_SWITCH,					/* 1- use test RMID       */
  FEAT_DBG_DAPD_VD,						    /* 1- enable DAPD_VD prints */
  FEAT_DBG_KernelErrorHandler, 				/* 1- enable KernelErrorHandler */ 
  FEAT_DBG_HWREL_PowerSupply,				/* 1- enable HwRel Power Supply prints*/
  FEAT_DBG_CLM_Pid,							/* 1- enable Pid level meausurement */
  FEAT_DBG_DftKey,                          /* Misc DFT features in customer SW, 0: disabled, 1: enabled */
  FEAT_DBG_UOAM_Fault_Op_Disabled,			/* 1- disable Fault Management alarm sending functionality */
  FEAT_DBG_UOAM_LoggingDataService,			/* 1- enable UOAM LoggingDataService prints*/
  FEAT_DBG_UOAM_Temperature,				/* 1- enables temperature management debug prints.*/
  FEAT_DBG_UOAM_Disable_PrintClimateInfo,	/* 1- disable climate debug prints */
  FEAT_DBG_UOAM_ClimateControl,				/* 1- enable climate control fault prints*/
  FEAT_DBG_UOAM_Enable_RD_Fan_Ctrl,         /* 1- Enables Fan control by R&D switch */
  FEAT_DBG_UOAM_MaxFanSpeed,                /* Fan max RPM */
  FEAT_DBG_UOAM_MinFanSpeed,                /* Fan relative min speed (e.g. 20%) */
  FEAT_DBG_UOAM_FanTxTemperature,           /* Fan Tx temperature */
  FEAT_DBG_UOAM_FanStartTemperature,        /* Fan start temperature */
  FEAT_DBG_UOAM_FanStopTemperature,         /* Fan stop temperature */
  FEAT_DBG_UOAM_FanMaxTemperature,          /* Fan maximum temperature */
  FEAT_DBG_UOAM_FanDefaultSpeed,            /* Fan relative default speed (e.g. 60%) */
  FEAT_DBG_UOAM_IpAddress,                  /* IP address for IP Stack initialization, for testing */
  FEAT_DBG_UOAM_MacAddress_UpperBytes,      /* Upper Bytes of MAC Address (e.g. MAC address: 02-00-00-00-06-01, type 0x02000000) */
  FEAT_DBG_UOAM_MacAddress_LowerBytes,      /* Lower Bytes of MAC Address (e.g. MAC address: 02-00-00-00-06-01, type 0x06010000) NOTE! Last two bytes must be zeros! */
  FEAT_DBG_UOAM_PropertyFileReader,         /* 1- enable property file reader prints */
  FEAT_DBG_UOAM_MTPropertyFile,             /* 1- MT on*/
  FEAT_DBG_UOAM_EthernetPortMonitoring,     /*Set first bit for monitoring MCU,second for monitoring Filter1, and third for Filter2*/
  FEAT_DBG_UOAM_Disable_TemperatureMngr,	/* 1- Disable Starting Temperature Management Statechart*/
  FEAT_DBG_Prof_Enable,                     /* Enables profile data handling */
  FEAT_DBG_Prof_Monitored_PID1,             /* PID of the monitored process for Function Execution Logger or 0, if all */
  FEAT_DBG_Prof_Monitored_PID2,             /* PID of the monitored process for Function Execution Logger */
  FEAT_DBG_Prof_Monitored_PID3,             /* PID of the monitored process for Function Execution Logger */
  FEAT_DBG_Prof_Monitored_PID4,             /* PID of the monitored process for Function Execution Logger */
  FEAT_DBG_Prof_IPAddr,                     /* IP-address for Function Execution Logger where to send UDP-frames */
  FEAT_DBG_Prof_Port,                       /* IP-port for Function Execution Logger where to send UDP-frames */
  FEAT_DBG_Prof_trans_task_pri,             /* Priority of transmission task */
  FEAT_DBG_Prof_RingBufferSize,             /* Size of ring buffer in bytes */
  FEAT_DBG_HWAPI_SELF_TEST,					/* 1- enable HW API self test */
  FEAT_DBG_UOAM_CreateLoggingDataService,	/* 1- disable creating LoggingDataService */
  FEAT_DBG_UOAM_DefaultGW,                  /* Default gateway for initializing IP Stack */
  FEAT_DBG_UOAM_Mask,                       /* Mask for initializing IP Stack */
  FEAT_DBG_HWREL_SCT,						/* enable SCT prints */
  FEAT_DBG_UOAM_Fault_AcksNotChecked,		/* enable checking akcknowledgements */
  FEAT_DBG_HWREL_FaultHandler,				/* enable HwRel FaultHandel printns */
  FEAT_DBG_UOAM_Disable_Fan_Ctrl,			/* Disable UOAM Fan control */
  FEAT_DBG_UOAM_CreateEventSender,          /* 1 - enable creating Eventsender application*/ 
  FEAT_DBG_UOAM_DataStorage,                /* Enable DataStorage prints */
  FEAT_DBG_UOAM_Fault_DisableFaultHistory,  /* Disable UOAM Fault History */
  FEAT_DBG_UOAM_Fault_EnableLoadTestPrints, /* not used anymore, use FEAT_DBG_UOAM_Fault instead */ 
  FEAT_DBG_Oic_PI_Delay,					/* Test PI Delay */
  FEAT_DBG_TX_Disable_Protection,           /* Disables autoshutdown after alarms */
  FEAT_DBG_HeapTracePID,                    /* At runtime this flag can be set with BTSlog tool. Full monitor mode is set for this pid */
  FEAT_DBG_RX_TEMPERATURE_FACTOR,			/* Rx temperature factor */
  FEAT_DBG_RX_CALIB_TEMPERATURE,			/* Rx calib temperature */
  FEAT_DBG_DAPD_SWITCH,                     /* R&D switch for dapd VD */
  FEAT_DBG_MaxNumOfFeat                     /* Keep this at last line */                
};


/* DBG_FEATURE_STRING define used in OAM dbg_prints. Remember to update this to
    match enum FEAT_DBG above. */
#define DBG_FEATURE_STRING {"GEN", "UDPPRINTPORT", "HEAP_TRACE", \
                            "PRINTFILTER", "STARTLOG_TIME","STARTLOG_SIZE",\
                            "WDOG", "MEM_LOAD_TEST", "HEAPLEN", "HEAPSIZE",\
                            "HEAPWALK", "HEAP", "LOG_HEAP_RESET","HEAP_POLL", "HEAP_FREE_LIMIT", \
                            "HEAP_BLOCK_LIMIT", "MCU_VD", "BootloaderBus_VD", "Clk_B_VD", \
                            "Dsp_VD", "Eeprom_Vd", "Fan_VD", "Flash_VD", \
                            "FrameNumberServeer_VD", "I2cCtrl_VD", "I2cSwitch_VD", "InSpap_VD", \
                            "IpStackCtrl_VD", "Led_VD", "Mci_VD", "Mea_VD", "Mfe_VD", \
                            "Msu_VD", "Predistortion_VD", "RFTestLoop_VD", "Thermometer_VD", \
                            "Watchdog_VD", "XBlock_VD", "CONFIG_DA_FIND", "CONFIG_DA_BEAT", \
                            "CONFIG_RETRY", "CONFIG_RETRY_MAX", "CONFIG_MC_MAX", "CONFIG_REFRESH_LIMIT", \
                            "UOAM_Soap_Log_Enable", "UOAM_Soap_GW_Print_Level", "SNS_Prints", \
                            "SNS_SLP_Prints", "EnablePostMortem", "UdpPrintIpAddr", \
                            "Heap_Monitoring","FEAT_DBG_Allocation_Monitoring", "PlatformUtilitiesCtrl", \
                            "UOAM_Gateway", "UOAM_UpdateIsti", "UOAM_Led","UOAM_SWDL",\
                            "DftCommonTests", "DftLTXTests", "DftTM", "DftDWI", "DftDWS",\
                            "Logging_Service","Tassu_Router", "UOAM_CMa", "I2cApp", "RFCtrl_VD",\
                            "UOAM_Slave_Startup", "UOAM_Unit_startup", "UOAM_ModuleReadyIndCollector",\
                            "UOAM_ModuleReadyIndSender", "UOAM_StateSender", "UOAM_BBB", "UOAM_Fault",\
                            "BtsTrace", "UDPCP", "UDPCP_TX", "UDPCP_RX", "TX_VD", "RX_VD",\
                            "UOAM_MTP_Manager", "UOAM_ResetHander","Statistic_Service","Statistic_PollCylce",\
                            "Statistic_Print","Statistic_FileCycle","Statistic_FileCount","HeapAlarm",\
                            "HeapAlarmMaxFreeLimit","HeapAlarmMaxBlockLimit","CLM_Print","CLM",\
							"BTSLogHandler","Middleware","TroubleShootingData","XMLParser",\
							"UOAM_CreateReset","UOAM_CreateSOAPGW",\
                            "UOAM_CreateFaultMngr","UOAM_CreateStateSender","UOAM_CreateLedMngr",\
                            "UOAM_CreateMtpMngr","UOAM_CreatePolling","UOAM_CreateSwMngr",\
                            "UOAM_CreateUpdateIsti","UOAM_CreatePropertyFileRead","CLM_Period","Statistic_Logging",\
                            "UOAM_MTPolling","UOAM_SOAP_GW_OP_MODE","RFREL_interprosessor","RFREL_system","RFREL_manager",\
                            "RFREL_propagation_delay_monitor","RFREL_power_monitor","RFREL_antenna_carrier_resource",\
                            "RFREL_antenna_carrier_api","OIC_RM_ID","OIC_VD","OIC_RD","DAPD_VD",\
                            "Kernel_Error_Handler","HWREL_PowerSupply", "CLM_Pid", "DftKey", "FEAT_DBG_UOAM_Fault_Op_Disabled",\
                            "UOAM_LogginDataService","UOAM_Temperature",\
                            "UOAM_Disable_PrintClimateInfo","UOAM_ClimateControl","UOAM_Enable_RD_Fan_Ctrl","UOAM_MaxFanSpeed",\
                            "UOAM_MinFanSpeed","UOAM_FanTxTemperature","UOAM_FanStartTemperature",\
                            "UOAM_FanStopTemperature","UOAM_FanMaxTemperature","UOAM_FanDefaultSpeed",\
                            "UOAM_IpAddress","UOAM_MacAddress_UpperBytes","UOAM_MacAddress_LowerBytes",\
                            "UOAM_PropertyFileReader","UOAM_MTPropertyFile", "UOAM_EthernetPortMonitoring",\
                            "Disable_TemperatureMngr","PROF_ENABLED","MONITORED_PID1","MONITORED_PID2",\
                            "MONITORED_PID3","MONITORED_PID4","PROF_IP_ADDRESS","PROF_PORT", \
                            "TRANS_TASK_PRI","RING_BUFFER_SIZE","HWAPI_SELF_TEST","UOAM_CreateLoggingDataService",\
                            "UOAM_DefaultGW","UOAM_Mask","HwRel_SCT_Test","FEAT_DBG_UOAM_Fault_AcksNotChecked",\
                            "HWREL_FaultHandler","UOAM_Disable_Fan_Ctrl", "UOAM_CreateEventSender", "UOAM_DataStorage",\
							 "UOAM_DisableFaultHistory", "UOAM_Fault_EnableLoadTestPrints", "Oic_PI_Delay", "TX_Disable_Protection" ,\
							 "HeapTracePID", "Rx_Temperature_factor","Rx_Calib_temperature","Dapd r&d switch"  }

/* Enumeration for interpreting FEAT_DBG_PrintFilter in sw_conf_table.
   Note: severity level filtering is supported only at higher level application printing */
enum PRINT_FILTER
{
  PRINT_FILTER_NONE = 0,  /* no log data to UPD port & RAM disk - default */
  PRINT_FILTER_RAMDISK,   /* INFO, WARNING and ERROR severity level printouts 
                             into RAM disk (startup log & crashdump log) */
  PRINT_FILTER_UDP_INFO,  /* same as previous but also to UDP printouts */
  PRINT_FILTER_UDP_DBG,    /* same as previous but DEBUG severity printouts 
                             (depending on selected feature) also included */
  PRINT_FILTER_SERIAL   /* same as previous but enables also serial print channel */
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

extern i32 GetRADParam(u32 id);

/* Macro to be used to get RAD params by applications */
#define Get_RAD_param(x) (GetRADParam(x))

/*Macro to be used by logging service to get RAD params without waiting semaphore */
#define Get_RAD_param_nowait(x) (sw_conf_table[x])

#ifdef __cplusplus
}
#endif

#endif /* SW_CONF_TABLE	*/


/***********************************************************************
* Development Workset : FLEXIBTS:SW_ENV_WS
*
* Design Part         : PLATFORM
*
* Description         : SW Configuration table defintion file from Helena 
*                       for porting support.
*
* Standard Notation   : -
*
* Reference           : -
*
* Parameters          : -
*
*
* Additional Information : -
* Definition Provided by : TRAWLER
* 
***********************************************************************/

