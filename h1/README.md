# H1 – Rechtsrahmen, Zuordnung je Task und Lückenerkennung (H1b)

Prüft, ob ein LLM-Agent (OpenAI Responses API, Websuche mit Domain-Filter) die für den
Bewerbungsprozess der Hochschule München geltenden Vorschriften findet (Stufe 1), sie den
19 Tasks zuordnet (Stufe 2) und fehlende Prozessschritte erkennt (H1b). Die Ergebnisse werden
automatisch gegen `input/soll_liste.csv` ausgewertet.

## Einrichtung (Linux-PC, per SSH)

```
cd h1
cp .env.example .env      # OPENAI_API_KEY=... eintragen; .env wird nie committet
docker compose build
```

## Start

Ein Testlauf von Konfiguration A und Auswertung:

```
docker compose run --rm ma-h1 python -m src.run --konfig A --laeufe 1
docker compose run --rm ma-h1 python -m src.evaluate
```

Alle Läufe (je Konfiguration 5):

```
docker compose run --rm ma-h1 python -m src.run --konfig A --laeufe 5
docker compose run --rm ma-h1 python -m src.run --konfig B --laeufe 5
docker compose run --rm ma-h1 python -m src.evaluate
```

`python -m src.evaluate --runs <run_id> [<run_id> ...]` wertet nur bestimmte Läufe aus.

## Konfigurationen

- **A (Hauptkonfiguration):** Stufe 1 (1 Aufruf) → Stufe 2 (19 Aufrufe) mit dem Rechtsrahmen des Agenten
- **B (Fehlerisolation):** nur Stufe 2; Rechtsrahmen = Namen der Regelwerke aus der Soll-Liste
  (ohne Fundstellen, ohne Lücken-Markierung)

Modell, `reasoning_effort`, Domains, Anzahl Läufe, Parallelität, Retry und Preise stehen in `config.yaml`.
`input/`, `prompts/` und `config.yaml` sind in den Container nur lesend gemountet – Änderungen daran
brauchen kein neues Image. Nach Änderungen an `src/` ist `docker compose build` nötig. `runs/` und `results/` werden schreibend gemountet und liegen direkt auf dem Host.

## Ausgaben

`runs/<JJJJMMTT-HHMMSS>_<konfig>_<nr>/`

| Datei | Inhalt |
| --- | --- |
| `meta.json` | Modell, effort, Domains, Start/Ende, Prompt-Hashes, Tokens, Kosten |
| `stufe1.json` | Rechtsrahmen des Agenten (nur A) |
| `rechtsrahmen_vorgabe.json` | vorgegebener Rechtsrahmen (nur B) |
| `funde.jsonl` | ein Fund je Zeile aus Stufe 2 |
| `lueckenkandidaten.json` | Regelwerke ohne Zuordnung + Funde mit `typ = moegliche_luecke` |
| `protokoll.json` | Fehler/Retries, fehlgeschlagene Tasks, Anzahl Websuchen, Cache-Tokens |
| `raw/` | jede API-Antwort unverändert (inkl. Websuche-Aktionen und Quellen) |

`results/`: `funde_bewertet.csv`, `uebersehen.csv`, `kennzahlen.csv`, `zusammenfassung.md`, `ERGEBNIS.md`.
In `ERGEBNIS.md` werden die Abschnitte 1–4 (und 5a) bei jedem `evaluate` neu erzeugt; alles ab der Markierung
`MANUELL START` bleibt erhalten.

## Bewertung (Kurzfassung)

- Normierung: Regelwerk-Kurzform (`src/normierung.py`), Fundstelle als Artikel/Paragraf + Absatz
  (`Art.26 Abs.11` = `Art. 26 Abs. 11` = `Art. 26(11)`).
- `korrekt` / `falscher_absatz` / `falscher_task` / `nicht_in_soll` (+ `manuell_pruefen`), Details in `DECISIONS.md`.
- Stufe 1: Recall/Präzision auf Ebene Regelwerk; Stufe 2: auf Ebene Fundstelle, gesamt und je Teilprozess;
  H1b: Lücken-Recall und falsche Lückenmeldungen (inkl. Kontrolle Gleichstellungsbeauftragte).
