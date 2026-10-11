# Regel 01: Session Handoff & Gedächtnis

## Ziel
Sicherstellen, dass der Benutzer jederzeit den KI-Client wechseln kann (z. B. von Gemini zu Claude oder Cursor) oder eine neue Sitzung starten kann, ohne Kontext zu verlieren.

## Pflichten jedes Agenten:

### 1. Bei Sitzungsbeginn (Onboarding)
- **Immer** als erstes `context/CURRENT_STATE.md` und `context/PROJECT_CONTEXT.md` lesen.
- Den aktuellen Status und die "Nächsten Schritte" zur Kenntnis nehmen.
- Den Nutzer kurz über den erkannten Stand informieren (z. B. "Ich sehe, wir waren zuletzt bei Schritt X stehengeblieben...").

### 2. Während der Sitzung
- Wichtige Architektur-Entscheidungen in `context/DECISIONS.md` festhalten.
- Keine Annahmen über den Tech-Stack oder Nutzerabsichten treffen, wenn diese nicht dokumentiert sind – stattdessen nachfragen.

### 3. Bei Sitzungsende oder nach Meilensteinen (Offboarding)
- `context/CURRENT_STATE.md` aktualisieren:
  - Datum und Name des aktuellen Agenten eintragen.
  - Abgeschlossene Punkte abhaken.
  - Neu entstandene offene Punkte und nächste Schritte klar formulieren.
  - Eventuelle Hindernisse (Blocker) oder unvollendete Teilaufgaben beschreiben.
