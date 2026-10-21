# ERGEBNIS H1 (inkl. H1b)

Automatisch erzeugt von `python -m src.evaluate` (Abschnitte 1–4 und Material 5a). Alle Läufe sind gegen die **aktuelle** Soll-Liste ausgewertet und nach (`version`, `konfig`) gruppiert; Werte = Mittelwert ± Standardabweichung über die Läufe. Abschnitte 5–8 unten sind manuell gepflegt. Begriffe: `README.md`, `DECISIONS.md`. Details je Lauf: `results/kennzahlen.csv`, `funde_bewertet.csv`, `luecken_bewertet.csv`, `uebersehen.csv`.

## 1. Lauf-Metadaten

| run_id | Version | Konfig | Modell-Snapshot | reasoning_effort | Dauer | Tokens in | Tokens out | Websuchen | Kosten USD (geschätzt) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20261020-145929_A_1 | v1 | A | `gpt-6-luna` | medium | 9 min 19 s | 922 889 | 111 545 | 95 | 1.0923 | ok |
| 20261021-094308_A_2 | v2 | A | `gpt-6-luna` | medium | 5 min 51 s | 886 828 | 123 339 | 95 | 1.0947 | ok |
| 20261021-094923_A_3 | v2 | A | `gpt-6-luna` | medium | 5 min 43 s | 866 917 | 116 962 | 91 | 1.0482 | ok |
| 20261021-095507_A_4 | v2 | A | `gpt-6-luna` | medium | 5 min 19 s | 920 122 | 117 443 | 94 | 1.0839 | ok |
| 20261021-100026_A_5 | v2 | A | `gpt-6-luna` | medium | 6 min 57 s | 919 326 | 119 993 | 97 | 1.1153 | ok |
| 20261021-100724_A_6 | v2 | A | `gpt-6-luna` | medium | 6 min 4 s | 923 271 | 120 465 | 97 | 1.1159 | ok |

### Übersicht je (version, konfig)

| Kennzahl | v1 A (n=1) | v2 A (n=5) |
| --- | --- | --- |
| Stufe 1 Recall (Regelwerk) | 100% | 98% ± 4% |
| Stufe 1 Präzision (Regelwerk) | 92% | 83% ± 11% |
| Stufe 2 Recall (Fundstelle) | 70% | 98% ± 2% |
| Stufe 2 Präzision (ohne neutral) | 58% | 54% ± 3% |
| Stufe 2 Anteil neutral | 28% | 24% ± 6% |
| Stufe 2 Recall inkl. Lückenmeldungen am Soll-Task | 91% | 98% ± 2% |
| Stufe 2 Anzahl Funde (zuordnung) | 120.0 | 209.4 ± 8.3 |
| H1b Lücken-Recall (streng) | 100% | 80% ± 5% |
| H1b Lücken-Recall (großzügig) | 100% | 80% ± 5% |
| H1b Lückenmeldungen (Funde) | 80.0 | 32.8 ± 6.6 |
| H1b Lückenmeldungen (dedupliziert) | 31.0 | 13.0 ± 0.7 |
| H1b falsche Lückenmeldungen (dedupliziert) | 14.0 | 4.2 ± 1.3 |
| H1b Kontrolle: Fehlmeldungen S23 | 1.0 | 0.4 ± 0.5 |
| Anteil Zuordnungen mit Hinweis | 0% | 95% ± 1% |
| Anteil unsicher | 26% | 15% ± 4% |
| Anteil nicht_in_soll / luecke_ohne_soll | 6% | 12% ± 5% |
| Tokens Input | 922 889 | 903 293 ± 25 168 |
| Tokens Output | 111 545 | 119 640 ± 2 573 |
| Websuchen | 95.0 | 94.8 ± 2.5 |
| Kosten USD (geschätzt) | 1.092 | 1.092 ± 0.028 |

## 2. Stufe 1 – Rechtsrahmen

Soll-Regelwerke = Regelwerke aus Zeilen mit `typ` zuordnung oder luecke. Regelwerke, die nur in Neutral-Zeilen stehen, zählen als „neutral“ (nicht als zusätzlich, nicht in der Präzision). Konfiguration B hat keine Stufe 1.

| Kennzahl | v1 A (n=1) | v2 A (n=5) |
| --- | --- | --- |
| Recall | 100% | 98% ± 4% |
| Präzision | 92% | 83% ± 11% |

In wie vielen Läufen hat Stufe 1 das Regelwerk genannt:

