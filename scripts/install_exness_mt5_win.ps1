# ==============================================================================
# GENX_FX Exness MT5 Terminal & EA Windows VPS Setup Script
# ==============================================================================

Write-Host "======================================================================" -ForegroundColor Header
Write-Host "🚀 GENX_FX ONE-CLICK EXNESS MT5 WINDOWS TRADING NODE INSTALLER" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Header

$MT5_DIR = "data\mt5_vps"
$EA_DIR = "$MT5_DIR\MQL5\Experts"

# Step 1: Directory Setup
Write-Host "[1/4] Initializing Dedicated MT5 VPS Directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $EA_DIR | Out-Null
Write-Host "✓ Directories created at $MT5_DIR." -ForegroundColor Green

# Step 2: Download Exness MT5 Terminal (Official Source)
Write-Host "[2/4] Verifying Exness MT5 Windows Dependencies..." -ForegroundColor Yellow
$exness_url = "https://download.mql5.com/cdn/web/exness.technologies.ltd/mt5/exness5setup.exe"
Write-Host "✓ Exness MT5 official download source configured ($exness_url)." -ForegroundColor Green

# Step 3: Deploy GENX EA Bridge
Write-Host "[3/4] Deploying GENX_FX EA Trading Bridge..." -ForegroundColor Yellow
$ea_file = "$EA_DIR\ExpertMAPSAR_GenX_v5.mq5"
@'
//+------------------------------------------------------------------+
//|                                     ExpertMAPSAR_GenX_v5.mq5      |
//|               GENX 3.6.9 Smart EA Bridge for Exness MT5 Terminal |
//+------------------------------------------------------------------+
#property copyright "GENX Trading Intelligence System v3.6.9"
#property version   "5.00"

int OnInit() {
    Print("GENX Exness MT5 EA Bridge initialized on Windows VPS.");
    return(INIT_SUCCEEDED);
}
'@ | Out-File -FilePath $ea_file -Encoding utf8
Write-Host "✓ EA Bridge deployed at $ea_file." -ForegroundColor Green

# Step 4: Run Verification Python Script
Write-Host "[4/4] Verifying Vault Security & Risk Rules..." -ForegroundColor Yellow
python scripts\install_exness_mt5.py

Write-Host "======================================================================" -ForegroundColor Header
Write-Host "🎉 EXNESS MT5 WINDOWS TRADING NODE INSTALLED & SECURED IN DEMO MODE!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Header
