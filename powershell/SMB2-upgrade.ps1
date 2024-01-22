#Obtain current state of the SMB server protocol configuration:
Get-SmbServerConfiguration | Select EnableSMB1Protocol, EnableSMB2Protocol
Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol


#Disable
Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
#Disable SMBv1 on the server:
Set-SmbServerConfiguration -EnableSMB1Protocol $false
#Enable SMBv2 and SMBv3 on the server:
Set-SmbServerConfiguration -EnableSMB2Protocol $true
#Check
Get-Item HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters | ForEach-Object {Get-ItemProperty $_.pspath}
