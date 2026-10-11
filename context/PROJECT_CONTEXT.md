# Projekt-Kontext & Vision: Historischer Recherche- und Verifikations-Workflow

---

## 1. Vision & Problemstellung
- **Zielgruppe:** Geschichtsstudentin (Abschlussarbeit / Bachelor- oder Masterarbeit).
- **Kernproblem:** Gängige KI-Modelle neigen zu "Halluzinationen" – sie erfinden historische Ereignisse, verfälschen Zitate oder erfinden nicht existierende Belege und Quellen. In den Geisteswissenschaften führt dies zu wissenschaftlicher Unbrauchbarkeit.
- **Lösung:** Ein fehlertoleranter, deterministischer Multi-Agenten-Workflow, der strikte Quellengebundenheit (*Strict Grounding*) und mechanische Zitatprüfung erzwingt.

---

## 2. Kernfunktionen
1. **Unverfälschbare Quellenarchivierung:**
   - Echte Python-Downloads von Webseiten und PDFs mit SHA-256 Hashes und Zugriffszeitstempel in `sources/raw/`.
   - Automatischer Quellenkatalog in `sources/catalog.json`.
2. **Deterministische Zitatverifikation (Anti-Halluzination):**
   - Jede Behauptung muss ein wörtliches Zitat enthalten.
   - Ein Python-Skript prüft Zeichenkette für Zeichenkette im Quelltext. Ohne 100% Fundstelle wird die Aussage verworfen.
3. **Wissenschaftliche Exzerpt-Generierung:**
   - Strukturierte Exzerpte in `sources/excerpts/` mit Quellenkritik (W-Fragen) und druckreifen Fußnoten-Zitaten.
4. **Multi-Agenten-Teilung:**
   - Trennung in `archivist` (Quellensammler), `factchecker` (Prüfer/Kritiker) und `synthesizer` (Redakteur).

---

## 3. Tech-Stack
- **Sprache & Runtime:** Python 3.12 (virtuelle Umgebung in `.venv/`)
- **Bibliotheken:**
  - `requests` (Web-Abrufe)
  - `beautifulsoup4` (HTML-Parsing und Textbereinigung)
  - `pypdf` (Extraktion wissenschaftlicher PDFs)
  - `difflib` & `hashlib` (Kryptografische Hashes & Fuzzy-/Exact-String-Matching)
- **Persistenz & Versionierung:**
  - JSON-Katalog (`sources/catalog.json`) & Markdown-Exzerpte (`sources/excerpts/`)
  - Git & GitHub (`origin/main`) mit 30-Minuten-Auto-Push via Windows-Aufgabenplanung

---

## 4. Offene Spezifika zur Abschlussarbeit
*(Vom Nutzer noch zu ergänzen):*
- Konkretes Epochen- oder Forschungsthema (z. B. Weimarer Republik, Antike, Kolonialgeschichte etc.)
- Bevorzugter Zitierstil (z. B. Deutsche Zitierweise mit Fußnoten, Chicago Notes & Bibliography, APA)