| Regelwerk | Status | v1 A | v2 A |
| --- | --- | --- | --- |
| GG | Soll | 1/1 | 5/5 |
| AGG | Soll | 1/1 | 5/5 |
| TV-L | Soll | 1/1 | 5/5 |
| SGB IX | Soll | 1/1 | 5/5 |
| BayGlG | Soll | 1/1 | 5/5 |
| DSGVO | Soll | 1/1 | 5/5 |
| BayDSG | Soll | 1/1 | 5/5 |
| AI Act | Soll | 1/1 | 5/5 |
| BayPVG | Soll | 1/1 | 5/5 |
| NachwG | Soll | 1/1 | 4/5 |
| WissZeitVG | Soll | 1/1 | 5/5 |
| TzBfG | Soll | 1/1 | 5/5 |
| BayHIG | neutral | 1/1 | 5/5 |
| BDSG | zusätzlich | 0/1 | 3/5 |
| BGB | zusätzlich | 1/1 | 5/5 |
| BayArchivG | zusätzlich | 0/1 | 1/5 |
| BayBGG | zusätzlich | 0/1 | 1/5 |
| BayDiV | zusätzlich | 0/1 | 1/5 |
| EntgTranspG | zusätzlich | 0/1 | 1/5 |
| Richtlinie (EU) 2016/2102 | zusätzlich | 0/1 | 1/5 |

## 3. Stufe 2 – Zuordnung je Task

Bewertet werden Funde mit `typ = zuordnung`. Präzision = korrekt / (korrekt + falscher_absatz + falscher_task + nicht_in_soll); `neutral` geht nicht ein und wird separat ausgewiesen. Teilprozess einer Soll-Zeile mit mehreren Tasks = Teilprozess des ersten Tasks.

| Kennzahl | v1 A (n=1) | v2 A (n=5) |
| --- | --- | --- |
| Funde (zuordnung) | 120.0 | 209.4 ± 8.3 |
| davon korrekt | 50.0 | 85.6 ± 5.0 |
| davon neutral | 34.0 | 50.4 ± 11.7 |
| davon falscher_absatz | 0.0 | 0.0 ± 0.0 |
| davon falscher_task | 32.0 | 51.0 ± 4.1 |
| davon nicht_in_soll | 4.0 | 22.4 ± 11.3 |
| Recall gesamt | 70% | 98% ± 2% |
| Präzision gesamt | 58% | 54% ± 3% |
| Anteil neutral | 28% | 24% ± 6% |
| Recall inkl. Lückenmeldungen am Soll-Task | 91% | 98% ± 2% |
| Recall TP1 | 50% | 100% ± 0% |
| Recall TP2 | 67% | 100% ± 0% |
| Recall TP3 | 75% | 100% ± 0% |
| Recall TP4 | 50% | 95% ± 11% |
| Recall TP5 | 100% | 93% ± 15% |
| Recall TP6 | 50% | 100% ± 0% |
| Recall GESAMT | 100% | 100% ± 0% |
| Präzision TP1 | 100% | 82% ± 10% |
| Präzision TP2 | 89% | 72% ± 12% |
| Präzision TP3 | 46% | 47% ± 3% |
| Präzision TP4 | 67% | 55% ± 10% |
| Präzision TP5 | 58% | 53% ± 7% |
| Präzision TP6 | 40% | 31% ± 5% |

Je Lauf:

| run_id | Version | Konfig | Funde | korrekt | neutral | falscher_absatz | falscher_task | nicht_in_soll | Recall | Präzision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20261020-145929_A_1 | v1 | A | 120 | 50 | 34 | 0 | 32 | 4 | 70% | 58% |
| 20261021-094308_A_2 | v2 | A | 200 | 78 | 64 | 0 | 46 | 12 | 96% | 57% |
| 20261021-094923_A_3 | v2 | A | 220 | 91 | 59 | 0 | 55 | 15 | 100% | 57% |
| 20261021-095507_A_4 | v2 | A | 209 | 86 | 52 | 0 | 55 | 16 | 100% | 55% |
| 20261021-100026_A_5 | v2 | A | 203 | 84 | 39 | 0 | 48 | 32 | 96% | 51% |
| 20261021-100724_A_6 | v2 | A | 215 | 89 | 38 | 0 | 51 | 37 | 100% | 50% |

In wie vielen Läufen wurde die Soll-Zuordnung korrekt getroffen:

