"""
Modul: snapshot.py
Laedt Webseiten oder Dokumente herunter, generiert kryptografische SHA-256 Hashes,
extrahiert bibliografische Identifikatoren (DOI, ISBN, URN) fuer Citavi
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
from typing import Optional, Dict, Any, Tuple

import requests
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = PROJECT_ROOT / "sources"
RAW_DIR = SOURCES_DIR / "raw"
CITAVI_DIR = SOURCES_DIR / "citavi"
CATALOG_FILE = SOURCES_DIR / "catalog.json"
CITAVI_MASTER_RIS = SOURCES_DIR / "citavi_import.ris"

DOI_REGEX = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b")
ISBN13_REGEX = re.compile(r"\b(97[89][- ]?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9])\b")
ISBN10_REGEX = re.compile(r"\b([0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X])\b")


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CITAVI_DIR.mkdir(parents=True, exist_ok=True)
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


def extract_identifiers_from_html(soup: BeautifulSoup, text: str, url: str) -> Tuple[Optional[str], Optional[str]]:
    """Extrahiert DOI und ISBN aus HTML-Metadaten oder Fliesstext."""
    detected_doi = None
    detected_isbn = None

    # 1. Pruefe standardisierte Meta-Tags (Google Scholar, Dublin Core, PRISM)
    meta_doi_keys = [
        "citation_doi", "dc.identifier", "doi", "prism.doi", "dc.identifier.doi", "bepress_citation_doi"
    ]
    for key in meta_doi_keys:
        tag = soup.find("meta", attrs={"name": re.compile(f"^{key}$", re.I)}) or \
              soup.find("meta", attrs={"property": re.compile(f"^{key}$", re.I)})
        if tag and tag.get("content"):
            content = tag["content"].strip()
            match = DOI_REGEX.search(content)
            if match:
                detected_doi = match.group(1)
                break

    # 2. Pruefe Meta-Tags fuer ISBN
    meta_isbn_keys = ["citation_isbn", "isbn", "dc.identifier.isbn"]
    for key in meta_isbn_keys:
        tag = soup.find("meta", attrs={"name": re.compile(f"^{key}$", re.I)}) or \
              soup.find("meta", attrs={"property": re.compile(f"^{key}$", re.I)})
        if tag and tag.get("content"):
            content = tag["content"].strip()
            match = ISBN13_REGEX.search(content) or ISBN10_REGEX.search(content)
            if match:
                detected_isbn = match.group(1).replace(" ", "").replace("-", "")
                break

    # 3. Pruefe URL auf DOI (z.B. doi.org/10.xxxx/...)
    if not detected_doi:
        match_url = DOI_REGEX.search(url)
        if match_url:
            detected_doi = match_url.group(1)

    # 4. Fallback: Suche in den ersten 5000 Zeichen des Fliesstexts
    header_text = text[:5000]
    if not detected_doi:
        match_text = DOI_REGEX.search(header_text)
        if match_text:
            detected_doi = match_text.group(1)

    if not detected_isbn:
        match_isbn = ISBN13_REGEX.search(header_text)
        if match_isbn:
            clean_isbn = match_isbn.group(1).replace(" ", "").replace("-", "")
            if len(clean_isbn) in (10, 13):
                detected_isbn = clean_isbn

    return detected_doi, detected_isbn


def clean_html_text(html_content: str, url: str) -> Tuple[str, str, Optional[str], Optional[str], Optional[str]]:
    soup = BeautifulSoup(html_content, "html.parser")
    
    title = soup.title.string.strip() if soup.title and soup.title.string else "Ohne Titel"
    
    # Extrahiere Autor aus Meta-Tags falls vorhanden
    author = None
    meta_author = soup.find("meta", attrs={"name": re.compile("^(citation_author|author|dc.creator)$", re.I)})
    if meta_author and meta_author.get("content"):
        author = meta_author["content"].strip()

    # Identifikatoren extrahieren BEVOR Tags zerstoert werden
    detected_doi, detected_isbn = extract_identifiers_from_html(soup, html_content, url)

    # Entferne irrelevante Tags fuer reinen Lesetext
    for element in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
        element.decompose()
        
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned_text = "\n\n".join(lines)
    
    return title, cleaned_text, author, detected_doi, detected_isbn


def extract_pdf_data(file_path: Path) -> Tuple[str, Optional[str], Optional[str]]:
    from pypdf import PdfReader
    reader = PdfReader(str(file_path))
    pages_text = []
    first_page_text = ""
    
    for idx, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        if idx == 1:
            first_page_text = page_text
        pages_text.append(f"--- [Seite {idx}] ---\n" + page_text.strip())
        
    cleaned_text = "\n\n".join(pages_text)
    
    # Pruefe Seite 1 auf DOI und ISBN
    detected_doi = None
    detected_isbn = None
    
    match_doi = DOI_REGEX.search(first_page_text)
    if match_doi:
        detected_doi = match_doi.group(1)
        
    match_isbn = ISBN13_REGEX.search(first_page_text)
    if match_isbn:
        detected_isbn = match_isbn.group(1).replace(" ", "").replace("-", "")

    return cleaned_text, detected_doi, detected_isbn


def generate_ris_record(entry: Dict[str, Any]) -> str:
    """Erzeugt einen Citavi-kompatiblen RIS-Datensatz."""
    record_type = "JOUR" if entry.get("doi") else ("BOOK" if entry.get("isbn") else "ELEC")
    lines = [
        f"TY  - {record_type}",
        f"ID  - {entry['id']}",
        f"TI  - {entry['title']}",
        f"AU  - {entry.get('author', 'Unbekannt')}"
    ]
    if entry.get("doi"):
        lines.append(f"DO  - {entry['doi']}")
    if entry.get("isbn"):
        lines.append(f"SN  - {entry['isbn']}")
    if entry.get("url"):
        lines.append(f"UR  - {entry['url']}")
    if entry.get("date_accessed"):
        lines.append(f"Y2  - {entry['date_accessed'][:10]}")
    lines.append("ER  - \n")
    return "\n".join(lines)


def write_citavi_export(entry: Dict[str, Any]) -> str:
    """Schreibt Einzelfile und haengt an Sammel-RIS an."""
    ensure_dirs()
    ris_content = generate_ris_record(entry)
    
    # Einzelfile
    single_file = CITAVI_DIR / f"{entry['id']}.ris"
    single_file.write_text(ris_content, encoding="utf-8")
    
    # Sammeldatei
    with open(CITAVI_MASTER_RIS, "a", encoding="utf-8") as f:
        f.write(ris_content)
        
    return str(single_file.relative_to(PROJECT_ROOT))


def capture_url(url: str, 
                title: Optional[str] = None, 
                author: Optional[str] = None, 
                doi: Optional[str] = None,
                isbn: Optional[str] = None,
                urn: Optional[str] = None,
                source_type: str = "web") -> Dict[str, Any]:
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
    
    detected_title, cleaned_text, detected_author, auto_doi, auto_isbn = clean_html_text(response.text, url)
    final_title = title or detected_title
    final_author = author or detected_author or "Unbekannt"
    final_doi = doi or auto_doi
    final_isbn = isbn or auto_isbn
    
    # Speichere Rohdatei und bereinigten Text
    raw_file = RAW_DIR / f"{source_id}_raw.html"
    text_file = RAW_DIR / f"{source_id}.txt"
    
    with open(raw_file, "wb") as f:
        f.write(raw_bytes)
        
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
        
    # Primaere Citavi-ID (Zauberstab) ermitteln
    citavi_quick_id = final_doi or final_isbn or url

    entry = {
        "id": source_id,
        "title": final_title,
        "author": final_author,
        "url": url,
        "doi": final_doi,
        "isbn": final_isbn,
        "urn": urn,
        "citavi_quick_id": citavi_quick_id,
        "source_type": source_type,
        "date_accessed": datetime.now().isoformat(timespec="seconds"),
        "sha256": sha256_hash,
        "text_file": str(text_file.relative_to(PROJECT_ROOT)),
        "raw_file": str(raw_file.relative_to(PROJECT_ROOT)),
        "char_count": len(cleaned_text),
        "verified": True
    }
    
    # RIS-Export fuer Citavi erzeugen
    entry["citavi_ris_file"] = write_citavi_export(entry)

    catalog["sources"].append(entry)
    save_catalog(catalog)
    return entry


def capture_file(file_path_str: str, 
                 title: Optional[str] = None, 
                 author: Optional[str] = None, 
                 doi: Optional[str] = None,
                 isbn: Optional[str] = None,
                 urn: Optional[str] = None,
                 source_type: str = "pdf") -> Dict[str, Any]:
    ensure_dirs()
    catalog = load_catalog()
    source_id = generate_source_id(catalog)
    
    src_path = Path(file_path_str)
    if not src_path.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {file_path_str}")
        
    raw_bytes = src_path.read_bytes()
    sha256_hash = hashlib.sha256(raw_bytes).hexdigest()
    
    if src_path.suffix.lower() == ".pdf":
        cleaned_text, auto_doi, auto_isbn = extract_pdf_data(src_path)
    else:
        cleaned_text = src_path.read_text(encoding="utf-8", errors="replace")
        auto_doi = None
        auto_isbn = None
        
    final_title = title or src_path.stem
    final_doi = doi or auto_doi
    final_isbn = isbn or auto_isbn
    citavi_quick_id = final_doi or final_isbn or str(src_path.name)
    
    text_file = RAW_DIR / f"{source_id}.txt"
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
        
    entry = {
        "id": source_id,
        "title": final_title,
        "author": author or "Unbekannt",
        "original_file": str(src_path),
        "doi": final_doi,
        "isbn": final_isbn,
        "urn": urn,
        "citavi_quick_id": citavi_quick_id,
        "source_type": source_type,
        "date_accessed": datetime.now().isoformat(timespec="seconds"),
        "sha256": sha256_hash,
        "text_file": str(text_file.relative_to(PROJECT_ROOT)),
        "char_count": len(cleaned_text),
        "verified": True
    }
    
    entry["citavi_ris_file"] = write_citavi_export(entry)

    catalog["sources"].append(entry)
    save_catalog(catalog)
    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description="Webseite oder Dokument herunterladen, DOI/ISBN fuer Citavi erfassen.")
    parser.add_argument("--url", help="URL der Quelle")
    parser.add_argument("--file", help="Pfad zu einer lokalen PDF- oder Textdatei")
    parser.add_argument("--title", help="Titel des Dokuments/der Quelle")
    parser.add_argument("--author", help="Autor oder Institution")
    parser.add_argument("--doi", help="Digital Object Identifier (z.B. 10.1000/182)")
    parser.add_argument("--isbn", help="ISBN des Buchs/Dokuments")
    parser.add_argument("--urn", help="URN (z.B. urn:nbn:de:...)")
    parser.add_argument("--type", default="web", choices=["web", "pdf", "archive", "primary_source"], help="Art der Quelle")
    
    args = parser.parse_args()
    
    if args.url:
        print(f"[*] Lade URL herunter: {args.url}")
        entry = capture_url(args.url, title=args.title, author=args.author, doi=args.doi, isbn=args.isbn, urn=args.urn, source_type=args.type)
    elif args.file:
        print(f"[*] Lese lokale Datei ein: {args.file}")
        entry = capture_file(args.file, title=args.title, author=args.author, doi=args.doi, isbn=args.isbn, urn=args.urn, source_type=args.type)
    else:
        parser.print_help()
        sys.exit(1)
        
    print(f"\n[ERFOLG] Quelle gesichert als ID: {entry['id']}")
    print(f"Titel:            {entry['title']}")
    print(f"Autor:            {entry.get('author')}")
    print(f"DOI:              {entry.get('doi') or 'Keine'}")
    print(f"ISBN:             {entry.get('isbn') or 'Keine'}")
    print(f"Citavi-Schnell-ID:{entry.get('citavi_quick_id')}")
    print(f"Citavi-RIS-Datei: {entry.get('citavi_ris_file')}")
    print(f"SHA-256:          {entry['sha256']}")
    print(f"Textdatei:        {entry['text_file']}")


if __name__ == "__main__":
    main()
