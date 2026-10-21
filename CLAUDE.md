# Projektregeln für Claude Code

Dieses Repo enthält die Experimente zur Masterarbeit von Sebastian Haug (Hochschule München, FK07).
Geplant wird in einem separaten Planungs-Chat. Die Kommunikation mit dir läuft **ausschließlich über Dateien in diesem Repo**.

## Beim Start jeder Sitzung – immer, ohne Rückfrage

1. `git pull` auf `main`.
2. Den Ordner `auftraege/` lesen. Jede Datei beginnt mit einer Zeile `Status: offen | in Arbeit | erledigt | blockiert`.
3. Alle Aufträge mit `Status: offen` in Nummernreihenfolge abarbeiten.
   - Die Basisspezifikation ist `ANWEISUNG_H1.md`. Aufträge ändern oder ergänzen sie.
   - Bei Widersprüchen gilt der **neueste** Auftrag.
4. Gibt es keinen offenen Auftrag, im Chat nur melden: „Kein offener Auftrag.“

## Status pflegen

- Zu Beginn eines Auftrags: Statuszeile auf `Status: in Arbeit` setzen, committen und pushen.
- Am Ende: `Status: erledigt (Commit <hash>, <Datum>)`, oder `Status: blockiert – <Grund>`, wenn es nicht weitergeht.
- An Auftragsdateien änderst du **nur** die Statuszeile.

## Zuständigkeiten

- **Planungs-Assistent (nicht du):** `h1/input/*` (Soll-Liste, Prozess, Firmenprofil), `h1/prompts/*`, `auftraege/*`, `ANWEISUNG_H1.md`.
  Diese Dateien änderst du nur, wenn ein Auftrag es ausdrücklich verlangt. Änderungsvorschläge schreibst du in `h1/results/ERGEBNIS.md`, Abschnitt 8.
- **Du:** Code (`h1/src/`), Docker, Läufe, Auswertung, `h1/DECISIONS.md`, `h1/results/`, `h1/runs/`.

## Rückmeldung

- Jede inhaltliche Rückmeldung gehört in `h1/results/ERGEBNIS.md` (Aufbau siehe `ANWEISUNG_H1.md`), Entscheidungen in `h1/DECISIONS.md`.
- Der Chat enthält am Ende nur: welcher Auftrag erledigt ist, und dass gepusht wurde.

## Ausführung, Git, Kosten

- Läufe nur im Docker-Container (Befehle siehe `h1/README.md`). Nach Codeänderungen `docker compose build`.
- Nach jedem abgeschlossenen Arbeitsschritt committen und pushen. Commit-Nachricht: `h1: <was>`. Niemals `.env` oder API-Keys committen.
- Kostengrenze: Kostet ein einzelner Lauf geschätzt mehr als **3 USD**, brich ab, setze den Auftrag auf `blockiert` und dokumentiere das.
