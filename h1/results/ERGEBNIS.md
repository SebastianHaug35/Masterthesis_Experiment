# ERGEBNIS H1 (inkl. H1b)

Automatisch erzeugt von `python -m src.evaluate` (Abschnitte 1–4 und Material für 5).
Abschnitte 5–8 unten sind manuell gepflegt. Begriffe: siehe `README.md` und `DECISIONS.md`.

## 1. Lauf-Metadaten

| run_id | Konfig | Modell-Snapshot | reasoning_effort | Dauer | Tokens in | Tokens out | Websuchen | Kosten USD (geschätzt) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20261020-145929_A_1 | A | `gpt-6-luna` | medium | 9 min 19 s | 922 889 | 111 545 | 95 | 1.0923 | ok |

## 2. Stufe 1 – Rechtsrahmen

### 20261020-145929_A_1

| Regelwerk (Agent) | normiert | Ebene | Sicherheit | Quelle |
| --- | --- | --- | --- | --- |
| DSGVO | DSGVO | EU | sicher | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679 |
| BayDSG | BayDSG | Land | sicher | https://www.gesetze-bayern.de/Content/Document/BayDSG/true |
| KI-VO | AI Act | EU | unsicher | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32024R1689 |
| AGG | AGG | Bund | sicher | https://www.gesetze-im-internet.de/agg/BJNR189710006.html |
| GG | GG | Bund | sicher | https://www.gesetze-im-internet.de/gg/art_33.html |
| SGB IX | SGB IX | Bund | sicher | https://www.gesetze-im-internet.de/sgb_9_2018/SGB_IX.pdf |
| BayHIG | BayHIG | Land | sicher | https://www.gesetze-bayern.de/Content/Document/BayHIG/true |
| BayPVG | BayPVG | Land | sicher | https://www.gesetze-bayern.de/Content/Document/BayPVG/true |
| BayGlG | BayGlG | Land | sicher | https://www.gesetze-bayern.de/Content/Document/BayGlG/true |
| TV-L | TV-L | Tarif | sicher | https://www.tdl-online.de/tarifvertraege/tv-l |
| WissZeitVG | WissZeitVG | Bund | unsicher | https://www.gesetze-im-internet.de/wisszeitvg/BJNR050610007.html |
| TzBfG | TzBfG | Bund | unsicher | https://www.gesetze-im-internet.de/tzbfg/BJNR196610000.html |
| NachwG | NachwG | Bund | sicher | https://www.gesetze-im-internet.de/nachwg/BJNR094610995.html |
| BGB | BGB | Bund | sicher | https://www.gesetze-im-internet.de/bgb/BGB.pdf |

- **Gefunden (10):** AGG, AI Act, BayDSG, BayGlG, BayPVG, DSGVO, GG, NachwG, SGB IX, TV-L
- **Übersehen (0):** –
- **Zusätzlich (4):** BGB, BayHIG, TzBfG, WissZeitVG
- Recall 100%, Präzision 71%

## 3. Stufe 2 – Zuordnung je Task

Bewertet werden Funde mit `typ = zuordnung`; Recall/Präzision auf Ebene Fundstelle (Lücken-Funde siehe Abschnitt 4).

### 20261020-145929_A_1

- Funde: 120 (korrekt 26, falscher_absatz 0, falscher_task 67, nicht_in_soll 27)
- Gesamt: Recall 67%, Präzision 22%
- Recall inkl. Lückenmeldungen, die eine vorhandene Soll-Zuordnung am selben Task nennen: 90%

| Teilprozess | Recall | Präzision |
| --- | --- | --- |
| TP1 | 50% | 43% |
| TP2 | 75% | 28% |
| TP3 | 50% | 19% |
| TP4 | 75% | 40% |
| TP5 | 100% | 14% |
| TP6 | 50% | 7% |
| GESAMT | 100% | – |

Übersehene Soll-Zeilen (Zuordnung): S03 AGG § 11 → T1.3; S04 TV-L → T1.2; S10 DSGVO Art. 13 → T2.1; S13 AI Act Art. 26 → T3.3; S17 DSGVO Art. 22 → T3.4; S21 SGB IX § 165 → T4.1; S29 AGG § 15 Abs. 4 → T6.2

## 4. H1b – Lückenkandidaten

### 20261020-145929_A_1

- Lücken-Recall: 100% · Kandidaten (dedupliziert nach Regelwerk + Norm): 32 · falsche Lückenmeldungen: 20 (davon Gleichstellungsbeauftragte: 3)

