"""
Modul: verifier.py
Deterministische Zitat- und Belegstellen-Verifikation gegen halluzinierte Fakten.
Prueft, ob ein Belegzitat tatsaechlich wortwoertlich in der gesicherten Quelle vorkommt.
"""

import argparse
import difflib
import json
import re
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = PROJECT_ROOT / "sources"
CATALOG_FILE = SOURCES_DIR / "catalog.json"


def normalize_whitespace(text: str) -> str:
    """Normalisiert Leerzeichen und Zeilenumbrueche fuer toleranten Vergleich."""
    return re.sub(r"\s+", " ", text).strip()


def find_quote_in_text(quote: str, full_text: str) -> Tuple[bool, Optional[int], Optional[str], float]:
    """
    Sucht das Zitat im Volltext.
    Rueckgabe: (is_exact_match, line_number, surrounding_context, similarity_score)
    """
    norm_quote = normalize_whitespace(quote)
    if not norm_quote:
        return False, None, None, 0.0

    lines = full_text.splitlines()
    
    # 1. Direkte Suche Zeile fuer Zeile
    for idx, line in enumerate(lines, start=1):
        if norm_quote.lower() in normalize_whitespace(line).lower():
            start_ctx = max(0, idx - 2)
            end_ctx = min(len(lines), idx + 2)
            context = "\n".join(f"  Z.{i+1}: {lines[i]}" for i in range(start_ctx, end_ctx))
            return True, idx, context, 1.0

    # 2. Mehrzeilige exakte Suche ueber normalisierten Text
    norm_full = normalize_whitespace(full_text)
    if norm_quote.lower() in norm_full.lower():
        # Finde ungefaehre Position
        pos = norm_full.lower().find(norm_quote.lower())
        char_count = 0
        target_line = 1
        for idx, line in enumerate(lines, start=1):
            char_count += len(line) + 1
            if char_count >= pos:
                target_line = idx
                break
        start_ctx = max(0, target_line - 2)
        end_ctx = min(len(lines), target_line + 3)
        context = "\n".join(f"  Z.{i+1}: {lines[i]}" for i in range(start_ctx, end_ctx))
        return True, target_line, context, 1.0

    # 3. Fuzzy-Suche (Aehnlichkeitspruefung), um fast richtige Zitate zu identifizieren
    best_ratio = 0.0
    best_line = 1
    quote_len = len(norm_quote)
    for idx, line in enumerate(lines, start=1):
        norm_l = normalize_whitespace(line)
        if len(norm_l) >= quote_len * 0.5:
            ratio = difflib.SequenceMatcher(None, norm_quote.lower(), norm_l.lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_line = idx

    if best_ratio >= 0.70:
        start_ctx = max(0, best_line - 2)
        end_ctx = min(len(lines), best_line + 2)
        context = "\n".join(f"  Z.{i+1}: {lines[i]}" for i in range(start_ctx, end_ctx))
        return False, best_line, context, best_ratio

    return False, None, None, best_ratio


def verify_claim(source_id: str, quote: str, claim: str) -> Dict[str, Any]:
    if not CATALOG_FILE.exists():
        raise FileNotFoundError(f"Quellenkatalog {CATALOG_FILE} existiert nicht.")

    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    source = next((s for s in catalog.get("sources", []) if s.get("id") == source_id), None)
    if not source:
        raise ValueError(f"Quelle mit ID '{source_id}' nicht im Katalog gefunden.")

    text_file_path = PROJECT_ROOT / source["text_file"]
    if not text_file_path.exists():
        raise FileNotFoundError(f"Quellendatei {text_file_path} nicht gefunden.")

    full_text = text_file_path.read_text(encoding="utf-8", errors="replace")

    is_exact, line_num, context, score = find_quote_in_text(quote, full_text)

    if is_exact:
        status = "VERIFIED"
        message = "Das Zitat ist wortwoertlich im Quelltext nachgewiesen."
    elif score >= 0.70:
        status = "PARTIAL_MATCH_WARNING"
        message = f"Vorsicht: Kein exakter Treffer ({score*100:.1f}% Aehnlichkeit). Moeglicherweise veraenderter Wortlaut oder Paraphrase."
    else:
        status = "HALLUCINATION_DETECTED"
        message = "ALARM: Das angebliche Belegzitat wurde im Quelltext NICHT gefunden! Aussage nicht belegbar."

    return {
        "status": status,
        "source_id": source_id,
        "source_title": source.get("title"),
        "claim": claim,
        "quote": quote,
        "line_number": line_num,
        "context": context,
        "similarity_score": score,
        "message": message
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Belegzitat und Behauptung gegen eine gesicherte Quelle verifizieren.")
    parser.add_argument("--source", required=True, help="ID der Quelle (z.B. src_001)")
    parser.add_argument("--quote", required=True, help="Wortwoertliches Zitat aus der Quelle")
    parser.add_argument("--claim", required=True, help="Historische Behauptung / These")

    args = parser.parse_args()

    try:
        result = verify_claim(args.source, args.quote, args.claim)
    except Exception as e:
        print(f"[FEHLER] {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print(f"VERIFIKATIONS-ERGEBNIS: [{result['status']}]")
    print("=" * 60)
    print(f"Quelle:      {result['source_id']} — {result['source_title']}")
    print(f"Behauptung:  {result['claim']}")
    print(f"Belegzitat:  \"{result['quote']}\"")
    print(f"Status-Info: {result['message']}")

    if result['line_number']:
        print(f"Fundstelle:  Zeile {result['line_number']}")
    if result['context']:
        print(f"\nKontext im Originaldokument:\n{result['context']}")
    print("=" * 60 + "\n")

    if result['status'] == "HALLUCINATION_DETECTED":
        sys.exit(2)


if __name__ == "__main__":
    main()
