@echo off
echo Archiving ASMg and DeviceClientApp projects...

:: Create archive directory if it doesn't exist
if not exist "C:\Projects\ASMg_DeviceClientApp_SW" mkdir "C:\Projects\ASMg_DeviceClientApp_SW"

:: Create temporary directory for archiving
set TEMP_DIR=%TEMP%\ASMg_Archive_%RANDOM%
mkdir "%TEMP_DIR%"

:: Copy ASMg project
echo Copying ASMg project...
xcopy /E /I /Y "%~dp0" "%TEMP_DIR%\ASMg"

:: Copy DeviceClientApp project
echo Copying DeviceClientApp project...
xcopy /E /I /Y "%~dp0\..\DeviceClientApp" "%TEMP_DIR%\DeviceClientApp"

:: Create archive
set TIMESTAMP=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set ARCHIVE_NAME=ASMg_Full_%TIMESTAMP%

echo Creating archive %ARCHIVE_NAME%.zip...
powershell Compress-Archive -Path "%TEMP_DIR%\*" -DestinationPath "C:\Projects\ASMg_DeviceClientApp_SW\%ARCHIVE_NAME%.zip" -Force

:: Clean up temporary files
echo Cleaning up temporary files...
rmdir /S /Q "%TEMP_DIR%"

echo Archiving completed successfully!
echo Archive created: C:\Projects\ASMg_DeviceClientApp_SW\%ARCHIVE_NAME%.zip
pause 