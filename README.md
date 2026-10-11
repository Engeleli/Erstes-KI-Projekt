# Erstes KI Projekt 🚀

Ein modernes, modulares KI-Projekt mit nativer Multi-Agenten-Unterstützung (Claude, Gemini, Cursor etc.), automatischem GitHub-Backup und persistentem Sitzungsgedächtnis.

---

## 📁 Projektstruktur

```
Erstes KI Projekt/
├── AGENTS.md                 # Universal-Leitfaden für alle KI-Agenten
├── CLAUDE.md                 # Spezifischer Einstieg für Claude Code
├── GEMINI.md                 # Spezifischer Einstieg für Gemini / Antigravity
├── .cursorrules              # Spezifischer Einstieg für Cursor
├── agents/                   # Spezialisierte Agenten-Rollen (.agent.md)
│   ├── planner.agent.md      # Planer & Systemarchitekt
│   ├── builder.agent.md      # Entwickler & Implementierer
│   └── reviewer.agent.md     # Reviewer & Tester
├── rules/                    # Feste Projektregeln
│   ├── 01-session-handoff.md # Protokoll für nahtlosen Sitzungswechsel
│   ├── 02-architecture-and-code.md # Code-Standards & Modularität
│   ├── 03-git-workflow.md    # Git-Workflow & Auto-Push
│   └── 04-safety-and-secrets.md # Schutz von API-Keys & Windows-Regeln
├── context/                  # Projektgedächtnis (bleibt immer erhalten)
│   ├── CURRENT_STATE.md      # Aktueller Arbeitsstand & nächste Schritte
│   ├── PROJECT_CONTEXT.md    # Projektziele, Vision & Tech-Stack
│   └── DECISIONS.md          # Architekturentscheidungen (ADR)
├── scripts/                  # Automatisierungs- & Wartungsskripte
│   ├── auto_push.ps1         # Automatischer 30-Minuten Git Push
│   ├── setup_auto_push.ps1   # Einrichtungs-Skript für Windows-Aufgabenplanung
│   └── stop_auto_push.ps1    # Deaktivierungs-Skript
└── src/                      # Quellcode der eigentlichen Anwendung
```

---

## 🤖 Zusammenarbeit mit Agenten

- **Sitzungs- und Client-Wechsel:** Jeder Agent liest beim Start automatisch `context/CURRENT_STATE.md` und aktualisiert sie am Ende. So geht nie Kontext verloren, selbst wenn du zwischen Gemini, Claude oder Cursor wechselst.
- **Automatischer Push:** Alle 30 Minuten sichert eine Windows-Aufgabe den aktuellen Code automatisch in dein GitHub-Repository ([Engeleli/Erstes-KI-Projekt](https://github.com/Engeleli/Erstes-KI-Projekt)).
