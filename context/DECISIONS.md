# Architektur-Entscheidungen (ADR Log)

Jede wesentliche Architekturentscheidung wird hier kurz mit Datum, Kontext und Begründung festgehalten.

---

### ADR-001: Multi-Agenten-Architektur und dateibasierte Persistenz
- **Datum:** 2026-10-11
- **Status:** Angenommen
- **Kontext:** Verschiedene KI-Agenten (Claude, Gemini, Cursor etc.) sollen nahtlos zusammenarbeiten und Sitzungswechsel ohne Kontextverlust ermöglichen.
- **Entscheidung:**
  - Zentrale Steuerung über `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
  - Trennung von Rollen (`agents/`), Richtlinien (`rules/`) und Projektgedächtnis (`context/`).
  - Handoff-Status in `context/CURRENT_STATE.md`.
- **Konsequenzen:** Jeder Agent hat sofortigen Zugriff auf Historie, Regeln und Rollen, unabhängig vom verwendeten AI-Client.

---

### ADR-002: Automatisierter 30-Minuten-Push via Windows Task Scheduler
- **Datum:** 2026-10-11
- **Status:** Angenommen
- **Kontext:** Sicherung des Arbeitsfortschritts gegen Datenverlust ohne manuellen Aufwand.
- **Entscheidung:** Ein PowerShell-Skript in `scripts/auto_push.ps1` prüft alle 30 Minuten auf Änderungen und pusht diese mit Zeitstempel nach GitHub.
