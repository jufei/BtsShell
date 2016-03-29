#include "inifile.h"
#include <formatio.h>
#include <ansi_c.h>
#include <utility.h>
#include <cvirte.h>		
#include <userint.h>
#include "Remotely.h"

static int menubarHandle; 
static int panelHandle;
static int bbucommonHandle;
static int rrucommonHandle;
static int customizingHandle;
static int outputHandle; 
static int configHandle;
static int itemHandle;
IniText inihandle; 
static int Threadflag=0;
static void *threadfunctiondata="";  

static int ExecutableProcess(char *cmd, char *checkpoint);
void SetLed(char *status, int flag);
static int WriteOupputBox(int flag);
static int ReadConfigFile( int item);

static int WriteConfig(int flag);
void DimAction(int flag);
static int Initial(int item, int flag);
//static int ItemInfo(int flag);
char *readfoldername(void);
void WriteLog(void);
void WriteLogDateTime(int fileHandle);
void KillSubprocess(void);
char *GetItemInfo(int flag);


int main (int argc, char *argv[])
{
	if (InitCVIRTE (0, argv, 0) == 0)
		return -1;	/* out of memory */
	if ((panelHandle = LoadPanel (0, "Remotely.uir", PANEL)) < 0)
		return -1;
	if ((configHandle = LoadPanel (0, "Remotely.uir", CONFIG)) < 0)
		return -1;
	if ((itemHandle = LoadPanel (0, "Remotely.uir", FILE_ITEM)) < 0)
		return -1;
	menubarHandle = GetPanelMenuBar (panelHandle); 
	GetPanelHandleFromTabPage (panelHandle, PANEL_TAB, 0, &bbucommonHandle);
	GetPanelHandleFromTabPage (panelHandle, PANEL_TAB, 1, &rrucommonHandle); 
	GetPanelHandleFromTabPage (panelHandle, PANEL_TAB, 2, &customizingHandle); 
	SetActiveTabPage (panelHandle, PANEL_TAB, 0);
	if(Initial(0, 0)<0 || Initial(1, 0)<0 || Initial(2, 0)<0 || Initial(3, 0)<0)
	{
		SetLed("Read file type information from config.ini to UI error,please try again!",0); 
	}
	WriteLog();
	DisplayPanel (panelHandle);
	RunUserInterface ();
																	 
	return 0;
}

int CVICALLBACK PBExit (int panel, int event, void *callbackData,
		int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_CLOSE:
			WriteLog();
			KillSubprocess(); 
			QuitUserInterface (0);
			if (panelHandle)
		    {
               DiscardPanel (panelHandle);
	        }
			if (configHandle)
			{
				DiscardPanel(configHandle);
			}
			if (itemHandle)
			{
				DiscardPanel(itemHandle);
			}
			break;
	}
	return 0;
}

int CVICALLBACK ViewOutput (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	
	switch (event)
	{
		case EVENT_COMMIT:
			if ((outputHandle = LoadPanel (0, "Remotely.uir", OUTPUTVIEW)) < 0)
				return -1;
			 DimAction(1); 
		//	 ResetTextBox (panelHandle, PANEL_TEXTBOX, "");  
			 if(WriteOupputBox(0))
			 {
			 	InstallPopup(outputHandle);
			 }
			 else
			 {
			  SetCtrlVal (panelHandle, PANEL_TEXTBOX, "Read data from output.txt error,please check it by manual!\r\n");
			 }
			 DimAction(0);
			break;
	}
	return 0;
}

int CVICALLBACK ViewExit (int panel, int event, void *callbackData,
		int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_CLOSE:
			RemovePopup (outputHandle);
			if (outputHandle)
		    {
               DiscardPanel (outputHandle);
	        }
			break;
	}
	return 0;
}

int CVICALLBACK ConfigExit (int panel, int event, void *callbackData,
		int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_CLOSE:
			 RemovePopup (configHandle); 
			break;
	}
	return 0;
}
int CVICALLBACK Item_Exit (int panel, int event, void *callbackData,
		int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_CLOSE:
			 if((Initial(1, 1)>=0) && (Initial(2, 1)>=0) && (Initial(3, 1)>=0))	 // write file type inforamtion to config.ini
			 {
			 	RemovePopup (itemHandle);
			 }
			 else
			 {
			    SetLed("Write file type or filter information from UI to config.ini error,please try again!",0);  
			 }
			break;
	}
	return 0;
}

int CVICALLBACK DownLoad (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			int status; char cmd[100]; char *info = "";   char *buffer = "";   char *folder = "";   
			
			 info = GetItemInfo(1);
			 buffer=(char*)malloc(100);
	 		 memset(buffer,0,100);
			 sprintf(buffer,"Do you want to download files: (%s) now?",info);
			 if (ConfirmPopup ("Download Action",buffer)) 
			 {
				 memset(cmd,0,100);
				 strcpy(cmd,"RemoteAction.exe -d:all");
				 DimAction(1); 
				 status = ExecutableProcess(cmd,"@action done@");
				 if (status)
				 {
			 	  	memset(buffer,0,100);
				  	folder= readfoldername();			// read file saved folder name
				  	sprintf(buffer,"Download files: (%s) finished! folder is:%s",info,folder);
				  	SetLed(buffer,1);
				}
				else
				{
 				    memset(buffer,0,100); 
				    sprintf(buffer,"Download files: (%s) failed,pls check detail info!",info); 	
				    SetLed(buffer,0); 
				}
				DimAction(0);
			 }
			 free(buffer);
			break;
	}
	return 0;
}
/*
int CVICALLBACK UpdateAllGet (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			int status; char cmd[100]; char *info = "";   char *buffer = "";   char *folder = "";   
			
			 info = GetItemInfo(1);		// get file item selection
			 buffer=(char*)malloc(100);
	 		 memset(buffer,0,100);
			 sprintf(buffer,"Do you want to Update-Get files: (%s) now?",info);
			 if (ConfirmPopup ("Update-Get Action",buffer)) 
			 {
				memset(cmd,0,100);
				strcpy(cmd,"RemoteAction.exe -d:all");
				DimAction(1); 
				status = ExecutableProcess(cmd,"@action done@");
				if (status)
				{
			 	  memset(buffer,0,100);
				  folder= readfoldername();			// read file saved folder name
				  sprintf(buffer,"Update-Get files: (%s) finished! folder is:%s",info,folder);
				  SetLed(buffer,1);
		
				}
				else
				{
				   memset(buffer,0,100); 
				   sprintf(buffer,"Update-Get files: (%s) failed,pls check detail info!",info); 	
				   SetLed(buffer,0); 
				}
				DimAction(0);
			 }
			 free(buffer);
			break;
	}
	return 0;
}
		 */
