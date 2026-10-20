# ERGEBNIS H1 (inkl. H1b)

Stand 20.10.2026. **Der Testlauf von Konfiguration A konnte nicht ausgeführt werden: Es liegt kein gültiger
OpenAI-API-Key vor** (Details in Abschnitt 6). Programm, Docker-Setup, Soll-Liste und Auswertung sind fertig und
getestet; die Abschnitte 1–4 werden nach dem ersten echten Lauf von `python -m src.evaluate` automatisch erzeugt
(alles oberhalb von `MANUELL START` wird dabei ersetzt).

## 1. Lauf-Metadaten

Noch kein Lauf. Konfiguriert: Modell-Snapshot `gpt-6-luna`, `reasoning_effort = medium`, Domains
eur-lex.europa.eu, gesetze-im-internet.de, gesetze-bayern.de, tdl-online.de.

## 2. Stufe 1 – Rechtsrahmen

Noch kein Lauf.

## 3. Stufe 2 – Zuordnung je Task

Noch kein Lauf.

## 4. H1b – Lückenkandidaten

Noch kein Lauf.

<!-- MANUELL START: alles ab hier bleibt bei erneutem evaluate.py erhalten -->

## 5. Auffälligkeiten

Noch keine Funde vorhanden. Nach dem Lauf listet `evaluate.py` alle `nicht_in_soll`-Funde mit Zitat der
Modellbegründung in Abschnitt 5a als Material für diesen Abschnitt.

## 6. Technische Probleme

- **Kein gültiger API-Key (blockierend).** `h1/.env` enthält keinen Key. Auf dem Rechner gefundene Keys
  (`Masterthesis/.env`, `openclaw-*/.env`, alle derselbe Key mit Endung …3JoA) liefern bei OpenAI
  `401 invalid_api_key`. Der Lauf bricht deshalb mit „OPENAI_API_KEY fehlt“ ab, bevor ein Lauf-Ordner entsteht.
- **Geprüft ohne gültigen Key:** Docker-Build (`ma-h1:latest`), Erzeugung des strikten JSON-Schemas aus den
  Pydantic-Modellen durch das SDK (openai 3.35.1), Aufbau der Responses-API-Anfrage bis zur Authentifizierung
  (Antwort 401, also kein Fehler im Request-Aufbau vor dem Server), Normierung von Regelwerken/Fundstellen und die
  komplette Auswertung (`evaluate.py`, zweimal hintereinander) mit einem synthetischen Lauf außerhalb von `runs/`.
- **Nicht geprüft:** ob `gpt-6-luna` Websuche mit Domain-Filter und Structured Outputs in *einem* Aufruf
  akzeptiert, Laufzeit, Tokenverbrauch, Kosten, Verhalten des Domain-Filters (z. B. ob tdl-online.de überhaupt
  durchsuchbare Volltexte des TV-L liefert).
- **GitHub:** Das HTTPS-Token (`gh`) auf dem Rechner ist ungültig; Push erfolgt über SSH (Remote umgestellt).

## 7. Offene Fragen und Annahmen

- **Modell-Snapshot:** Laut OpenAI-Modellseite gibt es für GPT-6 Luna keinen datierten Snapshot, nur `gpt-6-luna`
  → verwendet. Falls ein datierter Snapshot gewünscht ist, sobald verfügbar in `config.yaml` eintragen.
- **Preis der Websuche** (10 USD/1000 Aufrufe) ist eine Annahme; Kosten daher nur geschätzt.
- **Soll-Liste:** Zuordnung der Zeilen zu Tasks nach eigenem Verständnis (Begründung je Zeile in `DECISIONS.md`).
  Besonders prüfen: S08 (Art. 6 DSGVO als Platzhalter für „Rechtsgrundlage“), S13/S14 (Art. 26 AI Act aufgeteilt,
  S14 mit Abs. 11 ergänzt), S17 (Art. 22 DSGVO → T3.4 statt T3.2/T3.3), S20/S26 (BayPVG Art. 75a / Art. 75 als
  Normvorschlag; Art. 78 BayPVG beachten), Regelwerke ohne Fundstelle (TV-L, BayGlG, BayDSG, NachwG, AGG an T3.1/T4.2).
- **Eine Task je Soll-Zeile:** Normen, die fachlich an mehreren Tasks gelten (z. B. Art. 13 DSGVO an T2.1 *und*
  T2.2), werden am zweiten Task als `falscher_task` gewertet.
- **Lücken-Matching auf Regelwerksebene:** Ein Regelwerk aus Stufe 1 ohne Zuordnung in Stufe 2 trifft alle
  Soll-Lücken dieses Regelwerks. Das ist großzügig; Alternative wäre, nur `moegliche_luecke`-Funde zu zählen.
- **Konfiguration B** bekommt nur die Kurzformen der Regelwerke (ohne Titel).
- **Stufe-1-Fehler** bricht den Lauf ab; einzelne Stufe-2-Fehler nicht (Task bleibt ohne Funde, in `protokoll.json`).

## 8. Verbesserungsvorschläge

- **Soll-Liste:** Spalte `task_id` mehrwertig erlauben (`T2.1|T2.2`) und für jede leere Fundstelle die konkrete
  Norm ergänzen (TV-L § 12/§ 2, NachwG § 2, BayGlG Art. …, BayDSG Art. …), sonst ist „korrekt“ dort zu großzügig.
- **Soll-Liste:** fachlich naheliegende, bisher fehlende Normen ergänzen oder bewusst ausschließen, damit sie nicht
  als `nicht_in_soll` zählen (z. B. Art. 88 DSGVO, Art. 9 DSGVO bei Schwerbehinderung, § 22 AGG, Art. 26 Abs. 7 AI Act
  – Information der Arbeitnehmervertreter, BayHIG/WissZeitVG für befristete wiss. Mitarbeiter).
- **Prompts:** Kurzform der Regelwerke vorgeben („DSGVO“, „AI Act“, …) oder eine Feldbeschreibung im Schema, um die
  Normierung zu entlasten; Fundstellenformat vorgeben („Art. 26 Abs. 11“, eine Norm je Fund).
- **Datenformat:** im Fund ein optionales Feld `vorhandener_task` für Lücken, die an einen bestehenden Task angehängt
  werden könnten; Websuche-Quellen je Fund (URL-Liste) statt nur `quelle_url`.
- **Auswertung:** nach den ersten echten Läufen die `nicht_in_soll`-Liste durchgehen und die Muster in
  `src/normierung.py` um tatsächlich vorkommende Schreibweisen ergänzen.

<!-- MANUELL ENDE -->
