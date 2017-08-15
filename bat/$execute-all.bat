
::		json_string
::                ,  startdate_string = '2004-12-31'
::               ,  enddate_string = '2016-03-31' #'2013-12-31'
::                ,  period='Monthly'
::                ,  pctchangeorlogreturn = 'pctchange'
::                ,  source='local'

@echo off
set /p jsonstring=< managerweights.json  
echo %jsonstring%

for %%x in (managerweights.json) do (
    more +1 "%%x" >tmp
    move /y tmp "%%x"
)
rem Run your utility here
for %%x in (managerweights.json) do (
    type "%%x" >>tmp
    move /y tmp "%%x"
)

@echo off
setlocal
call :strlen result %jsonstring%
echo length of line is %result%
pause
if not %result% gtr 0 goto nothing_to_do:

::set jsonstring={"Granite Partners Small Core Plus":[0.5,0.2],"Harding Loevner Glob Eq ADR":[0.5,0.1],"Logan Capital Concentrated Val":[0.5,0.1],"Hilton Capital YP":[0.4,0.05]}

"C:\Anaconda\python.exe" "C:\Batches\AutomationProjects\EfficientFrontier\code_using_repository\py\outputefficientfrontier_runfrombatch.py" %jsonstring% 2006-12-31 2016-01-31 Monthly pctchange local 700
pause
goto exit_proc:

:nothing_to_do
echo "nothing to do"
pause
:exit_proc
pause

:strlen <resultVar> <stringVar>
(   
    setlocal EnableDelayedExpansion
    set "s=!%~2!#"
    set "len=0"
    for %%P in (4096 2048 1024 512 256 128 64 32 16 8 4 2 1) do (
        if "!s:~%%P,1!" NEQ "" ( 
            set /a "len+=%%P"
            set "s=!s:~%%P!"
        )
    )
)
( 
    endlocal
    set "%~1=%len%"
    exit /b
)
