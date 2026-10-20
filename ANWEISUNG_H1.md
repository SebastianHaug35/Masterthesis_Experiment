# Arbeitsanweisung für Claude Code – Hypothese 1 (inkl. H1b)

Diese Anweisung ist vollständig. Setze sie ohne Rückfragen um. Wo etwas nicht festgelegt ist, triff eine einfache Entscheidung und dokumentiere sie in `h1/DECISIONS.md`.

Quelle: README der Masterarbeit (Claude Doc), Stand 20.10.2026. Bei Änderungen wird diese Datei im Repo aktualisiert.

## Ziel

Ein Python-Programm, das prüft, ob ein LLM-Agent die für einen Geschäftsprozess geltenden Vorschriften findet (Stufe 1), sie einzelnen Tasks zuordnet (Stufe 2) und fehlende Prozessschritte erkennt (H1b). Ergebnisse werden automatisch gegen eine Soll-Liste ausgewertet. H2/H3 sind NICHT Teil dieses Auftrags.

## Technik

- Python 3.12, Pakete: `openai`, `pydantic`, `pandas`, `python-dotenv`, `pyyaml` (Versionen fest pinnen)
- OpenAI **Responses API**, Tool `{"type": "web_search"}` mit Domain-Filter auf genau diese Domains: `eur-lex.europa.eu`, `gesetze-im-internet.de`, `gesetze-bayern.de`, `tdl-online.de`
- API-Key aus `.env` (`OPENAI_API_KEY`), niemals im Code, Log oder Repo

## Modell

- Modell: **GPT-6 Luna** (OpenAI). Verwende den fest versionierten Snapshot-Namen laut OpenAI-Modellübersicht, keinen Alias. In `config.yaml` als `model` eintragen.
- `reasoning.effort`: `medium`
- Ausgabe über Structured Outputs (JSON-Schema aus den Pydantic-Modellen)
- Alles Konfigurierbare (Modell, effort, Domains, Anzahl Läufe) steht in `config.yaml`

## Ordnerstruktur

Genau diese Datei- und Ordnernamen verwenden:

```
h1/
  Dockerfile
  docker-compose.yml
  .dockerignore
  .env.example          # OPENAI_API_KEY=  (echte .env nie committen)
  .gitignore            # nur .env und __pycache__/ (runs/ und results/ werden committet)
  requirements.txt
  config.yaml
  README.md
  DECISIONS.md
  input/
    firmenprofil.json
    prozess.json
    soll_liste.csv
  prompts/
    stufe1.md
    stufe2.md
  src/
    __init__.py
    config.py           # lädt config.yaml + .env
    models.py           # Pydantic-Schemas (Rechtsrahmen, Fund, Meta)
    llm_client.py       # OpenAI Responses API, web_search mit Domain-Filter, Retry, Token-/Kostenzählung
    prompts.py          # lädt und füllt Prompt-Vorlagen
    stufe1.py           # Rechtsrahmen bestimmen
    stufe2.py           # Zuordnung je Task + Lückenkandidaten
    run.py              # CLI: --konfig A|B --laeufe N
    evaluate.py         # Abgleich mit Soll-Liste, Kennzahlen, ERGEBNIS.md
  runs/                 # pro Lauf ein Unterordner
  results/              # funde_bewertet.csv, uebersehen.csv, kennzahlen.csv, zusammenfassung.md, ERGEBNIS.md
```

## Docker

Ausführung ausschließlich im Container (Zielrechner: Linux-PC, Zugriff per SSH).

- **Basis-Image:** `python:3.12-slim`, nicht als root laufen (eigener User `app`), Zeitzone `Europe/Berlin`
- **Image-Name:** `ma-h1:latest` · **Service/Container-Name:** `ma-h1`
- **Volumes** (Host ↔ Container `/app/...`): `input/` und `prompts/` nur lesend, `runs/` und `results/` schreibend → Ergebnisse liegen direkt auf dem Host
- **Secrets:** `.env` über `env_file` in `docker-compose.yml`, nicht ins Image kopieren
- **Befehle** (so auch in `h1/README.md` dokumentieren):

