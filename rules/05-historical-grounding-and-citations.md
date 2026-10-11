# Regel 05: Historische Quellentreue, Citavi-Integration & Anti-Halluzination

## Ziel
In geschichtswissenschaftlichen Arbeiten sind erfundene Zitate, falsche Jahreszahlen oder ungepruefte Behauptungen wissenschaftlich inakzeptabel. Diese Regel verpflichtet alle Agenten auf strikte Quellengebundenheit (*Strict Grounding*) und nahtlose Citavi-Kompatibilitaet.

---

## 1. Das Verbot des "Gedaechtnis-Wissens"
- **Keine unbelegten Behauptungen:** Agenten duerfen historische Fakten, Statistiken, Personenangaben oder Zitate **niemals** aus ihrem internen Sprachmodell-Gedaechtnis erfinden.
- **Quellen-Pflicht:** Jede inhaltliche Behauptung muss auf einer Datei beruhen, die physisch im Ordner `sources/raw/` existiert und in `sources/catalog.json` registriert ist.

## 2. Der deterministische Beleg-Zwang
- Zu jeder geschichtlichen Kernaussage muss ein **woertliches Zitat** aus der Quellendatei angegeben werden.
- Bevor ein Exzerpt oder ein Textbaustein finalisiert wird, **muss** das Zitat mit `src/verifier.py` geprueft werden:
  ```powershell
  .\.venv\Scripts\python.exe -m src.verifier --source <src_id> --quote "<Zitat>" --claim "<Behauptung>"
  ```
- Gibt das Skript `HALLUCINATION_DETECTED` aus, ist die Aussage **ausnahmslos zu verwerfen**.

## 3. Citavi-Pflicht (ISBN, DOI, URN & RIS-Export)
Fuer jede Quelle, die erfasst wird, **muss** der Agent nach standardisierten Identifikatoren suchen:
- **DOI** (Digital Object Identifier) fuer Aufsaetze und Zeitschriftenartikel (z. B. `10.1007/...`).
- **ISBN** fuer Monografien und Sammelbaende.
- **URN / Permalink** fuer Digitalisate aus Archiven und Bibliotheken.
- Das Skript `src/snapshot.py` generiert automatisch einen `.ris`-Datensatz im Ordner `sources/citavi/` sowie in der Sammeldatei `sources/citavi_import.ris`, welcher per Doppelklick direkt in Citavi importiert werden kann.

## 4. Historische Quellenkritik (W-Fragen)
Jedes Exzerpt in `sources/excerpts/` muss die klassischen geschichtswissenschaftlichen W-Fragen beantworten:
1. **Wer?** Urheber/Verfasser (sozialer Stand, Rolle, moegliche Eigeninteressen).
2. **Wann & Wo?** Entstehungszeitpunkt und -ort.
3. **Quellengattung:** Primaerquelle (aus der Zeit selbst) oder Sekundärliteratur (spaetere Forschung).
4. **An wen?** Adressat (Amt, Oeffentlichkeit, Tagebuch/privat).
5. **Wozu?** Tendenz, Absicht, Propaganda oder nuetzliche Sachinformation.
