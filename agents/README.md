# Spezialisierte Agenten-Rollen

In diesem Ordner sind die Rollenprofile fuer den **historischen Recherche- und Verifikations-Workflow** hinterlegt.

| Rolle | Datei | Funktion im Recherche-Workflow |
|---|---|---|
| **Archivar** | [archivist.agent.md](file:///c:/Users/ellye/Documents/Erstes%20KI%20Projekt/agents/archivist.agent.md) | Quellen-Recherche, Web- & PDF-Download, SHA-256 Hashes via `src/snapshot.py` |
| **Quellenkritiker & Faktenpruefer** | [factchecker.agent.md](file:///c:/Users/ellye/Documents/Erstes%20KI%20Projekt/agents/factchecker.agent.md) | Deterministische Zitatpruefung via `src/verifier.py`, Aufdeckung von Halluzinationen |
| **Abschlussarbeits-Synthesizer** | [synthesizer.agent.md](file:///c:/Users/ellye/Documents/Erstes%20KI%20Projekt/agents/synthesizer.agent.md) | Erstellt wissenschaftliche Exzerpte, Argumentationsboegen und Fußnoten |

### Allgemeine Rollen (System-Entwicklung):
- [planner.agent.md](file:///c:/Users/ellye/Documents/Erstes%20KI%20Projekt/agents/planner.agent.md) — Systemarchitektur & Feature-Planung
- [builder.agent.md](file:///c:/Users/ellye/Documents/Erstes%20KI%20Projekt/agents/builder.agent.md) — Entwickler & Tool-Builder
- [reviewer.agent.md](file:///c:/Users/ellye/Documents/Erstes%20KI%20Projekt/agents/reviewer.agent.md) — Code-Review & QA
