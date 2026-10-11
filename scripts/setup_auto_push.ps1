# Einrichtung des automatischen 30-Minuten-Pushs in der Windows-Aufgabenplanung
$taskName = "ErstesKIProjekt_AutoPush"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $scriptDir "auto_push.ps1"

# Vorhandene Aufgabe ggf. entfernen
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# Aktion definieren: PowerShell im Hintergrund ausfuehren
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""

# Trigger definieren: Startet jetzt und wiederholt sich alle 30 Minuten
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 30)

# Einstellungen: Bei Akkubetrieb ausfuehren, Timeout auf 10 Minuten
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

# Aufgabe fuer aktuellen Benutzer registrieren
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Pusht alle 30 Minuten Aenderungen aus Erstes KI Projekt zu GitHub."

Write-Output "Aufgabe '$taskName' erfolgreich aktualisiert! Verweist auf $scriptPath."

