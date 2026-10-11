# Regel 02: Architektur- & Code-Standards

## 1. Verzeichnis-Disziplin
- Der eigentliche Anwendungscode gehört ausschließlich in das Verzeichnis `src/`.
- Hilfsskripte, Build- und Wartungstools gehören in `scripts/`.
- Dokumentation, Kontext und Übergabeprotokolle gehören in `context/`.
- Agentenspezifische Rollen und Regeln bleiben in `agents/` und `rules/`.

## 2. Code-Qualität
- **Modularität:** Schreibe kleine, spezialisierte Module mit klar abgegrenzten Verantwortlichkeiten (Single Responsibility Principle).
- **Typisierung & Doku:** Verwende präzise Typisierungen (TypeScript / Python Type Hints) und dokumentiere nicht-triviale Funktionen und Klassen.
- **Bestehenden Code respektieren:** Vorhandene Kommentare, Docstrings und Konventionen beibehalten, sofern der Nutzer nichts anderes verlangt.
- **Tests:** Für Kernlogik im `tests/`-Ordner Unittests anlegen und vor Abschluss ausführen.
