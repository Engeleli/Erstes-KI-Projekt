# Entfernt die automatische Push-Aufgabe aus der Windows-Aufgabenplanung
$taskName = "ErstesKIProjekt_AutoPush"
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
Write-Output "Aufgabe '$taskName' wurde erfolgreich entfernt."
