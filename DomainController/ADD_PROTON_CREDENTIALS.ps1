# Add ProtonMail and Wallet Credentials
# Updates .env and SecureVault with ProtonMail and wallet information

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "============================================================================"
Write-Host "  ADDING PROTONMAIL AND WALLET CREDENTIALS"
Write-Host "============================================================================"
Write-Host ""

# Update .env file
Write-Host "[1] Updating .env file..." -ForegroundColor Cyan

if (-not (Test-Path ".env")) {
    Write-Host "  Creating .env file..." -ForegroundColor Yellow
    "# Domain Controller Environment Variables`n# Team A6_9V`n" | Set-Content ".env"
}

$envContent = Get-Content ".env" -ErrorAction SilentlyContinue
if (-not $envContent) {
    $envContent = @()
}

# Remove old Proton entries
$envContent = $envContent | Where-Object {
    $_ -notmatch '^(PROTONMAIL_EMAIL|PROTON_WALLET|ADMIN_EMAIL|NAMECHEAP_EMAIL)=' -and
    $_ -notmatch '^# Email Accounts' -and
    $_ -notmatch '^# Proton'
}

# Add email accounts section
$newContent = @()
$newContent += $envContent
$newContent += ""
$newContent += "# Email Accounts"
$newContent += "# Updated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$newContent += "ADMIN_EMAIL=lengkundee01@gmail.com"
$newContent += "NAMECHEAP_EMAIL=keamouyleng369@gmail.com"
$newContent += "PROTONMAIL_EMAIL=keamouyleng@proton.me"
$newContent += ""
$newContent += "# Proton Wallet (BTC)"
$newContent += "# Add your BTC wallet address and password below:"
$newContent += "# PROTON_WALLET_BTC_ADDRESS="
$newContent += "# PROTON_WALLET_PASSWORD="

$newContent | Set-Content ".env"
Write-Host "  ✅ .env file updated" -ForegroundColor Green
Write-Host ""

# Update SecureVault
Write-Host "[2] Updating SecureVault..." -ForegroundColor Cyan

$vaultPath = "SecureVault\Credentials"
if (-not (Test-Path $vaultPath)) {
    New-Item -ItemType Directory -Path $vaultPath -Force | Out-Null
}

# Create ProtonMail credentials file
$protonMailFile = Join-Path $vaultPath "protonmail_credentials.json"
$protonMailData = @{
    email = "keamouyleng@proton.me"
    service = "ProtonMail"
    purpose = "Secure email communications"
    created = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    team = "A6_9V"
} | ConvertTo-Json -Depth 3

$protonMailData | Set-Content $protonMailFile
Write-Host "  ✅ ProtonMail credentials saved to SecureVault" -ForegroundColor Green

# Create wallet directory
$walletPath = Join-Path $vaultPath "Wallets"
if (-not (Test-Path $walletPath)) {
    New-Item -ItemType Directory -Path $walletPath -Force | Out-Null
}

# Create Proton Wallet file
$protonWalletFile = Join-Path $walletPath "proton_wallet.json"
$protonWalletData = @{
    wallet_type = "Proton Wallet"
    cryptocurrency = "BTC"
    service = "Proton Wallet"
    created = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    team = "A6_9V"
    note = "Add your BTC address and password in SecureVault"
} | ConvertTo-Json -Depth 3

$protonWalletData | Set-Content $protonWalletFile
Write-Host "  ✅ Wallet template created in SecureVault" -ForegroundColor Green
Write-Host ""

# Update credential inventory
Write-Host "[3] Updating credential inventory..." -ForegroundColor Cyan

$inventoryFile = Join-Path $vaultPath "CREDENTIAL_INVENTORY.json"
if (Test-Path $inventoryFile) {
    try {
        $inventory = Get-Content $inventoryFile | ConvertFrom-Json
    } catch {
        $inventory = @{}
    }
} else {
    $inventory = @{}
}

# Add ProtonMail entry
if (-not $inventory.PSObject.Properties['protonmail']) {
    $inventory | Add-Member -MemberType NoteProperty -Name "protonmail" -Value @{
        email = "keamouyleng@proton.me"
        service = "ProtonMail"
        location = "SecureVault/Credentials/protonmail_credentials.json"
        updated = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    }
}

# Add wallet entry
if (-not $inventory.PSObject.Properties['proton_wallet']) {
    $inventory | Add-Member -MemberType NoteProperty -Name "proton_wallet" -Value @{
        wallet_type = "Proton Wallet"
        cryptocurrency = "BTC"
        location = "SecureVault/Credentials/Wallets/proton_wallet.json"
        updated = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    }
}

$inventory | ConvertTo-Json -Depth 5 | Set-Content $inventoryFile
Write-Host "  ✅ Credential inventory updated" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "============================================================================"
Write-Host "  SUMMARY"
Write-Host "============================================================================"
Write-Host ""
Write-Host "✅ ProtonMail email added: keamouyleng@proton.me" -ForegroundColor Green
Write-Host "✅ Wallet template created for BTC" -ForegroundColor Green
Write-Host "✅ Credentials stored in SecureVault" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Add your BTC wallet address to SecureVault/Credentials/Wallets/proton_wallet.json" -ForegroundColor White
Write-Host "  2. Store wallet password securely (use SecureVault API Key Manager)" -ForegroundColor White
Write-Host "  3. Update .env file with wallet address if needed" -ForegroundColor White
Write-Host ""
Write-Host "============================================================================"
Write-Host ""