```
docker compose build
docker compose run --rm ma-h1 python -m src.run --konfig A --laeufe 1
docker compose run --rm ma-h1 python -m src.evaluate
```

## Git-Repository

- Repo: `https://github.com/SebastianHaug35/Masterthesis_Experiment` (Branch `main`), Projekt liegt im Unterordner `h1/`
- Nach jedem abgeschlossenen Arbeitsschritt (Code-Änderung, Testlauf, Auswertung) committen und pushen – inklusive `runs/`, `results/`, `ERGEBNIS.md` und `DECISIONS.md`
- Commit-Nachrichten auf Deutsch, Format: `h1: <was>` (z. B. `h1: Testlauf A_1 + Auswertung`)
- Niemals `.env` oder API-Keys committen; vor jedem Push prüfen
- Zweck: Der Planungs-Assistent liest die Ergebnisse direkt aus dem Repo, um diese Anweisung zu iterieren

## Eingabedaten

`input/firmenprofil.json`:

```json
{
  "name": "Hochschule München",
  "land": "Deutschland",
  "bundesland": "Bayern",
  "rechtsform": "Körperschaft des öffentlichen Rechts / staatliche Einrichtung (bayerische Hochschule)",
  "sektor": "öffentlich",
  "branche": "Bildung und Forschung",
  "beschaeftigte": "über 1.000",
  "personalvertretung": "Personalrat",
  "gleichstellungsbeauftragte": true,
  "ki_einsatz": "KI-Tool zur Vorauswahl von Bewerbungen (Ranking)",
  "dienstleister_ausserhalb_eu": false,
  "stelle": "Wissenschaftliche Mitarbeiterin/wissenschaftlicher Mitarbeiter nach TV-L"
}
```

`input/prozess.json` – genau diese Teilprozesse und Tasks, nichts ergänzen (die fehlenden Schritte sind Absicht):

```json
{
  "prozess": "Bewerbungsprozess wissenschaftliche Mitarbeiterstelle",
  "teilprozesse": [
    {"id": "TP1", "name": "Stelle ausschreiben", "tasks": [
      {"id": "T1.1", "name": "Bedarf melden"},
      {"id": "T1.2", "name": "Stellenprofil und Eingruppierung nach TV-L festlegen"},
      {"id": "T1.3", "name": "Ausschreibung intern und extern veröffentlichen"}]},
    {"id": "TP2", "name": "Bewerbungen annehmen", "tasks": [
      {"id": "T2.1", "name": "Unterlagen über Bewerbungsportal empfangen"},
      {"id": "T2.2", "name": "Eingang bestätigen"},
      {"id": "T2.3", "name": "Bewerberdaten im System anlegen"}]},
    {"id": "TP3", "name": "KI-Vorauswahl", "tasks": [
      {"id": "T3.1", "name": "Unterlagen mit KI-Tool auswerten"},
      {"id": "T3.2", "name": "Ranking erzeugen"},
      {"id": "T3.3", "name": "Ergebnis durch Fachabteilung prüfen"},
      {"id": "T3.4", "name": "Shortlist festlegen"}]},
    {"id": "TP4", "name": "Vorstellungsgespräche", "tasks": [
      {"id": "T4.1", "name": "Kandidaten einladen"},
      {"id": "T4.2", "name": "Gespräche mit Auswahlkommission und Gleichstellungsbeauftragter führen"},
      {"id": "T4.3", "name": "Gespräche dokumentieren"}]},
    {"id": "TP5", "name": "Auswahl und Einstellung", "tasks": [
      {"id": "T5.1", "name": "Auswahlentscheidung treffen"},
      {"id": "T5.2", "name": "Vertragsangebot erstellen"},
      {"id": "T5.3", "name": "Arbeitsvertrag abschließen"}]},
    {"id": "TP6", "name": "Absagen und Löschen", "tasks": [
      {"id": "T6.1", "name": "Absagen versenden"},
      {"id": "T6.2", "name": "Aufbewahrungsfrist abwarten"},
      {"id": "T6.3", "name": "Bewerberdaten löschen"}]}
  ]
}
```

