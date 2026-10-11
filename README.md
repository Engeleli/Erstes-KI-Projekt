# Historischer Recherche- & Verifikations-Workflow 🏛️

Ein Multi-Agenten-System fuer die geschichtswissenschaftliche Abschlussarbeit mit **kryptografischer Quellensicherung**, **deterministischer Zitat-Verifikation** gegen KI-Halluzinationen und automatischem 30-Minuten-GitHub-Backup.

---

## 🔍 Wie das System Halluzinationen verhindert

In der Geschichtswissenschaft sind erfundene Zitate oder falsche Jahreszahlen fatal. Dieses Repository loest das Problem auf zweifache Weise:

1. **Echte Schnappschuesse statt KI-Gedaechtnis:**
   - Webseiten und PDFs werden nicht von der KI "gelesen", sondern deterministisch ueber Python (`src/snapshot.py`) heruntergeladen und als Textkopie in `sources/raw/` abgelegt.
   - Jede Quelle erhaelt einen unveraenderlichen SHA-256 Hash und Zeitstempel in `sources/catalog.json`.

2. **Deterministische Zitat-Pruefung:**
   - Jede geschichtliche Aussage benoetigt ein woertliches Zitat.
   - `src/verifier.py` prueft Zeichenkette fuer Zeichenkette, ob das Zitat exakt im Quelltext vorkommt.
   - Bei Abweichung wird sofort `[HALLUCINATION_DETECTED]` gemeldet und die Aussage verworfen.

---

## 🤖 Die Agenten-Rollen

- **[archivist.agent.md](file:///c:/Users/ellye/Documents/Erstes%20KI%20Projekt/agents/archivist.agent.md):** Sucht Quellen in Bibliotheken/Archiven und sichert sie lokal.
- **[factchecker.agent.md](file:///c:/Users/ellye/Documents/Erstes%20KI%20Projekt/agents/factchecker.agent.md):** Kritischer Pruefer (Adversary), der Zitate prueft und Quellenkritik durchfuehrt.
- **[synthesizer.agent.md](file:///c:/Users/ellye/Documents/Erstes%20KI%20Projekt/agents/synthesizer.agent.md):** Fasst verifizierte Befunde zu wissenschaftlichen Exzerpten und Fußnoten zusammen.

---

## 🛠️ Schnellstart & Befehle

Virtuelle Umgebung aktivieren und Tools nutzen:

```powershell
# 1. Quelle sichern (Webseite oder PDF)
.\.venv\Scripts\python.exe -m src.snapshot --url "https://beispiel-archiv.de/dokument" --title "Dokumententitel"

# 2. Belegzitat pruefen
.\.venv\Scripts\python.exe -m src.verifier --source src_001 --quote "Wortwoertliches Zitat" --claim "Geschichtliche Behauptung"

# 3. Wissenschaftliches Exzerpt anlegen
.\.venv\Scripts\python.exe -m src.excerpt --source src_001 --topic "Mein Thema"
```

---

## 📁 Projektstruktur

```
Erstes KI Projekt/
├── AGENTS.md                 # Universal-Leitfaden fuer alle KI-Agenten
├── CLAUDE.md                 # Direkteinstieg fuer Claude
├── GEMINI.md                 # Direkteinstieg fuer Gemini
├── .cursorrules              # Direkteinstieg fuer Cursor
├── agents/                   # Spezialisierte Rollen (Archivar, Faktenpruefer, Synthesizer)
├── rules/                    # Feste Regeln (u.a. 05-historical-grounding-and-citations.md)
├── context/                  # Gedaechtnis (CURRENT_STATE.md, PROJECT_CONTEXT.md)
├── sources/                  # Rohquellen (.txt) und gepruefte Exzerpte (.md)
├── src/                      # Python-Werkzeuge (snapshot.py, verifier.py, excerpt.py)
└── scripts/                  # 30-Minuten Auto-Push zu GitHub
```
