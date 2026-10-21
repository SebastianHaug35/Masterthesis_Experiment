# ERGEBNIS H1 (inkl. H1b)

Automatisch erzeugt von `python -m src.evaluate` (Abschnitte 1–4 und Material 5a). Alle Läufe sind gegen die **aktuelle** Soll-Liste ausgewertet und nach (`version`, `konfig`) gruppiert; Werte = Mittelwert ± Standardabweichung über die Läufe. Abschnitte 5–8 unten sind manuell gepflegt. Begriffe: `README.md`, `DECISIONS.md`. Details je Lauf: `results/kennzahlen.csv`, `funde_bewertet.csv`, `luecken_bewertet.csv`, `uebersehen.csv`.

## 1. Lauf-Metadaten

| run_id | Version | Konfig | Suche | Modell-Snapshot | reasoning_effort | Dauer | Tokens in | Tokens out | Websuchen / Werkzeugaufrufe | Kosten USD (geschätzt) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20261020-145929_A_1 | v1 | A | openai | `gpt-6-luna` | medium | 9 min 19 s | 922 889 | 111 545 | 95 | 1.0923 | ok |
| 20261021-094308_A_2 | v2 | A | openai | `gpt-6-luna` | medium | 5 min 51 s | 886 828 | 123 339 | 95 | 1.0947 | ok |
| 20261021-094923_A_3 | v2 | A | openai | `gpt-6-luna` | medium | 5 min 43 s | 866 917 | 116 962 | 91 | 1.0482 | ok |
| 20261021-095507_A_4 | v2 | A | openai | `gpt-6-luna` | medium | 5 min 19 s | 920 122 | 117 443 | 94 | 1.0839 | ok |
| 20261021-100026_A_5 | v2 | A | openai | `gpt-6-luna` | medium | 6 min 57 s | 919 326 | 119 993 | 97 | 1.1153 | ok |
| 20261021-100724_A_6 | v2 | A | openai | `gpt-6-luna` | medium | 6 min 4 s | 923 271 | 120 465 | 97 | 1.1159 | ok |
| 20261021-112400_A_7 | v3 | A | eigen | `gpt-6-luna` | medium | 44 min 48 s | 637 571 | 56 129 | 301 (44 ohne Ergebnis) | 0.064 | ok (17 Fehler/Retries) |
| 20261021-123226_A_8 | v3 | A | eigen | `gpt-6-luna` | medium | 21 min 5 s | 570 033 | 56 072 | 304 (71 ohne Ergebnis) | 0.0595 | ok (16 Fehler/Retries) |
| 20261021-125331_A_9 | v3 | A | eigen | `gpt-6-luna` | medium | 17 min 43 s | 629 855 | 46 155 | 309 (81 ohne Ergebnis) | 0.0544 | ok (18 Fehler/Retries) |
| 20261021-131115_A_10 | v3 | A | eigen | `gpt-6-luna` | medium | 12 min 5 s | 624 583 | 47 532 | 301 (67 ohne Ergebnis) | 0.0578 | ok (17 Fehler/Retries) |
| 20261021-132320_A_11 | v3 | A | eigen | `gpt-6-luna` | medium | 9 min 57 s | 626 111 | 50 318 | 303 (69 ohne Ergebnis) | 0.0592 | ok (17 Fehler/Retries) |
| 20261021-133323_B_1 | v3 | B | eigen | `gpt-6-luna` | medium | 7 min 51 s | 472 154 | 39 822 | 285 (74 ohne Ergebnis) | 0.0457 | ok (19 Fehler/Retries) |
| 20261021-134114_B_2 | v3 | B | eigen | `gpt-6-luna` | medium | 6 min 15 s | 421 924 | 44 746 | 276 (56 ohne Ergebnis) | 0.0439 | ok (18 Fehler/Retries) |
| 20261021-134730_B_3 | v3 | B | eigen | `gpt-6-luna` | medium | 7 min 23 s | 428 417 | 42 910 | 280 (63 ohne Ergebnis) | 0.0424 | ok (17 Fehler/Retries) |
| 20261021-135453_B_4 | v3 | B | eigen | `gpt-6-luna` | medium | 6 min 32 s | 476 578 | 43 060 | 276 (51 ohne Ergebnis) | 0.0442 | ok (18 Fehler/Retries) |
| 20261021-140126_B_5 | v3 | B | eigen | `gpt-6-luna` | medium | 7 min 41 s | 448 645 | 39 736 | 275 (51 ohne Ergebnis) | 0.0418 | ok (18 Fehler/Retries) |

### Übersicht je (version, konfig)

| Kennzahl | v1 A (n=1) | v2 A (n=5) | v3 A (n=5) | v3 B (n=5) |
| --- | --- | --- | --- | --- |
| Stufe 1 Recall (Regelwerk) | 100% | 98% ± 4% | 87% ± 5% | – |
| Stufe 1 Präzision (Regelwerk) | 92% | 83% ± 11% | 93% ± 7% | – |
| Stufe 2 Recall (Fundstelle) | 70% | 98% ± 2% | 66% ± 8% | 67% ± 7% |
| Stufe 2 Präzision (ohne neutral) | 58% | 54% ± 3% | 60% ± 9% | 68% ± 5% |
| Stufe 2 Anteil neutral | 28% | 24% ± 6% | 26% ± 3% | 22% ± 4% |
| Stufe 2 Recall inkl. Lückenmeldungen am Soll-Task | 91% | 98% ± 2% | 66% ± 8% | 67% ± 7% |
| Stufe 2 Anzahl Funde (zuordnung) | 120.0 | 209.4 ± 8.3 | 83.6 ± 14.3 | 58.6 ± 11.0 |
| H1b Lücken-Recall (streng) | 100% | 80% ± 5% | 16% ± 6% | 11% ± 0% |
| H1b Lücken-Recall (großzügig) | 100% | 80% ± 5% | 47% ± 32% | 42% ± 24% |
| H1b Lückenmeldungen (Funde) | 80.0 | 32.8 ± 6.6 | 2.8 ± 1.1 | 3.6 ± 2.1 |
| H1b Lückenmeldungen (dedupliziert) | 31.0 | 13.0 ± 0.7 | 2.4 ± 0.5 | 2.6 ± 1.1 |
| H1b falsche Lückenmeldungen (dedupliziert) | 14.0 | 4.2 ± 1.3 | 0.8 ± 0.8 | 1.4 ± 0.9 |
| H1b Kontrolle: Fehlmeldungen S23 | 1.0 | 0.4 ± 0.5 | 0.0 ± 0.0 | 0.0 ± 0.0 |
| Anteil Zuordnungen mit Hinweis | 0% | 95% ± 1% | 84% ± 4% | 89% ± 4% |
| Anteil erfundene Normen (existiert = nein) | 0% | 0% ± 0% | 0% ± 0% | 0% ± 0% |
| Anzahl erfundene Normen | 0.0 | 0.0 ± 0.0 | 0.0 ± 0.0 | 0.0 ± 0.0 |
| Anteil Existenz nicht prüfbar | 0% | 0% ± 0% | 0% ± 0% | 0% ± 0% |
| Anteil Funde mit vorher geladener Norm | – | – | 94% ± 8% | 91% ± 9% |
| Werkzeugaufrufe | – | – | 303.6 ± 3.3 | 278.4 ± 4.2 |
| Werkzeugaufrufe ohne Ergebnis | – | – | 66.4 ± 13.6 | 59.0 ± 9.7 |
| Anteil unsicher | 26% | 15% ± 4% | 14% ± 3% | 10% ± 4% |
| Anteil nicht_in_soll / luecke_ohne_soll | 6% | 12% ± 5% | 7% ± 7% | 5% ± 3% |
| Tokens Input | 922 889 | 903 293 ± 25 168 | 617 631 ± 27 078 | 449 544 ± 24 759 |
| Tokens Output | 111 545 | 119 640 ± 2 573 | 51 241 ± 4 683 | 42 055 ± 2 199 |
| Websuchen | 95.0 | 94.8 ± 2.5 | 0.0 ± 0.0 | 0.0 ± 0.0 |
| Kosten USD (geschätzt) | 1.092 | 1.092 ± 0.028 | 0.059 ± 0.003 | 0.044 ± 0.002 |

## 2. Stufe 1 – Rechtsrahmen

Soll-Regelwerke = Regelwerke aus Zeilen mit `typ` zuordnung oder luecke. Regelwerke, die nur in Neutral-Zeilen stehen, zählen als „neutral“ (nicht als zusätzlich, nicht in der Präzision). Konfiguration B hat keine Stufe 1.

| Kennzahl | v1 A (n=1) | v2 A (n=5) | v3 A (n=5) | v3 B (n=5) |
| --- | --- | --- | --- | --- |
| Recall | 100% | 98% ± 4% | 87% ± 5% | – |
| Präzision | 92% | 83% ± 11% | 93% ± 7% | – |

In wie vielen Läufen hat Stufe 1 das Regelwerk genannt:

