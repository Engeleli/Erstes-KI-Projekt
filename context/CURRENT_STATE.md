# Aktueller Projektstatus (Session Handoff)

> **Wichtig für jeden Agenten (Claude, Gemini, etc.):**
> Lies diese Datei zu Beginn JEDER neuen Sitzung. Aktualisiere sie am Ende deiner Arbeit oder nach größeren Meilensteinen!

---

## 1. Letzter Stand
- **Datum:** 2026-10-11
- **Letzter Agent:** Gemini (Antigravity)
- **Status:** Citavi-Integration (automatische Erfassung von DOI, ISBN, URN & RIS-Export) vollständig implementiert und getestet!

## 2. Zuletzt erledigt
- [x] `src/snapshot.py` erweitert um:
  - Automatische Regex- und Meta-Tag-Erkennung von DOI und ISBN.
  - Generierung von `.ris`-Exportdateien im Ordner `sources/citavi/` und Sammeldatei `sources/citavi_import.ris` für 1-Klick-Import in Citavi.
- [x] `src/excerpt.py` erweitert um Citavi-Import-Box ("Zauberstab-ID" für sofortiges Einfügen in Citavi).
- [x] `rules/05-historical-grounding-and-citations.md` und `agents/archivist.agent.md` mit Citavi-Pflicht aktualisiert.
- [x] Testquelle `src_002` mit ISBN und RIS-Export erfolgreich angelegt.

## 3. Offene Punkte / Nächste Schritte
- [ ] Konkretes Thema / Fragestellung der Abschlussarbeit von der Studentin erfragen.
- [ ] Erste echte Primär-/Sekundärliteratur zum Thema erfassen und in Citavi bereitstellen.

## 4. Befehle für Citavi & Recherche:
- **Quelle sichern (mit DOI/ISBN):**  
  `.\.venv\Scripts\python.exe -m src.snapshot --url "<URL>" --title "<Titel>" --doi "<DOI>" --isbn "<ISBN>"`
- **Exzerpt anlegen:**  
  `.\.venv\Scripts\python.exe -m src.excerpt --source <id> --topic "<Thema>"`
- **Citavi-Import:** Datei `sources/citavi_import.ris` oder `sources/citavi/<id>.ris` direkt in Citavi öffnen.
