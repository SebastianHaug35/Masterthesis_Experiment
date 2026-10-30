# Daten von Sai et al. (Fall 3: Vergleichsdaten)

Quelle: Repository zur Studie von Sai, Sadiq, Han, Demartini, Rinderle-Ma (2024),
„Which Legal Requirements are Relevant to a Business Process? Comparing AI-Driven Methods as Expert Aid“,
RCIS 2024, LNBIP 513, S. 166–182 (Preprint: arXiv:2401.02986).
Abgerufen am 30.10.2026 von https://anonymous.4open.science/r/regulatory_relevance4process-D73C
(dort verfügbar bis 5.12.2028). Lizenz: MIT (siehe `LICENSE`). Dateien unverändert übernommen.

| Datei/Ordner | Inhalt |
|---|---|
| `MASTER_data.xlsx` | Gesamtdaten: Dokumente (`requirements_descriptions`), Prozessbeschreibungen je Ebene (`1_descriptions`, `2_descriptions`, `training_descriptions`), Rechtsabsätze mit Zuordnung der Fachleute je Teilprozess und Task (`1_matching`, `2_matching`, `training_matching`) |
| `korpus/` | Eingaben des Embedding-Verfahrens: Textsammlung je Fall (`Input_corpus_uc*.xlsx`), Teilprozess- und Task-Beschreibungen als Anfragen |
| `gold_standard/` | Referenzzuordnung je Fall und Ebene (process / subprocess / event) als Paare Anfrage–relevanter Absatz |
| `prompts_sai/` | GPT-4-Prompts der Studie (Aufgabe, Prozessbeschreibung je Fall, Regeltext) |

Fälle: uc1 = Schadensbearbeitung Reiseversicherung (1 Prozess, 7 Teilprozesse, 31 Tasks),
uc2 = Know Your Customer, Bank (1 Prozess, 7 Teilprozesse, 19 Tasks), training = Hire Employee (nur Prompt-Entwicklung).
Hinweis: Ein internes Dokument des Versicherers ist laut Studie nicht veröffentlicht; `1_matching` hat daher weniger Zeilen als die 489 Absätze im Paper.