`input/soll_liste.csv` – Spalten: `soll_id;regelwerk;fundstelle;task_id;typ;inhalt`

- `regelwerk` in Kurzform (DSGVO, AI Act, AGG, SGB IX, GG, TV-L, NachwG, BayPVG, BayGlG, BayDSG)
- `fundstelle` normiert, z. B. `Art. 26`, `§ 165`, `Art. 33 Abs. 2`; leer, wenn nur das Regelwerk feststeht
- `task_id` = Task aus prozess.json, `GESAMT` für prozessweite Vorschriften, `LUECKE` für Vorschriften ohne passenden Task
- `typ` = `zuordnung` oder `luecke`
- Inhalt = Tabelle „Soll-Liste" im Anhang dieser Datei. Lege die CSV daraus an; Zuordnung der Zeilen zu einzelnen Tasks nach bestem Verständnis und in `DECISIONS.md` begründen. Zeilen mit Status „Lücke" bekommen `task_id = LUECKE` und `typ = luecke`. Zeilen „abhängig von Annahme" (Drittland) und „nicht Teil des Prozesses" (Talentpool) entfallen, da `dienstleister_ausserhalb_eu = false`. Die Soll-Liste wird vom Autor vor den echten Läufen geprüft.

**Wichtig:** Die Soll-Liste ist der Goldstandard. Sie darf dem Agenten niemals im Prompt mitgegeben werden (Ausnahme: Konfiguration B, dort nur die Liste der Regelwerke ohne Fundstellen und ohne Lücken-Markierung).

## Ablauf eines Laufs

1. **Stufe 1:** Prompt `prompts/stufe1.md` mit Firmenprofil + gesamtem Prozess füllen → ein Aufruf → Rechtsrahmen als JSON.
2. **Stufe 2:** für jeden der 19 Tasks ein eigener Aufruf mit `prompts/stufe2.md`: Firmenprofil + gesamter Prozess + aktueller Task + Rechtsrahmen.
3. **Lückenkandidaten:** Regelwerke aus Stufe 1, die in Stufe 2 keinem Task zugeordnet wurden, plus alle Funde mit `typ = moegliche_luecke`.
4. Alles speichern, dann `evaluate.py`.

## Konfigurationen und Anzahl Läufe

- **A (Hauptkonfiguration):** Stufe 1 → Stufe 2 mit Rechtsrahmen des Agenten
- **B (Fehlerisolation):** nur Stufe 2, Rechtsrahmen = Regelwerke aus der Soll-Liste
- **Je Konfiguration 5 Läufe** (Modell ist nicht deterministisch). Gesamt: 10 Läufe, je Lauf 1 + 19 bzw. 19 Aufrufe.

**Sofort ausführen:** Sobald das Programm gebaut ist, führe ohne Rückfrage direkt EINEN Testlauf von Konfiguration A im Container aus, danach `evaluate.py` auf diesem Lauf, dann committen und pushen. Die restlichen Läufe erst nach Freigabe durch den Autor.

## Alles schriftlich in Dateien, nicht im Chat

Jede Rückmeldung von dir gehört in die Datei `h1/results/ERGEBNIS.md`, nicht in den Chat. Der Chat enthält am Ende nur den Hinweis, dass die Datei fertig und gepusht ist. Zweck: Der Planungs-Assistent liest alle Projektartefakte (Code, `DECISIONS.md`, `ERGEBNIS.md`, `results/`, `runs/`) aus dem Repo, um diese Anweisung zu iterieren. Die Datei muss daher ohne Chatverlauf verständlich sein.

Inhalt von `ERGEBNIS.md`, in dieser Reihenfolge:

