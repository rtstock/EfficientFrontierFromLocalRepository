@echo off
set /p texte=< test.json  
echo %texte%

for %%x in (test.json) do (
    more +1 "%%x" >tmp
    move /y tmp "%%x"
)
rem Run your utility here
for %%x in (test.json) do (
    ::echo X,Y,Z>tmp
    type "%%x" >>tmp
    move /y tmp "%%x"
)
pause