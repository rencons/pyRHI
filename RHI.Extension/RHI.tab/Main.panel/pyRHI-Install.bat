@ECHO OFF
@ECHO COPY pyRHI TOOL
@PAUSE

set "pyRHIlocal=%APPDATA%\pyRevit\Extensions\pyRHI.extension"
set "pyRHIserver=\\fs-hi\USERS\romangolev\pyRHI.extension"


:choice1
set /P a=Do you want to reinstall existing pyRHI [y/n]?
if /I "%a%" EQU "y" goto :rein
if /I "%a%" EQU "n" goto :inst

:rein
pyrevit extensions delete RHI --debug

:inst
xcopy "%pyRHIserver%" "%pyRHIlocal%" /r /s



@ECHO RD /S /Q %APPDATA%\pyRevit\Extensions\1
@ECHO RD /S /Q %APPDATA%\pyRevit\Extensions\pyRHI.extension
@ECHO xcopy "\\fs-hi\USERS\romangolev\pyRHI.extension" "%APPDATA%\pyRevit\Extensions\pyRHI.extension" /r /s
@ECHO ----------------------------------------------------------
@ECHO -----------------RESTART--PYREVIT-------------------------
@ECHO ----------------------------------------------------------