| Quelle | Task | Regelwerk | Fundstelle | Fehlender Schritt (Agent) | trifft Soll-Lücke |
| --- | --- | --- | --- | --- | --- |
| regelwerk_ohne_zuordnung | – | BayPVG | – | – | S20,S26 |
| moegliche_luecke | T1.1 | BayPVG | Art. 76 Abs. 3 Satz 1 | Falls die Bedarfsmeldung als Personalanforderung zum Haushaltsvoranschlag weitergeleitet wird, ist der Personalrat vorher anzuhören. Ein solcher Anhörungsschritt ist im Prozess nicht aufgeführt. | **nein** |
| moegliche_luecke | T1.2 | TV-L | § 12 Abs. 1 Sätze 1 bis 8; Anlage A Vorbemerkung Nr. 1 Abs. 2 und Teil II Abschnitt 6 | Die dauerhaft auszuübenden Aufgaben in Arbeitsvorgänge gliedern, deren Anforderungen und zeitliche Anteile bewerten und anhand der einschlägigen Tätigkeitsmerkmale die Entgeltgruppe bestimmen. Dieser  … | **nein** |
| moegliche_luecke | T1.2 | BayPVG | Art. 75 Abs. 1 Satz 1 Nr. 3a; Art. 70 Abs. 1 und 2 | Die vorgesehene Eingruppierung dem Personalrat zur Mitbestimmung vorlegen und das Zustimmungsverfahren vor der abschließenden Maßnahme durchführen. Eine Beteiligung des Personalrats ist im Prozess nic … | S26 |
| moegliche_luecke | T1.2 | BayGlG | Art. 7 Abs. 1 bis 3 | Bei der Vorbereitung der Stellenausschreibung die geschlechtsneutrale Ausschreibung, den Hinweis auf Teilzeitbeschäftigungsmöglichkeiten und gegebenenfalls die besondere Aufforderung des unterrepräsen … | **nein** |
| moegliche_luecke | T1.3 | SGB IX | § 165 Satz 1 | Vor der Veröffentlichung ist nach erfolgloser Prüfung einer internen Besetzung der freie oder neue Arbeitsplatz frühzeitig der Agentur für Arbeit zu melden. Eine Meldung an die Agentur für Arbeit ist  … | S06 |
| moegliche_luecke | T2.1 | DSGVO | Art. 13 Abs. 1 und 2 | Bei oder spätestens zum Zeitpunkt der Erhebung über das Portal die vorgeschriebenen Datenschutzinformationen bereitstellen, insbesondere zu Verantwortlichem, Zwecken, Rechtsgrundlage, Empfängern, Spei … | **nein** |
| moegliche_luecke | T2.1 | DSGVO | Art. 30 Abs. 1 | Die Verarbeitung der Bewerbungsdaten in das Verzeichnis der Verarbeitungstätigkeiten aufnehmen beziehungsweise den vorhandenen Eintrag für das Bewerbungsportal aktuell halten. | **nein** |
| moegliche_luecke | T2.1 | BayDSG | Art. 31 | Im Verzeichnis der Verarbeitungstätigkeiten zusätzlich die Rechtsgrundlage und, soweit einschlägig, die Verwendung von Profiling eintragen. | **nein** |
| moegliche_luecke | T2.1 | DSGVO | Art. 28 Abs. 3 | Falls ein externer Anbieter das Portal im Auftrag der Hochschule betreibt oder Bewerbungsdaten sonst weisungsgebunden verarbeitet, vor Beginn der Verarbeitung einen den Anforderungen des Art. 28 Abs.  … | **nein** |
| moegliche_luecke | T2.1 | DSGVO | Art. 35 Abs. 1 | Vor Beginn der Verarbeitung im Gesamtverfahren prüfen und dokumentieren, ob wegen des KI-gestützten Rankings und der weiteren Verarbeitung von Bewerberdaten eine Datenschutz-Folgenabschätzung erforder … | S18 |
| moegliche_luecke | T2.2 | DSGVO | Art. 13 Abs. 1 und 2 | Bei der Erhebung der Bewerberdaten muss die Hochschule die vorgeschriebenen Datenschutzinformationen bereitstellen. Dieser Schritt ist im Prozess nicht ausdrücklich beschrieben; die Information sollte … | **nein** |
| moegliche_luecke | T2.3 | DSGVO | Art. 6 Abs. 1 | Vor dem Anlegen der Daten die konkrete Rechtsgrundlage der Bewerberdatenverarbeitung festlegen und dokumentieren. | **nein** |
| moegliche_luecke | T2.3 | DSGVO | Art. 13 Abs. 1 und 2 | Bewerberinnen und Bewerber bei der Erhebung über Verantwortlichen, Zwecke, Rechtsgrundlage, Empfänger, Speicherdauer und ihre Rechte informieren. | **nein** |
| moegliche_luecke | T2.3 | DSGVO | Art. 28 Abs. 3 | Falls ein externer Anbieter Bewerberdaten im Auftrag verarbeitet, vorab einen den Anforderungen des Art. 28 Abs. 3 entsprechenden Auftragsverarbeitungsvertrag abschließen. | **nein** |
| moegliche_luecke | T2.3 | DSGVO | Art. 30 Abs. 1 | Die Verarbeitung von Bewerberdaten im Bewerbungsmanagement in das Verzeichnis der Verarbeitungstätigkeiten aufnehmen oder den Eintrag aktualisieren. | **nein** |
| moegliche_luecke | T2.3 | DSGVO | Art. 35 Abs. 1 und 3 | Vor der Verarbeitung prüfen und dokumentieren, ob wegen der KI-gestützten Bewerberauswahl und des Rankings eine Datenschutz-Folgenabschätzung erforderlich ist; falls ein voraussichtlich hohes Risiko b … | S18 |
| moegliche_luecke | T3.1 | DSGVO | Art. 13 Abs. 1 und 2 | Bewerberinnen und Bewerber bei Erhebung ihrer Daten transparent über die Verarbeitung mittels KI, deren Zwecke, Rechtsgrundlage, Empfänger und weitere Pflichtangaben informieren. | **nein** |
| moegliche_luecke | T3.1 | DSGVO | Art. 28 Abs. 1 und 3 | Falls der Anbieter oder Betreiber des KI-Tools Bewerberdaten im Auftrag der Hochschule verarbeitet, Auftragsverarbeiterstellung und einen den Anforderungen des Art. 28 entsprechenden Vertrag prüfen un … | **nein** |
| moegliche_luecke | T3.1 | DSGVO | Art. 30 Abs. 1 | Die Verarbeitung der Bewerberdaten einschließlich KI-Auswertung und Ranking im Verzeichnis der Verarbeitungstätigkeiten dokumentieren. | **nein** |
| moegliche_luecke | T3.1 | DSGVO | Art. 35 Abs. 1 und Abs. 3 Buchst. a | Vor Beginn der KI-Auswertung prüfen und dokumentieren, ob eine Datenschutz-Folgenabschätzung erforderlich ist; bei voraussichtlich hohem Risiko diese vor der Verarbeitung durchführen. | S18 |
| moegliche_luecke | T3.1 | KI-VO | Art. 4 | Sicherstellen und dokumentieren, dass die mit Betrieb und Nutzung des KI-Systems befassten Beschäftigten über ein ihrem Einsatzkontext angemessenes Maß an KI-Kompetenz verfügen. | S16 |
| moegliche_luecke | T3.1 | KI-VO | Art. 27 Abs. 1 und 2 | Vor der ersten Inbetriebnahme beziehungsweise Verwendung des Hochrisiko-KI-Systems eine Grundrechte-Folgenabschätzung durchführen und erforderlichenfalls aktualisieren. | S15 |
| moegliche_luecke | T3.1 | KI-VO | Art. 49 Abs. 3 | Falls das System als Hochrisiko-KI-System nach Anhang III eingestuft wird, vor seiner Verwendung die erforderliche Registrierung der Hochschule als Betreiber in der EU-Datenbank prüfen und gegebenenfa … | **nein** |
| moegliche_luecke | T3.1 | SGB IX | § 165 Satz 3 und 4 | Bei der späteren Einladung sicherstellen, dass schwerbehinderte Bewerberinnen und Bewerber, die sich beworben haben oder vorgeschlagen wurden, grundsätzlich zum Vorstellungsgespräch eingeladen werden; … | S06 |
| moegliche_luecke | T3.1 | BayPVG | Art. 75a Abs. 1 Nr. 2 | Vor Einführung oder Anwendung des automatisierten Verfahrens zur Personalverwaltung die Mitbestimmung des Personalrats prüfen und gegebenenfalls durchführen. | S20 |
| moegliche_luecke | T3.2 | DSGVO | Art. 35 Abs. 1, 2 und 7 | Vor dem erstmaligen Einsatz des KI-Rankings prüfen und dokumentieren, ob eine Datenschutz-Folgenabschätzung erforderlich ist; bei voraussichtlich hohem Risiko die Folgenabschätzung vorab durchführen u … | S18 |
| moegliche_luecke | T3.2 | KI-VO | Art. 26 Abs. 7 und 11 | Vor dem Einsatz des Hochrisiko-KI-Systems am Arbeitsplatz die betroffenen Beschäftigten und ihre Vertretung informieren; außerdem Bewerberinnen und Bewerber über den Einsatz informieren, soweit sie ei … | S14 |
| moegliche_luecke | T3.2 | KI-VO | Art. 27 Abs. 1 und 2 | Vor der erstmaligen Inbetriebnahme des Hochrisiko-KI-Systems eine Grundrechte-Folgenabschätzung durchführen und bei geänderten relevanten Umständen aktualisieren. | S15 |
| moegliche_luecke | T3.2 | KI-VO | Art. 86 Abs. 1 | Ein Verfahren vorsehen, um auf ein Verlangen betroffener Personen eine klare und aussagekräftige Erläuterung zur Rolle des KI-Systems und zu den wichtigsten Elementen der Entscheidung geben zu können. | **nein** |
| moegliche_luecke | T3.2 | BayPVG | Art. 75a Abs. 1 Nr. 2 und Art. 70 Abs. 1 | Vor Einführung oder Anwendung des automatisierten KI-Verfahrens zur Personalverwaltung die Mitbestimmung des Personalrats durchführen und dessen Zustimmung einholen, soweit keine gesetzliche oder tari … | S20 |
| moegliche_luecke | T3.2 | SGB IX | § 164 Abs. 1 und 2 | Bewerbungen schwerbehinderter Menschen nach Eingang der Schwerbehindertenvertretung und den weiteren in § 164 Abs. 1 genannten Vertretungen mitteilen und die vorgeschriebene Beteiligung sicherstellen; … | S05 |
| moegliche_luecke | T3.3 | KI-VO | Art. 14 Abs. 1–4; Art. 26 Abs. 1–2 | Die menschliche Prüfung konkret ausgestalten: zuständige Personen müssen die Grenzen und Ausgaben des Systems verstehen, Automatisierungsbias berücksichtigen und befugt sowie in der Lage sein, das Erg … | S14 |
| moegliche_luecke | T3.3 | KI-VO | Art. 4 | Sicherstellen, dass die mit der Prüfung befassten Personen über ein angemessenes Maß an KI-Kompetenz verfügen; entsprechende Maßnahmen sind im Prozess nicht beschrieben. | S16 |
| moegliche_luecke | T3.3 | DSGVO | Art. 35 Abs. 1 und gegebenenfalls Abs. 3 Buchst. a | Vor Beginn der betreffenden Verarbeitung prüfen und dokumentieren, ob eine Datenschutz-Folgenabschätzung erforderlich ist; falls ja, diese vorab durchführen. Ein solcher Prüfschritt ist im Gesamtproze … | S18 |
| moegliche_luecke | T3.3 | KI-VO | Art. 27 Abs. 1 | Falls das System als Hochrisiko-KI-System nach Anhang III Nr. 4 Buchst. a eingesetzt wird: vor seiner Inbetriebnahme eine Grundrechte-Folgenabschätzung durchführen und dokumentieren. Dieser Schritt is … | S15 |
| moegliche_luecke | T3.3 | SGB IX | § 165 Satz 3 und 4 | Bei schwerbehinderten Bewerbern sicherstellen, dass ein Ausschluss aufgrund fehlender fachlicher Eignung nur erfolgt, wenn diese offensichtlich fehlt; andernfalls sind sie zum Vorstellungsgespräch ein … | S06 |
| moegliche_luecke | T3.3 | BayPVG | Art. 75a Abs. 1 Nr. 2; gegebenenfalls Art. 75 Abs. 4 Satz 1 Nr. 13 | Vor Einführung oder Anwendung des KI-gestützten Verfahrens klären und dokumentieren, ob die Mitbestimmung des Personalrats wegen eines automatisierten Verfahrens zur Personalverwaltung oder wegen Rich … | S20,S26 |
| moegliche_luecke | T3.4 | DSGVO | Art. 22 Abs. 1 und 3 | Sicherstellen und dokumentieren, dass die Shortlist nicht lediglich das KI-Ranking übernimmt: Eine zuständige Person muss die Einzelfälle tatsächlich eigenständig prüfen, die Möglichkeit haben, vom Ra … | **nein** |
| moegliche_luecke | T3.4 | DSGVO | Art. 35 Abs. 1 und Abs. 3 Buchst. a | Vor dem Einsatz des KI-gestützten Bewertungs- und Rankingverfahrens prüfen und dokumentieren, ob eine Datenschutz-Folgenabschätzung erforderlich ist; bei voraussichtlich hohem Risiko diese vor der Ver … | S18 |
| moegliche_luecke | T3.4 | BayDSG | Art. 35 Abs. 1 und 2 | Die Shortlistentscheidung muss durch eine natürliche Person tatsächlich eigenständig getroffen werden und darf bei nachteiliger Rechtsfolge oder erheblicher Beeinträchtigung nicht ausschließlich auf a … | **nein** |
| moegliche_luecke | T3.4 | KI-VO | Art. 4 | Maßnahmen zur KI-Kompetenz der mit Betrieb und Nutzung des Systems befassten Beschäftigten vorsehen, passend zu deren Kenntnissen, Erfahrung, Schulung und dem Einsatzkontext. | S16 |
| moegliche_luecke | T3.4 | KI-VO | Art. 26 Abs. 1, 2 und 5; Art. 14 | Für den Betrieb als Hochrisiko-KI-System die Betreiberpflichten umsetzen: System gemäß Gebrauchsanweisung nutzen, geeignete natürliche Personen mit wirksamer menschlicher Aufsicht betrauen und die vor … | S14 |
| moegliche_luecke | T3.4 | KI-VO | Art. 27 Abs. 1 und 2 | Vor dem ersten Einsatz des Hochrisiko-Systems eine Grundrechte-Folgenabschätzung durchführen und dabei insbesondere den Auswahlprozess, betroffene Personengruppen, Risiken, menschliche Aufsicht und Ma … | S15 |
| moegliche_luecke | T3.4 | SGB IX | § 165 Satz 3 und 4 | Schwerbehinderte Bewerberinnen und Bewerber, die sich beworben haben oder vorgeschlagen wurden, in die Vorstellungsgespräche aufnehmen; eine Nicht-Einladung ist nur zulässig, wenn die fachliche Eignun … | S06 |
| moegliche_luecke | T3.4 | SGB IX | § 164 Abs. 1; § 178 Abs. 2 | Bewerbungen schwerbehinderter Menschen und Vermittlungsvorschläge der Schwerbehindertenvertretung unverzüglich mitteilen und die Schwerbehindertenvertretung im Verfahren nach § 164 Abs. 1 beteiligen;  … | S05,S22 |
| moegliche_luecke | T3.4 | BayPVG | Art. 75a Abs. 1 Nr. 2; Art. 70 Abs. 1 Satz 1 | Vor Einführung oder Anwendung des KI-Tools prüfen, ob es ein automatisiertes Verfahren zur Personalverwaltung ist, und gegebenenfalls die Zustimmung des Personalrats einholen. Die Zustimmung muss vor  … | S20 |
| moegliche_luecke | T3.4 | BayGlG | Art. 17 Abs. 2 und 3 | Die Gleichstellungsbeauftragte bei Personalangelegenheiten rechtzeitig und umfassend unterrichten sowie erforderliche Unterlagen frühzeitig vorlegen. Eine Beteiligung an Personalangelegenheiten und Vo … | **nein** |
| moegliche_luecke | T4.1 | SGB IX | § 165 Satz 3 und 4 | Vor dem Versand der Einladungen prüfen, ob schwerbehinderte oder gleichgestellte Bewerberinnen und Bewerber eingeladen werden. Eine Nichteinladung ist nur zulässig, wenn die fachliche Eignung offensic … | S06 |
| moegliche_luecke | T4.1 | SGB IX | § 178 Abs. 2 Satz 1 und 4 | Bei Bewerbungen schwerbehinderter Menschen die Schwerbehindertenvertretung unverzüglich und umfassend unterrichten und vor einer sie betreffenden Entscheidung anhören; ihr die Teilnahme an Vorstellung … | S22 |
| moegliche_luecke | T4.1 | BayGlG | Art. 17 Abs. 3 Satz 3 und 4 | Mit der Einladung auf das Recht der betroffenen Person hinweisen, die Teilnahme der Gleichstellungsbeauftragten am Vorstellungsgespräch zu beantragen; deren Teilnahme am Gespräch von einem solchen Ant … | **nein** |
| moegliche_luecke | T4.2 | BayGlG | Art. 17 Abs. 2 und Abs. 3 Sätze 2 bis 4 | Vor der Teilnahme der Gleichstellungsbeauftragten prüfen und dokumentieren, ob die jeweilige betroffene Person ihre Beteiligung am Vorstellungsgespräch beantragt hat. Spätestens mit der Einladung ist  … | **nein** |
| moegliche_luecke | T4.2 | SGB IX | § 165 | Im Zusammenhang mit der Einladung (TP4.1) sicherstellen, dass schwerbehinderte Bewerberinnen und Bewerber zu einem Vorstellungsgespräch eingeladen werden, sofern ihre fachliche Eignung nicht offensich … | S06 |
| moegliche_luecke | T4.2 | SGB IX | § 178 Abs. 2 | Bei betroffenen schwerbehinderten Bewerberinnen und Bewerbern die Schwerbehindertenvertretung unverzüglich und umfassend unterrichten und vor der Entscheidung anhören. Eine Beteiligung oder Anhörung d … | S22 |
| moegliche_luecke | T4.2 | BayPVG | Art. 69 Abs. 2; Art. 75 Abs. 1 Satz 1 Nr. 1 | Den Personalrat rechtzeitig und umfassend unterrichten und die erforderlichen Unterlagen zur Verfügung stellen; die Mitbestimmung bei der Einstellung ist vor deren Vollzug sicherzustellen. Eine Beteil … | S26 |
| moegliche_luecke | T4.2 | DSGVO | Art. 9 Abs. 1 und 2; Art. 32 Abs. 1 | Für den Fall, dass im Gespräch besondere Kategorien personenbezogener Daten erhoben oder notiert werden, vorab eine einschlägige Ausnahme nach Art. 9 Abs. 2 und geeignete Garantien sicherstellen. Gesp … | **nein** |
| moegliche_luecke | T4.3 | DSGVO | Art. 13 Abs. 1 Buchst. c und d | Vor der Erhebung beziehungsweise Dokumentation prüfen, ob Bewerberinnen und Bewerber über Zweck und Rechtsgrundlage der Gesprächsdokumentation sowie gegebenenfalls die berechtigten Empfänger informier … | **nein** |
| moegliche_luecke | T4.3 | BayGlG | Art. 17 Abs. 3 Satz 3 und 4 sowie Abs. 4 Satz 1 | Vor dem Gespräch die Bewerberinnen und Bewerber spätestens mit der Einladung auf ihr Antragsrecht zur Beteiligung der Gleichstellungsbeauftragten hinweisen und deren Beteiligung am Vorstellungsgespräc … | **nein** |
| moegliche_luecke | T4.3 | BayPVG | Art. 69 Abs. 1 und 2 | Sicherstellen, dass der Personalrat rechtzeitig und umfassend unterrichtet wird und die für seine Aufgaben erforderlichen Unterlagen zu den Auswahlgesprächen erhält; gegebenenfalls dokumentierte Gespr … | **nein** |
| moegliche_luecke | T4.3 | SGB IX | § 164 Abs. 1 | Bei schwerbehinderten Bewerberinnen und Bewerbern die vorgeschriebenen Mitteilungen und Beteiligungen der Schwerbehindertenvertretung sowie die Anhörung der zuständigen Vertretungen sicherstellen und  … | S05 |
| moegliche_luecke | T5.1 | BayGlG | Art. 17 Abs. 2 und Abs. 3 Sätze 2 bis 4 | Vor Abschluss der Auswahlentscheidung die Gleichstellungsbeauftragte rechtzeitig und umfassend unterrichten und erforderliche Unterlagen frühzeitig vorlegen. Eine Beteiligung in Personalangelegenheite … | **nein** |
| moegliche_luecke | T5.1 | BayPVG | Art. 75 Abs. 1 Satz 1 Nr. 1 | Den Personalrat im vorgeschriebenen Beteiligungsverfahren zur Einstellung beteiligen, bevor die Einstellungsmaßnahme umgesetzt wird; die Beteiligung im Prozess nachvollziehbar vorsehen. | S26 |
| moegliche_luecke | T5.1 | BayPVG | Art. 69 Abs. 2 Sätze 1 bis 3 | Den Personalrat rechtzeitig und umfassend unterrichten, erforderliche Unterlagen bereitstellen und eine gegebenenfalls verlangte Vorlage von Bewerbungsunterlagen ermöglichen. | **nein** |
| moegliche_luecke | T5.1 | BayPVG | Art. 75a Abs. 1 Nr. 2 | Die Mitbestimmung des Personalrats zur Einführung oder Anwendung des automatisierten Verfahrens zur Personalverwaltung sicherstellen, soweit keine gesetzliche oder tarifliche Regelung besteht. | S20 |
| moegliche_luecke | T5.1 | SGB IX | § 164 Abs. 1 | Bei schwerbehinderten Bewerberinnen und Bewerbern die Schwerbehindertenvertretung und die in § 176 SGB IX genannten Vertretungen unmittelbar nach Bewerbungseingang unterrichten; sie bei der Prüfung de … | S05 |
| moegliche_luecke | T5.1 | DSGVO | Art. 22 Abs. 1 bis 4 | Sicherstellen und dokumentieren, dass die Auswahlentscheidung tatsächlich auf einer eigenständigen, substanziellen menschlichen Prüfung beruht und nicht ausschließlich auf dem automatisierten Ranking. … | **nein** |
| moegliche_luecke | T5.1 | DSGVO | Art. 35 Abs. 1 und Abs. 3 Buchst. a | Vor dem Einsatz der KI-gestützten Bewerberbewertung prüfen und, falls voraussichtlich ein hohes Risiko für Rechte und Freiheiten besteht, eine Datenschutz-Folgenabschätzung durchführen; im Prozess ist … | S18 |
| moegliche_luecke | T5.1 | KI-VO | Art. 26 Abs. 1, 2 und 4 | Falls das Tool ein Hochrisiko-KI-System ist, sicherstellen, dass es gemäß seiner Betriebsanleitung verwendet wird, eine zur menschlichen Aufsicht befähigte und ermächtigte Person eingesetzt und unters … | S14 |
| moegliche_luecke | T5.1 | KI-VO | Art. 27 Abs. 1 | Vor der erstmaligen Verwendung eines erfassten Hochrisiko-KI-Systems eine Grundrechte-Folgenabschätzung durchführen, sofern die Hochschule als Betreiberin in den Anwendungsbereich der Vorschrift fällt … | S15 |
| moegliche_luecke | T5.2 | NachwG | § 2 Abs. 1 Satz 1 und 7–9, Abs. 4 und 5 | Sicherstellen, dass dem Arbeitnehmer die Niederschrift mit sämtlichen erforderlichen Angaben innerhalb der gesetzlichen Fristen ausgehändigt wird. Die Prozessbeschreibung nennt den Vertragsabschluss,  … | **nein** |
| moegliche_luecke | T5.2 | BayPVG | Art. 75 Abs. 1 Satz 1 Nr. 1 und Nr. 3a; Art. 70 Abs. 1 und 2 | Die Mitbestimmung des Personalrats zur Einstellung und Eingruppierung vor der entsprechenden Maßnahme dokumentieren und das Zustimmungsverfahren durchführen. Ein Beteiligungsschritt des Personalrats i … | S26 |
| moegliche_luecke | T5.3 | BayPVG | Art. 78 Abs. 1 Satz 1 Nr. 6 und Abs. 3 | Vor dem Abschluss beziehungsweise Vollzug der Einstellung prüfen und dokumentieren, ob der Personalrat über die Einstellung informiert wurde. | **nein** |
| moegliche_luecke | T5.3 | SGB IX | § 165 Satz 1 und 3; § 178 Abs. 2 | Prüfen und dokumentieren, ob die Stelle nach erfolgloser interner Besetzungsprüfung frühzeitig der Agentur für Arbeit gemeldet wurde; bei Bewerbungen schwerbehinderter Menschen die Einladungs- und Bet … | S06,S22 |
| moegliche_luecke | T6.2 | DSGVO | Art. 5 Abs. 1 Buchst. e und Art. 17 Abs. 1 Buchst. a | Eine konkrete, begründete Aufbewahrungsdauer samt Beginn und Ende festlegen und dokumentieren; nach Fristablauf prüfen, ob die Bewerbungsdaten noch für einen zulässigen Zweck benötigt werden, und sie  … | **nein** |
| moegliche_luecke | T6.2 | DSGVO | Art. 5 Abs. 2 | Die festgelegte Aufbewahrungsdauer und ihre Erforderlichkeit nachvollziehbar dokumentieren, sodass die Hochschule die Einhaltung der Speicherbegrenzung nachweisen kann. | **nein** |
| moegliche_luecke | T6.2 | DSGVO | Art. 6 Abs. 1 und Abs. 3 | Für die fortgesetzte Speicherung während der Wartezeit die einschlägige Rechtsgrundlage und den dafür maßgeblichen Zweck festlegen und dokumentieren. | **nein** |
| moegliche_luecke | T6.2 | DSGVO | Art. 32 Abs. 1 | Für die Zeit der Aufbewahrung geeignete technische und organisatorische Schutzmaßnahmen sicherstellen, etwa angemessene Zugriffsbeschränkungen und Schutz vor unbefugter Verarbeitung oder Verlust. | **nein** |
| moegliche_luecke | T6.2 | BayDSG | Art. 26 Abs. 6 | Vor einer Löschung prüfen und gegebenenfalls dokumentieren, ob die Bewerbungsunterlagen einem öffentlichen Archiv zur Übernahme anzubieten sind; bei bestehender Anbietungspflicht erst nach dem Angebot … | **nein** |
| moegliche_luecke | T6.2 | BayArchivG | Art. 14 Abs. 1 und 2 | Klären, ob die Hochschule die Unterlagen in einem eigenen oder sonstigen öffentlichen Archiv archiviert. Falls nicht, nicht mehr benötigte Unterlagen dem zuständigen staatlichen Archiv zur Übernahme a … | **nein** |
| moegliche_luecke | T6.3 | DSGVO | Art. 5 Abs. 1 Buchst. e | Eine konkrete, begründete Aufbewahrungsfrist und ein eindeutiger Löschzeitpunkt für die jeweiligen Bewerbungsdaten festlegen und dokumentieren. Der Prozess nennt zwar eine Aufbewahrungsfrist, aber wed … | **nein** |
| moegliche_luecke | T6.3 | BayDSG / BayArchivG | Art. 26 Abs. 6 BayDSG; Art. 14 Abs. 1 und 2 BayArchivG | Vor der Löschung feststellen, ob die Bewerbungsunterlagen nach den für die Hochschule geltenden Archivierungsregelungen einem Archiv anzubieten sind; gegebenenfalls Anbietung und Entscheidung des Arch … | **nein** |

