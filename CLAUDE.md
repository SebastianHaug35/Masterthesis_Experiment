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

- **Planungs-Assistent (nicht du):** `budget.yaml`, `h1/input/*` (Soll-Liste, Prozess, Firmenprofil), `h1/prompts/*`, `auftraege/*`, `ANWEISUNG_H1.md`.
  Diese Dateien änderst du nur, wenn ein Auftrag es ausdrücklich verlangt. Änderungsvorschläge schreibst du in `h1/results/ERGEBNIS.md`, Abschnitt 8.
- **Du:** Code (`h1/src/`), Docker, Läufe, Auswertung, `h1/DECISIONS.md`, `h1/results/`, `h1/runs/`.

## Rückmeldung

- Jede inhaltliche Rückmeldung gehört in `h1/results/ERGEBNIS.md` (Aufbau siehe `ANWEISUNG_H1.md`), Entscheidungen in `h1/DECISIONS.md`.
- Der Chat enthält am Ende nur: welcher Auftrag erledigt ist, und dass gepusht wurde.

## Ausführung, Git, Kosten

- Läufe nur im Docker-Container (Befehle siehe `h1/README.md`). Nach Codeänderungen `docker compose build`.
- Nach jedem abgeschlossenen Arbeitsschritt committen und pushen. Commit-Nachricht: `h1: <was>`. Niemals `.env` oder API-Keys committen.
- **Kostenkontrolle (gilt immer, für jeden Auftrag):**
  - Jeder API-Aufruf wird mit Zeit, Auftrag, run_id, Tokens und geschätzten Kosten in `kosten/verbrauch.csv` (Repo-Wurzel) protokolliert. Die Datei wird mitcommittet.
  - **Vor jedem einzelnen API-Aufruf** prüft der Code: Summe seit `stichtag` + geschätzte Kosten dieses Aufrufs ≤ `budget_usd` aus `budget.yaml`. Sonst kein Aufruf, Lauf abbrechen, Auftrag `blockiert – Budget erreicht`, dokumentieren, pushen.
  - Ab `warnung_ab_anteil` des Budgets steht eine Warnung oben in `h1/results/ERGEBNIS.md`.
  - Bei `insufficient_quota` / `credit_balance_exhausted`: sofort abbrechen, kein Retry.
  - Ist in `.env` ein `OPENAI_ADMIN_KEY` gesetzt, wird nach jedem Lauf zusätzlich der tatsächliche Verbrauch über die Costs-API von OpenAI abgefragt und neben der Schätzung protokolliert. Ohne Admin-Key gilt nur die Schätzung.
  - Strengere Grenzen eines Auftrags (z. B. je Lauf) gelten zusätzlich.
  - `budget.yaml` änderst du nie.