| Regelwerk | Status | v1 A | v2 A | v3 A |
| --- | --- | --- | --- | --- |
| GG | Soll | 1/1 | 5/5 | 3/5 |
| AGG | Soll | 1/1 | 5/5 | 5/5 |
| TV-L | Soll | 1/1 | 5/5 | 5/5 |
| SGB IX | Soll | 1/1 | 5/5 | 5/5 |
| BayGlG | Soll | 1/1 | 5/5 | 5/5 |
| DSGVO | Soll | 1/1 | 5/5 | 5/5 |
| BayDSG | Soll | 1/1 | 5/5 | 5/5 |
| AI Act | Soll | 1/1 | 5/5 | 5/5 |
| BayPVG | Soll | 1/1 | 5/5 | 5/5 |
| NachwG | Soll | 1/1 | 4/5 | 0/5 |
| WissZeitVG | Soll | 1/1 | 5/5 | 5/5 |
| TzBfG | Soll | 1/1 | 5/5 | 4/5 |
| BayHIG | neutral | 1/1 | 5/5 | 5/5 |
| BDSG | zusätzlich | 0/1 | 3/5 | 0/5 |
| BGB | zusätzlich | 1/1 | 5/5 | 1/5 |
| BayArchivG | zusätzlich | 0/1 | 1/5 | 0/5 |
| BayBGG | zusätzlich | 0/1 | 1/5 | 0/5 |
| BayDiV | zusätzlich | 0/1 | 1/5 | 0/5 |
| EntgTranspG | zusätzlich | 0/1 | 1/5 | 0/5 |
| Richtlinie (EU) 2016/2102 | zusätzlich | 0/1 | 1/5 | 0/5 |
| bdsg_2018 | zusätzlich | 0/1 | 0/5 | 1/5 |
| bgb | zusätzlich | 0/1 | 0/5 | 2/5 |

## 3. Stufe 2 – Zuordnung je Task

Bewertet werden Funde mit `typ = zuordnung`. Präzision = korrekt / (korrekt + falscher_absatz + falscher_task + nicht_in_soll); `neutral` geht nicht ein und wird separat ausgewiesen. Teilprozess einer Soll-Zeile mit mehreren Tasks = Teilprozess des ersten Tasks.

| Kennzahl | v1 A (n=1) | v2 A (n=5) | v3 A (n=5) | v3 B (n=5) |
| --- | --- | --- | --- | --- |
| Funde (zuordnung) | 120.0 | 209.4 ± 8.3 | 83.6 ± 14.3 | 58.6 ± 11.0 |
| davon korrekt | 50.0 | 85.6 ± 5.0 | 36.4 ± 5.7 | 31.0 ± 5.4 |
| davon neutral | 34.0 | 50.4 ± 11.7 | 22.0 ± 3.6 | 12.8 ± 3.7 |
| davon falscher_absatz | 0.0 | 0.0 ± 0.0 | 0.0 ± 0.0 | 0.0 ± 0.0 |
| davon falscher_task | 32.0 | 51.0 ± 4.1 | 19.2 ± 5.4 | 11.8 ± 2.0 |
| davon nicht_in_soll | 4.0 | 22.4 ± 11.3 | 6.0 ± 7.5 | 3.0 ± 2.3 |
| Recall gesamt | 70% | 98% ± 2% | 66% ± 8% | 67% ± 7% |
| Präzision gesamt | 58% | 54% ± 3% | 60% ± 9% | 68% ± 5% |
| Anteil neutral | 28% | 24% ± 6% | 26% ± 3% | 22% ± 4% |
| Recall inkl. Lückenmeldungen am Soll-Task | 91% | 98% ± 2% | 66% ± 8% | 67% ± 7% |
| Recall TP1 | 50% | 100% ± 0% | 55% ± 33% | 70% ± 21% |
| Recall TP2 | 67% | 100% ± 0% | 93% ± 15% | 87% ± 18% |
| Recall TP3 | 75% | 100% ± 0% | 50% ± 35% | 40% ± 14% |
| Recall TP4 | 50% | 95% ± 11% | 55% ± 21% | 50% ± 31% |
| Recall TP5 | 100% | 93% ± 15% | 47% ± 30% | 73% ± 37% |
| Recall TP6 | 50% | 100% ± 0% | 100% ± 0% | 100% ± 0% |
| Recall GESAMT | 100% | 100% ± 0% | 87% ± 18% | 73% ± 15% |
| Präzision TP1 | 100% | 82% ± 10% | 88% ± 16% | 73% ± 30% |
| Präzision TP2 | 89% | 72% ± 12% | 71% ± 10% | 75% ± 19% |
| Präzision TP3 | 46% | 47% ± 3% | 50% ± 39% | 64% ± 17% |
| Präzision TP4 | 67% | 55% ± 10% | 64% ± 21% | 68% ± 21% |
| Präzision TP5 | 58% | 53% ± 7% | 83% ± 17% | 96% ± 9% |
| Präzision TP6 | 40% | 31% ± 5% | 39% ± 3% | 42% ± 9% |

Je Lauf:

| run_id | Version | Konfig | Funde | korrekt | neutral | falscher_absatz | falscher_task | nicht_in_soll | Recall | Präzision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20261020-145929_A_1 | v1 | A | 120 | 50 | 34 | 0 | 32 | 4 | 70% | 58% |
| 20261021-094308_A_2 | v2 | A | 200 | 78 | 64 | 0 | 46 | 12 | 96% | 57% |
| 20261021-094923_A_3 | v2 | A | 220 | 91 | 59 | 0 | 55 | 15 | 100% | 57% |
| 20261021-095507_A_4 | v2 | A | 209 | 86 | 52 | 0 | 55 | 16 | 100% | 55% |
| 20261021-100026_A_5 | v2 | A | 203 | 84 | 39 | 0 | 48 | 32 | 96% | 51% |
| 20261021-100724_A_6 | v2 | A | 215 | 89 | 38 | 0 | 51 | 37 | 100% | 50% |
| 20261021-112400_A_7 | v3 | A | 102 | 37 | 27 | 0 | 19 | 19 | 65% | 49% |
| 20261021-123226_A_8 | v3 | A | 94 | 41 | 22 | 0 | 26 | 5 | 74% | 57% |
| 20261021-125331_A_9 | v3 | A | 67 | 34 | 17 | 0 | 13 | 3 | 70% | 68% |
| 20261021-131115_A_10 | v3 | A | 74 | 28 | 23 | 0 | 23 | 0 | 52% | 55% |
| 20261021-132320_A_11 | v3 | A | 81 | 42 | 21 | 0 | 15 | 3 | 70% | 70% |
| 20261021-133323_B_1 | v3 | B | 47 | 26 | 10 | 0 | 10 | 1 | 65% | 70% |
| 20261021-134114_B_2 | v3 | B | 74 | 39 | 14 | 0 | 15 | 6 | 70% | 65% |
| 20261021-134730_B_3 | v3 | B | 63 | 29 | 17 | 0 | 12 | 5 | 74% | 63% |
| 20261021-135453_B_4 | v3 | B | 60 | 34 | 15 | 0 | 10 | 1 | 70% | 76% |
| 20261021-140126_B_5 | v3 | B | 49 | 27 | 8 | 0 | 12 | 2 | 57% | 66% |

In wie vielen Läufen wurde die Soll-Zuordnung korrekt getroffen:

| Soll | Regelwerk | Fundstelle | Task(s) | v1 A (n=1) | v2 A (n=5) | v3 A (n=5) | v3 B (n=5) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | GG | Art. 33 Abs. 2 | GESAMT | 1/1 | 5/5 | 3/5 | 2/5 |
| S02 | AGG | § 7 | GESAMT | 1/1 | 5/5 | 5/5 | 5/5 |
| S03 | AGG | § 11 | T1.3 | 0/1 | 5/5 | 4/5 | 3/5 |
| S04 | TV-L | – | T1.2 | 0/1 | 5/5 | 2/5 | 4/5 |
| S07 | BayGlG | – | T1.2|T1.3 | 1/1 | 5/5 | 2/5 | 2/5 |
| S08 | DSGVO | Art. 6 | T2.1|T2.3 | 1/1 | 5/5 | 5/5 | 5/5 |
| S09 | BayDSG | – | T2.1|T2.3 | 1/1 | 5/5 | 4/5 | 4/5 |
| S10 | DSGVO | Art. 13 | T2.1|T2.2 | 0/1 | 5/5 | 5/5 | 4/5 |
| S11 | DSGVO | Art. 32 | GESAMT | 1/1 | 5/5 | 5/5 | 4/5 |
| S12 | AI Act | Anhang III Nr. 4 | T3.1|T3.2 | 1/1 | 5/5 | 2/5 | 3/5 |
| S13 | AI Act | Art. 26 | T3.1|T3.2|T3.3|T3.4 | 1/1 | 5/5 | 3/5 | 5/5 |
| S17 | DSGVO | Art. 22 | T3.4|T5.1 | 0/1 | 5/5 | 1/5 | 0/5 |
| S19 | AGG | – | T3.1|T3.2 | 1/1 | 5/5 | 4/5 | 0/5 |
| S21 | SGB IX | § 165 | T4.1 | 0/1 | 5/5 | 0/5 | 3/5 |
| S23 | BayGlG | Art. 17 | T4.1|T4.2 | 0/1 | 5/5 | 4/5 | 4/5 |
| S24 | AGG | – | T4.2 | 1/1 | 5/5 | 2/5 | 0/5 |
| S25 | DSGVO | Art. 5 Abs. 2 | T4.3|T6.2 | 1/1 | 4/5 | 5/5 | 3/5 |
| S27 | TV-L | – | T5.2|T5.3 | 1/1 | 5/5 | 4/5 | 5/5 |
| S28 | NachwG | – | T5.2|T5.3 | 1/1 | 4/5 | 0/5 | 3/5 |
| S29 | AGG | § 15 Abs. 4 | T6.2 | 0/1 | 5/5 | 5/5 | 5/5 |
| S30 | DSGVO | Art. 17 | T6.3 | 1/1 | 5/5 | 5/5 | 5/5 |
| S46 | WissZeitVG | § 2 | T1.2|T5.2|T5.3 | 1/1 | 5/5 | 3/5 | 5/5 |
| S47 | TzBfG | § 14 Abs. 4 | T5.2|T5.3 | 1/1 | 5/5 | 3/5 | 3/5 |