| Soll-Lücke | Regelwerk | Fundstelle | Inhalt | erkannt |
| --- | --- | --- | --- | --- |
| S05 | SGB IX | § 164 | Prüfung Besetzung freier Stellen mit schwerbehinderten Menschen, Kontakt Agentur für Arbeit | ja |
| S06 | SGB IX | § 165 | Meldung freier Stellen an die Agentur für Arbeit (öffentlicher Arbeitgeber) | ja |
| S14 | AI Act | Art. 26 Abs. 11 | Information der Betroffenen über den KI-Einsatz | ja |
| S15 | AI Act | Art. 27 | Grundrechte-Folgenabschätzung (öffentliche Stelle) | ja |
| S16 | AI Act | Art. 4 | KI-Kompetenz der Mitarbeitenden | ja |
| S18 | DSGVO | Art. 35 | Datenschutz-Folgenabschätzung | ja |
| S20 | BayPVG | Art. 75a | Mitbestimmung Personalrat bei Einführung des KI-Tools (Norm prüfen) | ja |
| S22 | SGB IX | § 178 | Beteiligung der Schwerbehindertenvertretung | ja |
| S26 | BayPVG | Art. 75 | Mitbestimmung Personalrat bei Einstellung (Norm prüfen) | ja |

## 5a. Material: Funde `nicht_in_soll` (manuell prüfen)

