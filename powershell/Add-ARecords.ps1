# Define DNS server and zone information
$dnsServer = "INSERT-DNS-SERVER-NAME"
$zoneName = "INSERT-DNS-ZONE-NAME"

# Import the DNS module - not sure if required
Import-Module DnsServer

# Connect to the DNS server
$dnsSession = New-DnsServerSession -ComputerName $dnsServer

# Function to check if A record exists
function DoesARecordExist {
    param (
        [string]$recordName
    )

    $existingRecord = Get-DnsServerResourceRecord -ZoneName $zoneName -Name $recordName -RRType A -ErrorAction SilentlyContinue
    return [bool]($existingRecord -ne $null)
}

# Function to add A record if it doesn't exist
function AddARecord {
    param (
        [string]$recordName,
        [string]$recordIPAddress
    )

    if (-not (DoesARecordExist -recordName $recordName)) {
        Add-DnsServerResourceRecordA -ZoneName $zoneName -Name $recordName -IPv4Address $recordIPAddress -TimeToLive 01:00:00
        Write-Host "A record added successfully: $recordName - $recordIPAddress"
    } else {
        Write-Host "A record already exists: $recordName - $recordIPAddress"
    }
}

# Read input from CSV file [1st column is hostname, 2nd column is IP Address]
$csvFilePath = "MISSING-A-RECORDS.csv"
$csvData = Import-Csv -Path $csvFilePath

# Process each row in the CSV
foreach ($row in $csvData) {
    $recordName = $row.HostName
    $recordIPAddress = $row.IPAddress
    AddARecord -recordName $recordName -recordIPAddress $recordIPAddress
}

# Close the DNS session
Remove-DnsServerSession -Session $dnsSession
