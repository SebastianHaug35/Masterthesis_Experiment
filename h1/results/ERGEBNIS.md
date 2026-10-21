# ERGEBNIS H1 (inkl. H1b)

Automatisch erzeugt von `python -m src.evaluate` (Abschnitte 1–4 und Material 5a). Alle Läufe sind gegen die **aktuelle** Soll-Liste ausgewertet und nach (`version`, `konfig`) gruppiert; Werte = Mittelwert ± Standardabweichung über die Läufe. Abschnitte 5–8 unten sind manuell gepflegt. Begriffe: `README.md`, `DECISIONS.md`. Details je Lauf: `results/kennzahlen.csv`, `funde_bewertet.csv`, `luecken_bewertet.csv`, `uebersehen.csv`.

## 1. Lauf-Metadaten

| run_id | Version | Konfig | Modell-Snapshot | reasoning_effort | Dauer | Tokens in | Tokens out | Websuchen | Kosten USD (geschätzt) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20261020-145929_A_1 | v1 | A | `gpt-6-luna` | medium | 9 min 19 s | 922 889 | 111 545 | 95 | 1.0923 | ok |
| 20261021-094308_A_2 | v2 | A | `gpt-6-luna` | medium | 5 min 51 s | 886 828 | 123 339 | 95 | 1.0947 | ok |

### Übersicht je (version, konfig)

| Kennzahl | v1 A (n=1) | v2 A (n=1) |
| --- | --- | --- |
| Stufe 1 Recall (Regelwerk) | 100% | 100% |
| Stufe 1 Präzision (Regelwerk) | 92% | 92% |
| Stufe 2 Recall (Fundstelle) | 70% | 96% |
| Stufe 2 Präzision (ohne neutral) | 58% | 57% |
| Stufe 2 Anteil neutral | 28% | 32% |
| Stufe 2 Recall inkl. Lückenmeldungen am Soll-Task | 91% | 96% |
| Stufe 2 Anzahl Funde (zuordnung) | 120.0 | 200.0 |
| H1b Lücken-Recall (streng) | 100% | 78% |
| H1b Lücken-Recall (großzügig) | 100% | 78% |
| H1b Lückenmeldungen (Funde) | 80.0 | 28.0 |
| H1b Lückenmeldungen (dedupliziert) | 31.0 | 13.0 |
| H1b falsche Lückenmeldungen (dedupliziert) | 14.0 | 4.0 |
| H1b Kontrolle: Fehlmeldungen S23 | 1.0 | 1.0 |
| Anteil Zuordnungen mit Hinweis | 0% | 94% |
| Anteil unsicher | 26% | 18% |
| Anteil nicht_in_soll / luecke_ohne_soll | 6% | 8% |
| Tokens Input | 922 889 | 886 828 |
| Tokens Output | 111 545 | 123 339 |
| Websuchen | 95.0 | 95.0 |
| Kosten USD (geschätzt) | 1.092 | 1.095 |

## 2. Stufe 1 – Rechtsrahmen

Soll-Regelwerke = Regelwerke aus Zeilen mit `typ` zuordnung oder luecke. Regelwerke, die nur in Neutral-Zeilen stehen, zählen als „neutral“ (nicht als zusätzlich, nicht in der Präzision). Konfiguration B hat keine Stufe 1.

| Kennzahl | v1 A (n=1) | v2 A (n=1) |
| --- | --- | --- |
| Recall | 100% | 100% |
| Präzision | 92% | 92% |

In wie vielen Läufen hat Stufe 1 das Regelwerk genannt:

| Regelwerk | Status | v1 A | v2 A |
| --- | --- | --- | --- |
| GG | Soll | 1/1 | 1/1 |
| AGG | Soll | 1/1 | 1/1 |
| TV-L | Soll | 1/1 | 1/1 |
| SGB IX | Soll | 1/1 | 1/1 |
| BayGlG | Soll | 1/1 | 1/1 |
| DSGVO | Soll | 1/1 | 1/1 |
| BayDSG | Soll | 1/1 | 1/1 |
| AI Act | Soll | 1/1 | 1/1 |
| BayPVG | Soll | 1/1 | 1/1 |
| NachwG | Soll | 1/1 | 1/1 |
| WissZeitVG | Soll | 1/1 | 1/1 |
| TzBfG | Soll | 1/1 | 1/1 |
| BayHIG | neutral | 1/1 | 1/1 |
| BGB | zusätzlich | 1/1 | 1/1 |

