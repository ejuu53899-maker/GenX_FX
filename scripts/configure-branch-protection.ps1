# Configure Branch Protection Rules
# Sets up branch protection for main and develop branches
#
# Usage: Set $env:GITHUB_TOKEN environment variable before running
#   $env:GITHUB_TOKEN = "your-token-here"
#   .\scripts\configure-branch-protection.ps1

$ErrorActionPreference = "Continue"

# Get token from environment variable
$token = $env:GITHUB_TOKEN
if (-not $token) {
    Write-Host "❌ GITHUB_TOKEN environment variable not set" -ForegroundColor Red
    Write-Host "Set it with: `$env:GITHUB_TOKEN = 'your-token'" -ForegroundColor Yellow
    exit 1
}

$owner = "Mouy-leng"
$repo = "Workspace-Monorepo"

Write-Host "Configuring branch protection rules..." -ForegroundColor Cyan

$headers = @{
    "Authorization" = "Bearer $token"
    "Accept" = "application/vnd.github.v3+json"
}

# Branch protection settings
$protectionSettings = @{
    required_status_checks = @{
        strict = $true
        contexts = @("CI")
    }
    enforce_admins = $false
    required_pull_request_reviews = @{
        required_approving_review_count = 1
        dismiss_stale_reviews = $true
        require_code_owner_reviews = $false
    }
    restrictions = $null
    allow_force_pushes = $false
    allow_deletions = $false
} | ConvertTo-Json -Depth 10

# Protect main branch
Write-Host "Protecting 'main' branch..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "https://api.github.com/repos/$owner/$repo/branches/main/protection" `
        -Method Put -Headers $headers -Body $protectionSettings -ContentType "application/json" | Out-Null
    Write-Host "✅ Main branch protected" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not protect main branch: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Protect develop branch (if exists)
Write-Host "Protecting 'develop' branch..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "https://api.github.com/repos/$owner/$repo/branches/develop/protection" `
        -Method Put -Headers $headers -Body $protectionSettings -ContentType "application/json" | Out-Null
    Write-Host "✅ Develop branch protected" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Develop branch doesn't exist yet or protection failed" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Branch protection configuration complete!" -ForegroundColor Green
