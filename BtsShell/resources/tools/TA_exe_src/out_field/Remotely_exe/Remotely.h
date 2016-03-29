/**************************************************************************/
/* LabWindows/CVI User Interface Resource (UIR) Include File              */
/* Copyright (c) National Instruments 2013. All Rights Reserved.          */
/*                                                                        */
/* WARNING: Do not add to, delete from, or otherwise modify the contents  */
/*          of this include file.                                         */
/**************************************************************************/

#include <userint.h>

#ifdef __cplusplus
    extern "C" {
#endif

     /* Panels and Controls: */

#define  CONFIG                           1       /* callback function: ConfigExit */
#define  CONFIG_BOX                       2       /* control type: textBox, callback function: (none) */
#define  CONFIG_SAVE                      3       /* control type: command, callback function: Save */
#define  CONFIG_EDIT                      4       /* control type: command, callback function: Edit */

#define  FILE_ITEM                        2       /* callback function: Item_Exit */
#define  FILE_ITEM_SCFC                   2       /* control type: radioButton, callback function: (none) */
#define  FILE_ITEM_SWCONFIG               3       /* control type: radioButton, callback function: (none) */
#define  FILE_ITEM_SEARCH                 4       /* control type: radioButton, callback function: (none) */
#define  FILE_ITEM_TECHLOGS               5       /* control type: radioButton, callback function: (none) */
#define  FILE_ITEM_VENDOR                 6       /* control type: radioButton, callback function: (none) */
#define  FILE_ITEM_SELFDEFI               7       /* control type: radioButton, callback function: (none) */
#define  FILE_ITEM_SYSINFO                8       /* control type: radioButton, callback function: (none) */
#define  FILE_ITEM_HWF                    9       /* control type: radioButton, callback function: (none) */
#define  FILE_ITEM_CONFIG                 10      /* control type: radioButton, callback function: (none) */
#define  FILE_ITEM_DECORATION             11      /* control type: deco, callback function: (none) */
#define  FILE_ITEM_TEXTMSG                12      /* control type: textMsg, callback function: (none) */
#define  FILE_ITEM_DECORATION_3           13      /* control type: deco, callback function: (none) */
#define  FILE_ITEM_DECORATION_2           14      /* control type: deco, callback function: (none) */
#define  FILE_ITEM_TEXTMSG_3              15      /* control type: textMsg, callback function: (none) */
#define  FILE_ITEM_TEXTMSG_2              16      /* control type: textMsg, callback function: (none) */
#define  FILE_ITEM_S_FILENAME             17      /* control type: string, callback function: (none) */
#define  FILE_ITEM_S_FILEPATH             18      /* control type: string, callback function: (none) */
#define  FILE_ITEM_SELFDEFIFILE           19      /* control type: string, callback function: (none) */
#define  FILE_ITEM_SELFDEFIPATH           20      /* control type: string, callback function: (none) */
#define  FILE_ITEM_FILTER                 21      /* control type: string, callback function: (none) */

#define  OUTPUTVIEW                       3       /* callback function: ViewExit */
#define  OUTPUTVIEW_OUTPUTBOX             2       /* control type: textBox, callback function: (none) */
#define  OUTPUTVIEW_TABLE                 3       /* control type: table, callback function: (none) */

#define  PANEL                            4       /* callback function: PBExit */
#define  PANEL_TEXTBOX                    2       /* control type: textBox, callback function: (none) */
#define  PANEL_OUTPUT                     3       /* control type: command, callback function: ViewOutput */
#define  PANEL_LED                        4       /* control type: LED, callback function: (none) */
#define  PANEL_TAB                        5       /* control type: tab, callback function: (none) */

     /* tab page panel controls */
#define  BBUCOMMON_DOWNLOAD               2       /* control type: command, callback function: DownLoad */
#define  BBUCOMMON_UPDATEALLPUT           3       /* control type: command, callback function: UpdateAllPut */
#define  BBUCOMMON_ENABLEPORT             4       /* control type: command, callback function: EnablePort */
#define  BBUCOMMON_SENDCMD                5       /* control type: command, callback function: SendCmd */
#define  BBUCOMMON_CONFIGCMD              6       /* control type: command, callback function: ConfigCMD */
#define  BBUCOMMON_UPLOAD                 7       /* control type: command, callback function: UpLoad */
#define  BBUCOMMON_DECORATION_8           8       /* control type: deco, callback function: (none) */
#define  BBUCOMMON_DECORATION_9           9       /* control type: deco, callback function: (none) */
#define  BBUCOMMON_DECORATION_10          10      /* control type: deco, callback function: (none) */
#define  BBUCOMMON_DECORATION_11          11      /* control type: deco, callback function: (none) */

     /* tab page panel controls */
#define  CUSTOM_CHECKSFP                  2       /* control type: command, callback function: CheckSFP */
#define  CUSTOM_CHECKUPTIME               3       /* control type: command, callback function: CheckUptime */
#define  CUSTOM_ANALYZEFILTER             4       /* control type: command, callback function: AnalyzeFilter */
#define  CUSTOM_FETCHLOGS                 5       /* control type: command, callback function: FetchLogs */
#define  CUSTOM_UPDATEVENDOR              6       /* control type: command, callback function: UpdateVendor */
#define  CUSTOM_SEARCHFILE                7       /* control type: command, callback function: SearchFile */
#define  CUSTOM_RECORDUPTIME              8       /* control type: command, callback function: RecordUptime */
#define  CUSTOM_DECORATION_10             9       /* control type: deco, callback function: (none) */
#define  CUSTOM_DECORATION_12             10      /* control type: deco, callback function: (none) */
#define  CUSTOM_DECORATION_11             11      /* control type: deco, callback function: (none) */
#define  CUSTOM_DECORATION_9              12      /* control type: deco, callback function: (none) */
#define  CUSTOM_DECORATION_8              13      /* control type: deco, callback function: (none) */
#define  CUSTOM_UPDATENAME                14      /* control type: string, callback function: (none) */

     /* tab page panel controls */
#define  RRUCOMMON_GETRRULOG              2       /* control type: command, callback function: GetRruLog */
#define  RRUCOMMON_ENABLEVSWR             3       /* control type: command, callback function: EnableVSWR */
#define  RRUCOMMON_ENABLEOPT              4       /* control type: command, callback function: EnableOPT */
#define  RRUCOMMON_DECORATION_8           5       /* control type: deco, callback function: (none) */
#define  RRUCOMMON_DECORATION_10          6       /* control type: deco, callback function: (none) */


     /* Control Arrays: */

#define  CTRLARRAY                        1

     /* Menu Bars, Menus, and Menu Items: */

#define  MENUBAR                          1
#define  MENUBAR_CONFIG                   2
#define  MENUBAR_CONFIG_CONFIGIP          3       /* callback function: Config */
#define  MENUBAR_CONFIG_CONFIGITEM        4       /* callback function: ConfigItem */
#define  MENUBAR_HELP                     5       /* callback function: Help */


     /* Callback Prototypes: */

int  CVICALLBACK AnalyzeFilter(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK CheckSFP(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK CheckUptime(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
void CVICALLBACK Config(int menubar, int menuItem, void *callbackData, int panel);
int  CVICALLBACK ConfigCMD(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK ConfigExit(int panel, int event, void *callbackData, int eventData1, int eventData2);
void CVICALLBACK ConfigItem(int menubar, int menuItem, void *callbackData, int panel);
int  CVICALLBACK DownLoad(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK Edit(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK EnableOPT(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK EnablePort(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK EnableVSWR(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK FetchLogs(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK GetRruLog(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
void CVICALLBACK Help(int menubar, int menuItem, void *callbackData, int panel);
int  CVICALLBACK Item_Exit(int panel, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK PBExit(int panel, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK RecordUptime(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK Save(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK SearchFile(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK SendCmd(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK UpdateAllPut(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK UpdateVendor(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK UpLoad(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK ViewExit(int panel, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK ViewOutput(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);


#ifdef __cplusplus
    }
#endif