## 4. H1b – Lückenkandidaten

Kategorien je Lückenmeldung (`typ = moegliche_luecke`), dedupliziert nach Regelwerk + Artikel/Paragraf: `luecke_korrekt` (trifft Soll-Lücke), `luecke_neutral` (trifft Neutral-Zeile), `luecke_an_vorhandener_zuordnung` (trifft nur eine Soll-Zuordnung), `luecke_ohne_soll` (trifft nichts). Falsch = die beiden letzten. Lücken-Recall streng = nur Lückenmeldungen; großzügig = zusätzlich Regelwerke aus Stufe 1 (B: Vorgabe) ohne Zuordnung. Kontrolle = Lückenmeldungen, die S23 (Gleichstellungsbeauftragte, vorhandener Schritt) treffen.

| Kennzahl | v1 A (n=1) | v2 A (n=5) | v3 A (n=5) | v3 B (n=5) |
| --- | --- | --- | --- | --- |
| Lücken-Recall streng | 100% | 80% ± 5% | 16% ± 6% | 11% ± 0% |
| Lücken-Recall großzügig | 100% | 80% ± 5% | 47% ± 32% | 42% ± 24% |
| Lückenmeldungen (Funde) | 80.0 | 32.8 ± 6.6 | 2.8 ± 1.1 | 3.6 ± 2.1 |
| Lückenmeldungen (dedupliziert) | 31.0 | 13.0 ± 0.7 | 2.4 ± 0.5 | 2.6 ± 1.1 |
| davon luecke_korrekt | 9.0 | 7.2 ± 0.4 | 1.4 ± 0.5 | 1.0 ± 0.0 |
| davon luecke_neutral | 8.0 | 1.6 ± 0.9 | 0.2 ± 0.4 | 0.2 ± 0.4 |
| davon luecke_an_vorhandener_zuordnung | 10.0 | 1.2 ± 0.8 | 0.4 ± 0.5 | 1.0 ± 1.0 |
| davon luecke_ohne_soll | 4.0 | 3.0 ± 0.7 | 0.4 ± 0.5 | 0.4 ± 0.5 |
| falsche Lückenmeldungen | 14.0 | 4.2 ± 1.3 | 0.8 ± 0.8 | 1.4 ± 0.9 |
| Kontrolle: Fehlmeldungen S23 | 1.0 | 0.4 ± 0.5 | 0.0 ± 0.0 | 0.0 ± 0.0 |
| Regelwerke ohne Zuordnung | 1.0 | 0.8 ± 0.8 | 3.8 ± 2.8 | 2.6 ± 1.5 |

In wie vielen Läufen wurde die Soll-Lücke erkannt (streng):

