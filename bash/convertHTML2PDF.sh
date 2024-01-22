@echo off
for /R %%i in (*.html) do "C:\helloWorld\wkhtmltox\bin\wkhtmltopdf.exe" "%%i" "C:\helloWorld\VulnAssessPDF\%%~ni.pdf"
