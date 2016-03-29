Set oArgs = WScript.Arguments 

If oArgs.Count = 3 Then 
    test_name = WScript.Arguments(0)   
    result_dir = WScript.Arguments(1)    
    keep_qtp_open = WScript.Arguments(2) 
End If
'WScript.StdOut.Write(test_name &"---"&result_dir&"---"&mod_list)

Dim qtApp 'As QuickTest.Application ' Declare the Application object variable
Set qtApp = CreateObject("QuickTest.Application") ' Create a Application object

if (qtApp is nothing) then
	WScript.StdOut.Write("<QTP> instanciation was NOT SUCCESSFUL!   ")
	Wscript.Quit(111)
end if

WScript.StdOut.Write("<QTP> instanciation was SUCCESSFUL!     ")

Dim qtOptions 'As QuickTest.RunResultsOptions ' Declare a Run Results Options object variable
Dim pDefColl 'As QuickTest.ParameterDefinitions ' Declare a Parameter Definitions collection
Dim pDef ' As QuickTest.ParameterDefinition ' Declare a ParameterDefinition object
Dim rtParams 'As QuickTest.Parameters ' Declare a Parameters collection
Dim rtParam ' As QuickTest.Parameter ' Declare a Parameter object
Dim cnt
Dim Indx

' Open the test
qtApp.Open test_name, False ' Open a test named "Test1"
Dim qtTest
set qtTest=qtApp.Test

if (qtTest is nothing) then
	WScript.StdOut.Write("<QTP> automated test case open was NOT SUCCESSFUL!  ")
	Wscript.Quit(222)
end if
WScript.StdOut.Write("<QTP> automated test case open was SUCCESSFUL!   ")

qtApp.Launch ' Start QuickTest
qtApp.Visible = False ' Make the QuickTest application visible

' Retrieve the parameters collection defined for the test.
Set pDefColl = qtApp.Test.ParameterDefinitions

Set rtParams = pDefColl.GetParameters() ' Retrieve the Parameters collection defined for the test. 

qtp_file="c:\qtp_para.txt"
Dim arrFileLines()	
i = 0  
Set objFSO = CreateObject("Scripting.FileSystemObject")	
Set objFile = objFSO.OpenTextFile(qtp_file, 1)	 

Do Until objFile.AtEndOfStream	 
    Redim Preserve arrFileLines(i)	  
    arrFileLines(i) = objFile.ReadLine 
    i = i + 1				
Loop  
objFile.Close 
For l = Lbound(arrFileLines) to UBound(arrFileLines) 
 'Wscript.Echo arrFileLines(l)	 
'Next
'For Each Modify In AllModList   
   tmp = Split(arrFileLines(l),"=", 2)
   WScript.StdOut.Write(tmp(0) &":"&tmp(1)&"--**--")  
   Set rtParam = rtParams.Item(tmp(0)) ' Retrieve a specific parameter.
   rtParam.Value = tmp(1) ' Change the parameter value.
   
Next

Set qtOptions = CreateObject("QuickTest.RunResultsOptions") ' Create a Results Option object
qtOptions.ResultsLocation = result_dir ' Set the Results location to temporary location
qtApp.Test.Run qtOptions, True, rtParams ' Run the test with changed parameters.
'set LastError = qtApp.Test.LastRunResults.LastError
result = qtApp.Test.LastRunResults.Status
If "N" = keep_qtp_open Then
	qtApp.Quit ' Exit QuickTest			  Y-- keep open, N--- close
End If
If ("failed" = LCase(result)) Then
	Wscript.Quit(555)
End If
Wscript.Quit(666)