## 3. Stufe 2 – Zuordnung je Task

Bewertet werden Funde mit `typ = zuordnung`. Präzision = korrekt / (korrekt + falscher_absatz + falscher_task + nicht_in_soll); `neutral` geht nicht ein und wird separat ausgewiesen. Teilprozess einer Soll-Zeile mit mehreren Tasks = Teilprozess des ersten Tasks.

| Kennzahl | v1 A (n=1) | v2 A (n=1) |
| --- | --- | --- |
| Funde (zuordnung) | 120.0 | 200.0 |
| davon korrekt | 50.0 | 78.0 |
| davon neutral | 34.0 | 64.0 |
| davon falscher_absatz | 0.0 | 0.0 |
| davon falscher_task | 32.0 | 46.0 |
| davon nicht_in_soll | 4.0 | 12.0 |
| Recall gesamt | 70% | 96% |
| Präzision gesamt | 58% | 57% |
| Anteil neutral | 28% | 32% |
| Recall inkl. Lückenmeldungen am Soll-Task | 91% | 96% |
| Recall TP1 | 50% | 100% |
| Recall TP2 | 67% | 100% |
| Recall TP3 | 75% | 100% |
| Recall TP4 | 50% | 75% |
| Recall TP5 | 100% | 100% |
| Recall TP6 | 50% | 100% |
| Recall GESAMT | 100% | 100% |
| Präzision TP1 | 100% | 91% |
| Präzision TP2 | 89% | 79% |
| Präzision TP3 | 46% | 47% |
| Präzision TP4 | 67% | 47% |
| Präzision TP5 | 58% | 64% |
| Präzision TP6 | 40% | 31% |

Je Lauf:

| run_id | Version | Konfig | Funde | korrekt | neutral | falscher_absatz | falscher_task | nicht_in_soll | Recall | Präzision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20261020-145929_A_1 | v1 | A | 120 | 50 | 34 | 0 | 32 | 4 | 70% | 58% |
| 20261021-094308_A_2 | v2 | A | 200 | 78 | 64 | 0 | 46 | 12 | 96% | 57% |

In wie vielen Läufen wurde die Soll-Zuordnung korrekt getroffen:

| Soll | Regelwerk | Fundstelle | Task(s) | v1 A (n=1) | v2 A (n=1) |
| --- | --- | --- | --- | --- | --- |
| S01 | GG | Art. 33 Abs. 2 | GESAMT | 1/1 | 1/1 |
| S02 | AGG | § 7 | GESAMT | 1/1 | 1/1 |
| S03 | AGG | § 11 | T1.3 | 0/1 | 1/1 |
| S04 | TV-L | – | T1.2 | 0/1 | 1/1 |
| S07 | BayGlG | – | T1.2|T1.3 | 1/1 | 1/1 |
| S08 | DSGVO | Art. 6 | T2.1|T2.3 | 1/1 | 1/1 |
| S09 | BayDSG | – | T2.1|T2.3 | 1/1 | 1/1 |
| S10 | DSGVO | Art. 13 | T2.1|T2.2 | 0/1 | 1/1 |
| S11 | DSGVO | Art. 32 | GESAMT | 1/1 | 1/1 |
| S12 | AI Act | Anhang III Nr. 4 | T3.1|T3.2 | 1/1 | 1/1 |
| S13 | AI Act | Art. 26 | T3.1|T3.2|T3.3|T3.4 | 1/1 | 1/1 |
| S17 | DSGVO | Art. 22 | T3.4|T5.1 | 0/1 | 1/1 |
| S19 | AGG | – | T3.1|T3.2 | 1/1 | 1/1 |
| S21 | SGB IX | § 165 | T4.1 | 0/1 | 1/1 |
| S23 | BayGlG | Art. 17 | T4.1|T4.2 | 0/1 | 1/1 |
| S24 | AGG | – | T4.2 | 1/1 | 1/1 |
| S25 | DSGVO | Art. 5 Abs. 2 | T4.3|T6.2 | 1/1 | 0/1 |
| S27 | TV-L | – | T5.2|T5.3 | 1/1 | 1/1 |
| S28 | NachwG | – | T5.2|T5.3 | 1/1 | 1/1 |
| S29 | AGG | § 15 Abs. 4 | T6.2 | 0/1 | 1/1 |
| S30 | DSGVO | Art. 17 | T6.3 | 1/1 | 1/1 |
| S46 | WissZeitVG | § 2 | T1.2|T5.2|T5.3 | 1/1 | 1/1 |
| S47 | TzBfG | § 14 Abs. 4 | T5.2|T5.3 | 1/1 | 1/1 |

