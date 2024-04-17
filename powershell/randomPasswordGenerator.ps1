function Random-Password {
    param (
        [Parameter(Mandatory=$true)]
        [int]$Length,
        [string]$Characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?'
    )
     
    $password = -join (1..$length | ForEach-Object { Get-Random -InputObject $characters.ToCharArray() })
    return $password
}