| Soll | Regelwerk | Fundstelle | Task(s) | v1 A (n=1) | v2 A (n=5) |
| --- | --- | --- | --- | --- | --- |
| S01 | GG | Art. 33 Abs. 2 | GESAMT | 1/1 | 5/5 |
| S02 | AGG | § 7 | GESAMT | 1/1 | 5/5 |
| S03 | AGG | § 11 | T1.3 | 0/1 | 5/5 |
| S04 | TV-L | – | T1.2 | 0/1 | 5/5 |
| S07 | BayGlG | – | T1.2|T1.3 | 1/1 | 5/5 |
| S08 | DSGVO | Art. 6 | T2.1|T2.3 | 1/1 | 5/5 |
| S09 | BayDSG | – | T2.1|T2.3 | 1/1 | 5/5 |
| S10 | DSGVO | Art. 13 | T2.1|T2.2 | 0/1 | 5/5 |
| S11 | DSGVO | Art. 32 | GESAMT | 1/1 | 5/5 |
| S12 | AI Act | Anhang III Nr. 4 | T3.1|T3.2 | 1/1 | 5/5 |
| S13 | AI Act | Art. 26 | T3.1|T3.2|T3.3|T3.4 | 1/1 | 5/5 |
| S17 | DSGVO | Art. 22 | T3.4|T5.1 | 0/1 | 5/5 |
| S19 | AGG | – | T3.1|T3.2 | 1/1 | 5/5 |
| S21 | SGB IX | § 165 | T4.1 | 0/1 | 5/5 |
| S23 | BayGlG | Art. 17 | T4.1|T4.2 | 0/1 | 5/5 |
| S24 | AGG | – | T4.2 | 1/1 | 5/5 |
| S25 | DSGVO | Art. 5 Abs. 2 | T4.3|T6.2 | 1/1 | 4/5 |
| S27 | TV-L | – | T5.2|T5.3 | 1/1 | 5/5 |
| S28 | NachwG | – | T5.2|T5.3 | 1/1 | 4/5 |
| S29 | AGG | § 15 Abs. 4 | T6.2 | 0/1 | 5/5 |
| S30 | DSGVO | Art. 17 | T6.3 | 1/1 | 5/5 |
| S46 | WissZeitVG | § 2 | T1.2|T5.2|T5.3 | 1/1 | 5/5 |
| S47 | TzBfG | § 14 Abs. 4 | T5.2|T5.3 | 1/1 | 5/5 |

## 4. H1b – Lückenkandidaten

Kategorien je Lückenmeldung (`typ = moegliche_luecke`), dedupliziert nach Regelwerk + Artikel/Paragraf: `luecke_korrekt` (trifft Soll-Lücke), `luecke_neutral` (trifft Neutral-Zeile), `luecke_an_vorhandener_zuordnung` (trifft nur eine Soll-Zuordnung), `luecke_ohne_soll` (trifft nichts). Falsch = die beiden letzten. Lücken-Recall streng = nur Lückenmeldungen; großzügig = zusätzlich Regelwerke aus Stufe 1 (B: Vorgabe) ohne Zuordnung. Kontrolle = Lückenmeldungen, die S23 (Gleichstellungsbeauftragte, vorhandener Schritt) treffen.

| Kennzahl | v1 A (n=1) | v2 A (n=5) |
| --- | --- | --- |
| Lücken-Recall streng | 100% | 80% ± 5% |
| Lücken-Recall großzügig | 100% | 80% ± 5% |
| Lückenmeldungen (Funde) | 80.0 | 32.8 ± 6.6 |
| Lückenmeldungen (dedupliziert) | 31.0 | 13.0 ± 0.7 |
| davon luecke_korrekt | 9.0 | 7.2 ± 0.4 |
| davon luecke_neutral | 8.0 | 1.6 ± 0.9 |
| davon luecke_an_vorhandener_zuordnung | 10.0 | 1.2 ± 0.8 |
| davon luecke_ohne_soll | 4.0 | 3.0 ± 0.7 |
| falsche Lückenmeldungen | 14.0 | 4.2 ± 1.3 |
| Kontrolle: Fehlmeldungen S23 | 1.0 | 0.4 ± 0.5 |
| Regelwerke ohne Zuordnung | 1.0 | 0.8 ± 0.8 |

In wie vielen Läufen wurde die Soll-Lücke erkannt (streng):