1. **Lauf-Metadaten:** run_id, Modell-Snapshot, reasoning_effort, Dauer, Tokens, Kosten
2. **Stufe 1:** Liste der gefundenen Regelwerke, Vergleich mit Soll (gefunden / übersehen / zusätzlich)
3. **Stufe 2:** Anzahl Funde, Verteilung der Bewertungen (korrekt, falscher_absatz, falscher_task, nicht_in_soll), Recall und Präzision gesamt und je Teilprozess
4. **H1b:** erkannte Lückenkandidaten mit beschriebenem fehlenden Schritt, Abgleich mit den Soll-Lücken, falsche Lückenmeldungen
5. **Auffälligkeiten:** auffällige oder vermutlich erfundene Funde mit Zitat aus der Rohantwort
6. **Technische Probleme:** Fehler, Abbrüche, Workarounds, Grenzen von Websuche/Domain-Filter
7. **Offene Fragen und Annahmen:** alles, wozu du eigentlich eine Rückfrage gehabt hättest, mit der Entscheidung, die du stattdessen getroffen hast
8. **Verbesserungsvorschläge:** für Prompts, Soll-Liste, Datenformat und Auswertung

## Prompt Stufe 1 (`prompts/stufe1.md`)

```
# Rolle und Aufgabe
Du bist ein Compliance-Analyst für deutsches und europäisches Recht.
Deine Aufgabe: Bestimme alle Gesetze, Verordnungen und Tarifverträge,
die für den unten beschriebenen Geschäftsprozess der genannten
Organisation gelten. Ordne noch KEINE einzelnen Paragrafen den Tasks zu –
das geschieht in einem späteren Schritt.

# Regeln
- Recherchiere ausschließlich in diesen Quellen:
  eur-lex.europa.eu, gesetze-im-internet.de, gesetze-bayern.de, tdl-online.de
- Nenne nur Regelwerke, die du in einer dieser Quellen tatsächlich gefunden hast.
  Erfinde nichts. Wenn du unsicher bist, markiere den Eintrag als "unsicher".
- Berücksichtige die Besonderheiten der Organisation
  (Rechtsform, Bundesland, öffentlicher Arbeitgeber, Personalvertretung).
- Vollständigkeit ist wichtiger als Präzision: Lieber ein Regelwerk zu viel
  als eines zu wenig.
- Nenne auch Regelwerke, die für den Prozess gelten, für die es aber
  scheinbar keinen passenden Prozessschritt gibt.

# Organisation
{firmenprofil}

# Geschäftsprozess
{prozess: Teilprozesse und Tasks}

# Ausgabe
Antworte ausschließlich mit JSON:
{
  "rechtsrahmen": [
    {
      "regelwerk": "z. B. DSGVO",
      "vollstaendiger_titel": "...",
      "ebene": "EU | Bund | Land | Tarif",
      "begruendung": "Warum gilt das für diese Organisation und diesen Prozess?",
      "betroffene_teilprozesse": ["1", "3"],
      "quelle_url": "...",
      "fassung_datum": "...",
      "sicherheit": "sicher | unsicher"
    }
  ]
}
```

## Prompt Stufe 2 (`prompts/stufe2.md`)

```
# Rolle und Aufgabe
Du bist ein Compliance-Analyst für deutsches und europäisches Recht.
Bestimme für den unten markierten TASK alle konkreten Vorschriften
(Artikel/Paragraf, möglichst mit Absatz), die bei seiner Ausführung
einzuhalten sind.

# Regeln
- Nutze den vorgegebenen Rechtsrahmen als Ausgangspunkt; recherchiere
  die konkreten Fundstellen nur in: eur-lex.europa.eu,
  gesetze-im-internet.de, gesetze-bayern.de, tdl-online.de
- Erfinde nichts. Bei Unsicherheit: "sicherheit": "unsicher".
- Vollständigkeit ist wichtiger als Präzision.
- Wenn eine Vorschrift einen Prozessschritt verlangt, der im gesamten
  Prozess fehlt, gib sie mit "typ": "moegliche_luecke" aus und beschreibe
  den fehlenden Schritt.

# Organisation
{firmenprofil}
# Gesamter Prozess
{prozess}
# Aktueller TASK
{task_id}: {task_name} (Teilprozess {tp_id}: {tp_name})
# Rechtsrahmen
{rechtsrahmen}

# Ausgabe: ausschließlich JSON nach Schema
```