## 4. H1b – Lückenkandidaten

Kategorien je Lückenmeldung (`typ = moegliche_luecke`), dedupliziert nach Regelwerk + Artikel/Paragraf: `luecke_korrekt` (trifft Soll-Lücke), `luecke_neutral` (trifft Neutral-Zeile), `luecke_an_vorhandener_zuordnung` (trifft nur eine Soll-Zuordnung), `luecke_ohne_soll` (trifft nichts). Falsch = die beiden letzten. Lücken-Recall streng = nur Lückenmeldungen; großzügig = zusätzlich Regelwerke aus Stufe 1 (B: Vorgabe) ohne Zuordnung. Kontrolle = Lückenmeldungen, die S23 (Gleichstellungsbeauftragte, vorhandener Schritt) treffen.

| Kennzahl | v1 A (n=1) | v2 A (n=1) |
| --- | --- | --- |
| Lücken-Recall streng | 100% | 78% |
| Lücken-Recall großzügig | 100% | 78% |
| Lückenmeldungen (Funde) | 80.0 | 28.0 |
| Lückenmeldungen (dedupliziert) | 31.0 | 13.0 |
| davon luecke_korrekt | 9.0 | 7.0 |
| davon luecke_neutral | 8.0 | 2.0 |
| davon luecke_an_vorhandener_zuordnung | 10.0 | 1.0 |
| davon luecke_ohne_soll | 4.0 | 3.0 |
| falsche Lückenmeldungen | 14.0 | 4.0 |
| Kontrolle: Fehlmeldungen S23 | 1.0 | 1.0 |
| Regelwerke ohne Zuordnung | 1.0 | 0.0 |

In wie vielen Läufen wurde die Soll-Lücke erkannt (streng):