int CVICALLBACK UpLoad (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	int index=0;   int status; char cmd[100]; 
	switch (event)
	{
		case EVENT_COMMIT:
			int status; char cmd[100]; char *info = "";   char *buffer = ""; 
			
			 info = GetItemInfo(1);
			 buffer=(char*)malloc(100);
	 		 memset(buffer,0,100);
			 sprintf(buffer,"Do you want to upload files: (%s) now?",info);
			 if (ConfirmPopup ("Upload Action",buffer)) 
			 {
				memset(cmd,0,100);
				strcpy(cmd,"RemoteAction.exe -u:all");
				DimAction(1); 
				status = ExecutableProcess(cmd,"@action done@");
				if (status)
				{
					memset(buffer,0,100);
				    sprintf(buffer,"Upload files: (%s) finished",info);
				    SetLed(buffer,1);
				}
				else
				{
					memset(buffer,0,100);
				    sprintf(buffer,"Upload files: (%s) failed,pls check detail info!",info); 	
				    SetLed(buffer,0);  
				}
				DimAction(0);
			 }
			 free(buffer);
			break;
	}
	return 0;
}
int CVICALLBACK UpdateAllPut (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 int status; char cmd[100];  char *info = "";  char *buffer = "";
			 
			 info = GetItemInfo(1);		// get file item selection
			 buffer=(char*)malloc(100);
	 		 memset(buffer,0,100);
			 sprintf(buffer,"Do you want to Update-Put files: (%s) now?",info);
		
			 if (ConfirmPopup ("Update-Put All Files",buffer)) 
			 {
				memset(cmd,0,100);
				strcpy(cmd,"RemoteAction.exe -u:allupdate");
				DimAction(1); 
				status = ExecutableProcess(cmd,"@action done@");
				if (status)
				{
					memset(buffer,0,100);
					sprintf(buffer,"Update-Put files: (%s) finished!",info);  
				    SetLed(buffer,1);
				}
				else
				{
					memset(buffer,0,100); 
				    sprintf(buffer,"Update-Put files: (%s) failed,pls check detail info!",info); 	
				    SetLed(buffer,0);
				}
				DimAction(0);
			 }
			 free(buffer);
			break;
	}
	return 0;
}

int CVICALLBACK SendCmd (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 int status; char cmd[100];
			 if (ConfirmPopup ("Send Command","Do you want to send command now?")) 
			 {
				memset(cmd,0,100);
				strcpy(cmd,"RemoteAction.exe -c:normal");
				DimAction(1); 
				status = ExecutableProcess(cmd,"@action done@");
				if (status)
				{
				  SetLed("Action finished!",1);
				}
				else
				{
				  SetLed("Action failed,please check detail info",0); 
				}
				DimAction(0);
			 }
		
			break;
	}
	return 0;
}

int CVICALLBACK UpdateVendor (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	char *name = "";	int ret=0;
	switch (event)
	{
		case EVENT_COMMIT:
			 int status; char cmd[100];
			 
			 name=(char*)malloc(100); 
			 memset(name,0,100);
			 GetCtrlVal (customizingHandle, CUSTOM_UPDATENAME, name); 
			 ret = strlen(name);
						 
			 if ((NULL != (strstr (name, ".xml")))&&(ret != 4))
			 {
				 if (ConfirmPopup ("Update Vendor","Do you want to update vendor now?")) 
				 {
					memset(cmd,0,100);
					strcpy(cmd,"RemoteAction.exe -d:vendor");
					DimAction(1); 
					status = ExecutableProcess(cmd,"@action done@");
					if (status)
					{
						  SetLed("Get vendor finished!",1);
						  if(Initial(0, 1)<0)    //  write local vendor name to config.ini 
						  {
						    SetLed("Write local vendor name to config.ini error,please try again!",0);   
						  }
						  else
						  {
							  if(ConfirmPopup ("Confirm carrying on...","Make sure upgrading finished then continue updating process?"))
							  {
								    memset(cmd,0,100);
									strcpy(cmd,"RemoteAction.exe -u:update");
									status = ExecutableProcess(cmd,"@action done@");
									if (status)
									{
										DimAction(0); 
									    SetLed("Update vendor finished!",1); 
									}
							  }
							  else
							  {
							   DimAction(0); 
							   SetLed("U canceled the update process...",0);   
							  }
						  }
					}
					else
					{
					  SetLed("Action failed,please check detail info",0); 
					}
					DimAction(0);
				 }
			 }
			 else
			 {
				 MessagePopup ("Error", "Please confirm you have input vendor name(.xml) before updating!");
			 }
			 
			 free(name);
			 
			break;
	}
	return 0;
}

int CVICALLBACK EnablePort (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 int status; char cmd[100];
			 if (ConfirmPopup ("Enable Port","Do you want to enable SSH and RD port now?")) 
			 {
				memset(cmd,0,100);
				strcpy(cmd,"enableport.exe -e:all");
				DimAction(1); 
				status = ExecutableProcess(cmd,"@action done@");
				if (status)
				{
				  SetLed("Action finished!",1);
				}
				else
				{
				  SetLed("Action failed,please check detail info",0); 
				}
				DimAction(0);
			 }
			break;
	}
	return 0;
}

int CVICALLBACK EnableOPT (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 int status; char cmd[100];
			 if (ConfirmPopup ("Enable OPT","Do you want to enable OPT now?")) 
			 {
				memset(cmd,0,100);
				strcpy(cmd,"RemoteAction.exe -c:opt");
				DimAction(1); 
				status = ExecutableProcess(cmd,"@action done@");
				if (status)
				{
				    SetLed("Enable opt finished!",1); 
				}
				else
				{
				   SetLed("Action failed,please check detail info",0); 
				}
				DimAction(0);
			 }
			break;
	}
	return 0;
}
int CVICALLBACK EnableVSWR (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 int status; char cmd[100];
			 if (ConfirmPopup ("Enable VSWR","Do you want to enable vswr now?")) 
			 {
				memset(cmd,0,100);
				strcpy(cmd,"RemoteAction.exe -c:vswr");
				DimAction(1); 
				status = ExecutableProcess(cmd,"@action done@");
				if (status)
				{
				    SetLed("Enable vswr finished!",1);
				}
				else
				{
				    SetLed("Action failed,please check detail info",0); 
				}
				DimAction(0);
			 }
			break;
	}
	return 0;
}

int CVICALLBACK CheckCmd (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
		
			
			break;
	}			   
	return 0;
}

int CVICALLBACK Edit (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 if (0==SetCtrlAttribute (configHandle, CONFIG_BOX, ATTR_CTRL_MODE, VAL_HOT))
			 {
				SetCtrlAttribute (configHandle, CONFIG_BOX, ATTR_TEXT_BGCOLOR, VAL_WHITE);
			  	SetCtrlVal (panelHandle, PANEL_TEXTBOX,  "You can edit bbuip box now...!\r\n");       
			 }   
			break;
	}
	return 0;
}

