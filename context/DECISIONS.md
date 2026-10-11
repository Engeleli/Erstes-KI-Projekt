# Architektur-Entscheidungen (ADR Log)

Jede wesentliche Architekturentscheidung wird hier kurz mit Datum, Kontext und Begründung festgehalten.

---

### ADR-001: Multi-Agenten-Architektur und dateibasierte Persistenz
- **Datum:** 2026-10-11
- **Status:** Angenommen
- **Kontext:** Verschiedene KI-Agenten (Claude, Gemini, Cursor etc.) sollen nahtlos zusammenarbeiten und Sitzungswechsel ohne Kontextverlust ermöglichen.
- **Entscheidung:** Zentrale Steuerung über `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`. Trennung von Rollen (`agents/`), Richtlinien (`rules/`) und Projektgedächtnis (`context/`). Handoff-Status in `context/CURRENT_STATE.md`.

---

### ADR-002: Automatisierter 30-Minuten-Push via Windows Task Scheduler
- **Datum:** 2026-10-11
- **Status:** Angenommen
- **Kontext:** Sicherung des Arbeitsfortschritts gegen Datenverlust ohne manuellen Aufwand.
- **Entscheidung:** Ein PowerShell-Skript in `scripts/auto_push.ps1` prüft alle 30 Minuten auf Änderungen und pusht diese mit Zeitstempel nach GitHub.

---

### ADR-003: Deterministische Anti-Halluzinations-Pipeline fuer Geschichtswissenschaft
- **Datum:** 2026-10-11
- **Status:** Angenommen
- **Kontext:** Historische Arbeiten erfordern 100% verifizierbare Belege. KIs halluzinieren Zitate und Jahreszahlen.
- **Entscheidung:**
  - Echte Python-Downloads sichern Textkopien mit SHA-256 Hashes in `sources/raw/`.
  - Strikter Beleg-Zwang: Jede Behauptung muss ein wörtliches Zitat enthalten.
  - Das Tool `src/verifier.py` prüft den Quelltext deterministisch per String-Match. Bei Nicht-Auffinden wird die Behauptung als Halluzination abgewiesen.

---

### ADR-004: Dreiteilige Agenten-Rollenstruktur fuer historische Forschung
- **Datum:** 2026-10-11
- **Status:** Angenommen
- **Entscheidung:** Trennung der Aufgaben in drei spezialisierte Agenten:
  1. `archivist.agent.md` — Quellensuche & unverfälschte Sicherung.
  2. `factchecker.agent.md` — Adversarial Verification & Quellenkritik.
  3. `synthesizer.agent.md` — Erstellung von Exzerpten und wissenschaftlichen Fußnoten.
