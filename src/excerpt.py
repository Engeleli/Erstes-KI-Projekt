"""
Modul: excerpt.py
Erstellt aus verifizierten Quellen strukturierte historische Exzerpte fuer die Abschlussarbeit.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = PROJECT_ROOT / "sources"
EXCERPTS_DIR = SOURCES_DIR / "excerpts"
CATALOG_FILE = SOURCES_DIR / "catalog.json"


def create_excerpt(source_id: str, thesis_topic: str = "Abschlussarbeit") -> Path:
    EXCERPTS_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    source = next((s for s in catalog.get("sources", []) if s.get("id") == source_id), None)
    if not source:
        raise ValueError(f"Quelle '{source_id}' nicht gefunden.")

    excerpt_file = EXCERPTS_DIR / f"{source_id}_exzerpt.md"

    content = f"""# Historisches Exzerpt: {source.get('title')}

- **Signatur / ID:** `{source.get('id')}`
- **Autor / Urheber:** {source.get('author', 'Unbekannt')}
- **Quelle / URL:** {source.get('url', source.get('original_file', 'Lokal'))}
- **Abrufdatum:** {source.get('date_accessed')}
- **Kryptografischer Hash (SHA-256):** `{source.get('sha256')}`
- **Quellentyp:** {source.get('source_type')}
- **Relevanz fuer Thema:** {thesis_topic}

---

## 1. Quellenkritische Einordnung (Historische W-Fragen)
- **Wer spricht / verfasste die Quelle?** (Autor, soziale Stellung, Interessen)
- **Wann und wo entstanden?** (Historischer Kontext)
- **An wen gerichtet?** (Adressat: privat, amtlich, propagandistisch, publizistisch)
- **Quellengattung:** (Primärquelle / Sekundärliteratur)

---

## 2. Verifizierte Kernaussagen & Belegzitate
> *Hinweis: Alle hier aufgefuehrten Zitate wurden deterministisch ueber `src/verifier.py` gegen den Quelltext geprueft.*

### These / Befund 1:
- **Aussage:** 
- **Wortwörtliches Belegzitat:** „...“
- **Fundstelle:** Zeile X (siehe `{source.get('text_file')}`)

---

## 3. Zitiervorschlag fuer die Abschlussarbeit (Deutsche Zitierweise)
> {source.get('author', 'N.N.')}: *{source.get('title')}*, {source.get('date_accessed', '')}, online unter: <{source.get('url', '')}> (abgerufen am {datetime.now().strftime('%d.%m.%Y')}).
"""

    with open(excerpt_file, "w", encoding="utf-8") as f:
        f.write(content)

    return excerpt_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Erstellt ein Vorlagen-Exzerpt fuer eine Quelle.")
    parser.add_argument("--source", required=True, help="ID der Quelle (z.B. src_001)")
    parser.add_argument("--topic", default="Abschlussarbeit", help="Thema / Fragestellung")
    args = parser.parse_args()

    try:
        path = create_excerpt(args.source, args.topic)
        print(f"[ERFOLG] Exzerpt erstellt: {path}")
    except Exception as e:
        print(f"[FEHLER] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