| Soll-Lücke | Regelwerk | Fundstelle | Inhalt | v1 A (n=1) | v2 A (n=1) |
| --- | --- | --- | --- | --- | --- |
| S05 | SGB IX | § 164 | Prüfung Besetzung freier Stellen mit schwerbehinderten Menschen, Beteiligung der … | 1/1 | 1/1 |
| S06 | SGB IX | § 165 | Meldung freier Stellen an die Agentur für Arbeit (öffentlicher Arbeitgeber, Satz … | 1/1 | 1/1 |
| S14 | AI Act | Art. 26 Abs. 11 | Information der Betroffenen über den KI-Einsatz | 1/1 | 1/1 |
| S15 | AI Act | Art. 27 | Grundrechte-Folgenabschätzung (öffentliche Stelle) | 1/1 | 1/1 |
| S16 | AI Act | Art. 4 | KI-Kompetenz der Mitarbeitenden | 1/1 | 0/1 |
| S18 | DSGVO | Art. 35 | Datenschutz-Folgenabschätzung | 1/1 | 1/1 |
| S20 | BayPVG | Art. 75a | Mitbestimmung Personalrat bei Einführung/Anwendung des KI-Tools (Abs. 1 Nr. 2, a … | 1/1 | 1/1 |
| S22 | SGB IX | § 178 | Beteiligung der Schwerbehindertenvertretung | 1/1 | 1/1 |
| S26 | BayPVG | Art. 78 Abs. 3 | Mitteilung an den Personalrat über die Einstellung (Mitbestimmung nach Art. 78 A … | 1/1 | 0/1 |

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

### Lückenmeldungen v2 A (1 Läufe, dedupliziert je Lauf)

| Regelwerk | Norm | Kategorie | Läufe | Meldungen | Soll-Lücke | Soll-Zuordnung | Beispiel fehlender Schritt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI Act | Art. 26 | luecke_korrekt | 1 | 1 | S14 | S13 | Falls und sobald die Vorschrift für das eingesetzte System gilt: Bewerbende darüber informieren, dass sie der Verwendung des Hochrisiko-KI-Systems unterliegen;  … |
| AI Act | Art. 27 | luecke_korrekt | 1 | 2 | S15 | – | Vor der erstmaligen Nutzung des Hochrisiko-KI-Systems ist als öffentliche Stelle eine Bewertung der Auswirkungen auf die Grundrechte durchzuführen, sofern die V … |
| BayPVG | Art. 75a | luecke_korrekt | 1 | 4 | S20 | – | Vor Einführung, Anwendung oder erheblicher Änderung des KI-gestützten automatisierten Verfahrens zur Personalverwaltung die Mitbestimmung des Personalrats durch … |
| DSGVO | Art. 35 | luecke_korrekt | 1 | 2 | S18 | – | Vor Beginn der KI-Auswertung eine Datenschutz-Folgenabschätzung durchführen, sofern die systematische und umfassende Bewertung personenbezogener Aspekte auf aut … |
| SGB IX | § 164 | luecke_korrekt | 1 | 3 | S05 | – | Vor beziehungsweise im Zuge der Besetzung ist zu prüfen, ob der freie Arbeitsplatz mit schwerbehinderten Menschen besetzt werden kann; die erforderliche frühzei … |
| SGB IX | § 165 | luecke_korrekt | 1 | 2 | S06 | S21 | Nach erfolgloser Prüfung einer internen Besetzung ist der neue oder neu zu besetzende Arbeitsplatz frühzeitig der Agentur für Arbeit zu melden; dieser gesondert … |
| SGB IX | § 178 | luecke_korrekt | 1 | 1 | S22 | – | Bei Bewerbungen schwerbehinderter Menschen die Schwerbehindertenvertretung über den einschlägigen Vorgang unterrichten und ihre gesetzliche Möglichkeit zur Teil … |
| AI Act | Art. 49 | luecke_neutral | 1 | 2 | – | – | Vor der Nutzung ist zu prüfen und gegebenenfalls die Registrierung der Hochschule und des verwendeten Systems in der EU-Datenbank vorzunehmen. |
| DSGVO | Art. 30 | luecke_neutral | 1 | 1 | – | – | Ein Verzeichnis der Verarbeitungstätigkeiten führen oder aktualisieren, das die Verarbeitung von Bewerberdaten im Auswahlverfahren einschließlich der Gesprächsd … |
| BayGlG | Art. 17 | luecke_an_vorhandener_zuordnung | 1 | 4 | – | S07,S23 | Ein etwaiges Begehren einer betroffenen Person auf Beteiligung der Gleichstellungsbeauftragten auch für die Personalangelegenheit der KI-Vorauswahl entgegennehm … |
| BayPVG | Art. 69 | luecke_ohne_soll | 1 | 1 | – | – | Personalrat rechtzeitig und umfassend unterrichten und ihm die für seine Aufgaben erforderlichen Unterlagen zur Verfügung stellen. |
| BayPVG | Art. 70 | luecke_ohne_soll | 1 | 2 | – | – | Die erforderliche Zustimmung des Personalrats zur mitbestimmungspflichtigen Maßnahme vor ihrer Durchführung einholen. |
| BayPVG | Art. 75 | luecke_ohne_soll | 1 | 3 | – | – | Die personalvertretungsrechtliche Mitbestimmung bei der Eingruppierung ist vor der endgültigen Eingruppierungsmaßnahme sicherzustellen; ein entsprechender Betei … |

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

### v2 A (18 Funde, 8 Normen)

| Regelwerk | Norm | Läufe | Funde | Tasks | unsicher | Fundstelle (Beispiel) | Quelle | Zitat Begründung |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BayPVG | Art. 75 | 1 | 4 | T1.2,T4.1,T5.1,T5.2 | 25% | Art. 75 Abs. 1 Satz 1 Nr. 3a | https://www.gesetze-bayern.de/Content/Document/BayPVG-75 | Der Personalrat hat bei der Eingruppierung mitzubestimmen. Der Prozess enthält zwar die Festlegung der Eingruppierung, benennt aber keine Beteiligung des Personalrats. |
| BDSG | § 26 | 1 | 3 | T2.1,T4.2 | 33% | § 26 Abs. 1 | https://www.gesetze-im-internet.de/bdsg_2018/__26.html | Bewerbungsdaten werden für die Entscheidung über die Begründung eines Beschäftigungsverhältnisses verarbeitet; Bewerbende sind nach § 26 Abs. 8 Beschäftigte im Sinne dieser Vorschrift. |
| BayPVG | Art. 69 | 1 | 3 | T4.3,T5.1 | 0% | Art. 69 Abs. 2 Satz 1 | https://www.gesetze-bayern.de/Content/Document/BayPVG-69 | Der Personalrat ist zur Aufgabenerfüllung rechtzeitig und umfassend zu unterrichten. Die Gesprächsdokumentation kann hierfür relevant sein, soweit sie für seine Aufgaben und die personalvertretungsrec … |
| ArbGG | § 61b | 1 | 2 | T6.2,T6.3 | 0% | § 61b Abs. 1 | https://www.gesetze-im-internet.de/arbgg/__61b.html | Die Klagefrist kann für die Dauer relevant sein, während der Unterlagen zur Verteidigung gegen einen geltend gemachten Anspruch benötigt werden. |
| BGB | § 611a | 1 | 2 | T5.3 | 0% | § 611a Abs. 1 | https://www.gesetze-im-internet.de/bgb/__611a.html | Der Vertrag begründet ein Arbeitsverhältnis mit weisungsgebundener, fremdbestimmter Arbeit in persönlicher Abhängigkeit; die Regelung beschreibt den arbeitsvertraglichen Rahmen. |
| BayPVG | Art. 70 | 1 | 2 | T3.1,T3.3 | 50% | Art. 70 Abs. 1 Satz 1 | https://www.gesetze-bayern.de/Content/Document/BayPVG/true | Soweit die Einführung oder Anwendung des automatisierten Verfahrens der Mitbestimmung nach Art. 75a BayPVG unterliegt, darf die Maßnahme grundsätzlich erst mit Zustimmung des Personalrats getroffen we … |
| AI Act | Art. 113 | 1 | 1 | T3.1 | 0% | Art. 113 Abs. 3 Buchst. c Ziff. i | https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/deu | Die Vorschrift legt den für die Anwendung der Hochrisiko-Pflichten maßgeblichen Termin fest und ist für die zeitliche Einordnung des aktuellen KI-Einsatzes entscheidend. |
| AI Act | Art. 6 | 1 | 1 | T3.2 | 100% | Art. 6 Abs. 2 | https://eur-lex.europa.eu/legal-content/DE/TXT/HTML/?uri=CELEX:02024R1689-20260727 | KI-Systeme für Einstellung oder Auswahl natürlicher Personen sind in Anhang III erfasst. Ein Ranking von Bewerbenden spricht für eine solche Verwendung; die konkrete Einstufung hängt von Funktion und  … |

<!-- MANUELL START: alles ab hier bleibt bei erneutem evaluate.py erhalten -->

## 5. Auffälligkeiten

Bezogen auf Lauf `20261020-145929_A_1`. Stichproben habe ich auf gesetze-bayern.de nachgeprüft (20.10.2026).
Hinweise auf erfundene Normen gibt es bisher nicht.

**5.1 Das Modell widerspricht der Soll-Liste – und hat nach Prüfung recht (Soll-Liste anpassen)**

- **BayPVG, Mitbestimmung bei Einstellung (S26):** Fund F177 (T5.3, Lücke): *„Art. 78 Abs. 1 Satz 1 Nr. 6 nimmt
  wissenschaftliche Mitarbeiterinnen und Mitarbeiter im Sinne des Art. 74 BayHIG grundsätzlich von den dort genannten
  Beteiligungsrechten, darunter der Mitbestimmung nach Art. 75 Abs. 1, aus. Nach Art. 78 Abs. 3 soll der Personalrat in
  diesen Fällen jedoch eine Mitteilung über die Einstellung erhalten.“* Geprüft: Art. 78 Abs. 1 Satz 1 Nr. 6 BayPVG
  schließt „sonstige Beschäftigte mit vorwiegend wissenschaftlicher … Tätigkeit“ von Art. 75 Abs. 1 aus, Abs. 3 sieht
  eine Mitteilung bei Einstellung vor. Die Soll-Lücke S26 („Mitbestimmung Personalrat bei Einstellung“) ist für diese
  Stelle damit vermutlich falsch; richtig wäre „Mitteilung an den Personalrat, Art. 78 Abs. 3 BayPVG“. Art. 75a
  (KI-Tool) ist von der Ausnahme nicht erfasst – S20 bleibt.
- **BayGlG, Kontrolle Gleichstellungsbeauftragte:** 3 Lückenmeldungen (dedupliziert) zählen als „falsch“. Beispiele:
  F112 (T4.1): *„Mit der Einladung auf das Recht der betroffenen Person hinweisen, die Teilnahme der
  Gleichstellungsbeauftragten am Vorstellungsgespräch zu beantragen; deren Teilnahme am Gespräch von einem solchen Antrag
  abhängig machen.“* Geprüft: Art. 17 Abs. 3 Satz 3 und 4 BayGlG: *„Eine Beteiligung an Vorstellungsgesprächen findet nur
  auf Antrag der Betroffenen statt. Auf das Antragsrecht … ist spätestens im Rahmen der Einladung zum Vorstellungsgespräch
  hinzuweisen.“* Das Modell meldet also nicht den vorhandenen Schritt als Lücke, sondern einen **tatsächlich fehlenden
  Teilschritt** (Hinweis auf das Antragsrecht in T4.1). Zudem steht T4.2 („Gespräche mit … Gleichstellungsbeauftragter
  führen“) im Widerspruch zur Vorschrift, weil die Teilnahme ohne Antrag nicht vorgesehen ist. Die Kontrolle ist so
  nicht trennscharf; siehe Abschnitt 8.
- **Art. 75a BayPVG:** Das Modell nennt durchgehend Abs. 1 **Nr. 2** („automatisierte Verfahren zur
  Personalverwaltung“). In der Soll-Liste ist bisher nur „Art. 75a“ eingetragen, mein Vorschlag war Nr. 1 (technische
  Überwachungseinrichtungen). Beides ist geltendes Recht (geprüft); welche Nummer gilt, entscheidet der Autor.
- **Art. 35 BayDSG** (F100, Lücke an T3.4) gibt es tatsächlich: „Automatisierte Einzelentscheidungen“, das
  Landes-Gegenstück zu Art. 22 DSGVO (geprüft). Ein Kandidat für die Soll-Liste.

**5.2 Muster in den Funden**

- **Breite statt Zuordnung:** Allgemeine Normen werden fast jedem Task zugeordnet, z. B. Art. 5 Abs. 1 DSGVO an 13
  Tasks, Art. 32 DSGVO an 6, Art. 4 BayDSG an 6, § 7 AGG an 5. Daraus stammen die meisten der 67 `falscher_task`-Bewertungen (von 120 Zuordnungen).
  Fachlich ist das oft nicht falsch, aber die Soll-Liste kennt nur einen Task pro Norm.
- **„Lücke“ für fehlende Details vorhandener Schritte:** 80 der 200 Funde haben `typ = moegliche_luecke`. Viele davon
  nennen eine Vorschrift, die zu einem vorhandenen Task gehört, und bemängeln fehlende Details (z. B. Art. 13 DSGVO an
  T2.1: *„Bei oder spätestens zum Zeitpunkt der Erhebung über das Portal die vorgeschriebenen Datenschutzinformationen
  bereitstellen …“*). Folge: Die Soll-Zuordnungen S04 (TV-L, T1.2), S10 (Art. 13, T2.1), S17 (Art. 22, T3.4) und
  S21 (§ 165, T4.1) werden nur als Lücke genannt und zählen im strengen Recall als übersehen. Der Recall inkl.
  dieser Meldungen liegt bei 90 % statt 67 %.
- **Dieselbe Lücke an vielen Tasks:** DSFA (Art. 35 DSGVO) wird an 7 Tasks gemeldet, Grundrechte-Folgenabschätzung
  (Art. 27 AI Act) an 5, Art. 75a BayPVG an 5. Die Deduplizierung in H1b fängt das ab.
- **Zusätzliche Regelwerke** (Stufe 1, nicht in Soll): BayHIG, WissZeitVG, TzBfG, BGB. Für eine befristete
  wissenschaftliche Stelle sind sie plausibel (Art. 71/72 BayHIG Qualifikation, WissZeitVG/TzBfG Befristung).
  BGB (§§ 145 ff., 611a) ist eher Allgemeinwissen.
- **Weitere `nicht_in_soll`-Funde** sind überwiegend plausibel: Art. 9, 12, 18, 19, 24, 25, 28, 29, 30 DSGVO;
  Art. 49 Abs. 3 (Registrierung von Betreibern, die Behörden sind) und Art. 86 AI Act (Recht auf Erläuterung).
  Manuell prüfen: F001 Art. 76 Abs. 3 BayPVG (Anhörung bei Personalanforderungen zum Haushaltsvoranschlag; vom Modell
  selbst als „unsicher“ markiert), BayArchivG Art. 14 / Art. 26 Abs. 6 BayDSG (Anbietungspflicht an das Archiv vor
  der Löschung).
- **Unsicherheit:** 26 % der Funde sind als „unsicher“ markiert. In Stufe 1 hat das Modell ausgerechnet die KI-VO
  als „unsicher“ markiert. Begründung: *„die konkrete Einstufung hängt von Zweck, Funktionsweise und tatsächlichem
  Einfluss des Tools auf die Auswahl ab“*.
- **Quellen:** Alle 200 `quelle_url` liegen in den vier erlaubten Domains. 58 % stimmen exakt mit einer URL aus den
  Websuche-Quellen überein, der Rest sind Varianten derselben Dokumente (z. B. `TXT` statt `ALL` bei EUR-Lex,
  Einzelnorm-URLs wie `BayHIG-71`).

## 6. Technische Probleme

- **Lauf A_1 ohne Fehler:** 20 Aufrufe, keine Retries, keine fehlgeschlagenen Tasks, 9 min 19 s. 95 Websuchen, alle
  683 Quellen-URLs liegen innerhalb der vier Domains, der Domain-Filter greift also. tdl-online.de wurde genutzt
  (TV-L-PDF i. d. F. ÄTV Nr. 13).
- **Kosten** ca. 1,09 USD je Lauf A (922 889 Input-, 111 545 Output-Tokens; ~0,95 USD davon Websuche zur
  angenommenen Rate von 10 USD/1000). Hochgerechnet auf 10 Läufe: ca. 10–11 USD.
- **Auswertung korrigiert (meine Seite, nicht das Modell):** Die erste Auswertung hat bei Fundstellen mit mehreren
  Normen nur die erste gezählt. Beispiele: *„Art. 6 Abs. 2 und 3, Anhang III Nr. 4 Buchst. a“* oder Regelwerk
  *„DSGVO / BayDSG“*. Dadurch wurde u. a. S12 (Anhang III Nr. 4) als übersehen gewertet. Jetzt wird jede Norm und
  jeder Absatz einzeln ausgewertet (Absatzlisten und -bereiche wie „Abs. 1, 2 und 5“ und „Abs. 1–4“, `§§ 7, 11`,
  Regelwerk je `;`-Abschnitt). Effekt: Stufe-2-Recall 57 % → 67 %, Präzision 20 % → 22 %, falsche Lückenmeldungen 22 → 20.
- **Bekannte Grenze der Normierung:** „Anlage A Vorbemerkung Nr. 1 Abs. 2“ (TV-L) wird nicht als eigene Norm erkannt.
  Der Absatz wird der vorherigen Norm zugeschlagen. Für die Bewertung ist das bisher ohne Folgen.
- **Code liegt im Image:** Nach Änderungen an `src/` muss `docker compose build` erneut laufen. Nur `input/`,
  `prompts/` und `config.yaml` sind gemountet.
- **GitHub:** Das HTTPS-Token auf dem Rechner ist ungültig, daher Push per SSH.

## 7. Offene Fragen und Annahmen

- **S26 (BayPVG, Einstellung):** Wegen Art. 78 Abs. 1 Satz 1 Nr. 6 BayPVG ändern zu „Mitteilung an den Personalrat,
  Art. 78 Abs. 3“ (weiter `luecke`)? Bisher **unverändert**, weil die Soll-Liste nur der Autor ändert.
- **Kontrolle Gleichstellungsbeauftragte:** Soll ein Hinweis auf das Antragsrecht (Art. 17 Abs. 3 Satz 4 BayGlG, T4.1)
  als echte Soll-Lücke aufgenommen werden? Bisher zählt jede BayGlG-Lückenmeldung als falsch, auch die fachlich
  richtige. Unverändert gelassen.
- **Recall-Definition:** Strenger Recall (nur `typ = zuordnung`) bleibt die Hauptkennzahl laut Anweisung. Zusätzlich
  gibt es `s2_recall_inkl_luecke`. Welche der beiden soll in der Arbeit berichtet werden?
- **Präzision:** Wird eine Norm an mehreren Tasks genannt, zählt jede Nennung außerhalb des Soll-Tasks als
  `falscher_task`. Das senkt die Präzision stark (22 %). Ob das gewollt ist, hängt von der Antwort auf Vorschlag 8.1 ab.
- Alle übrigen Annahmen (Modell-Snapshot, Preise, Zuordnung der Soll-Zeilen) stehen in `DECISIONS.md`.

## 8. Verbesserungsvorschläge

1. **Soll-Liste, mehrere Tasks je Norm:** `task_id` mehrwertig erlauben (`T2.1|T2.2|T2.3`) oder prozessweite Normen
   (Art. 5 Abs. 1, Art. 32 DSGVO, Art. 4 BayDSG, § 7 AGG) als `GESAMT` führen. Das ist der größte Hebel für eine
   aussagekräftige Präzision.
2. **Soll-Liste, fachliche Korrekturen:** S26 → Art. 78 Abs. 3 BayPVG (siehe 5.1); neue Soll-Lücke „Hinweis auf
   Antragsrecht Gleichstellungsbeauftragte in der Einladung“ (Art. 17 Abs. 3 Satz 4 BayGlG, T4.1); Art. 75a Nr. 1
   oder Nr. 2 festlegen.
3. **Soll-Liste, Ergänzungen (oder als „neutral“ markieren):** Art. 35 BayDSG, Art. 9, 12, 25, 28, 30 DSGVO,
   Art. 49 Abs. 3 und Art. 86 AI Act, BayHIG Art. 71/72, WissZeitVG §§ 1–2, TzBfG § 14. Eine Spalte `neutral`
   (relevant, aber nicht bewertet) würde `nicht_in_soll` entlasten.
4. **Prompt Stufe 2:** `moegliche_luecke` schärfen. Nur verwenden, wenn **kein** Task des Prozesses den Schritt
   abdeckt; fehlende Details eines vorhandenen Tasks als `zuordnung` mit Hinweis ausgeben. Optional ein drittes
   Feld/`typ` `anforderung_an_task` für „Task vorhanden, Detail fehlt“.
5. **Prompt Stufe 2:** „Eine Norm je Fund“ und das Format „Art. 26 Abs. 11“ vorgeben. Regelwerk in Kurzform
   (DSGVO, AI Act, …). Das senkt den Normierungsaufwand.
6. **Prompt Stufe 2:** Allgemeine Grundsätze (Art. 5 DSGVO, § 7 AGG) nur bei dem Task nennen, bei dem sie konkret
   werden. Oder bewusst zulassen und über Vorschlag 1 abbilden.
7. **Auswertung:** Neben „falsche Lückenmeldung“ die Kategorie „Lücke an vorhandener Soll-Zuordnung“ getrennt
   ausweisen. Sie ist eine andere Fehlerart als eine frei erfundene Lücke.
8. **Prozessmodell:** T4.2 widerspricht Art. 17 Abs. 3 Satz 3 BayGlG (Teilnahme nur auf Antrag). Entweder T4.2
   umformulieren („… ggf. mit Gleichstellungsbeauftragter auf Antrag“) oder den Widerspruch bewusst als Testfall nutzen.

<!-- MANUELL ENDE -->
