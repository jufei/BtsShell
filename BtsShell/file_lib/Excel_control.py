#####################################################################################
#>>------------------------------Revision------------------------------------------
#>>0100 piguo 2011-05-12 "backup_excelfile" and "write_excelfile" added for haishen
#>>0101 piguo 2011-05-16 change "sSheet.Cells(xCell,yCell).Value = inValue" to be
#       "sSheet.Cells(int(xCell),int(yCell)).Value = inValue" for haishen
#####################################################################################
import os, sys, time, shutil
import traceback
import xlrd, xlwt, xlutils
from xlutils.copy import copy


def backup_excelfile(filePath, fileName):
        sourceFile = os.path.join(filePath, fileName)
        if not os.path.isfile(sourceFile):
                print "WRN - Source excel %s is not exist!" % sourceFile
                return True
        tdd = time.localtime()
        tddString = '%s_%s_%s_%s_%s_%s' % (tdd[0],tdd[1],tdd[2],tdd[3],tdd[4],tdd[5])
        
        destFile = os.path.join(filePath, "%s_%s.%s" % (fileName.split('.')[0], tddString, fileName.split('.')[1]))
        shutil.copyfile(sourceFile, destFile)
        return True
                
def write_excelfile(filePath, fileName, sheetName, xCell, yCell, inValue):
        sourceFile = os.path.join(filePath, fileName)
        wWorkBook = None
        sheetIndex = None
        
        if os.path.isfile(sourceFile):
                sWorkBook = xlrd.open_workbook(sourceFile)
                if sheetName in sWorkBook.sheet_names():
                        sheetIndex = sWorkBook.sheet_names().index(sheetName)
                else:
                        print "WRN - Sheet %s not exist!" % sheetName

                wWorkBook = copy(sWorkBook)
        else:
                print "ERR - Source excel %s is not exist!" % sourceFile
                print "INF - Create new excel named %s" % sourceFile
		
                wWorkBook = xlwt.Workbook(encoding = 'utf-8')

        if wWorkBook:
                if sheetIndex != None:
                        wSheet = wWorkBook.get_sheet(sheetIndex)
                        wSheet.write(int(xCell), int(yCell), inValue)
                else:
                        print "INF - Add new sheet named %s" % sheetName
                        wSheet = wWorkBook.add_sheet(sheetName, cell_overwrite_ok = True)
                        wSheet.write(int(xCell), int(yCell), inValue)

                wWorkBook.save(sourceFile)
                return True
        else:
                return False

def read_excelfile(filePath, fileName, sheetName, xCell, yCell):
        sourceFile = os.path.join(filePath, fileName)
        wWorkBook = None
        sheetIndex = None
        if os.path.isfile(sourceFile):
                try:
                        sWorkBook = xlrd.open_workbook(sourceFile)
                        if sheetName in sWorkBook.sheet_names():
                                sheetIndex = sWorkBook.sheet_by_name(sheetName)
                                return sheetIndex.cell(int(xCell), int(yCell)).value
                        else:
                                print "WRN - Sheet %s not exist!" % sheetName
                except Exception, p_Err:
                        print "ERR - %s" % p_Err

        else:
                print "WRN - Excel file %s not exist!" % sheetName

        return None
    
def get_all_excel_items(file_path, sheet_name, row_num_for_name, care_name_list):
    """This keyword will parse excel and return all the file item dictionary list.

    | Input Paramaters | Man. | Description |
    | file_path        | Yes  | the excel file path |
    | sheet_name       | Yes  | target excel sheet name |
    | row_num_for_name | Yes  | the row number of indict the column name |
    | care_name_list   | Yes  | list all the column name which you cared |   
    
    | return | item dictionary list | 

    Example
    | ${check_list} | create list | Internal database ID | Version | Fault ID and name |
    | get_all_excel_items | D:\\test.xls | Sheet1 | 8 | ${check_list} |
    """

    data = []

    if not os.path.isfile(file_path):
        print "WRN - Excel file %s not exist!" % sheetName
        return None        
    try:
        sWorkBook = xlrd.open_workbook(file_path)
        if sheet_name not in sWorkBook.sheet_names():
            print "WRN - Sheet %s not exist!" % sheetName
            return None
        sheetIndex = sWorkBook.sheet_by_name(sheet_name)
        item_list =  sheetIndex.row_values(row_num_for_name-1)
        index_list = []
        for item_name in care_name_list:
            index_list.append(item_list.index(item_name))

        for i in range(row_num_for_name, sheetIndex.nrows):                    
            item_list =  sheetIndex.row_values(i)                    
            item_dict = {}
            for i in range(len(index_list)):
                item_dict[care_name_list[i]] = item_list[index_list[i]]
            data.append(item_dict)
            
        return data

    except Exception, p_Err:
        print "ERR - '%s'" % p_Err
                                
if __name__ == '__main__':
	#backup_excelfile(os.getcwd(), "test.xls")
	print read_excelfile(os.getcwd(), "test.xls", 'test', 1, 1)
	#write_excelfile(os.getcwd(), "test.xls", 'test4', 1, 1, 234)
