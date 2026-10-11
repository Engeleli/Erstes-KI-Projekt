# AGENTS.md — Master-Leitfaden für alle KI-Agenten

> **GILT FÜR:** Claude, Gemini, Cursor, Copilot, ChatGPT und jeden anderen KI-Coding-Agenten.
> Dieser Leitfaden ist die primäre Einstiegsquelle für deine Arbeit in diesem Repository.

---

## 1. Schnelleinstieg & Protokoll beim Start (PFLICHT)
Bevor du irgendeine Aktion oder Code-Änderung vornimmst:
1. **Lies den aktuellen Status:** `context/CURRENT_STATE.md`
2. **Lies den Projekt-Kontext:** `context/PROJECT_CONTEXT.md`
3. **Prüfe die Projektregeln:** Lies alle Regeln im Ordner `rules/`.

## 2. Struktur des Projekts
```
├── AGENTS.md                 # Dieses Dokument (Universal-Einstieg)
├── CLAUDE.md                 # Claude-spezifischer Einstiegspunkt
├── GEMINI.md                 # Gemini-spezifischer Einstiegspunkt
├── .cursorrules              # Cursor-spezifischer Einstiegspunkt
├── agents/                   # Spezialisierte Rollen (.agent.md)
│   ├── planner.agent.md      # Planer & Architekt
│   ├── builder.agent.md      # Entwickler & Implementierer
│   └── reviewer.agent.md     # Reviewer & Tester
├── rules/                    # System- und Verhaltensregeln
│   ├── 01-session-handoff.md # Protokoll für Sitzungs- und Client-Wechsel
│   ├── 02-architecture-and-code.md # Code-Standards und Modularität
│   ├── 03-git-workflow.md    # Git-Commits und Auto-Push Verhalten
│   └── 04-safety-and-secrets.md # Secrets, .env und OS-Regeln
├── context/                  # Projektgedächtnis
│   ├── CURRENT_STATE.md      # Live-Zustand & Nächste Schritte
│   ├── PROJECT_CONTEXT.md    # Vision, Features, Tech-Stack
│   └── DECISIONS.md          # Architekturentscheidungen (ADR)
├── scripts/                  # Automatisierungs- & Wartungsskripte
│   ├── auto_push.ps1         # 30-Minuten Git Auto-Push
│   ├── setup_auto_push.ps1   # Registriert Task in Windows-Aufgabenplanung
│   └── stop_auto_push.ps1    # Entfernt Task aus Windows-Aufgabenplanung
└── src/                      # Quellcode der eigentlichen Anwendung
```

## 3. Protokoll bei Sitzungsende (PFLICHT)
Sobald du deine Aufgabe abgeschlossen hast oder die Sitzung beendet wird:
- Aktualisiere `context/CURRENT_STATE.md` mit dem aktuellen Stand, offenen Punkten und nächsten Schritten.
- Neue Architekturentscheidungen in `context/DECISIONS.md` erfassen.
- Führe einen sauberen Git-Commit durch (`git commit -m "..."`).

---
*Befolge diese Richtlinien gewissenhaft, um nahtloses Arbeiten im Multi-Agenten-Team zu gewährleisten.*