## Datenformat der Ergebnisse

Pro Lauf `runs/<run_id>/` mit `run_id = <JJJJMMTT-HHMMSS>_<konfig>_<nr>`:

`meta.json`:

```json
{"run_id": "...", "konfig": "A", "lauf_nr": 1, "modell": "<snapshot>",
 "reasoning_effort": "medium", "domains": ["..."],
 "start": "ISO-8601", "ende": "ISO-8601",
 "prompt_hash_stufe1": "sha256", "prompt_hash_stufe2": "sha256",
 "tokens_input": 0, "tokens_output": 0, "kosten_usd_geschaetzt": 0.0}
```

`stufe1.json`: Liste `rechtsrahmen` mit `regelwerk, vollstaendiger_titel, ebene, begruendung, betroffene_teilprozesse, quelle_url, fassung_datum, sicherheit`.

`funde.jsonl` – eine Zeile je Fund aus Stufe 2:

```json
{"run_id": "...", "fund_id": "F001", "task_id": "T3.1",
 "regelwerk": "AI Act", "fundstelle": "Art. 26 Abs. 11",
 "typ": "zuordnung | moegliche_luecke",
 "fehlender_schritt": "nur bei moegliche_luecke, sonst null",
 "begruendung": "...", "quelle_url": "...", "fassung_datum": "...",
 "sicherheit": "sicher | unsicher"}
```

`raw/` – jede API-Antwort unverändert als JSON (inkl. aufgerufener Such-URLs).

## Auswertung (`evaluate.py`)

Normierung: Regelwerk-Kurzform, Fundstelle ohne Leerzeichen-/Schreibvarianten (`Art.26 Abs.11` = `Art. 26 Abs. 11`).

Bewertung je Fund (Spalte `bewertung`):

- `korrekt` – Regelwerk + Artikel/Paragraf stimmen mit einer Soll-Zeile überein (Absatz gleich oder in der Soll-Liste nicht angegeben) und Task passt (bei `GESAMT` jeder Task)
- `falscher_absatz` – Artikel/Paragraf stimmt, Absatz weicht ab
- `falscher_task` – Vorschrift in Soll-Liste, aber anderem Task zugeordnet
- `nicht_in_soll` – keine Übereinstimmung → zusätzlich Spalte `manuell_pruefen = true` (Autor entscheidet später: irrelevant oder erfunden)

Zusätzlich je Soll-Zeile: `gefunden` (ja/nein) → Liste der übersehenen Vorschriften.

`results/` enthält:

- `funde_bewertet.csv` – alle Funde aller Läufe mit Bewertung
- `uebersehen.csv` – je Lauf die nicht gefundenen Soll-Zeilen
- `kennzahlen.csv` – je Lauf und je Konfiguration (Mittelwert + Standardabweichung über alle Läufe):
  - Stufe 1: Recall und Präzision auf Ebene Regelwerk
  - Stufe 2: Recall und Präzision auf Ebene Fundstelle, gesamt und je Teilprozess
  - H1b: Lücken-Recall = Anteil der Soll-Zeilen mit `typ = luecke`, die als Lückenkandidat erkannt wurden; Anzahl falscher Lückenmeldungen (insbesondere Gleichstellungsbeauftragte = vorhandener Schritt, darf nicht als Lücke kommen)
  - Anteil `unsicher`, Anteil `nicht_in_soll`, Tokens und Kosten
- `zusammenfassung.md` – kurze Tabelle A vs. B
- `ERGEBNIS.md` – siehe oben

## Abnahme

- Ein Testlauf von A läuft im Container fehlerfrei durch, alle Dateien entstehen im obigen Format
- `evaluate.py` läuft auf einem Lauf und auf allen Läufen
- `h1/README.md` erklärt Start: `docker compose run --rm ma-h1 python -m src.run --konfig A --laeufe 5` und `docker compose run --rm ma-h1 python -m src.evaluate`
- Alles ist committet und auf `main` gepusht