int CVICALLBACK Save (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	char *value = "";
	switch (event)
	{
		case EVENT_COMMIT:
			 value = (char*)malloc(50);
			 memset(value,0,50);
			 GetPanelAttribute (configHandle, ATTR_TITLE, value);
			 if (strcmp("CheckBBUIP", value)==0)
			 {
				 if(1==WriteConfig(MENUBAR_CONFIG_CONFIGIP))
			 	{
					SetCtrlAttribute (configHandle, CONFIG_BOX, ATTR_TEXT_BGCOLOR, VAL_OFFWHITE);
					SetCtrlAttribute (configHandle, CONFIG_BOX, ATTR_CTRL_MODE, VAL_INDICATOR);
			 		SetCtrlVal (panelHandle, PANEL_TEXTBOX,  "Save bbuip.txt successfully!\r\n");  
			 	}
			 
			 }
			 if (strcmp("CheckCMD", value)==0)       
			 {
				 if(1==WriteConfig(BBUCOMMON_CONFIGCMD))
			 	{
					SetCtrlAttribute (configHandle, CONFIG_BOX, ATTR_TEXT_BGCOLOR, VAL_OFFWHITE);
					SetCtrlAttribute (configHandle, CONFIG_BOX, ATTR_CTRL_MODE, VAL_INDICATOR);
			 		SetCtrlVal (panelHandle, PANEL_TEXTBOX,  "Save command.txt successfully!\r\n");  
			 	}
			 }
			 free(value);
			 
			break;
	}
	return 0;
}
int CVICALLBACK GetRruLog (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			  int status; char cmd[100];
			 if (ConfirmPopup ("Get RRUlog","Do you want to Get RRUlog now?")) 
			 {
				memset(cmd,0,100);
				strcpy(cmd,"RemoteAction.exe -d:rrulog");
				DimAction(1); 
				status = ExecutableProcess(cmd,"@action done@");
				if (status)
				{
				  SetLed("Action finished!",1);
				}
				else
				{
				  SetLed("Action failed,please check detail info",0); 
				}
				DimAction(0);
			 }
			break;
	}
	return 0;
}

//////////////////////////////////////////manualbar callback function/////////////////////////////////////////////////
void CVICALLBACK Config (int menuBar, int menuItem, void *callbackData,
		int panel)
{
			  DimAction(1);
			  WriteLog();
			  ResetTextBox (panelHandle, PANEL_TEXTBOX, "");
			  switch (menuItem)
			  {
			  	case MENUBAR_CONFIG_CONFIGIP:
					if (ReadConfigFile(MENUBAR_CONFIG_CONFIGIP))
					{
						if (0==InstallPopup(configHandle))
						{
							SetPanelAttribute (configHandle, ATTR_TITLE, "CheckBBUIP");
							SetCtrlAttribute (configHandle, CONFIG_BOX, ATTR_ENTER_IS_NEWLINE, 1);
							SetCtrlAttribute (configHandle, CONFIG_BOX, ATTR_TEXT_BGCOLOR, VAL_OFFWHITE);
						}
					
					}
					else
					{
						SetCtrlVal (panelHandle, PANEL_TEXTBOX, "Read data from bbuip.txt error,please check it by manual!\r\n");        
					}
					break;
				case BBUCOMMON_CONFIGCMD:
					if (ReadConfigFile(BBUCOMMON_CONFIGCMD))
					{
						if (0==InstallPopup(configHandle))
						{
							SetPanelAttribute (configHandle, ATTR_TITLE, "CheckCMD");    
							SetCtrlAttribute (configHandle, CONFIG_BOX, ATTR_ENTER_IS_NEWLINE, 1);
							SetCtrlAttribute (configHandle, CONFIG_BOX, ATTR_TEXT_BGCOLOR, VAL_OFFWHITE);
						}
					}
					else
					{
						SetCtrlVal (panelHandle, PANEL_TEXTBOX, "Read data from cmd.txt error,please check it by manual!\r\n");
					}
					
			  }
			  DimAction(0);   
}  

void CVICALLBACK ConfigItem (int menuBar, int menuItem, void *callbackData,
		int panel)
{
	 if((Initial(1, 0)>=0) && (Initial(2, 0)>=0) && (Initial(3, 0)>=0))
	 {
	 	InstallPopup(itemHandle);
	 }
	 else
	 {
	     SetLed("Read file type or filter information from config.ini to UI error,please try again!",0); 
	 }
	 
}

int CVICALLBACK RecordUptime (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 int status; char cmd[100];
			 if (ConfirmPopup ("Record uptime","Do you want to record uptime now?")) 
			 {
				memset(cmd,0,100);
				strcpy(cmd,"RemoteAction.exe -c:uptime");
				DimAction(1); 
				status = ExecutableProcess(cmd,"@action done@");
				if (status)
				{
				    SetLed("Get uptime information finished!",1);
					memset(cmd,0,100);
					strcpy(cmd,"uptimerecord.exe");
					DimAction(1); 
					status = ExecutableProcess(cmd,"@action done@");
					if (status)
					{
						 SetLed("Record uptime information finished!",1);
					}
					else
					{
						SetLed("Record uptime inforamtion failed,please check detail info",0);  
					}
					DimAction(0);
				}
				else
				{
				   SetLed("Get uptime inforamtion failed,please check detail info",0); 
				}
				DimAction(0);
			 }
			break;
	}
	return 0;
}
int CVICALLBACK CheckUptime (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 char buffer[20000]; char pathName[MAX_PATHNAME_LEN];		char dirName[MAX_PATHNAME_LEN];   FILE    *hFile;	  char *p = ""; int i=0; int lenth=0; char temp[20]; //char value[50];
			 int flag =0;		 int row = 0; int column = 0; int insertcolumn = 0;  int confirmresult = 0;	 
	 
			 typedef struct
				{ 
					int x;
					int y; 
				} Point;

			 confirmresult = ConfirmPopup ("Check uptime","Do you want to check uptime now?");
		 
			 if ((outputHandle = LoadPanel (0, "Remotely.uir", OUTPUTVIEW)) < 0)
				 {
				 SetCtrlVal (panelHandle, PANEL_TEXTBOX,  "Load check uptime panel error,please try again!\r\n"); 
			 	 return -1;
				 }
			 SetPanelAttribute (outputHandle, ATTR_TITLE, "CheckUptimeRecord");
			 SetCtrlAttribute (outputHandle, OUTPUTVIEW_OUTPUTBOX, ATTR_VISIBLE, 0);
			 SetCtrlAttribute (outputHandle, OUTPUTVIEW_TABLE, ATTR_VISIBLE, 1);    
			 GetProjectDir (dirName); 
			 MakePathname (dirName, "uptime.csv", pathName);
			 WriteLog();
		   	 ResetTextBox (panelHandle, PANEL_TEXTBOX, ""); 
		 
			 if (hFile = fopen(pathName, "r"))
			{
		    	while (fgets(buffer, (int)sizeof(buffer), hFile))
		    	{
					row++;
					InsertTableRows (outputHandle, OUTPUTVIEW_TABLE, -1, 1, VAL_CELL_STRING);
			
					column = 0;
					p = buffer;
					flag = 0;
					do
					{
						column++;
						if (insertcolumn == 0)
						{
							InsertTableColumns (outputHandle, OUTPUTVIEW_TABLE, -1, 1, VAL_CELL_STRING);
						}
						lenth = FindPattern (p, 0, -1, ",", 0, 0);   // strip  ","
						if (lenth >=0)
						{
							memset(temp,0,20);
							for (i=0;i<lenth;i++)
							{
								temp[i] = *p;
								p++;
							}
							p++;
							SetTableCellVal (outputHandle, OUTPUTVIEW_TABLE, MakePoint(column, row), temp);
						}
						else
						{

							lenth = FindPattern (p, 0, -1, "\n", 0, 0);	  // strip  "\n"
							if (lenth >=0)								 // if find "\n"  write last string to last column
							{
							    memset(temp,0,20);
								for (i=0;i<lenth;i++)
								{
									temp[i] = *p;
									p++;
								}
								SetTableCellVal (outputHandle, OUTPUTVIEW_TABLE, MakePoint(column, row), temp);
								flag = -1;
								insertcolumn = 1;
							}
							else		// if not find "\n", write all to last column
							{
								SetTableCellVal (outputHandle, OUTPUTVIEW_TABLE, MakePoint(column, row), p);
								flag = -1;
								insertcolumn = 1;
							}
		
						}
				
					}while( flag != -1);
					SetTableColumnAttribute (outputHandle, OUTPUTVIEW_TABLE, -1, ATTR_COLUMN_WIDTH, 80);
					memset(buffer,0,20000);
												 
		    	}
		    	fclose(hFile);
			} 
			if (confirmresult)    // if user select yes to check uptime  install popup
			 {
				InstallPopup(outputHandle);
			 }
			else				 // if user select no, discard panel due to load it at beginning of this function
			{
				if (outputHandle)
				    {
		               DiscardPanel (outputHandle);
			        }
			}
			break;
	}
	return 0;
}

