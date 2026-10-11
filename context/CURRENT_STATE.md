# Aktueller Projektstatus (Session Handoff)

> **Wichtig für jeden Agenten (Claude, Gemini, etc.):**
> Lies diese Datei zu Beginn JEDER neuen Sitzung. Aktualisiere sie am Ende deiner Arbeit oder nach größeren Meilensteinen!

---

## 1. Letzter Stand
- **Datum:** 2026-10-11
- **Letzter Agent:** Gemini (Antigravity)
- **Status:** Historischer Recherche- und Verifikations-Workflow vollstaendig implementiert, getestet und quellengesichert!

## 2. Zuletzt erledigt
- [x] Python 3.12 und virtuelle Umgebung `.venv` mit `requests`, `beautifulsoup4`, `pypdf` eingerichtet.
- [x] Deterministische Tools implementiert:
  - `src/snapshot.py`: Laedt Webseiten/PDFs herunter, erzeugt SHA-256 Hashes und speichert Quellentexte in `sources/raw/`.
  - `src/verifier.py`: Anti-Halluzinations-Engine; verifiziert Zitate zeilengenau und faengt erfundene Zitate ab.
  - `src/excerpt.py`: Generiert wissenschaftliche Exzerpte nach Standards der Geschichtswissenschaft.
- [x] Quellenspeicher `sources/` und `sources/catalog.json` initialisiert.
- [x] Erste Testquelle gesichert und Verifikation erfolgreich getestet (echtes Zitat -> `VERIFIED`; Fake-Zitat -> `HALLUCINATION_DETECTED`).
- [x] Regel 05 (`rules/05-historical-grounding-and-citations.md`) hinzugefuegt.
- [x] Agenten-Rollen `archivist`, `factchecker` und `synthesizer` definiert.
- [x] Multi-Agent-Infrastruktur und 30-Minuten-Auto-Push aktiv.

## 3. Offene Punkte / Nächste Schritte
- [ ] Konkretes Thema der Abschlussarbeit der Studentin erfahren (Epoche, Fragestellung, Personen, Ereignis).
- [ ] Erste echte Primär-/Sekundärquellen zum konkreten Thema der Studentin recherchieren und mit `src/snapshot.py` archivieren.
- [ ] Erstes themenspezifisches Exzerpt fuer die Arbeit erstellen.

## 4. Wichtige Befehle fuer alle Agenten:
- **Quelle sichern:** `.\.venv\Scripts\python.exe -m src.snapshot --url "<URL>" --title "<Titel>" --author "<Autor>"`
- **Zitat pruefen:** `.\.venv\Scripts\python.exe -m src.verifier --source <id> --quote "<Zitat>" --claim "<Aussage>"`
- **Exzerpt anlegen:** `.\.venv\Scripts\python.exe -m src.excerpt --source <id> --topic "<Thema>"`