---

## Anhang: Soll-Liste (Entwurf, durch Experten zu validieren)

| Teilprozess | Vorschrift | Inhalt | Status |
| --- | --- | --- | --- |
| Gesamt | Art. 33 Abs. 2 GG | Bestenauslese im öffentlichen Dienst | vorhanden |
| 1 Ausschreiben | §§ 7, 11 AGG | diskriminierungsfreie Ausschreibung | vorhanden |
| 1 Ausschreiben | TV-L | Eingruppierung | vorhanden |
| 1 Ausschreiben | §§ 164, 165 SGB IX | Meldung an Agentur für Arbeit, Prüfung Besetzung mit Schwerbehinderten | Lücke (ungeplant) |
| 1 Ausschreiben | BayGlG | Vorgaben zur Ausschreibung | vorhanden |
| 2 Annahme | DSGVO + bayer. Landesrecht (BayDSG) | Rechtsgrundlage Verarbeitung (genaue Norm prüfen) | vorhanden |
| 2 Annahme | Art. 13 DSGVO | Informationspflicht | vorhanden |
| 2 Annahme | Art. 32 DSGVO | Sicherheit Bewerbungsportal | vorhanden |
| 3 KI-Vorauswahl | AI Act Anhang III Nr. 4 | Einstufung Hochrisiko | vorhanden |
| 3 KI-Vorauswahl | Art. 26 AI Act | menschliche Aufsicht, Protokollierung | vorhanden |
| 3 KI-Vorauswahl | Art. 26 AI Act | Information der Betroffenen über KI-Einsatz | Lücke (geplant) |
| 3 KI-Vorauswahl | Art. 27 AI Act | Grundrechte-Folgenabschätzung (öffentliche Stelle) | Lücke |
| 3 KI-Vorauswahl | Art. 4 AI Act | KI-Kompetenz der Mitarbeitenden | Lücke |
| 3 KI-Vorauswahl | Art. 22 DSGVO | automatisierte Einzelentscheidung | vorhanden |
| 3 KI-Vorauswahl | Art. 35 DSGVO | Datenschutz-Folgenabschätzung | Lücke |
| 3 KI-Vorauswahl | Art. 44 ff. DSGVO | Drittlandübermittlung (nur bei Nicht-EU-Anbieter) | abhängig von Annahme |
| 3 KI-Vorauswahl | AGG | algorithmische Benachteiligung | vorhanden |
| 3 KI-Vorauswahl | BayPVG (Norm prüfen) | Mitbestimmung Personalrat bei Einführung des Tools | Lücke |
| 4 Gespräche | § 165 SGB IX | Einladung schwerbehinderter Bewerber | vorhanden |
| 4 Gespräche | § 178 SGB IX | Beteiligung Schwerbehindertenvertretung | Lücke (ungeplant) |
| 4 Gespräche | BayGlG | Beteiligung Gleichstellungsbeauftragte | vorhanden (Kontrolle) |
| 4 Gespräche | AGG | zulässige Fragen | vorhanden |
| 4 Gespräche | Art. 5 Abs. 2 DSGVO | Rechenschaftspflicht Dokumentation | vorhanden |
| 5 Einstellung | BayPVG | Mitbestimmung Personalrat bei Einstellung | Lücke (geplant) |
| 5 Einstellung | TV-L, NachwG | Vertrag, Nachweis Arbeitsbedingungen | vorhanden |
| 6 Absagen | § 15 Abs. 4 AGG | 2-Monats-Frist → ca. 6 Monate Aufbewahrung | vorhanden |
| 6 Absagen | Art. 17 DSGVO | Löschung | vorhanden |
| 6 Absagen | Art. 6 Abs. 1 lit. a DSGVO | Talentpool nur mit Einwilligung | nicht Teil des Prozesses |

**Kontrolle:** Die Gleichstellungsbeauftragte ist bewusst im Prozess enthalten → der Agent muss den Schritt als vorhanden erkennen und darf ihn nicht als Lücke melden.