int CVICALLBACK FetchLogs (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 int status; char cmd[100];  char *buffer=""; char *info = ""; char *folder="";
	 
			 info = GetItemInfo(2); 
			 buffer=(char*)malloc(100);
			 memset(buffer,0,100);
			 sprintf(buffer,"Do you want to fetch filter logs: (%s) now?",info);
			 
			 if (ConfirmPopup ("Fetch Filter Logs",buffer)) 
			 {
				memset(cmd,0,100);
				strcpy(cmd,"RemoteAction.exe -d:filter");
				DimAction(1); 
				status = ExecutableProcess(cmd,"@action done@");
				if (status)
				{   
					memset(buffer,0,100);
					folder= readfoldername();
					sprintf(buffer,"Fetch filter logs: (%s) finished! folder is:%s",info,folder);  
				    SetLed(buffer,1);
				}
				else
				{
				   memset(buffer,0,100); 
				   sprintf(buffer,"Fetch filter logs: (%s) failed,pls check detail info!",info); 	
				   SetLed(buffer,0);
				}
				DimAction(0);
			 }
			 free(buffer);
			break;
	}
	return 0;
}
int CVICALLBACK AnalyzeFilter (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 int status; char cmd[100];  char *buffer=""; char *info = "";
	 
			 info = GetItemInfo(2); 
			 buffer=(char*)malloc(100);
			 memset(buffer,0,100);
			 sprintf(buffer,"Do you want to analyze filter logs: (%s) now?",info);
			 
			 if (ConfirmPopup ("Analyze Filter Logs",buffer)) 
			 {
				memset(cmd,0,100);
				strcpy(cmd,"filter.exe -a:techlogs");
				DimAction(1); 
				status = ExecutableProcess(cmd,"@action done@");
				if (status)
				{   
					memset(buffer,0,100);
					sprintf(buffer,"Analyze filter logs: (%s) finished!",info);  
				    SetLed(buffer,1);
				}
				else
				{
				   memset(buffer,0,100); 
				   sprintf(buffer,"Analyze filter logs: (%s) failed,pls check detail info!",info); 	
				   SetLed(buffer,0);
				}
				DimAction(0);
			 }
			 free(buffer);
			break;
	}
	return 0;
}
int CVICALLBACK SearchFile (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 int status; char cmd[100]; char *info = "";   char *buffer = "";   char *folder = "";   
			
			 info = GetItemInfo(3);
			 buffer=(char*)malloc(1000);
	 		 memset(buffer,0,1000);
			 sprintf(buffer,"Do you want to search files: (%s) now?",info);
			 if (ConfirmPopup ("Search File",buffer)) 
			 {
				 memset(cmd,0,100);
				 strcpy(cmd,"RemoteAction.exe -c:search");
				 DimAction(1); 
				 status = ExecutableProcess(cmd,"@action done@");
				 if (status)
				 {
					SetLed("Search files is finished!",1);
					memset(cmd,0,100);
					strcpy(cmd,"filter.exe -a:search");
					DimAction(1); 
					status = ExecutableProcess(cmd,"@action done@");
					if (status)
					{
						 SetLed("Analyze searched files information finished!",1);
					}
					else
					{
						SetLed("Analyze searched files information failed,please check detail info",0);  
					}
					DimAction(0);
			
				}
				else
				{
 				    memset(buffer,0,1000); 
				    sprintf(buffer,"Search files: (%s) failed,pls check detail info!",info); 	
				    SetLed(buffer,0); 
				}
				DimAction(0);
			 }
			 free(buffer);
			break;
	}
	return 0;
}
int CVICALLBACK CheckSFP (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 int status; char cmd[100];  char *buffer=""; char *info = "";
	 
			 info = GetItemInfo(1); 
			 buffer=(char*)malloc(100);
			 memset(buffer,0,100);
			 sprintf(buffer,"Do you want to analyze logs: (%s) now?",info);
			 
			 if (ConfirmPopup ("Analyze Logs",buffer)) 
			 {
				memset(cmd,0,100);
				strcpy(cmd,"filter.exe -a:sysinfo");
				DimAction(1); 
				status = ExecutableProcess(cmd,"@action done@");
				if (status)
				{   
					memset(buffer,0,100);
					sprintf(buffer,"Analyze logs: (%s) finished!",info);  
				    SetLed(buffer,1);
				}
				else
				{
				   memset(buffer,0,100); 
				   sprintf(buffer,"Analyze logs: (%s) failed,pls check detail info!",info); 	
				   SetLed(buffer,0);
				}
				DimAction(0);
			 }
			 free(buffer);
			break;
	}
	return 0;
}
void CVICALLBACK Help (int menuBar, int menuItem, void *callbackData,
		int panel)
{
	if ((outputHandle = LoadPanel (0, "Remotely.uir", OUTPUTVIEW)) < 0)
		 {
		 SetCtrlVal (panelHandle, PANEL_TEXTBOX,  "Load check uptime panel error,please try again!\r\n"); 
	 	 return;
		 }
	 SetPanelAttribute (outputHandle, ATTR_TITLE, "HelpInformation");
	 DimAction(1); 
	 if(WriteOupputBox(1))
	 {
	 	InstallPopup(outputHandle);
	 }
	 else
	 {
	  SetCtrlVal (panelHandle, PANEL_TEXTBOX, "Read data from help.txt error,please check it by manual!\r\n");
	 }
	 DimAction(0);
	
}


