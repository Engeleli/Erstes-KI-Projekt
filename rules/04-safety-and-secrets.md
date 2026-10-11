# Regel 04: Sicherheit, Secrets & Betriebssystem

## 1. Schutz von API-Keys & Zugangsdaten
- **NIEMALS** echte API-Keys, Passwörter oder Tokens im Code oder in Git einchecken.
- Verwende eine `.env`-Datei für lokale Secrets.
- Die `.env`-Datei ist in `.gitignore` eingetragen.
- Stelle stets eine `.env.example`-Datei mit Platzhaltern bereit (z. B. `OPENAI_API_KEY=your_key_here`).

## 2. Windows-Kompatibilität
- Das Host-System ist Windows mit PowerShell.
- Verwende in PowerShell keine Linux-spezifischen Pipes oder Befehle (z. B. `grep`, `cat` ohne PowerShell-Alias), sondern native Cmdlets oder universelle Pfad-Syntax.
- Im Code (Python / JS) immer plattformunabhängige Pfade verwenden (`os.path.join` / `pathlib.Path` oder `path.join`).

