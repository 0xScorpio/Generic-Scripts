# Define DNS server and zone information
$dnsServer = "HOSTNAME-DOMAINCONTROLLER"
$zoneName = "ZONE"

# Import the DNS module - not sure if required
Import-Module DnsServer

# Connect to the DNS server
$dnsSession = New-DnsServerSession -ComputerName $dnsServer

# Function to check if A record exists (with case normalization)
function DoesARecordExist {
    param (
        [string]$recordName
    )

    $recordNameNormalized = $recordName.ToLower()
    $existingRecord = Get-DnsServerResourceRecord -ZoneName $zoneName -Name $recordNameNormalized -RRType A -ErrorAction SilentlyContinue
    return [bool]($existingRecord -ne $null)
}

# Function to add A record if it doesn't exist (with case normalization)
function AddARecord {
    param (
        [string]$recordName,
        [string]$recordIPAddress
    )

    $recordNameNormalized = $recordName.ToLower()
    
    if (-not (DoesARecordExist -recordName $recordNameNormalized)) {
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
