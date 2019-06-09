REM This command must be run from the multi-part-print-cost/build-files dir
cd ..
FOR /F "tokens=* USEBACKQ" %%F IN (`cd`) DO (
SET currentDir=%%F
)
SET PYTHONPATH=%PYTHONPATH%%currentDir%;
cd
pyinstaller build-files\multi-part-print-cost.spec
copy README.md dist\
Xcopy /E /I bin dist\bin
Xcopy /E /I profiles dist\profiles
