"""
Modul: snapshot.py
Laedt Webseiten oder Dokumente herunter, generiert kryptografische SHA-256 Hashes
und legt unverfaelschte lokale Textkopien im Ordner sources/raw/ ab.
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import requests
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = PROJECT_ROOT / "sources"
RAW_DIR = SOURCES_DIR / "raw"
CATALOG_FILE = SOURCES_DIR / "catalog.json"


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if not CATALOG_FILE.exists():
        with open(CATALOG_FILE, "w", encoding="utf-8") as f:
            json.dump({"description": "Quellenkatalog", "sources": []}, f, indent=2)


def load_catalog() -> Dict[str, Any]:
    ensure_dirs()
    try:
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"description": "Quellenkatalog", "sources": []}


def save_catalog(catalog: Dict[str, Any]) -> None:
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)


def generate_source_id(catalog: Dict[str, Any]) -> str:
    existing_ids = [s.get("id", "") for s in catalog.get("sources", [])]
    idx = 1
    while f"src_{idx:03d}" in existing_ids:
        idx += 1
    return f"src_{idx:03d}"


def clean_html_text(html_content: str) -> tuple[str, str]:
    soup = BeautifulSoup(html_content, "html.parser")
    
    title = soup.title.string.strip() if soup.title and soup.title.string else "Ohne Titel"
    
    # Entferne irrelevante Tags
    for element in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
        element.decompose()
        
    text = soup.get_text(separator="\n")
    # Zeilen bereinigen
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned_text = "\n\n".join(lines)
    return title, cleaned_text


def extract_pdf_text(file_path: Path) -> str:
    from pypdf import PdfReader
    reader = PdfReader(str(file_path))
    pages_text = []
    for idx, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        pages_text.append(f"--- [Seite {idx}] ---\n" + page_text.strip())
    return "\n\n".join(pages_text)


def capture_url(url: str, title: Optional[str] = None, author: Optional[str] = None, source_type: str = "web") -> Dict[str, Any]:
    ensure_dirs()
    catalog = load_catalog()
    source_id = generate_source_id(catalog)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HistorischerRechercheBot/1.0"
    }
    
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    raw_bytes = response.content
    
    sha256_hash = hashlib.sha256(raw_bytes).hexdigest()
    
    detected_title, cleaned_text = clean_html_text(response.text)
    final_title = title or detected_title
    
    # Speichere Rohdatei und bereinigten Text
    raw_file = RAW_DIR / f"{source_id}_raw.html"
    text_file = RAW_DIR / f"{source_id}.txt"
    
    with open(raw_file, "wb") as f:
        f.write(raw_bytes)
        
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
        
    entry = {
        "id": source_id,
        "title": final_title,
        "author": author or "Unbekannt",
        "url": url,
        "source_type": source_type,
        "date_accessed": datetime.now().isoformat(timespec="seconds"),
        "sha256": sha256_hash,
        "text_file": str(text_file.relative_to(PROJECT_ROOT)),
        "raw_file": str(raw_file.relative_to(PROJECT_ROOT)),
        "char_count": len(cleaned_text),
        "verified": True
    }
    
    catalog["sources"].append(entry)
    save_catalog(catalog)
    return entry


def capture_file(file_path_str: str, title: Optional[str] = None, author: Optional[str] = None, source_type: str = "pdf") -> Dict[str, Any]:
    ensure_dirs()
    catalog = load_catalog()
    source_id = generate_source_id(catalog)
    
    src_path = Path(file_path_str)
    if not src_path.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {file_path_str}")
        
    raw_bytes = src_path.read_bytes()
    sha256_hash = hashlib.sha256(raw_bytes).hexdigest()
    
    if src_path.suffix.lower() == ".pdf":
        cleaned_text = extract_pdf_text(src_path)
    else:
        cleaned_text = src_path.read_text(encoding="utf-8", errors="replace")
        
    final_title = title or src_path.stem
    
    text_file = RAW_DIR / f"{source_id}.txt"
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
        
    entry = {
        "id": source_id,
        "title": final_title,
        "author": author or "Unbekannt",
        "original_file": str(src_path),
        "source_type": source_type,
        "date_accessed": datetime.now().isoformat(timespec="seconds"),
        "sha256": sha256_hash,
        "text_file": str(text_file.relative_to(PROJECT_ROOT)),
        "char_count": len(cleaned_text),
        "verified": True
    }
    
    catalog["sources"].append(entry)
    save_catalog(catalog)
    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description="Webseite oder Dokument herunterladen und verifizieren.")
    parser.add_argument("--url", help="URL der Quelle")
    parser.add_argument("--file", help="Pfad zu einer lokalen PDF- oder Textdatei")
    parser.add_argument("--title", help="Titel des Dokuments/der Quelle")
    parser.add_argument("--author", help="Autor oder Institution")
    parser.add_argument("--type", default="web", choices=["web", "pdf", "archive", "primary_source"], help="Art der Quelle")
    
    args = parser.parse_args()
    
    if args.url:
        print(f"[*] Lade URL herunter: {args.url}")
        entry = capture_url(args.url, title=args.title, author=args.author, source_type=args.type)
    elif args.file:
        print(f"[*] Lese lokale Datei ein: {args.file}")
        entry = capture_file(args.file, title=args.title, author=args.author, source_type=args.type)
    else:
        parser.print_help()
        sys.exit(1)
        
    print(f"\n[ERFOLG] Quelle gesichert als ID: {entry['id']}")
    print(f"Titel:      {entry['title']}")
    print(f"SHA-256:    {entry['sha256']}")
    print(f"Textdatei:  {entry['text_file']}")
    print(f"Zeichen:    {entry['char_count']}")


if __name__ == "__main__":
    main()