| Soll-Lücke | Regelwerk | Fundstelle | Inhalt | v1 A (n=1) | v2 A (n=5) | v3 A (n=5) | v3 B (n=5) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S05 | SGB IX | § 164 | Prüfung Besetzung freier Stellen mit schwerbehinderten Menschen, Beteiligung der … | 1/1 | 5/5 | 0/5 | 0/5 |
| S06 | SGB IX | § 165 | Meldung freier Stellen an die Agentur für Arbeit (öffentlicher Arbeitgeber, Satz … | 1/1 | 4/5 | 1/5 | 0/5 |
| S14 | AI Act | Art. 26 Abs. 11 | Information der Betroffenen über den KI-Einsatz | 1/1 | 5/5 | 0/5 | 0/5 |
| S15 | AI Act | Art. 27 | Grundrechte-Folgenabschätzung (öffentliche Stelle) | 1/1 | 5/5 | 2/5 | 3/5 |
| S16 | AI Act | Art. 4 | KI-Kompetenz der Mitarbeitenden | 1/1 | 1/5 | 0/5 | 0/5 |
| S18 | DSGVO | Art. 35 | Datenschutz-Folgenabschätzung | 1/1 | 5/5 | 3/5 | 0/5 |
| S20 | BayPVG | Art. 75a | Mitbestimmung Personalrat bei Einführung/Anwendung des KI-Tools (Abs. 1 Nr. 2, a … | 1/1 | 5/5 | 0/5 | 0/5 |
| S22 | SGB IX | § 178 | Beteiligung der Schwerbehindertenvertretung | 1/1 | 5/5 | 1/5 | 2/5 |
| S26 | BayPVG | Art. 78 Abs. 3 | Mitteilung an den Personalrat über die Einstellung (Mitbestimmung nach Art. 78 A … | 1/1 | 1/5 | 0/5 | 0/5 |

### Lückenmeldungen v1 A (1 Läufe, dedupliziert je Lauf)

| Regelwerk | Norm | Kategorie | Läufe | Meldungen | Soll-Lücke | Soll-Zuordnung | Beispiel fehlender Schritt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI Act | Art. 26 | luecke_korrekt | 1 | 3 | S14 | S13 | Vor dem Einsatz des Hochrisiko-KI-Systems am Arbeitsplatz die betroffenen Beschäftigten und ihre Vertretung informieren; außerdem Bewerberinnen und Bewerber übe … |
| AI Act | Art. 27 | luecke_korrekt | 1 | 5 | S15 | – | Vor der ersten Inbetriebnahme beziehungsweise Verwendung des Hochrisiko-KI-Systems eine Grundrechte-Folgenabschätzung durchführen und erforderlichenfalls aktual … |
| AI Act | Art. 4 | luecke_korrekt | 1 | 3 | S16 | – | Sicherstellen und dokumentieren, dass die mit Betrieb und Nutzung des KI-Systems befassten Beschäftigten über ein ihrem Einsatzkontext angemessenes Maß an KI-Ko … |
| BayPVG | Art. 75a | luecke_korrekt | 1 | 5 | S20 | – | Vor Einführung oder Anwendung des automatisierten Verfahrens zur Personalverwaltung die Mitbestimmung des Personalrats prüfen und gegebenenfalls durchführen. |
| BayPVG | Art. 78 | luecke_korrekt | 1 | 1 | S26 | – | Vor dem Abschluss beziehungsweise Vollzug der Einstellung prüfen und dokumentieren, ob der Personalrat über die Einstellung informiert wurde. |
| DSGVO | Art. 35 | luecke_korrekt | 1 | 7 | S18 | – | Vor Beginn der Verarbeitung im Gesamtverfahren prüfen und dokumentieren, ob wegen des KI-gestützten Rankings und der weiteren Verarbeitung von Bewerberdaten ein … |
| SGB IX | § 164 | luecke_korrekt | 1 | 4 | S05,S22 | – | Bewerbungen schwerbehinderter Menschen nach Eingang der Schwerbehindertenvertretung und den weiteren in § 164 Abs. 1 genannten Vertretungen mitteilen und die vo … |
| SGB IX | § 165 | luecke_korrekt | 1 | 7 | S06,S22 | S21 | Vor der Veröffentlichung ist nach erfolgloser Prüfung einer internen Besetzung der freie oder neue Arbeitsplatz frühzeitig der Agentur für Arbeit zu melden. Ein … |
| SGB IX | § 178 | luecke_korrekt | 1 | 2 | S22 | – | Bei Bewerbungen schwerbehinderter Menschen die Schwerbehindertenvertretung unverzüglich und umfassend unterrichten und vor einer sie betreffenden Entscheidung a … |
| AI Act | Art. 14 | luecke_neutral | 1 | 1 | – | S13 | Die menschliche Prüfung konkret ausgestalten: zuständige Personen müssen die Grenzen und Ausgaben des Systems verstehen, Automatisierungsbias berücksichtigen un … |
| AI Act | Art. 49 | luecke_neutral | 1 | 1 | – | – | Falls das System als Hochrisiko-KI-System nach Anhang III eingestuft wird, vor seiner Verwendung die erforderliche Registrierung der Hochschule als Betreiber in … |
| AI Act | Art. 86 | luecke_neutral | 1 | 1 | – | – | Ein Verfahren vorsehen, um auf ein Verlangen betroffener Personen eine klare und aussagekräftige Erläuterung zur Rolle des KI-Systems und zu den wichtigsten Ele … |
| BayDSG | Art. 35 | luecke_neutral | 1 | 1 | – | S09 | Die Shortlistentscheidung muss durch eine natürliche Person tatsächlich eigenständig getroffen werden und darf bei nachteiliger Rechtsfolge oder erheblicher Bee … |
| DSGVO | Art. 28 | luecke_neutral | 1 | 3 | – | – | Falls ein externer Anbieter das Portal im Auftrag der Hochschule betreibt oder Bewerbungsdaten sonst weisungsgebunden verarbeitet, vor Beginn der Verarbeitung e … |
| DSGVO | Art. 30 | luecke_neutral | 1 | 3 | – | – | Die Verarbeitung der Bewerbungsdaten in das Verzeichnis der Verarbeitungstätigkeiten aufnehmen beziehungsweise den vorhandenen Eintrag für das Bewerbungsportal  … |
| DSGVO | Art. 5 | luecke_neutral | 1 | 3 | – | S25,S30 | Eine konkrete, begründete Aufbewahrungsdauer samt Beginn und Ende festlegen und dokumentieren; nach Fristablauf prüfen, ob die Bewerbungsdaten noch für einen zu … |
| DSGVO | Art. 9 | luecke_neutral | 1 | 1 | – | S11 | Für den Fall, dass im Gespräch besondere Kategorien personenbezogener Daten erhoben oder notiert werden, vorab eine einschlägige Ausnahme nach Art. 9 Abs. 2 und … |
| BayDSG | Art. 26 | luecke_an_vorhandener_zuordnung | 1 | 2 | – | S09 | Vor einer Löschung prüfen und gegebenenfalls dokumentieren, ob die Bewerbungsunterlagen einem öffentlichen Archiv zur Übernahme anzubieten sind; bei bestehender … |
| BayDSG | Art. 31 | luecke_an_vorhandener_zuordnung | 1 | 1 | – | S09 | Im Verzeichnis der Verarbeitungstätigkeiten zusätzlich die Rechtsgrundlage und, soweit einschlägig, die Verwendung von Profiling eintragen. |
| BayGlG | Art. 17 | luecke_an_vorhandener_zuordnung | 1 | 5 | – | S07,S23 | Die Gleichstellungsbeauftragte bei Personalangelegenheiten rechtzeitig und umfassend unterrichten sowie erforderliche Unterlagen frühzeitig vorlegen. Eine Betei … |
| BayGlG | Art. 7 | luecke_an_vorhandener_zuordnung | 1 | 1 | – | S07 | Bei der Vorbereitung der Stellenausschreibung die geschlechtsneutrale Ausschreibung, den Hinweis auf Teilzeitbeschäftigungsmöglichkeiten und gegebenenfalls die  … |
| DSGVO | Art. 13 | luecke_an_vorhandener_zuordnung | 1 | 5 | – | S10 | Bei oder spätestens zum Zeitpunkt der Erhebung über das Portal die vorgeschriebenen Datenschutzinformationen bereitstellen, insbesondere zu Verantwortlichem, Zw … |
| DSGVO | Art. 22 | luecke_an_vorhandener_zuordnung | 1 | 2 | – | S17 | Sicherstellen und dokumentieren, dass die Shortlist nicht lediglich das KI-Ranking übernimmt: Eine zuständige Person muss die Einzelfälle tatsächlich eigenständ … |
| DSGVO | Art. 32 | luecke_an_vorhandener_zuordnung | 1 | 1 | – | S11 | Für die Zeit der Aufbewahrung geeignete technische und organisatorische Schutzmaßnahmen sicherstellen, etwa angemessene Zugriffsbeschränkungen und Schutz vor un … |
| DSGVO | Art. 6 | luecke_an_vorhandener_zuordnung | 1 | 2 | – | S08 | Vor dem Anlegen der Daten die konkrete Rechtsgrundlage der Bewerberdatenverarbeitung festlegen und dokumentieren. |
| NachwG | § 2 | luecke_an_vorhandener_zuordnung | 1 | 1 | – | S28 | Sicherstellen, dass dem Arbeitnehmer die Niederschrift mit sämtlichen erforderlichen Angaben innerhalb der gesetzlichen Fristen ausgehändigt wird. Die Prozessbe … |
| TV-L | § 12 | luecke_an_vorhandener_zuordnung | 1 | 1 | – | S04,S27 | Die dauerhaft auszuübenden Aufgaben in Arbeitsvorgänge gliedern, deren Anforderungen und zeitliche Anteile bewerten und anhand der einschlägigen Tätigkeitsmerkm … |
| BayArchivG | Art. 14 | luecke_ohne_soll | 1 | 1 | – | – | Klären, ob die Hochschule die Unterlagen in einem eigenen oder sonstigen öffentlichen Archiv archiviert. Falls nicht, nicht mehr benötigte Unterlagen dem zustän … |
| BayPVG | Art. 69 | luecke_ohne_soll | 1 | 3 | – | – | Den Personalrat rechtzeitig und umfassend unterrichten und die erforderlichen Unterlagen zur Verfügung stellen; die Mitbestimmung bei der Einstellung ist vor de … |
| BayPVG | Art. 75 | luecke_ohne_soll | 1 | 3 | – | – | Die vorgesehene Eingruppierung dem Personalrat zur Mitbestimmung vorlegen und das Zustimmungsverfahren vor der abschließenden Maßnahme durchführen. Eine Beteili … |
| BayPVG | Art. 76 | luecke_ohne_soll | 1 | 1 | – | – | Falls die Bedarfsmeldung als Personalanforderung zum Haushaltsvoranschlag weitergeleitet wird, ist der Personalrat vorher anzuhören. Ein solcher Anhörungsschrit … |

### Lückenmeldungen v2 A (5 Läufe, dedupliziert je Lauf)

| Regelwerk | Norm | Kategorie | Läufe | Meldungen | Soll-Lücke | Soll-Zuordnung | Beispiel fehlender Schritt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI Act | Art. 26 | luecke_korrekt | 5 | 16 | S14 | S13 | Falls und sobald die Vorschrift für das eingesetzte System gilt: Bewerbende darüber informieren, dass sie der Verwendung des Hochrisiko-KI-Systems unterliegen;  … |
| AI Act | Art. 27 | luecke_korrekt | 5 | 25 | S15 | – | Vor der erstmaligen Nutzung des Hochrisiko-KI-Systems ist als öffentliche Stelle eine Bewertung der Auswirkungen auf die Grundrechte durchzuführen, sofern die V … |
| BayPVG | Art. 75a | luecke_korrekt | 5 | 19 | S20 | – | Vor Einführung, Anwendung oder erheblicher Änderung des KI-gestützten automatisierten Verfahrens zur Personalverwaltung die Mitbestimmung des Personalrats durch … |
| DSGVO | Art. 35 | luecke_korrekt | 5 | 17 | S18 | – | Vor Beginn der KI-Auswertung eine Datenschutz-Folgenabschätzung durchführen, sofern die systematische und umfassende Bewertung personenbezogener Aspekte auf aut … |
| SGB IX | § 164 | luecke_korrekt | 5 | 13 | S05 | – | Vor beziehungsweise im Zuge der Besetzung ist zu prüfen, ob der freie Arbeitsplatz mit schwerbehinderten Menschen besetzt werden kann; die erforderliche frühzei … |
| SGB IX | § 178 | luecke_korrekt | 5 | 7 | S22 | – | Bei Bewerbungen schwerbehinderter Menschen die Schwerbehindertenvertretung über den einschlägigen Vorgang unterrichten und ihre gesetzliche Möglichkeit zur Teil … |
| SGB IX | § 165 | luecke_korrekt | 4 | 6 | S06 | S21 | Nach erfolgloser Prüfung einer internen Besetzung ist der neue oder neu zu besetzende Arbeitsplatz frühzeitig der Agentur für Arbeit zu melden; dieser gesondert … |
| AI Act | Art. 4 | luecke_korrekt | 1 | 1 | S16 | – | Die mit Betrieb und Nutzung des KI-Systems befassten Beschäftigten müssen über ein ihrem Kontext und Kenntnisstand angemessenes Maß an KI-Kompetenz verfügen; hi … |
| BayPVG | Art. 78 | luecke_korrekt | 1 | 1 | S26 | – | Den Personalrat über die Einstellung informieren, sofern die Stelle unter die Ausnahmekategorie des Art. 78 Abs. 1 Satz 1 Nr. 6 BayPVG fällt. |
| AI Act | Art. 49 | luecke_neutral | 5 | 14 | – | – | Vor der Nutzung ist zu prüfen und gegebenenfalls die Registrierung der Hochschule und des verwendeten Systems in der EU-Datenbank vorzunehmen. |
| DSGVO | Art. 30 | luecke_neutral | 2 | 2 | – | – | Ein Verzeichnis der Verarbeitungstätigkeiten führen oder aktualisieren, das die Verarbeitung von Bewerberdaten im Auswahlverfahren einschließlich der Gesprächsd … |
| DSGVO | Art. 25 | luecke_neutral | 1 | 1 | – | – | Datenschutzfreundliche Voreinstellungen des Bewerbersystems festlegen und überprüfen, insbesondere Datenumfang, Sichtbarkeit und Zugriffsberechtigungen. |
| BayDSG | Art. 26 | luecke_an_vorhandener_zuordnung | 3 | 5 | – | S09 | Soweit eine Anbietungspflicht besteht: Unterlagen dem öffentlichen Archiv anbieten und die Archiventscheidung beziehungsweise den Ablauf der Entscheidungsfrist  … |
| BayGlG | Art. 17 | luecke_an_vorhandener_zuordnung | 2 | 5 | – | S07,S23 | Ein etwaiges Begehren einer betroffenen Person auf Beteiligung der Gleichstellungsbeauftragten auch für die Personalangelegenheit der KI-Vorauswahl entgegennehm … |
| DSGVO | Art. 13 | luecke_an_vorhandener_zuordnung | 1 | 1 | – | S10 | Bewerberinnen und Bewerber bei Erhebung ihrer Daten über eine gegebenenfalls automatisierte Entscheidungsfindung einschließlich Profiling sowie über aussagekräf … |
| BayPVG | Art. 75 | luecke_ohne_soll | 5 | 16 | – | – | Die personalvertretungsrechtliche Mitbestimmung bei der Eingruppierung ist vor der endgültigen Eingruppierungsmaßnahme sicherzustellen; ein entsprechender Betei … |
| BayArchivG | Art. 6 | luecke_ohne_soll | 4 | 6 | – | – | Vor der Löschung nicht mehr benötigte Unterlagen dem zuständigen staatlichen Archiv zur Übernahme anbieten; dabei etwaige einschlägige Vereinbarungen oder Ausna … |
| BayPVG | Art. 70 | luecke_ohne_soll | 4 | 7 | – | – | Die erforderliche Zustimmung des Personalrats zur mitbestimmungspflichtigen Maßnahme vor ihrer Durchführung einholen. |
| BayPVG | Art. 69 | luecke_ohne_soll | 2 | 2 | – | – | Personalrat rechtzeitig und umfassend unterrichten und ihm die für seine Aufgaben erforderlichen Unterlagen zur Verfügung stellen. |

### Lückenmeldungen v3 A (5 Läufe, dedupliziert je Lauf)

| Regelwerk | Norm | Kategorie | Läufe | Meldungen | Soll-Lücke | Soll-Zuordnung | Beispiel fehlender Schritt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DSGVO | Art. 35 | luecke_korrekt | 3 | 3 | S18 | – | Vor dem Einsatz des Rankings prüfen und gegebenenfalls eine Datenschutz-Folgenabschätzung durchführen; im Gesamtprozess ist hierfür kein eigener Task aufgeführt … |
| AI Act | Art. 27 | luecke_korrekt | 2 | 2 | S15 | – | Vor der Inbetriebnahme des Hochrisiko-KI-Systems eine Grundrechte-Folgenabschätzung durchführen und die Ergebnisse der Marktüberwachungsbehörde mitteilen. |
| SGB IX | § 165 | luecke_korrekt | 1 | 1 | S06 | S21 | Freie und neu zu besetzende Arbeitsplätze nach erfolgloser Prüfung einer internen Besetzung frühzeitig der Agentur für Arbeit melden; dieser Prozessschritt ist  … |
| SGB IX | § 178 | luecke_korrekt | 1 | 2 | S22 | – | Sofern schwerbehinderte oder gleichgestellte Bewerberinnen oder Bewerber betroffen sind, ist die Schwerbehindertenvertretung rechtzeitig und umfassend in die si … |
| DSGVO | Art. 19 | luecke_neutral | 1 | 1 | – | – | Soweit Bewerberdaten Empfängern offengelegt wurden, diese Empfänger über die Löschung unterrichten, sofern die Mitteilung nicht unmöglich oder mit unverhältnism … |
| AI Act | Art. 26 | luecke_an_vorhandener_zuordnung | 2 | 3 | – | S13 | Automatisch erzeugte Protokolle des Hochrisiko-KI-Systems, soweit sie der Kontrolle der Hochschule unterliegen, für mindestens sechs Monate oder eine abweichend … |
| BayPVG | Art. 75 | luecke_ohne_soll | 1 | 1 | – | – | Die Beteiligung des Personalrats an der Einstellung ist im Gesamtprozess nicht ausdrücklich vorgesehen. Vor Vollzug der Einstellung ist zu prüfen und gegebenenf … |
| BayPVG | Art. 76 | luecke_ohne_soll | 1 | 1 | – | – | Den Personalrat vor der Weiterleitung von Personalanforderungen zum Haushaltsvoranschlag anhören. Ein solcher Anhörungsschritt ist im Gesamtprozess nicht ausdrü … |

### Lückenmeldungen v3 B (5 Läufe, dedupliziert je Lauf)

| Regelwerk | Norm | Kategorie | Läufe | Meldungen | Soll-Lücke | Soll-Zuordnung | Beispiel fehlender Schritt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI Act | Art. 27 | luecke_korrekt | 3 | 3 | S15 | – | Vor der ersten Inbetriebnahme des Hochrisiko-KI-Systems eine Grundrechte-Folgenabschätzung durchführen; sie muss unter anderem betroffene Personengruppen, spezi … |
| SGB IX | § 178 | luecke_korrekt | 2 | 2 | S22 | – | Bei Bewerbungen schwerbehinderter Menschen die Schwerbehindertenvertretung vor der Auswahlentscheidung unverzüglich und umfassend unterrichten und anhören sowie … |
| DSGVO | Art. 30 | luecke_neutral | 1 | 1 | – | – | Die Bewerbungsverarbeitung in das schriftliche, gegebenenfalls elektronisch geführte Verzeichnis der Verarbeitungstätigkeiten aufnehmen und die vorgeschriebenen … |
| AI Act | Art. 26 | luecke_an_vorhandener_zuordnung | 3 | 8 | – | S13 | Den Betrieb des KI-Systems anhand der Betriebsanleitung überwachen und bei den gesetzlich beschriebenen Risiken die vorgeschriebenen Meldungen vornehmen sowie d … |
| DSGVO | Art. 13 | luecke_an_vorhandener_zuordnung | 2 | 2 | – | S10 | Bewerberinnen und Bewerber bei Erhebung ihrer Daten über Verantwortlichen, Verarbeitungszwecke und Rechtsgrundlage sowie die weiteren vorgeschriebenen Datenschu … |
| BayPVG | Art. 69 | luecke_ohne_soll | 1 | 1 | – | – | Den Personalrat rechtzeitig und umfassend über die geplante Personalmaßnahme informieren und ihm die hierfür erforderlichen Unterlagen bereitstellen, soweit die … |
| BayPVG | Art. 76 | luecke_ohne_soll | 1 | 1 | – | – | Vor Weiterleitung der Personalanforderung zum Haushaltsvoranschlag den Personalrat anhören; ein solcher Schritt ist im Gesamtprozess nicht ausdrücklich aufgefüh … |

## 5a. Material: Funde `nicht_in_soll` / `luecke_ohne_soll` (manuell prüfen)

Zusammengefasst je Regelwerk + Norm über alle Läufe einer Gruppe; Zitat und Quelle aus dem ersten Fund.

### v1 A (12 Funde, 7 Normen)

| Regelwerk | Norm | Läufe | Funde | Tasks | unsicher | Fundstelle (Beispiel) | Quelle | Zitat Begründung |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BayPVG | Art. 69 | 1 | 3 | T4.2,T4.3,T5.1 | 0% | Art. 69 Abs. 2; Art. 75 Abs. 1 Satz 1 Nr. 1 | https://www.gesetze-bayern.de/Content/Document/BayPVG-69 | Der Personalrat ist zur Durchführung seiner Aufgaben rechtzeitig und umfassend zu unterrichten. Bei der Einstellung besteht grundsätzlich Mitbestimmung. Die genannten Vorschriften begründen nicht ohne … |
| BayPVG | Art. 75 | 1 | 3 | T1.2,T5.1,T5.2 | 33% | Art. 75 Abs. 1 Satz 1 Nr. 3a; Art. 70 Abs. 1 und 2 | https://www.gesetze-bayern.de/Content/Document/BayPVG-75 | Die Eingruppierung ist eine mitbestimmungspflichtige Personalangelegenheit. Soweit die Eingruppierung in T1.2 abschließend festgelegt wird, ist das Verfahren nach Art. 70 zu beachten. Der amtliche Abr … |
| BGB | § 145 | 1 | 2 | T5.2,T5.3 | 0% | § 145; § 147 Abs. 2; § 148; § 150 Abs. 2 | https://www.gesetze-im-internet.de/bgb/BJNR001950896.html | Wird das Vertragsangebot als Antrag abgegeben, ist die Hochschule grundsätzlich daran gebunden, sofern die Bindung nicht ausgeschlossen wird. Für ein Angebot an eine abwesende Person gilt ohne festgel … |
| BGB | § 126 | 1 | 1 | T5.3 | 0% | § 126 Abs. 1 und 2 | https://www.gesetze-im-internet.de/bgb/__126.html | Für die tariflich verlangte Schriftform ist die gesetzliche Schriftform maßgeblich. Sie erfordert grundsätzlich eine eigenhändige Unterschrift; bei einem Vertrag müssen beide Parteien auf derselben Ur … |
| BGB | § 611a | 1 | 1 | T5.2 | 0% | § 611a Abs. 1 und 2 | https://www.gesetze-im-internet.de/bgb/__611a.html | Das Angebot muss die vorgesehene Beschäftigung als Arbeitsverhältnis mit weisungsgebundener Arbeit und vereinbarter Vergütung abbilden. Die Bezeichnung im Angebot ist nicht entscheidend, wenn die tats … |
| BayArchivG | Art. 14 | 1 | 1 | T6.2 | 0% | Art. 14 Abs. 1 und 2 | https://www.gesetze-bayern.de/Content/Document/BayArchivG-14 | Für staatliche Hochschulen und staatlich beaufsichtigte juristische Personen des öffentlichen Rechts sieht Art. 14 je nach Archivierungsmodell eigene Archivierung oder die Anbietung nicht mehr benötig … |
| BayPVG | Art. 76 | 1 | 1 | T1.1 | 100% | Art. 76 Abs. 3 Satz 1 | https://www.gesetze-bayern.de/Content/Document/BayPVG-76 | Die Vorschrift greift bei der Weiterleitung von Personalanforderungen zum Haushaltsvoranschlag. Ob T1.1 eine solche Weiterleitung umfasst, ist aus der Beschreibung nicht ersichtlich. |

### v2 A (143 Funde, 17 Normen)

| Regelwerk | Norm | Läufe | Funde | Tasks | unsicher | Fundstelle (Beispiel) | Quelle | Zitat Begründung |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BayPVG | Art. 75 | 5 | 24 | T1.2,T3.2,T3.4,T4.1,T4.2,T5.1,T5.2,T5.3 | 21% | Art. 75 Abs. 1 Satz 1 Nr. 3a | https://www.gesetze-bayern.de/Content/Document/BayPVG-75 | Der Personalrat hat bei der Eingruppierung mitzubestimmen. Der Prozess enthält zwar die Festlegung der Eingruppierung, benennt aber keine Beteiligung des Personalrats. |
| AI Act | Art. 6 | 5 | 19 | T3.1,T3.2,T3.3,T3.4,T5.1 | 42% | Art. 6 Abs. 2 | https://eur-lex.europa.eu/legal-content/DE/TXT/HTML/?uri=CELEX:02024R1689-20260727 | KI-Systeme für Einstellung oder Auswahl natürlicher Personen sind in Anhang III erfasst. Ein Ranking von Bewerbenden spricht für eine solche Verwendung; die konkrete Einstufung hängt von Funktion und  … |
| BayPVG | Art. 69 | 5 | 13 | T3.4,T4.2,T4.3,T5.1 | 8% | Art. 69 Abs. 2 Satz 1 | https://www.gesetze-bayern.de/Content/Document/BayPVG-69 | Der Personalrat ist zur Aufgabenerfüllung rechtzeitig und umfassend zu unterrichten. Die Gesprächsdokumentation kann hierfür relevant sein, soweit sie für seine Aufgaben und die personalvertretungsrec … |
| BayPVG | Art. 70 | 5 | 11 | T3.1,T3.3,T3.4,T5.1,T5.2,T5.3 | 36% | Art. 70 Abs. 1 Satz 1 | https://www.gesetze-bayern.de/Content/Document/BayPVG/true | Soweit die Einführung oder Anwendung des automatisierten Verfahrens der Mitbestimmung nach Art. 75a BayPVG unterliegt, darf die Maßnahme grundsätzlich erst mit Zustimmung des Personalrats getroffen we … |
| BGB | § 611a | 4 | 8 | T5.2,T5.3 | 0% | § 611a Abs. 1 | https://www.gesetze-im-internet.de/bgb/__611a.html | Der Vertrag begründet ein Arbeitsverhältnis mit weisungsgebundener, fremdbestimmter Arbeit in persönlicher Abhängigkeit; die Regelung beschreibt den arbeitsvertraglichen Rahmen. |
| BayArchivG | Art. 6 | 4 | 6 | T6.2,T6.3 | 17% | Art. 6 Abs. 1 | https://www.gesetze-bayern.de/Content/Document/BayArchivG-6 | Öffentliche Stellen des Freistaates Bayern müssen nicht mehr benötigte Unterlagen grundsätzlich dem zuständigen staatlichen Archiv anbieten; dies umfasst auch Unterlagen mit personenbezogenen Daten. E … |
| ArbGG | § 61b | 4 | 5 | T6.2,T6.3 | 0% | § 61b Abs. 1 | https://www.gesetze-im-internet.de/arbgg/__61b.html | Die Klagefrist kann für die Dauer relevant sein, während der Unterlagen zur Verteidigung gegen einen geltend gemachten Anspruch benötigt werden. |
| BDSG | § 26 | 3 | 39 | T2.1,T2.3,T3.1,T3.2,T3.3,T3.4,T4.2,T4.3,T5.1,T5.2,T5.3,T6.1, … | 10% | § 26 Abs. 1 | https://www.gesetze-im-internet.de/bdsg_2018/__26.html | Bewerbungsdaten werden für die Entscheidung über die Begründung eines Beschäftigungsverhältnisses verarbeitet; Bewerbende sind nach § 26 Abs. 8 Beschäftigte im Sinne dieser Vorschrift. |
| BGB | § 145 | 3 | 3 | T5.2 | 0% | § 145 | https://www.gesetze-im-internet.de/bgb/__145.html | Ein Vertragsangebot ist ein Antrag im Sinne des BGB und bindet den Antragenden grundsätzlich, sofern die Bindung nicht ausgeschlossen ist. |
| BayPVG | Art. 76 | 3 | 3 | T1.1 | 67% | Art. 76 Abs. 3 Satz 1 | https://www.gesetze-bayern.de/Content/Document/BayPVG/true | Art. 76 Abs. 3 Satz 1 BayPVG verlangt vor der Weiterleitung von Personalanforderungen zum Haushaltsvoranschlag die Anhörung des Personalrats. Das kann beim Melden eines Personalbedarfs relevant werden … |
| BGB | § 126 | 2 | 3 | T5.3 | 0% | § 126 Abs. 1 | https://www.gesetze-im-internet.de/bgb/__126.html | Die Schriftform ist für den befristeten Arbeitsvertrag gesetzlich vorgeschrieben und wird durch die in § 126 BGB bestimmten Formanforderungen konkretisiert. |
| AI Act | Art. 113 | 2 | 2 | T3.1,T3.2 | 0% | Art. 113 Abs. 3 Buchst. c Ziff. i | https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/deu | Die Vorschrift legt den für die Anwendung der Hochrisiko-Pflichten maßgeblichen Termin fest und ist für die zeitliche Einordnung des aktuellen KI-Einsatzes entscheidend. |
| BayBGG | Art. 14 | 1 | 2 | T1.3,T2.1 | 0% | Art. 14 Abs. 1 | https://www.gesetze-bayern.de/Content/Document/BayBGG-14 | Art. 14 Abs. 1 erfasst die Internet- und Intranetauftritte sowie IT-Angebote öffentlicher Stellen und bildet die landesgesetzliche Grundlage für deren barrierefreie Gestaltung. ([gesetze-bayern.de](ht … |
| BayDiV | § 9 | 1 | 2 | T1.3,T2.1 | 0% | § 9 Abs. 1 | https://www.gesetze-bayern.de/Content/Document/BayDiV-9 | § 9 Abs. 1 konkretisiert die Anforderungen an barrierefreie IT-Angebote öffentlicher Stellen und gilt auch für Websites und mobile Anwendungen im Sinne der Richtlinie (EU) 2016/2102. ([gesetze-bayern. … |
| AI Act | Art. 111 | 1 | 1 | T3.3 | 0% | Art. 111 Abs. 2 | https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng | Die Organisation ist eine staatliche Hochschule und damit eine öffentliche Stelle; die Übergangsregel wirkt sich auf den zeitlichen Anwendungsstand der Betreiberpflichten aus. |
| BGB | § 147 | 1 | 1 | T5.2 | 0% | § 147 Abs. 2 | https://www.gesetze-im-internet.de/bgb/__147.html | Die Vorschrift bestimmt, bis wann ein an eine abwesende Person gerichtetes Vertragsangebot angenommen werden kann. |
| GG | Art. 3 | 1 | 1 | T3.1 | 0% | Art. 3 Abs. 3 | https://www.gesetze-im-internet.de/gg/art_3.html | Die Hochschule ist als staatliche Stelle an das grundrechtliche Benachteiligungsverbot gebunden, das auch die Auswahl von Bewerbenden begrenzt. |

### v3 A (32 Funde, 9 Normen)

| Regelwerk | Norm | Läufe | Funde | Tasks | unsicher | Fundstelle (Beispiel) | Quelle | Zitat Begründung |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AI Act | Art. 6 | 3 | 3 | T3.1,T3.2,T3.4 | 67% | Art. 6 Abs. 2 | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:02024R1689-20260727#art_6 | KI-Systeme zur Einstellung oder Auswahl natürlicher Personen, insbesondere zum Sichten oder Filtern von Bewerbungen und Bewerten von Bewerbenden, sind grundsätzlich in Anhang III aufgeführt und können … |
| ArbGG | § 61b | 3 | 3 | T6.2 | 0% | § 61b Abs. 1 | https://www.gesetze-im-internet.de/arbgg/__61b.html | Die Klagefrist nach einer schriftlichen Anspruchsanmeldung ist für die Beurteilung relevant, wie lange Bewerbungsunterlagen gegebenenfalls zur Verteidigung gegen einen Anspruch aufbewahrt werden müsse … |
| BDSG | § 26 | 1 | 18 | T2.1,T2.2,T2.3,T3.2,T3.4,T4.3,T5.1,T5.3,T6.2,T6.3 | 11% | § 26 Abs. 1 | https://www.gesetze-im-internet.de/bdsg_2018/__26.html | Die Norm erlaubt erforderliche Datenverarbeitung für die Entscheidung über die Begründung eines Beschäftigungsverhältnisses und erfasst damit auch den Empfang von Bewerbungsunterlagen. |
| BayPVG | Art. 75 | 1 | 2 | T4.2,T5.1 | 100% | Art. 75 Abs. 1 | https://www.gesetze-bayern.de/Content/Document/BayPVG-75 | Der Personalrat hat bei Einstellungen mitzubestimmen. Die Vorstellungsgespräche gehören zum Auswahlverfahren, das der Einstellungsentscheidung vorausgeht; das konkrete Beteiligungsverfahren ist im Pro … |
| GG | Art. 3 | 1 | 2 | T4.2 | 0% | Art. 3 Abs. 2 | https://www.gesetze-im-internet.de/gg/art_3.html | Als staatliche Hochschule muss die Auswahlkommission die Gleichberechtigung von Frauen und Männern beachten und auf die Beseitigung bestehender Nachteile hinwirken. |
| BGB | § 145 | 1 | 1 | T5.2 | 0% | § 145 | https://www.gesetze-im-internet.de/bgb/__145.html | Beim Erstellen eines Vertragsangebots ist zu beachten, dass der Antrag auf Vertragsschluss den Antragenden grundsätzlich bindet. |
| BGB | § 611a | 1 | 1 | T5.2 | 0% | § 611a Abs. 1 | https://www.gesetze-im-internet.de/bgb/__611a.html | Das Angebot betrifft den Abschluss eines Arbeitsvertrags; die Vorschrift beschreibt dessen arbeitsrechtlichen Charakter und grenzt das Arbeitsverhältnis anhand der tatsächlichen Vertragsgestaltung ab. |
| BayPVG | Art. 69 | 1 | 1 | T1.1 | 100% | Art. 69 Abs. 2 Satz 1 und 2 | https://www.gesetze-bayern.de/Content/Document/BayPVG-69 | Das Personalvertretungsgesetz gewährt dem Personalrat für die Durchführung seiner Aufgaben ein Recht auf rechtzeitige und umfassende Unterrichtung samt erforderlichen Unterlagen. Das ist bei der Bedar … |
| BayPVG | Art. 76 | 1 | 1 | T1.1 | 100% | Art. 76 Abs. 3 Satz 1 | https://www.gesetze-bayern.de/Content/Document/BayPVG-76 | Art. 76 Abs. 3 Satz 1 BayPVG verlangt die Anhörung des Personalrats vor der Weiterleitung von Personalanforderungen zum Haushaltsvoranschlag. Da T1.1 eine Bedarfsmeldung betrifft, ist die Vorschrift r … |

### v3 B (17 Funde, 6 Normen)

| Regelwerk | Norm | Läufe | Funde | Tasks | unsicher | Fundstelle (Beispiel) | Quelle | Zitat Begründung |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AI Act | Art. 6 | 4 | 6 | T3.2,T3.3 | 50% | Art. 6 Abs. 2 | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:02024R1689-20260727#art_6 | Die Vorschrift ordnet die in Anhang III genannten KI-Systeme grundsätzlich als Hochrisiko-KI-Systeme ein. Ein KI-System zur Vorauswahl und zum Ranking von Bewerbungen fällt grundsätzlich in den Anwend … |
| GG | Art. 3 | 2 | 3 | T1.2 | 0% | Art. 3 Abs. 2 | https://www.gesetze-im-internet.de/gg/art_3.html | Als staatliche Hochschule muss die Organisation bei der Festlegung des Stellenprofils und der Auswahlvoraussetzungen die Gleichberechtigung von Frauen und Männern beachten und tatsächliche Nachteile v … |
| ArbGG | § 61b | 2 | 2 | T6.2 | 0% | § 61b Abs. 1 | https://www.gesetze-im-internet.de/arbgg/__61b.html | Die Klagefrist kann für die Dauer relevant sein, in der Unterlagen zur Abwehr oder Durchsetzung eines Entschädigungsanspruchs benötigt werden. |
| BayPVG | Art. 69 | 2 | 2 | T1.1 | 100% | Art. 69 Abs. 2 | https://www.gesetze-bayern.de/Content/Document/BayPVG-69 | Der Personalrat ist zur Durchführung seiner Aufgaben rechtzeitig und umfassend zu unterrichten. Ob bereits die Bedarfsmeldung eine solche Information auslöst, hängt davon ab, ob die konkrete Personalm … |
| TzBfG | § 15 | 1 | 3 | T5.3 | 0% | § 15 Abs. 1 | https://www.gesetze-im-internet.de/tzbfg/__15.html | Ein kalendermäßig befristeter Arbeitsvertrag endet mit Ablauf der vereinbarten Zeit. Die Vorschrift ist für die Gestaltung des Endes des auf drei Jahre befristeten Arbeitsverhältnisses relevant. |
| BayPVG | Art. 76 | 1 | 1 | T1.1 | 100% | Art. 76 Abs. 3 | https://www.gesetze-bayern.de/Content/Document/BayPVG | Art. 76 Abs. 3 Satz 1 sieht die Anhörung des Personalrats vor der Weiterleitung von Personalanforderungen zum Haushaltsvoranschlag vor. Das kann bei der Meldung des Personalbedarfs einschlägig sein. |

## 5b. Material: Funde mit nicht existierender Norm (`existiert = nein`)

Geprüft mit `lade_norm` (Cache) auf Ebene Artikel/Paragraf; Absätze werden nicht geprüft.

### v1 A (0 von 200 Funden)

Keine.

### v2 A (0 von 1211 Funden)

Keine.

### v3 A (0 von 432 Funden)

Keine.

### v3 B (0 von 311 Funden)

Keine.

<!-- MANUELL START: alles ab hier bleibt bei erneutem evaluate.py erhalten -->

## Vergleich v2 → v3 (OpenAI-Websuche gegen eigenes Werkzeug)

Stand 21.10.2026. v2 = 5 × A mit OpenAI-Websuche; v3 = 5 × A und 5 × B mit eigenen Werkzeugen. Die Prompts
unterscheiden sich nur in der Quellenregel (v3: Werkzeuge, Pflicht `lade_norm` vor jeder Fundstelle). Alle
Läufe sind gegen dieselbe Soll-Liste ausgewertet. Mittelwert ± Std, n = 5.

| Kennzahl | v2 A | v3 A | v3 B |
| --- | --- | --- | --- |
| Kosten je Lauf (USD, geschätzt) | 1,09 ± 0,03 | **0,059 ± 0,003** | 0,044 ± 0,002 |
| Stufe 1 Recall (Regelwerk) | 98 % ± 4 | 87 % ± 5 | – |
| Stufe 2 Recall | 98 % ± 2 | **66 % ± 8** | 67 % ± 7 |
| Stufe 2 Präzision (ohne neutral) | 54 % ± 3 | 60 % ± 9 | 68 % ± 5 |
| Zuordnungen je Lauf | 209 ± 8 | 84 ± 14 | 59 ± 11 |
| Lücken-Recall streng | 80 % ± 5 | **16 % ± 6** | 11 % ± 0 |
| falsche Lückenmeldungen (dedupliziert) | 4,2 ± 1,3 | 0,8 ± 0,8 | 1,4 ± 0,9 |
| erfundene Normen (Artikel/Paragraf) | 0 | 0 | 0 |

**Kurzfassung:** Das eigene Werkzeug senkt die Kosten um ca. 95 %, verschlechtert aber Vollständigkeit und
Lückenerkennung stark. Die Ursache liegt vor allem im Werkzeug-Setup (Limit 15 je Task, Schwächen der
Regelwerkssuche, siehe 5.2), nicht im Modell. v3 ist in dieser Form **kein gleichwertiger Ersatz** für v2.

**Erkenntnisse aus v2 (bleiben gültig):** Stufe 1 und die Zuordnung waren mit Websuche nahezu vollständig
(Recall 98 %). Der Prompt v2 senkte die falschen Lückenmeldungen gegenüber v1 von 14 auf 4. Dafür gingen
organisatorische Lücken verloren (Art. 4 AI Act 1/5, Art. 78 Abs. 3 BayPVG 1/5), und das Feld `hinweis` wurde fast
immer gefüllt (95 %). BayPVG Art. 75 (Eingruppierung/Einstellung) war die häufigste falsche Lücke.

## 5. Auffälligkeiten (v3)

**5.1 Kosten und Ablauf**

- 10 Läufe ohne technischen Fehler, ohne fehlgeschlagene Tasks und ohne Retry. Die Gesamtkosten von Auftrag 003
  betragen **0,51 USD** (`kosten/verbrauch.csv`, 824 API-Aufrufe), also deutlich unter 3 USD Auftrags- und 5 USD Projektbudget.
- Laufzeit A: 45 → 10 min, je wärmer der Cache wurde. Laufzeit B: 6–8 min. Die Wartezeit liegt fast ganz bei den
  Quellen (1 Anfrage/s je Domain, SPARQL-Abfragen bei Cellar ca. 15–30 s, nur beim ersten Mal).
- Ohne Websuche entfallen 85–90 % der Kosten. Dazu sinkt der Input um ca. 30 %, weil die Werkzeugausgaben
  kürzer sind als die Seiten aus der Websuche.

**5.2 Warum v3 weniger findet**

- **Werkzeuglimit:** In 16–19 von 20 Aufrufen je Lauf wurde das Limit erreicht (Stufe 1: 30, Stufe 2: 15). Das
  Modell muss dann ohne weitere Recherche antworten. Dadurch sinkt die Zahl der Zuordnungen von 209 (v2) auf 84 je Lauf.
- **Ein großer Teil des Limits geht für die Suche nach Regelwerken drauf:** In Stufe 2 sind 48 % (A) bzw. 50 % (B)
  der Aufrufe `suche_regelwerk`, obwohl der Rechtsrahmen vorgegeben ist; nur 30 % (A) bzw. 20 % (B) sind `lade_norm`.
  27 % (A) bzw. 20 % (B) der Suchen bleiben ohne Ergebnis.
- **Schwäche meines Werkzeugs (Bayern-Abkürzungen):** `suche_regelwerk("BayPVG")` und ebenso BayGlG und BayDSG
  liefern „nicht gefunden“ (78-, 68- bzw. 62-mal über alle Läufe). Die Suche von gesetze-bayern.de findet reine
  Abkürzungen nicht. `lade_norm("BayPVG", …)` hätte direkt funktioniert, weil die Abkürzung über die Dokument-URL
  aufgelöst wird; das erkennt das Modell aber nicht. Folge: BayPVG kommt in v3 kaum vor (7 Funde in 10 Läufen),
  S20 (Art. 75a) wird nie erkannt.
- **EU-Abkürzungen:** `lade_norm("DSGVO", …)` und `suche_volltext("DSGVO", …)` scheitern 46- bzw. 46-mal, weil das
  Werkzeug ohne fest eingebaute Liste nur „Verordnung (EU) 2016/679“ auflöst (DECISIONS 41). Das Modell wechselt
  danach meist zur Nummer. Die Fehlversuche kosten aber Aufrufe.
- **Falscher Bund-Treffer:** Bei „SGB IX“ landete das Modell mehrfach beim Slug `sgb9ua_ndg` (einem Änderungsgesetz)
  statt bei `sgb_9_2018`; 21 `lade_norm`-Aufrufe darauf liefen ins Leere. Ursache: Die Titelsuche bevorzugt kurze
  Titel, und für eine Abkürzung liefert `suche_regelwerk` nicht zuerst die direkte Auflösung.
- **Stufe 1 (A):** NachwG fehlt in **allen** 5 Läufen, GG in 2, TzBfG in 1. Zusätzliche Regelwerke
  tauchen teils nur als Slug auf (`bgb`, `bdsg_2018`), weil `suche_regelwerk` für Bundesrecht den Slug statt der
  amtlichen Abkürzung ausgibt.

**5.3 Lücken (H1b)**

- Das Modell meldet kaum noch Lücken (2–4 Meldungen je Lauf). Erkannt werden nur noch S15 (Grundrechte-FA, A 2/5,
  B 3/5), S18 (DSFA, A 3/5) und S22 (Schwerbehindertenvertretung, A 1/5, B 2/5). Die Lückenregel verlangt, vorher
  alle Tasks zu prüfen, und das Limit lässt dafür keinen Raum. Es fehlt also Recherchetiefe. Ein Hinweis auf
  bessere Präzision ist das nicht.
- Der großzügige Lücken-Recall (47 % ± 32 %) streut stark. Er hängt davon ab, ob ein Regelwerk (meist BayPVG
  oder SGB IX) zufällig keinem Task zugeordnet wurde.

**5.4 Erfundene Normen**

- Die Existenzprüfung über `lade_norm` (Ebene Artikel/Paragraf) findet in **keinem** Lauf (v1–v3, 2 154 Funde)
  eine nicht existierende Norm. Nicht prüfbar sind nur 6 Funde zu TV-L-Anlagen (v2).
- **A_2 F080 „AI Act Art. 113 Abs. 3 Buchst. c Ziff. i“:** Art. 113 existiert. Das Modell zitierte die konsolidierte
  Fassung vom 27.07.2026, die auch das Werkzeug nutzt. Ob Abs. 3 mit dieser Gliederung existiert, prüft die
  Auswertung nicht, weil sie keine Absätze prüft.
- In v3 haben 94 % (A) bzw. 91 % (B) der Funde ihre Norm vorher mit `lade_norm` geladen. Die Ausnahmen stammen
  meist aus Aufrufen, bei denen das Limit vor dem Laden erreicht war (z. B. A_8 T5.1: 11 Funde ohne vorheriges Laden).

**5.5 A gegen B: Wie viel des Fehlers stammt aus Stufe 1?**

- Stufe-2-Recall A 66 % ± 8 gegen B 67 % ± 7: Der Unterschied ist kleiner als die Streuung. Der Fehler entsteht
  in v3 fast vollständig in **Stufe 2**, nicht in Stufe 1.
- Einzige klare Ausnahme ist NachwG. Stufe 1 übersieht es in allen A-Läufen, und S28 wird in A nie getroffen (0/5), in B
  in 3/5 Läufen.
- B ist präziser (68 % gegen 60 %) bei weniger Funden (59 gegen 84). Ohne zusätzliche Regelwerke aus Stufe 1
  ordnet das Modell weniger Normen außerhalb der Soll-Liste zu (nicht_in_soll 15 gegen 51 Funde).
- Schwankung zwischen den Läufen: Recall ± 7–8 Pp., deutlich mehr als in v2 (± 2). Das passt dazu, dass das
  Limit die Recherche an zufälligen Stellen abschneidet.

## 6. Technische Probleme

- **EUR-Lex blockt Skripte** (AWS-WAF-Challenge, HTTP 202). EU-Texte kommen über Cellar (`publications.europa.eu`)
  desselben Herausgebers; als Quelle wird die EUR-Lex-URL angegeben (DECISIONS 40). Grenze: Abkürzungen wie DSGVO oder AI Act
  löst das Werkzeug nicht auf, nur Nummern und Titelwörter.
- **gesetze-bayern.de:** Die Suche läuft über ein Formular mit Token und Sitzung (nur seriell). Sie findet Gesetze
  über Titelwörter („Personalvertretung Bayern“ → BayPVG), aber **nicht über reine Abkürzungen** (5.2). Normtexte
  aus der Gesamtansicht funktionieren zuverlässig.
- **gesetze-im-internet.de:** Auflösung über Slug und Titel funktioniert. Grenze: Die Ausgabe ist der Slug (`bgb`,
  `bdsg_2018`), nicht die amtliche Abkürzung. Die Titelsuche kann Änderungsgesetze vor das Stammgesetz stellen
  (`sgb9ua_ndg`).
- **tdl-online.de:** Der TV-L (i. d. F. ÄTV Nr. 14) wird aus dem PDF in Paragrafen zerlegt; Anlagen
  (Entgeltordnung) nicht.
- **Eigene Fehler, behoben:** (1) Der erste v3-Lauf A lief ohne Sitzungs-Lock für die Bayern-Suche. Ich habe ihn
  nach einem Aufruf abgebrochen (0,0004 USD), er liegt in `runs_ungueltig/`. (2) Die Normierung trennte
  „Verordnung (EU) 2016/679“ am Schrägstrich. 21 v3-Funde, die das Modell mit der EU-Nummer statt „DSGVO“ angab,
  galten deshalb als `nicht_in_soll`. Jetzt korrigiert, alle Läufe neu ausgewertet (v3 A Präzision 56 % → 60 %).
- `kosten/verbrauch.csv` protokolliert jeden API-Aufruf. Ein Admin-Key ist nicht gesetzt, daher gibt es keinen
  Abgleich mit der Costs-API.

## 7. Offene Fragen und Annahmen

- Entscheidungen zu v3: `DECISIONS.md`, Punkte 40–55. Die wichtigste ist die Nutzung von Cellar statt
  eur-lex.europa.eu (Punkt 40). Bitte bestätigen, dass das als „Quelle EUR-Lex“ gilt.
- Ein v3-Ergebnis mit dem verbesserten Werkzeug gibt es nicht. Läufe nach einer Werkzeugänderung wären eine
  neue Version und brauchen einen Auftrag.
- Die Existenzprüfung geht nur bis Artikel/Paragraf. Eine Prüfung auf Absätze wäre möglich (Absatznummern im
  geladenen Text), ist aber nicht beauftragt.

## 8. Verbesserungsvorschläge

1. **Werkzeug (Code, mein Bereich, für v4):** `suche_regelwerk` liefert zuerst die direkte Auflösung einer
   Abkürzung (Bund-Slug, Bayern-Dokument), dann die Suchtreffer. Das behebt die Fehlversuche bei
   BayPVG/BayGlG/BayDSG und `sgb9ua_ndg`. Für Bundesrecht wird die amtliche Abkürzung (`jurabk`) statt des Slugs ausgegeben.
2. **Rechtsrahmen mit Kennung übergeben:** Stufe 1 gibt je Regelwerk die Kennung aus dem Werkzeug mit
   (z. B. „Verordnung (EU) 2016/679“ zu DSGVO). Stufe 2 kann dann direkt `lade_norm` aufrufen, statt erneut zu suchen.
   Das spart etwa die Hälfte der Aufrufe in Stufe 2.
3. **Limits erhöhen:** Stufe 2 von 15 auf 30–40 Aufrufe. Bei ca. 0,003 USD je Task und Lauf ist das finanziell unkritisch
   (geschätzt ≤ 0,15 USD je Lauf).
4. **Prompt Stufe 2 (Planungs-Assistent):** Hinweis aufnehmen, Regelwerke des Rechtsrahmens direkt mit
   `lade_norm`/`inhaltsverzeichnis` anzusprechen und `suche_regelwerk` nur für neue Regelwerke zu nutzen; EU-Rechtsakte
   als „Verordnung (EU) JJJJ/NNNN“.
5. **Soll-Liste:** Weiter offen aus v2: BayPVG Art. 75 (Eingruppierung) für wiss. Personal fachlich klären;
   BayArchivG Art. 6 / Art. 26 BayDSG (Anbietungspflicht vor Löschung) als neutral prüfen.
6. **Vorschlag für den nächsten Auftrag:** v4 = v3 + Vorschläge 1–4, je 5 × A und 5 × B (geschätzt ≤ 1,50 USD
   gesamt). Ziel: Recall und Lückenerkennung von v2 bei Kosten von v3.

<!-- MANUELL ENDE -->