Automatisch gelistet; Begründung = Zitat aus der Rohantwort des Modells.

### 20261020-145929_A_1 (40 Funde)

| fund_id | Task | Regelwerk | Fundstelle | Sicherheit | Zitat Begründung |
| --- | --- | --- | --- | --- | --- |
| F001 | T1.1 | BayPVG | Art. 76 Abs. 3 Satz 1 | unsicher | Die Vorschrift greift bei der Weiterleitung von Personalanforderungen zum Haushaltsvoranschlag. Ob T1.1 eine solche Weiterleitung umfasst, ist aus der Beschreibung nicht ersichtlich. |
| F002 | T1.1 | BayHIG | Art. 11 Abs. 1 Satz 3 und 4 | sicher | Bei der Meldung des Personalbedarfs für eine Stelle sind der Aufgabenbedarf der Hochschule sowie die in Forschung und Lehre und bei der Förderung des wissenschaftlichen Nachwuchses erbrachten Leistungen als Maßstäbe für  … |
| F003 | T1.1 | BayHIG | Art. 11 Abs. 3 Satz 1 und Satz 5 | sicher | Die Hochschule bewirtschaftet Stellen und Mittel im Rahmen des Staatshaushalts nach den geltenden staatlichen Vorschriften und berücksichtigt bei ihrer Wirtschaftsführung die Grundsätze der Wirtschaftlichkeit und Sparsam … |
| F004 | T1.2 | BayHIG | Art. 71 Abs. 2 | sicher | Für eine wissenschaftliche Mitarbeiterin oder einen wissenschaftlichen Mitarbeiter im privatrechtlichen Arbeitsverhältnis gelten grundsätzlich die in Art. 71 Abs. 1 Satz 1 Nrn. 2 bis 4 genannten Qualifikationsvoraussetzu … |
| F005 | T1.2 | BayHIG | Art. 72 Abs. 2 Sätze 1 bis 6 | sicher | Wissenschaftlichen Mitarbeiterinnen und Mitarbeitern obliegen wissenschaftliche Dienstleistungen; hierzu können auch Lehre und – in bestimmten Bereichen – Tätigkeiten in der Krankenversorgung gehören. Die Aufgabenbeschre … |
| F017 | T2.1 | DSGVO | Art. 25 Abs. 1 und 2 | sicher | Das Bewerbungsportal ist so auszugestalten, dass Datenschutzgrundsätze bereits bei der Gestaltung umgesetzt werden und standardmäßig nur die für den Bewerbungszweck erforderlichen personenbezogenen Daten verarbeitet werd … |
| F019 | T2.1 | DSGVO | Art. 30 Abs. 1 | sicher | Die Hochschule muss als Verantwortliche ein Verzeichnis der Verarbeitungstätigkeiten führen. Die Prozessbeschreibung nennt keine entsprechende Dokumentation; sie kann allerdings außerhalb des operativen Bewerbungsablaufs … |
| F021 | T2.1 | DSGVO | Art. 28 Abs. 3 | unsicher | Die Nutzung eines Bewerbungsportals kann eine Auftragsverarbeitung einschließen; aus der Beschreibung geht nicht hervor, ob das Portal intern oder durch einen Auftragsverarbeiter betrieben wird. Der erforderliche Vertrag … |
| F022 | T2.1 | DSGVO | Art. 9 Abs. 1 und Abs. 2 Buchst. b | unsicher | Bewerbungsunterlagen können besondere Kategorien personenbezogener Daten enthalten, etwa Gesundheitsdaten oder Angaben zur Religionszugehörigkeit. Werden solche Daten tatsächlich verarbeitet, gilt grundsätzlich das Verar … |
| F028 | T2.2 | DSGVO | Art. 12 Abs. 1 | sicher | Soweit die Eingangsbestätigung Datenschutzinformationen oder Mitteilungen zu Betroffenenrechten enthält, müssen diese in präziser, transparenter, verständlicher und leicht zugänglicher Form sowie in klarer und einfacher  … |
| F035 | T2.3 | DSGVO | Art. 9 Abs. 1 und 2 | unsicher | Falls die gespeicherten Bewerbungsunterlagen besondere Kategorien personenbezogener Daten enthalten, etwa Gesundheitsdaten oder Angaben zur Gewerkschaftszugehörigkeit, ist deren Verarbeitung grundsätzlich untersagt, sofe … |
| F036 | T2.3 | DSGVO | Art. 25 Abs. 1 und 2 | sicher | Das Bewerbersystem ist so auszuwählen und einzurichten, dass Datenschutz bereits bei der Verarbeitung berücksichtigt wird. Voreinstellungen sollten insbesondere den Datenzugriff auf den erforderlichen Personenkreis und d … |
| F037 | T2.3 | DSGVO | Art. 28 Abs. 3 | unsicher | Der Prozess nennt ein Bewerbungsportal, lässt aber offen, ob ein externer Anbieter die Daten im Auftrag der Hochschule verarbeitet und ob ein Auftragsverarbeitungsvertrag besteht. |
| F038 | T2.3 | DSGVO | Art. 29 | sicher | Beschäftigte, die Bewerberdaten im System anlegen oder darauf zugreifen, dürfen diese grundsätzlich nur auf Weisung des Verantwortlichen und im Rahmen ihrer Zugriffsberechtigung verarbeiten. |
| F039 | T2.3 | DSGVO | Art. 30 Abs. 1 | sicher | Der Verantwortliche muss ein Verzeichnis der Verarbeitungstätigkeiten führen. Ein entsprechender Schritt ist im beschriebenen Prozess nicht genannt. |
| F045 | T3.1 | DSGVO | Art. 9 Abs. 1 und Abs. 2 Buchst. b | unsicher | Falls die Auswertung besondere Kategorien personenbezogener Daten verarbeitet, etwa Gesundheits- oder Behinderungsangaben, gilt grundsätzlich das Verarbeitungsverbot des Art. 9 Abs. 1. Eine Ausnahme muss einschlägig sein … |
| F049 | T3.1 | DSGVO | Art. 24 und Art. 25 Abs. 1 und 2 | sicher | Die Hochschule muss angemessene technische und organisatorische Maßnahmen zur DSGVO-konformen Verarbeitung festlegen und nachweisen. Das KI-Verfahren ist so auszugestalten, dass Datenschutzgrundsätze bereits bei der Gest … |
| F050 | T3.1 | DSGVO | Art. 28 Abs. 1 und 3 | unsicher | Der Prozess nennt ein KI-Tool, lässt aber offen, ob ein Dienstleister Bewerberdaten verarbeitet. Bei Auftragsverarbeitung darf die Hochschule nur einen hinreichend geeigneten Auftragsverarbeiter einsetzen; die Verarbeitu … |
| F051 | T3.1 | DSGVO | Art. 30 Abs. 1 | sicher | Die regelmäßige Verarbeitung im Bewerbungsverfahren ist nicht als gelegentlich beschrieben; außerdem kann sie besondere Daten oder ein Risiko für Rechte und Freiheiten betreffen. Das Verzeichnis nach Art. 30 ist im Proze … |
| F058 | T3.1 | KI-VO | Art. 49 Abs. 3 | unsicher | Für Betreiber, die öffentliche Stellen sind, sieht die KI-VO bei den erfassten Hochrisiko-KI-Systemen eine Registrierung vor der Inbetriebnahme oder Nutzung vor. Eine Registrierung ist im Prozess nicht erwähnt. |
| F059 | T3.1 | KI-VO | Art. 86 Abs. 1 | unsicher | Wenn eine auf Grundlage der Ausgaben des Hochrisiko-KI-Systems getroffene Entscheidung rechtliche oder ähnlich erhebliche Auswirkungen hat und die betroffene Person die gesetzlich genannten Voraussetzungen erfüllt, beste … |
| F076 | T3.2 | KI-VO | Art. 86 Abs. 1 | unsicher | Das Erläuterungsrecht greift, wenn eine Entscheidung auf der Ausgabe eines Hochrisiko-Systems beruht und rechtliche oder ähnlich erhebliche Auswirkungen hat. Ob ein bloßes Ranking mit anschließender wirksamer menschliche … |
| F099 | T3.4 | DSGVO | Art. 9 Abs. 1 und Abs. 2 | unsicher | Falls die Shortlist-Verarbeitung besondere Kategorien personenbezogener Daten enthält oder solche Daten aus Bewerbungsunterlagen ableitet, ist deren Verarbeitung grundsätzlich untersagt, sofern keine einschlägige Ausnahm … |
| F128 | T4.3 | DSGVO | Art. 9 Abs. 1 und Abs. 2 | sicher | Falls Gesprächsnotizen besondere Kategorien personenbezogener Daten festhalten, etwa Gesundheitsdaten oder Angaben zur Religion, ist deren Verarbeitung grundsätzlich untersagt, sofern keine Ausnahme nach Art. 9 Abs. 2 gr … |
| F135 | T4.3 | BayPVG | Art. 69 Abs. 1 und 2 | sicher | Der Personalrat hat Aufgaben unter anderem bei der Gleichbehandlung im Beschäftigungs- und Einstellungsverfahren und ist zu deren Durchführung rechtzeitig und umfassend zu unterrichten; erforderliche Unterlagen sind ihm  … |
| F142 | T5.1 | BayPVG | Art. 69 Abs. 2 Sätze 1 bis 3 | sicher | Die Prozessbeschreibung nennt keine Unterrichtung des Personalrats oder Bereitstellung der für seine Aufgaben erforderlichen Unterlagen im Auswahl- und Einstellungsverfahren. |
| F157 | T5.2 | BGB | § 145; § 147 Abs. 2; § 148; § 150 Abs. 2 | sicher | Wird das Vertragsangebot als Antrag abgegeben, ist die Hochschule grundsätzlich daran gebunden, sofern die Bindung nicht ausgeschlossen wird. Für ein Angebot an eine abwesende Person gilt ohne festgelegte Frist die Annah … |
| F158 | T5.2 | BGB | § 611a Abs. 1 und 2 | sicher | Das Angebot muss die vorgesehene Beschäftigung als Arbeitsverhältnis mit weisungsgebundener Arbeit und vereinbarter Vergütung abbilden. Die Bezeichnung im Angebot ist nicht entscheidend, wenn die tatsächliche Durchführun … |
| F159 | T5.2 | BayHIG | Art. 72 Abs. 1 Satz 2 und Abs. 2 | sicher | Wissenschaftliche Mitarbeiterinnen und Mitarbeiter werden, insbesondere bei vorgesehener befristeter Tätigkeit, im privatrechtlichen Arbeitsverhältnis beschäftigt; ihnen obliegen wissenschaftliche Dienstleistungen. Das i … |
| F160 | T5.2 | TzBfG | § 14 Abs. 1, 2 und 4; gegebenenfalls § 15 Abs. 3 | unsicher | Falls das Angebot eine Befristung vorsieht, muss die Befristung auf eine gesetzlich zulässige Grundlage gestützt und zu ihrer Wirksamkeit schriftlich vereinbart werden. Bei vereinbarter Probezeit in einem befristeten Arb … |
| F161 | T5.2 | WissZeitVG | § 1 Abs. 1 und 2; § 2 Abs. 1, 2 und 4 | unsicher | Falls eine Befristung nach dem Wissenschaftszeitvertragsgesetz vorgesehen ist, müssen die jeweiligen Voraussetzungen und Befristungsgrenzen geprüft werden. Im Arbeitsvertrag ist anzugeben, ob die Befristung auf diesem Ge … |
| F167 | T5.3 | BGB | § 126 Abs. 1 und 2 | sicher | Für die tariflich verlangte Schriftform ist die gesetzliche Schriftform maßgeblich. Sie erfordert grundsätzlich eine eigenhändige Unterschrift; bei einem Vertrag müssen beide Parteien auf derselben Urkunde unterschreiben … |
| F168 | T5.3 | BGB | §§ 145 und 147; § 611a Abs. 1 und 2 | sicher | Der Vertragsschluss setzt ein wirksames Angebot und dessen rechtzeitige Annahme voraus. § 611a beschreibt die arbeitsvertraglichen Hauptpflichten: weisungsgebundene Arbeit in persönlicher Abhängigkeit und die Pflicht des … |
| F175 | T5.3 | TzBfG | § 14 Abs. 1 und 4 | sicher | Nur falls der Arbeitsvertrag befristet geschlossen werden soll: Die Befristung benötigt eine gesetzliche Grundlage; § 14 Abs. 1 regelt sachgrundgestützte Befristungen. Zu ihrer Wirksamkeit bedarf die Befristung der Schri … |
| F176 | T5.3 | WissZeitVG | § 1 Abs. 1 und 2; § 2 Abs. 1, 2 und 4 | sicher | Nur falls die wissenschaftliche Stelle befristet besetzt wird und die Hochschule die Befristung auf das WissZeitVG stützen will: Es muss geprüft werden, ob die Beschäftigung und der Befristungsgrund die Voraussetzungen d … |
| F177 | T5.3 | BayPVG | Art. 78 Abs. 1 Satz 1 Nr. 6 und Abs. 3 | sicher | Art. 78 Abs. 1 Satz 1 Nr. 6 nimmt wissenschaftliche Mitarbeiterinnen und Mitarbeiter im Sinne des Art. 74 BayHIG grundsätzlich von den dort genannten Beteiligungsrechten, darunter der Mitbestimmung nach Art. 75 Abs. 1, a … |
| F188 | T6.2 | DSGVO | Art. 18 Abs. 1 Buchst. c und Abs. 2 | sicher | Verlangt eine betroffene Person eine Einschränkung, weil die Hochschule die Daten für ihre Zwecke nicht mehr benötigt, die Person sie aber zur Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen benötigt, kan … |
| F191 | T6.2 | BayArchivG | Art. 14 Abs. 1 und 2 | sicher | Für staatliche Hochschulen und staatlich beaufsichtigte juristische Personen des öffentlichen Rechts sieht Art. 14 je nach Archivierungsmodell eigene Archivierung oder die Anbietung nicht mehr benötigter Unterlagen an da … |
| F195 | T6.3 | DSGVO | Art. 18 Abs. 1 Buchst. c | sicher | Verlangt eine betroffene Person eine Einschränkung statt einer Löschung, weil sie die Daten zur Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen benötigt, sind die Daten unter den Voraussetzungen des Artik … |
| F196 | T6.3 | DSGVO | Art. 19 | sicher | Wurden Bewerberdaten offengelegt, muss die Hochschule Empfänger über eine Löschung nach Art. 17 Abs. 1 informieren, soweit dies nicht unmöglich oder mit unverhältnismäßigem Aufwand verbunden ist. Das kann insbesondere Da … |

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