////////////////////////////////////////////////////////////////////selfdefined function//////////////////////////////////////
static int ExecutableProcess(char *cmd, char *checkpoint)
{
	 FILE    *hFile;
    char    buffer[300]; // long enough for single line of output from ipconfig
    char    tempFileName[L_tmpnam];
    char    command[L_tmpnam + 25];
    int     hProc;
   
    int     res=0;  int checkflag = 0; 
    
    tmpnam(tempFileName);
    sprintf(command, "cmd.exe /C %s > %s", cmd,tempFileName); 
//     sprintf(command, "cmd.exe /C %s", cmd);
 //   if (LaunchExecutableEx(command, LE_SHOWNORMAL, &hProc) >= 0)
	if (LaunchExecutableEx(command, LE_HIDE, &hProc) >= 0)   
    {
		SetLed("running...please wait...",0);
		ProcessSystemEvents ();   
		WriteLog();
		ResetTextBox (panelHandle, PANEL_TEXTBOX, "");    
        while (!ExecutableHasTerminated(hProc));
		{
        	RetireExecutableHandle(hProc);
		}
    
        if (hFile = fopen(tempFileName, "r"))
        {
            while (fgets(buffer, (int)sizeof(buffer), hFile))
            {
               
				SetCtrlVal (panelHandle, PANEL_TEXTBOX, buffer); 
				if (!checkflag)
				{
					if(NULL != strstr (buffer, checkpoint))
					{
						checkflag = 1;
						res = 1;
					}
				}
            }
            fclose(hFile);
        //    DeleteFile(tempFileName);
			remove (tempFileName);
        }
    }
	return res;
}
void KillSubprocess(void)
{
    char    command[300];
    int     hProc;

    
	memset(command,0,300);
	strcpy(command,"cmd.exe /C TASKKILL /F /IM RemoteAction.exe");
	if (LaunchExecutableEx(command, LE_HIDE, &hProc) >= 0)   
    {
		WriteLog();
        while (!ExecutableHasTerminated(hProc));
		{
        	RetireExecutableHandle(hProc);
		}
    }
}
char *GetItemInfo(int flag)
{
	 char *result="";	  int value=0;	  int status = -1;    char buffer[100];
	 
	 result=(char*)malloc(1000);
	 memset(result,0,1000);
	 
	 if (1 == flag)  // file tpye operation
	 {
		 if ((GetCtrlVal (itemHandle, FILE_ITEM_VENDOR, &value)) >=0 && 1==value) 
		 {
		    result = strcat(result,"vendor,");
		 }
		 if ((GetCtrlVal (itemHandle, FILE_ITEM_SCFC, &value)) >=0 && 1==value) 
		 {
		    result = strcat(result,"scf,");
		 }
		 if ((GetCtrlVal (itemHandle, FILE_ITEM_CONFIG, &value)) >=0 && 1==value) 
		 {
		    result = strcat(result,"config,");
		 }
		 if ((GetCtrlVal (itemHandle, FILE_ITEM_SWCONFIG, &value)) >=0 && 1==value) 
		 {
		    result = strcat(result,"swconfig,");
		 }
		 if ((GetCtrlVal (itemHandle, FILE_ITEM_HWF, &value)) >=0 && 1==value) 
		 {
		    result = strcat(result,"hwf,");
		 }
		 if ((GetCtrlVal (itemHandle, FILE_ITEM_SYSINFO, &value)) >=0 && 1==value) 
		 {
		    result = strcat(result,"sysinfo,");
		 }
		 if ((GetCtrlVal (itemHandle, FILE_ITEM_SELFDEFI, &value)) >=0 && 1==value) 
		 {
			memset(buffer,0,100);
			GetCtrlVal (itemHandle, FILE_ITEM_SELFDEFIFILE, buffer);
		    result = strcat(result,buffer);
		 }
	 }
	 if (2 == flag)   //  filter operation
	 {
		 if ((GetCtrlVal (itemHandle, FILE_ITEM_TECHLOGS, &value)) >=0 && 1==value) 
		 {
		    result = strcat(result,"techlogs");
		 }
	
	 }
	 if (3 == flag)  //   search operation
	 {
	    if ((GetCtrlVal (itemHandle, FILE_ITEM_SEARCH, &value)) >=0 && 1==value) 
		 {
			 GetCtrlVal (itemHandle, FILE_ITEM_S_FILENAME, result);
		 }
	 
	 }
	 return result;
}
void SetLed(char *status, int flag)
{
	  SetCtrlAttribute (panelHandle, PANEL_LED, ATTR_LABEL_TEXT, status);
	  SetCtrlVal (panelHandle, PANEL_LED, flag);
}

static int WriteOupputBox(int flag) 
{
	FILE    *hFile;  char pathName[MAX_PATHNAME_LEN]; char dirName[MAX_PATHNAME_LEN]; char buffer[300];

	
	ResetTextBox (outputHandle, OUTPUTVIEW_OUTPUTBOX, ""); 
	GetProjectDir (dirName); 
	if (0 == flag)    // mean write output.txt to box
	{
    	MakePathname (dirName, "output.txt", pathName);
	}
	if (1 == flag)     // mean write help.txt to box
	{
	   MakePathname (dirName, "help.txt", pathName); 
	}
	if (hFile = fopen(pathName, "r"))
    {
        while (fgets(buffer, (int)sizeof(buffer), hFile))
        {
			SetCtrlVal (outputHandle, OUTPUTVIEW_OUTPUTBOX, buffer); 
        }
	}
	else
	{
	  return 0;
	}
	if(hFile)
	{
	    fclose(hFile);  
	}		
	return 1;
}

