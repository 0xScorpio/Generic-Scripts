@echo off
setlocal enabledelayedexpansion

REM Domain controller IP address to exclude
set "dcIpAddress=10.72.3.101"  REM Replace with your domain controller's IP address

REM Path to your names file
set "namesFile=resolve2IP.txt"

REM Output file for IP addresses
set "outputFile=resolvedIPaddresses.txt"

REM Loop through each name in the file
for /f "tokens=*" %%a in (%namesFile%) do (
    set "name=%%a"

    REM Perform nslookup for each name
    for /f "tokens=2" %%i in ('nslookup !name! ^| findstr /C:"Address"') do (
        REM Check if the obtained IP address is not the domain controller's IP
        if "%%i" neq "%dcIpAddress%" (
            REM Append results to the output file
            echo !name!: %%i>> %outputFile%
        )
    )
)

echo IP addresses (excluding domain controller) have been retrieved and saved to %outputFile%.
pause
