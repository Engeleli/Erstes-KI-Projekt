# Auto-Push Script fuer Erstes KI Projekt
$projectDir = "C:\Users\ellye\Documents\Erstes KI Projekt"
$logFile = Join-Path $projectDir "auto_push.log"

function Write-Log {
    param([string]$message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$ts] $message"
    Add-Content -Path $logFile -Value $entry -Encoding UTF8
    Write-Output $entry
}

Set-Location $projectDir

# Pruefe, ob Remote-Repository existiert
$remote = git remote get-url origin 2>$null
if (-not $remote) {
    Write-Log "WARNUNG: Kein Git-Remote 'origin' konfiguriert."
    exit 1
}

# Pruefe auf geaenderte oder neue Dateien
$changes = git status --porcelain
if ($changes) {
    Write-Log "Aenderungen gefunden. Erstelle Commit..."
    git add -A
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitOut = git commit -m "Auto-Commit: $timestamp" 2>&1
    Write-Log ($commitOut -join " ")
} else {
    Write-Log "Keine lokalen Dateiaenderungen."
}

# Pruefe, ob unpushte Commits vorliegen
$unpushed = git cherry -v 2>$null
if ($unpushed -or $changes) {
    Write-Log "Pushe Aenderungen zu GitHub..."
    $pushOut = git push origin main 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "Erfolgreich zu GitHub gepusht!"
    } else {
        Write-Log "FEHLER beim Pushen (Exit Code: $LASTEXITCODE)"
    }
} else {
    Write-Log "Bereits aktuell. Kein Push erforderlich."
}