static int ReadConfigFile( int item)
{
	FILE    *hFile; 		 char pathName[MAX_PATHNAME_LEN]; char dirName[MAX_PATHNAME_LEN];	 char buffer[300]; 	
	
	ResetTextBox (configHandle, CONFIG_BOX, ""); 
	GetProjectDir (dirName); 
	switch(item)
	{
		case MENUBAR_CONFIG_CONFIGIP:
			MakePathname (dirName, "bbuip.txt", pathName);
			break;
		case BBUCOMMON_CONFIGCMD:
			MakePathname (dirName, "command.txt", pathName); 
			break;
	}
	if (hFile = fopen(pathName, "r"))
    {
        while (fgets(buffer, (int)sizeof(buffer), hFile))
        {
			SetCtrlVal (configHandle, CONFIG_BOX, buffer); 
        }
	}
	else
	{
	  return 0;
	}
	if(hFile)
	{
	    fclose(hFile);  
	}
	return 1;
	

}  
static int WriteConfig(int flag)
{
	  int fHandle=-1,linenumber=0,i=0,size=0,findflag=0; char *buffer=""; char pathName[MAX_PATHNAME_LEN];		char dirName[MAX_PATHNAME_LEN];   
	  
	  	GetProjectDir (dirName); 
		if(MENUBAR_CONFIG_CONFIGIP == flag)
		{
    		 MakePathname (dirName, "bbuip.txt", pathName);
	  
			 fHandle = OpenFile (pathName, VAL_WRITE_ONLY, VAL_TRUNCATE, VAL_ASCII);
			 if(fHandle<0)
			 {
	   		   SetCtrlVal (panelHandle, PANEL_TEXTBOX,  "Open bbuip.txt file error,please check by yourself!\r\n"); 
			   return -1;
			 }
			 buffer=(char*)malloc(1000); 
			 GetNumTextBoxLines (configHandle, CONFIG_BOX, &linenumber);
			 for(i=0;i<linenumber;i++)
			 {
				memset(buffer,0,1000);  
				GetTextBoxLine (configHandle, CONFIG_BOX, i, buffer);
				strcat(buffer,"\n");
				size=strlen(buffer);
				if (size > 7)
					{
					WriteFile (fHandle, buffer, size);
					}
			 }
			 free(buffer);
			 if(( CloseFile(fHandle))<0)
			 {
	   		   SetCtrlVal (panelHandle, PANEL_TEXTBOX,  "Close bbuip.txt file error,please try again!\r\n"); 
			   return -1;
			 
			 }
			 GetFileSize (pathName, &size); 
			 if(size==0)
			 {
	   		   SetCtrlVal (panelHandle, PANEL_TEXTBOX,  "bbuip.txt size is zero,please check and try again!\r\n"); 
			   return -1;
			 }
		
		}
		if(BBUCOMMON_CONFIGCMD == flag)
		{
			MakePathname (dirName, "command.txt", pathName);
	  
			 fHandle = OpenFile (pathName, VAL_WRITE_ONLY, VAL_TRUNCATE, VAL_ASCII);
			 if(fHandle<0)
			 {
	   		   SetCtrlVal (panelHandle, PANEL_TEXTBOX,  "Open command.txt file error,please check by yourself!\r\n"); 
			   return -1;
			 }
			 buffer=(char*)malloc(1000); 
			 GetNumTextBoxLines (configHandle, CONFIG_BOX, &linenumber); 
			 for(i=0;i<linenumber;i++)
			 {
				memset(buffer,0,1000);  
				GetTextBoxLine (configHandle, CONFIG_BOX, i, buffer);
				strcat(buffer,"\n");
				size=strlen(buffer);
				WriteFile (fHandle, buffer, size);
			 }
			 free(buffer);
			 if(( CloseFile(fHandle))<0)
			 {
	   		   SetCtrlVal (panelHandle, PANEL_TEXTBOX,  "Close command.txt file error,please try again!\r\n"); 
			   return -1;
			 
			 }
			 GetFileSize (pathName, &size); 
			 if(size==0)
			 {
	   		   SetCtrlVal (panelHandle, PANEL_TEXTBOX,  "command.txt size is zero,please check and try again!\r\n"); 
			 }
		}
		
	return 1;
}
void WriteLogDateTime(int fileHandle)
{
	char *buffer="";  int hour=0,minute=0,second=0,year=0,month=0,day=0;

	buffer=(char*)malloc(1000);   
	memset(buffer,0,1000);
								  
	GetSystemDate (&month, &day, &year);
	GetSystemTime (&hour, &minute, &second);  
	
	sprintf(buffer,"=========================%d-%d-%d    %d:%d:%d=========================\n\n",year,month,day,hour,minute,second);
	WriteFile (fileHandle, buffer, strlen(buffer)); 
	free(buffer);
}
void WriteLog(void)
{
	 char *buffer=""; char pathName[MAX_PATHNAME_LEN];		char dirName[MAX_PATHNAME_LEN];  int fHandle=-1,linenumber=0,i=0,size=0;	int file_size=0,file_status=0;
	 
	GetProjectDir (dirName); 
    MakePathname (dirName, "log.txt", pathName);
	file_status = GetFileSize (pathName, &file_size);
	
	
	if(-1==file_status)
	{
		fHandle = OpenFile (pathName, VAL_WRITE_ONLY, VAL_TRUNCATE, VAL_ASCII);
		WriteLogDateTime(fHandle);
		
	}
	if(0==file_status)
	{
		fHandle = OpenFile (pathName, VAL_WRITE_ONLY, VAL_APPEND, VAL_ASCII);
		WriteLogDateTime(fHandle);
	}
  	 buffer=(char*)malloc(1000); 
	 GetNumTextBoxLines (panelHandle, PANEL_TEXTBOX, &linenumber);
	 for(i=0;i<linenumber;i++)
	 {
		memset(buffer,0,1000);  
		GetTextBoxLine (panelHandle, PANEL_TEXTBOX, i, buffer);
		strcat(buffer,"\n");
		size=strlen(buffer);
		WriteFile (fHandle, buffer, size);
	 }
	 free(buffer); 

	CloseFile(fHandle);														 

}
void DimAction(int flag)
{
	SetCtrlAttribute (panelHandle, PANEL_OUTPUT, ATTR_DIMMED, flag);
	SetCtrlAttribute (panelHandle, PANEL_TAB, ATTR_DIMMED, flag); 
	/*
	SetCtrlAttribute (bbucommonHandle, BBUCOMMON_DOWNLOAD, ATTR_DIMMED, flag); 
	SetCtrlAttribute (bbucommonHandle, BBUCOMMON_UPLOAD, ATTR_DIMMED, flag);
	SetCtrlAttribute (bbucommonHandle, BBUCOMMON_CONFIGCMD, ATTR_DIMMED, flag);
	SetCtrlAttribute (bbucommonHandle, BBUCOMMON_SENDCMD, ATTR_DIMMED, flag);
	SetCtrlAttribute (bbucommonHandle, BBUCOMMON_ENABLEPORT, ATTR_DIMMED, flag);
	SetCtrlAttribute (bbucommonHandle, BBUCOMMON_UPDATEALLPUT, ATTR_DIMMED, flag);
	
	SetCtrlAttribute (rrucommonHandle, RRUCOMMON_ENABLEOPT, ATTR_DIMMED, flag);
	SetCtrlAttribute (rrucommonHandle, RRUCOMMON_ENABLEVSWR, ATTR_DIMMED, flag);
	SetCtrlAttribute (rrucommonHandle, RRUCOMMON_GETRRULOG, ATTR_DIMMED, flag);
	
	
	SetCtrlAttribute (customizingHandle, CUSTOM_UPDATENAME, ATTR_DIMMED, flag);
	SetCtrlAttribute (customizingHandle, CUSTOM_UPDATEVENDOR, ATTR_DIMMED, flag);
	SetCtrlAttribute (customizingHandle, CUSTOM_CHECKSFP, ATTR_DIMMED, flag);
	SetCtrlAttribute (customizingHandle, CUSTOM_SEARCHFILE, ATTR_DIMMED, flag);
	SetCtrlAttribute (customizingHandle, CUSTOM_RECORDUPTIME, ATTR_DIMMED, flag);
	SetCtrlAttribute (customizingHandle, CUSTOM_CHECKUPTIME, ATTR_DIMMED, flag);
	SetCtrlAttribute (customizingHandle, CUSTOM_FETCHLOGS, ATTR_DIMMED, flag);
	SetCtrlAttribute (customizingHandle, CUSTOM_ANALYZEFILTER, ATTR_DIMMED, flag);  */
	
	
	SetMenuBarAttribute (menubarHandle, MENUBAR_CONFIG, ATTR_DIMMED, flag);
	SetMenuBarAttribute (menubarHandle, MENUBAR_HELP, ATTR_DIMMED, flag);
	
}
static int Initial(int item, int flag)
{
	char pathName[MAX_PATHNAME_LEN]; char dirName[MAX_PATHNAME_LEN];  char *buffer=""; int value=0;  int status=0;  
	
	GetProjectDir (dirName); 
	MakePathname (dirName, "config.ini", pathName);
	inihandle = Ini_New (0);
	status = Ini_ReadFromFile (inihandle, pathName);
	buffer=(char*)malloc(300);
	memset(buffer,0,300);
	
	if ((status)<0)
	{
		return status;
	}
	if (0 == item)  // system operation
	{
	
		if(1 == flag)   //write
		{
			 GetCtrlVal (customizingHandle, CUSTOM_UPDATENAME, buffer);
			 Ini_PutString (inihandle, "system", "update_vendor_name", buffer);

			 Ini_WriteToFile (inihandle, pathName);   
		}
		if(0 == flag)	  // read
		{
			Ini_GetStringIntoBuffer (inihandle, "system", "update_vendor_name", buffer, 100);
			SetCtrlVal (customizingHandle, CUSTOM_UPDATENAME, buffer);     
		}

		
	}
	if (1 == item)	   //  item operation
	{
		if(1 == flag)	   // write
		{
			status = GetCtrlVal (itemHandle, FILE_ITEM_VENDOR, &value);
			 if ((status)<0) 
				{
				return status;
				}
			 status = Ini_PutInt (inihandle, "item", "vendor", value);
			 if ((status)<0) 
				{
				return status;
				}
		 
			 status = GetCtrlVal (itemHandle, FILE_ITEM_SCFC, &value);
			 if ((status)<0) 
				{
				return status;
				}
			 status = Ini_PutInt (inihandle, "item", "scfc", value);
			 if ((status)<0) 
				{
				return status;
				}
		 
			 status = GetCtrlVal (itemHandle, FILE_ITEM_CONFIG, &value);
			 if ((status)<0) 
				{
				return status;
				}
			 status = Ini_PutInt (inihandle, "item", "config", value);
			 if ((status)<0) 
				{
				return status;
				}
		 
			 status = GetCtrlVal (itemHandle, FILE_ITEM_SWCONFIG, &value);
			 if ((status)<0) 
				{
				return status;
				}
			 status = Ini_PutInt (inihandle, "item", "swconfig", value);
			 if ((status)<0) 
				{
				return status;
				}
		 
			 status = GetCtrlVal (itemHandle, FILE_ITEM_HWF, &value);
			 if ((status)<0) 
				{
				return status;
				}
			 status = Ini_PutInt (inihandle, "item", "hwf", value);
			 if ((status)<0) 
				{
				return status;
				}
		 
			 status = GetCtrlVal (itemHandle, FILE_ITEM_SYSINFO, &value);
			 if ((status)<0) 
				{
				return status;
				}
			 status = Ini_PutInt (inihandle, "item", "sysinfo", value);
			 if ((status)<0) 
				{
				return status;
				}
			 
			 status = GetCtrlVal (itemHandle, FILE_ITEM_SELFDEFI, &value);
			 if ((status)<0) 
				{
				return status;
				}
			 status = Ini_PutInt (inihandle, "item", "selfdefi", value);
			 if ((status)<0) 
				{
				return status;
				}
			 
			 status = GetCtrlVal (itemHandle, FILE_ITEM_SELFDEFIPATH, buffer);
			if ((status)<0) 
			{
				return status;
			}
			status = Ini_PutString (inihandle, "item", "selfpath", buffer);
			if ((status)<0) 
			{
				return status;
			}
			
			status = GetCtrlVal (itemHandle, FILE_ITEM_SELFDEFIFILE, buffer);
			if ((status)<0) 
			{
				return status;
			}
			status = Ini_PutString (inihandle, "item", "selffile", buffer);
			if ((status)<0) 
			{
				return status;
			}
			 
			 
		 
			 status = Ini_WriteToFile (inihandle, pathName);
			 if ((status)<0) 
				{
				return status;
				}
		}
		if(0 == flag)		//	   read
		{
			status = Ini_GetInt (inihandle, "item", "vendor", &value);
			if ((status)<0) 
				{
				return status;
				}
			status = SetCtrlVal (itemHandle, FILE_ITEM_VENDOR, value); 
			if ((status)<0) 
				{
				return status;
				}
		
			status = Ini_GetInt (inihandle, "item", "scfc", &value);
			if ((status)<0) 
				{
				return status;
				}
			status = SetCtrlVal (itemHandle, FILE_ITEM_SCFC, value); 
			if ((status)<0) 
				{
				return status;
				}
		
			status = Ini_GetInt (inihandle, "item", "config", &value);
			if ((status)<0) 
				{
				return status;
				}
			status = SetCtrlVal (itemHandle, FILE_ITEM_CONFIG, value); 
			if ((status)<0) 
				{
				return status;
				}
		
			status = Ini_GetInt (inihandle, "item", "swconfig", &value);
			if ((status)<0) 
				{
				return status;
				}
			status = SetCtrlVal (itemHandle, FILE_ITEM_SWCONFIG, value); 
			if ((status)<0) 
				{
				return status;
				}
		
			status = Ini_GetInt (inihandle, "item", "hwf", &value);
			if ((status)<0) 
				{
				return status;
				}
			status = SetCtrlVal (itemHandle, FILE_ITEM_HWF, value); 
			if ((status)<0) 
				{
				return status;
				}
			
			status = Ini_GetInt (inihandle, "item", "sysinfo", &value);
			if ((status)<0) 
				{
				return status;
				}
			status = SetCtrlVal (itemHandle, FILE_ITEM_SYSINFO, value); 
			if ((status)<0) 
				{
				return status;
				}
			
			status = Ini_GetInt (inihandle, "item", "selfdefi", &value);
			if ((status)<0) 
				{
				return status;
				}
			status = SetCtrlVal (itemHandle, FILE_ITEM_SELFDEFI, value); 
			if ((status)<0) 
				{
				return status;
				}
			
			status = Ini_GetStringIntoBuffer (inihandle, "item", "selfpath", buffer, 300);
			if ((status)<0) 
			{
				return status;
			}
			status = SetCtrlVal (itemHandle, FILE_ITEM_SELFDEFIPATH, buffer); 
			if ((status)<0) 
			{
				return status;
			}
			
			status = Ini_GetStringIntoBuffer (inihandle, "item", "selffile", buffer, 300);
			if ((status)<0) 
			{
				return status;
			}
			status = SetCtrlVal (itemHandle, FILE_ITEM_SELFDEFIFILE, buffer); 
			if ((status)<0) 
			{
				return status;
			}
			
		}
	}
	if (2 == item)	   // filter operation
	{
	
		if(1==flag)
		{
			status = GetCtrlVal (itemHandle, FILE_ITEM_TECHLOGS, &value);
		    if ((status)<0) 
			{
				return status;
			}
		    status = Ini_PutInt (inihandle, "filter", "techlogs", value);
			if ((status)<0) 
			{
				return status;
			}
			status = GetCtrlVal (itemHandle, FILE_ITEM_FILTER, buffer);
			if ((status)<0) 
			{
				return status;
			}
			status = Ini_PutString (inihandle, "filter", "filter", buffer);
			if ((status)<0) 
			{
				return status;
			}
			status = Ini_WriteToFile (inihandle, pathName);
			if ((status)<0) 
			{
				return status;
			} 
		}
		if(0==flag)
		{
			status = Ini_GetInt (inihandle, "filter", "techlogs", &value);
			if ((status)<0) 
			{
				return status;
			}
			status = SetCtrlVal (itemHandle, FILE_ITEM_TECHLOGS, value); 
			if ((status)<0) 
			{
				return status;
			}
			status = Ini_GetStringIntoBuffer (inihandle, "filter", "filter", buffer, 300);
			if ((status)<0) 
			{
				return status;
			}
			status = SetCtrlVal (itemHandle, FILE_ITEM_FILTER, buffer); 
			if ((status)<0) 
			{
				return status;
			}
	
		}
	
	}
	if (3 == item)	   // search operation
	{
	
		if(1==flag)
		{
			status = GetCtrlVal (itemHandle, FILE_ITEM_SEARCH, &value);
		    if ((status)<0) 
			{
				return status;
			}
		    status = Ini_PutInt (inihandle, "search", "search", value);
			if ((status)<0) 
			{
				return status;
			}
			memset(buffer,0,100); 
			status = GetCtrlVal (itemHandle, FILE_ITEM_S_FILENAME, buffer);
			if ((status)<0) 
			{
				return status;
			}
			status = Ini_PutString (inihandle, "search", "file_name", buffer);
			if ((status)<0) 
			{
				return status;
			}
			memset(buffer,0,100); 
			status = GetCtrlVal (itemHandle, FILE_ITEM_S_FILEPATH, buffer);
			if ((status)<0) 
			{
				return status;
			}
			status = Ini_PutString (inihandle, "search", "file_path", buffer);
			if ((status)<0) 
			{
				return status;
			}
			status = Ini_WriteToFile (inihandle, pathName);
			if ((status)<0) 
			{
				return status;
			} 
		}
		if(0==flag)
		{
			status = Ini_GetInt (inihandle, "search", "search", &value);
			if ((status)<0) 
			{
				return status;
			}
			status = SetCtrlVal (itemHandle, FILE_ITEM_SEARCH, value); 
			if ((status)<0) 
			{
				return status;
			}
			memset(buffer,0,100); 
			status = Ini_GetStringIntoBuffer (inihandle, "search", "file_name", buffer, 300);
			if ((status)<0) 
			{
				return status;
			}
			status = SetCtrlVal (itemHandle, FILE_ITEM_S_FILENAME, buffer); 
			if ((status)<0) 
			{
				return status;
			}
			memset(buffer,0,100); 
			status = Ini_GetStringIntoBuffer (inihandle, "search", "file_path", buffer, 300);
			if ((status)<0) 
			{
				return status;
			}
			status = SetCtrlVal (itemHandle, FILE_ITEM_S_FILEPATH, buffer); 
			if ((status)<0) 
			{
				return status;
			}
		}
	}
	free(buffer); 
	Ini_Dispose (inihandle); 
	return 1;
}
/*
static int ItemInfo(int flag)
{
	char pathName[MAX_PATHNAME_LEN]; char dirName[MAX_PATHNAME_LEN];  int value=0;  int status=0;
	
	GetProjectDir (dirName); 
	MakePathname (dirName, "config.ini", pathName);
	inihandle = Ini_New (0);
	status = Ini_ReadFromFile (inihandle, pathName);
	
	if ((status)<0)
	{
		return status;
	}

	if(flag)
	{
		status = GetCtrlVal (itemHandle, FILE_ITEM_VENDOR, &value);
		 if ((status)<0) 
			{
			return status;
			}
		 status = Ini_PutInt (inihandle, "item", "vendor", value);
		 if ((status)<0) 
			{
			return status;
			}
		 
		 status = GetCtrlVal (itemHandle, FILE_ITEM_SCFC, &value);
		 if ((status)<0) 
			{
			return status;
			}
		 status = Ini_PutInt (inihandle, "item", "scfc", value);
		 if ((status)<0) 
			{
			return status;
			}
		 
		 status = GetCtrlVal (itemHandle, FILE_ITEM_CONFIG, &value);
		 if ((status)<0) 
			{
			return status;
			}
		 status = Ini_PutInt (inihandle, "item", "config", value);
		 if ((status)<0) 
			{
			return status;
			}
		 
		 status = GetCtrlVal (itemHandle, FILE_ITEM_SWCONFIG, &value);
		 if ((status)<0) 
			{
			return status;
			}
		 status = Ini_PutInt (inihandle, "item", "swconfig", value);
		 if ((status)<0) 
			{
			return status;
			}
		 
		 status = GetCtrlVal (itemHandle, FILE_ITEM_HWF, &value);
		 if ((status)<0) 
			{
			return status;
			}
		 status = Ini_PutInt (inihandle, "item", "hwf", value);
		 if ((status)<0) 
			{
			return status;
			}
		 
		 status = Ini_WriteToFile (inihandle, pathName);
		 if ((status)<0) 
			{
			return status;
			}
	}
	else if(!flag)
	{
		status = Ini_GetInt (inihandle, "item", "vendor", &value);
		if ((status)<0) 
			{
			return status;
			}
		status = SetCtrlVal (itemHandle, FILE_ITEM_VENDOR, value); 
		if ((status)<0) 
			{
			return status;
			}
		
		status = Ini_GetInt (inihandle, "item", "scfc", &value);
		if ((status)<0) 
			{
			return status;
			}
		status = SetCtrlVal (itemHandle, FILE_ITEM_SCFC, value); 
		if ((status)<0) 
			{
			return status;
			}
		
		status = Ini_GetInt (inihandle, "item", "config", &value);
		if ((status)<0) 
			{
			return status;
			}
		status = SetCtrlVal (itemHandle, FILE_ITEM_CONFIG, value); 
		if ((status)<0) 
			{
			return status;
			}
		
		status = Ini_GetInt (inihandle, "item", "swconfig", &value);
		if ((status)<0) 
			{
			return status;
			}
		status = SetCtrlVal (itemHandle, FILE_ITEM_SWCONFIG, value); 
		if ((status)<0) 
			{
			return status;
			}
		
		status = Ini_GetInt (inihandle, "item", "hwf", &value);
		if ((status)<0) 
			{
			return status;
			}
		status = SetCtrlVal (itemHandle, FILE_ITEM_HWF, value); 
		if ((status)<0) 
			{
			return status;
			}
	}
	Ini_Dispose (inihandle); 
	return 1;
}   */