| Soll-Lücke | Regelwerk | Fundstelle | Inhalt | v1 A (n=1) | v2 A (n=5) |
| --- | --- | --- | --- | --- | --- |
| S05 | SGB IX | § 164 | Prüfung Besetzung freier Stellen mit schwerbehinderten Menschen, Beteiligung der … | 1/1 | 5/5 |
| S06 | SGB IX | § 165 | Meldung freier Stellen an die Agentur für Arbeit (öffentlicher Arbeitgeber, Satz … | 1/1 | 4/5 |
| S14 | AI Act | Art. 26 Abs. 11 | Information der Betroffenen über den KI-Einsatz | 1/1 | 5/5 |
| S15 | AI Act | Art. 27 | Grundrechte-Folgenabschätzung (öffentliche Stelle) | 1/1 | 5/5 |
| S16 | AI Act | Art. 4 | KI-Kompetenz der Mitarbeitenden | 1/1 | 1/5 |
| S18 | DSGVO | Art. 35 | Datenschutz-Folgenabschätzung | 1/1 | 5/5 |
| S20 | BayPVG | Art. 75a | Mitbestimmung Personalrat bei Einführung/Anwendung des KI-Tools (Abs. 1 Nr. 2, a … | 1/1 | 5/5 |
| S22 | SGB IX | § 178 | Beteiligung der Schwerbehindertenvertretung | 1/1 | 5/5 |
| S26 | BayPVG | Art. 78 Abs. 3 | Mitteilung an den Personalrat über die Einstellung (Mitbestimmung nach Art. 78 A … | 1/1 | 1/5 |

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

<!-- MANUELL START: alles ab hier bleibt bei erneutem evaluate.py erhalten -->

> **Stand 21.10.2026, Auftrag 002 blockiert:** 5 × A (v2) sind fertig. Die Läufe B brachen ab, weil das
> OpenAI-Guthaben aufgebraucht war (`429 insufficient_quota / credit_balance_exhausted`). Die Abschnitte 5–8 sind
> daher **vorläufig und betreffen nur A**. Den Vergleich A gegen B (Fehleranteil Stufe 1) ergänze ich nach den B-Läufen.

## Abbruch und weiteres Vorgehen (Stand 21.10.2026)

**Abbruch:** Während der B-Läufe war das OpenAI-Guthaben aufgebraucht (`429 insufficient_quota /
credit_balance_exhausted`). 5 × A (v2) sind vollständig und ausgewertet. Die angefangenen B-Läufe liegen in
`h1/runs_ungueltig/` und gehen nicht in die Auswertung ein. Auftrag 002 steht auf `blockiert`.

**Vorläufige Schlüsse (nur A, n = 5; Mittelwert ± Std):**

1. **Stufe 1 funktioniert:** Recall 98 % ± 4 %. Alle Soll-Regelwerke wurden in jedem Lauf gefunden, nur NachwG
   fehlte einmal. Präzision 83 % ± 11 %; die zusätzlichen Regelwerke sind meist plausibel, falsch ist keines.
2. **Stufe 2 ist vollständig, aber breit:** Recall 98 % ± 2 %, Präzision ohne neutral 54 % ± 3 %. Das Modell
   ordnet Normen eher zu vielen Tasks zu als zu wenigen.
3. **H1b gelingt teilweise:** Lücken-Recall 80 % ± 5 %. Die bekannten Lücken (DSFA, Grundrechte-Folgenabschätzung,
   Information über den KI-Einsatz, Schwerbehindertenvertretung, Personalrat beim KI-Tool) werden sicher erkannt.
   Unsicher sind organisatorische Voraussetzungen (Art. 4 AI Act, 1/5) und Sonderregeln (Art. 78 BayPVG, 1/5).
4. **Der Prompt ist der Hebel:** Von v1 auf v2 fallen die falschen Lückenmeldungen von 14 auf 4,2 ± 1,3, der
   Lücken-Recall sinkt von 100 % auf 80 %. Präziser fordern und vollständig erkennen ziehen gegeneinander.

**Noch offen:**

- Wie viel des Fehlers aus Stufe 1 stammt (A gegen B). Erwartung: wenig Unterschied, weil Stufe 1 fast alle
  Regelwerke findet. Belegt ist das erst mit B.
- Systematische Prüfung auf erfundene Normen (offen: A_2 F080, Art. 113 Abs. 3 AI Act).
- Vorbehalte für die Arbeit: Mit n = 5 ist die Streuung nur grob geschätzt. Die Soll-Liste wurde nach A_1
  angepasst, teils dort, wo das Modell recht hatte; die v2-Werte sind dadurch tendenziell zu günstig. Eine
  fachliche Prüfung der Soll-Liste durch Dritte wäre sinnvoll.

**Weiteres Vorgehen (Optionen für den Planungs-Assistenten):**

- **Option A – Auftrag 002 abschließen:** Guthaben aufladen, voraussichtlich ca. 6,50 USD für 5 × B (B_1 kostete
  1,26 USD für 18 von 19 Tasks; ca. 85–90 % davon Websuche, Preis 10 USD/1000 nur angenommen). Empfehlung:
  ca. 10 USD mit Puffer. Danach `--konfig B --laeufe 5`, Auswertung, Abschnitte 5–8 final und Vergleich A/B.
- **Option B – zuerst Prompt v3, dann A und B gemeinsam:** Die Vorschläge 8.1/8.2 (Lückenregel für
  organisatorische Voraussetzungen, `hinweis` schärfen) zuerst umsetzen und dann A und B in v3 laufen lassen.
  Vorteil: A und B laufen mit demselben Prompt-Stand. Kosten ca. 12 USD für 5 × A + 5 × B.
- **In beiden Fällen vorher (kleine Code-Änderung):** Bei `insufficient_quota` den Lauf sofort abbrechen, statt
  mit fehlenden Tasks weiterzulaufen (siehe Abschnitt 6).

## 5. Auffälligkeiten (vorläufig, nur A)

**Vergleich v1 → v2** (A_1 mit v1-Prompt gegen 5 × A mit v2-Prompt; beide gegen die neue Soll-Liste ausgewertet).
A_1 lief noch **ohne Befristung** im Firmenprofil. Trotzdem fand es WissZeitVG und TzBfG in Stufe 1, und S46/S47
werden auch in A_1 getroffen.

- **Stufe-2-Recall 70 % → 98 % ± 2 %.** Den größten Teil bringt der Prompt: In v1 wurden S10, S17 und S21 nur
  als Lücke gemeldet (Recall inkl. dieser Meldungen in A_1: 91 %). Mit dem neuen Feld `hinweis` landen sie als
  `zuordnung` am richtigen Task. Die neue Soll-Liste (mehrere Tasks, `GESAMT`) macht viele frühere
  `falscher_task`-Funde korrekt. Daher steigt die Präzision von A_1 schon allein durch die Soll-Liste von 22 % (v1-Auswertung) auf 58 %.
  v2 liegt bei 54 % ± 3 %, 24 % der Zuordnungen sind neutral.
- **Lückenmeldungen sinken stark:** 80 → 33 ± 7 Funde, dedupliziert 31 → 13 ± 1; falsche Lückenmeldungen
  14 → 4,2 ± 1,3. `luecke_an_vorhandener_zuordnung` fällt von 10 auf 1,2.
- **Dabei gehen echte Lücken verloren:** Der Lücken-Recall (streng) fällt von 100 % auf 80 % ± 5 %. Verloren gehen
  vor allem **S16 (Art. 4 AI Act, KI-Kompetenz, 1/5 Läufe)** und **S26 (Art. 78 Abs. 3 BayPVG, 1/5)**, dazu
  S06 in 1 von 5 Läufen. Art. 4 AI Act nennt das Modell meist als `zuordnung` mit `hinweis` an T3.1/T3.3, statt
  eine fehlende Schulung als eigenen Prozessschritt zu melden. Das ist eine Folge der Prompt-Regel „nur wenn KEIN
  Task den Schritt abdeckt“.
- **BayPVG Art. 75 statt 78:** Der häufigste Fehler bei den Lücken ist `luecke_ohne_soll` BayPVG Art. 75
  (5/5 Läufe, 16 Meldungen): Mitbestimmung bei Eingruppierung bzw. Einstellung. Dazu kommt Art. 70 (Verfahren der Mitbestimmung, 4/5).
  Die Ausnahme in Art. 78 Abs. 1 Satz 1 Nr. 6 für wissenschaftliches Personal (in A_1 erkannt) nennen nur 2 von 5
  v2-Läufen: A_3 meldet Art. 78 Abs. 3 als Lücke, A_4 nennt Art. 78 Abs. 1 Satz 1 Nr. 6 als `zuordnung` an T5.3 mit Hinweis.
- **Kontrolle Gleichstellungsbeauftragte:** 0,4 ± 0,5 Fehlmeldungen zu S23 (v1: 1). Mit der Umformulierung von
  T4.1/T4.2 meldet das Modell den Hinweis auf das Antragsrecht kaum noch als fehlend.
- **`hinweis` wird fast immer gefüllt (95 %):** Das Feld enthält meist Prüf- oder Dokumentationshinweise, nicht nur
  echte Lücken im Task. Als Signal für „Detail fehlt“ ist es deshalb kaum trennscharf.
- **Schwankung zwischen den Läufen:** gering bei Recall (± 2–5 Pp.) und Kosten (± 0,03 USD), deutlicher bei der
  Stufe-1-Präzision (83 % ± 11 %). Zusätzliche Regelwerke wechseln von Lauf zu Lauf: BGB 5/5, BDSG 3/5, BayArchivG,
  BayBGG, BayDiV, EntgTranspG und RL (EU) 2016/2102 je 1/5. NachwG fehlte in 1 von 5 Läufen.
- **Mögliche erfundene Normen:** Systematisch geprüft ist das noch nicht. Eine Stichprobe ist auffällig:
  A_2 F080 *„AI Act Art. 113 Abs. 3 Buchst. c Ziff. i“* (Quelle: konsolidierte Fassung 2024/1689 vom 27.07.2026).
  In der Ursprungsfassung hat Art. 113 keinen Abs. 3. Ob eine Änderungsverordnung ihn eingefügt hat, prüfe ich
  zusammen mit den B-Läufen. Neu tauchen außerdem `BDSG § 26` (für Landesbehörden nicht anwendbar, BayDSG gilt) und
  `ArbGG § 61b` (Klagefrist bei AGG-Entschädigung; fachlich plausibel für T6.2) auf.

## 6. Technische Probleme

- **5 × A (v2) ohne Fehler:** keine Retries, keine fehlgeschlagenen Tasks; je ca. 5–7 min, 1,09 ± 0,03 USD.
- **OpenAI-Guthaben aufgebraucht (Blocker):** Ab Lauf B_1 (20261021-101333) lieferte die API
  `429 insufficient_quota / credit_balance_exhausted`. B_1 fehlt T5.3, B_2 ist komplett leer, B_3 wurde von mir
  abgebrochen. Ich habe die drei Ordner nach `h1/runs_ungueltig/` verschoben, damit sie nicht ausgewertet werden.
  Schwäche im Code: `insufficient_quota` wird wie ein Rate-Limit wiederholt, und der Lauf läuft mit fehlenden Tasks weiter.
  Vorschlag: bei `insufficient_quota` sofort abbrechen.
- Verbraucht in Auftrag 002 bisher ca. 5,5 USD (A) + 1,26 USD (B_1, unvollständig).

## 7. Offene Fragen und Annahmen

- Entscheidungen zur v2-Auswertung: `DECISIONS.md`, Punkte 25–39. Die wichtigsten: Neutral steht vor
  „Lücke an vorhandener Zuordnung“. Den Absatz prüft die Lückenbewertung nur, wenn beide Seiten einen nennen.
  „Regelwerk ohne Zuordnung“ zählt nicht mehr als falsche Lückenmeldung.
- Fortsetzung: Nach dem Aufladen des Guthabens 5 × B neu starten (`--konfig B --laeufe 5`). Die Nummerierung
  beginnt wieder bei B_1, weil `naechste_lauf_nr` nur `runs/` sieht. Die run_ids bleiben durch den Zeitstempel eindeutig.

## 8. Verbesserungsvorschläge (vorläufig)

1. **Prompt Stufe 2, Lückenregel:** Organisatorische Voraussetzungen ohne eigenen Task (Schulung, Folgenabschätzung,
   Beteiligung von Gremien) ausdrücklich als `moegliche_luecke` nennen, auch wenn ein Task thematisch berührt ist. So
   kommen S16/S26 zurück.
2. **Feld `hinweis` schärfen:** „nur, wenn am Task tatsächlich ein Detail fehlt; allgemeine Prüfhinweise → null“.
3. **Soll-Liste:** BayPVG Art. 75 Abs. 1 (Eingruppierung) für wiss. Personal fachlich klären. Wenn Art. 78 Abs. 1
   Nr. 6 auch die Eingruppierung ausnimmt, bleibt die Meldung falsch; andernfalls wäre es eine weitere Soll-Lücke.
   BayArchivG Art. 6 / Art. 26 BayDSG (Anbietungspflicht vor Löschung, 4/5 Läufe) als neutral oder als Soll-Lücke prüfen.
4. **Code:** Abbruch bei `insufficient_quota` (siehe Abschnitt 6).

<!-- MANUELL ENDE -->
