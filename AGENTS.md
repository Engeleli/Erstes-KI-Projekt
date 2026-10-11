# AGENTS.md — Master-Leitfaden für alle KI-Agenten

> **GILT FÜR:** Claude, Gemini, Cursor, Copilot, ChatGPT und jeden anderen KI-Coding-Agenten.
> Dieser Leitfaden ist die primäre Einstiegsquelle für deine Arbeit in diesem Repository.

---

## 1. Schnelleinstieg & Protokoll beim Start (PFLICHT)
Bevor du irgendeine Aktion oder Code-Änderung vornimmst:
1. **Lies den aktuellen Status:** `context/CURRENT_STATE.md`
2. **Lies den Projekt-Kontext:** `context/PROJECT_CONTEXT.md`
3. **Prüfe die Projektregeln:** Lies alle Regeln im Ordner `rules/` (insb. [05-historical-grounding-and-citations.md](file:///c:/Users/ellye/Documents/Erstes%20KI%20Projekt/rules/05-historical-grounding-and-citations.md)).

## 2. Struktur des Projekts
```
├── AGENTS.md                 # Dieses Dokument (Universal-Einstieg)
├── CLAUDE.md                 # Claude-spezifischer Einstiegspunkt
├── GEMINI.md                 # Gemini-spezifischer Einstiegspunkt
├── .cursorrules              # Cursor-spezifischer Einstiegspunkt
├── agents/                   # Spezialisierte Rollen (.agent.md)
│   ├── archivist.agent.md    # Quellen-Sammler & Web-/PDF-Downloader
│   ├── factchecker.agent.md  # Adversarial Faktenprüfer & Zitatverifikation
│   ├── synthesizer.agent.md  # Redaktion, Exzerpte & Fußnoten
│   ├── planner.agent.md      # Planer & Architekt
│   ├── builder.agent.md      # Entwickler & Implementierer
│   └── reviewer.agent.md     # Reviewer & Tester
├── rules/                    # System- und Verhaltensregeln
│   ├── 01-session-handoff.md # Protokoll für Sitzungs- und Client-Wechsel
│   ├── 02-architecture-and-code.md # Code-Standards und Modularität
│   ├── 03-git-workflow.md    # Git-Commits und Auto-Push Verhalten
│   ├── 04-safety-and-secrets.md # Secrets, .env und OS-Regeln
│   └── 05-historical-grounding-and-citations.md # Anti-Halluzinations-Gebot
├── context/                  # Projektgedächtnis
│   ├── CURRENT_STATE.md      # Live-Zustand & Nächste Schritte
│   ├── PROJECT_CONTEXT.md    # Vision, Features, Tech-Stack
│   └── DECISIONS.md          # Architekturentscheidungen (ADR)
├── sources/                  # Gesicherte Quellentexte & Exzerpte
│   ├── raw/                  # Unveränderliche Quelltexte (.txt/.html) mit Hashes
│   ├── excerpts/             # Geprüfte Exzerpte für die Abschlussarbeit
│   └── catalog.json          # Quellen-Index mit SHA-256 Hashes
├── src/                      # Python-Verifikationswerkzeuge
│   ├── snapshot.py           # Lädt Seiten/PDFs deterministisch herunter
│   ├── verifier.py           # Zitat- & Halluzinations-Prüfengine
│   └── excerpt.py            # Generiert wissenschaftliche Exzerpte
└── scripts/                  # Automatisierungs- & Wartungsskripte
    ├── auto_push.ps1         # 30-Minuten Git Auto-Push
    ├── setup_auto_push.ps1   # Registriert Task in Windows-Aufgabenplanung
    └── stop_auto_push.ps1    # Entfernt Task aus Windows-Aufgabenplanung
```

## 3. Anti-Halluzinations-Workflow (PFLICHT FÜR RECHERCHE)
1. **Keine Behauptung ohne Quelle:** Zuerst mit `src/snapshot.py` die Quelle sichern.
2. **Jede Behauptung belegen:** Mit `src/verifier.py` das wörtliche Zitat gegen den Text prüfen.
3. **Nur verifizierte Fakten:** Erst nach Status `[VERIFIED]` darf die Aussage in die Abschlussarbeit / Exzerpte einfließen.

## 4. Protokoll bei Sitzungsende (PFLICHT)
Sobald du deine Aufgabe abgeschlossen hast oder die Sitzung beendet wird:
- Aktualisiere `context/CURRENT_STATE.md` mit dem aktuellen Stand, offenen Punkten und nächsten Schritten.
- Neue Architekturentscheidungen in `context/DECISIONS.md` erfassen.
- Führe einen sauberen Git-Commit durch (`git commit -m "..."`).
