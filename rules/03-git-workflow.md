# Regel 03: Git-Workflow & Auto-Push

## 1. Automatischer 30-Minuten-Push
- Ein Windows Task führt alle 30 Minuten das Skript `scripts/auto_push.ps1` aus.
- Dieses Skript committet alle Änderungen mit Zeitstempel und pusht nach `origin main`.
- **Wichtig für Agenten:** Keine unfertigen, kaputten Codezeilen im Projektverzeichnis hinterlassen, die den Build brechen würden. Vor Unterbrechungen Zwischenstände syntaktisch korrekt halten!

## 2. Manuelle Commits durch Agenten
- Nach Abschluss einer zusammenhängenden Aufgabe soll der Agent proaktiv einen manuellen Git-Commit mit prägnanter Commit-Nachricht erstellen (z. B. `feat(api): add auth endpoint`).
- Bei größeren Meilensteinen direkt pushen (`git push origin main`), ohne auf den 30-Minuten-Takt zu warten.