char *readfoldername(void)
{
	char pathName[MAX_PATHNAME_LEN]; char dirName[MAX_PATHNAME_LEN];  char *buffer="";
	
	GetProjectDir (dirName); 
	MakePathname (dirName, "config.ini", pathName);
	inihandle = Ini_New (0); 
	Ini_ReadFromFile (inihandle, pathName); 
	buffer=(char*)malloc(100);
	memset(buffer,0,100);

	Ini_GetStringIntoBuffer (inihandle, "system", "download_folder_name", buffer, 100);

	Ini_Dispose (inihandle);
	return buffer;
}

int CVICALLBACK ConfigCMD (int panel, int control, int event,
		void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			 DimAction(1);
			  WriteLog();
			  ResetTextBox (panelHandle, PANEL_TEXTBOX, "");
		
			if (ReadConfigFile(BBUCOMMON_CONFIGCMD))
			{
				if (0==InstallPopup(configHandle))
				{
					SetPanelAttribute (configHandle, ATTR_TITLE, "CheckCMD");    
					SetCtrlAttribute (configHandle, CONFIG_BOX, ATTR_ENTER_IS_NEWLINE, 1);
					SetCtrlAttribute (configHandle, CONFIG_BOX, ATTR_TEXT_BGCOLOR, VAL_OFFWHITE);
				}
			}
			else
			{
				SetCtrlVal (panelHandle, PANEL_TEXTBOX, "Read data from cmd.txt error,please check it by manual!\r\n");
			}
					
		
			  DimAction(0);   
			break;
	}
	return 0;
}
