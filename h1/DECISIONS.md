# Entscheidungen (H1)

Stand 20.10.2026. Alles, was `ANWEISUNG_H1.md` offen lässt, ist hier mit Begründung festgehalten.

## Modell und API

1. **Modell-Snapshot `gpt-6-luna`.** Die OpenAI-Modellseite (developers.openai.com/api/docs/models/gpt-6-luna,
   abgerufen 20.10.2026) listet für GPT-6 Luna keinen datierten Snapshot; einziger Snapshot ist `gpt-6-luna`.
   Sobald ein datierter Snapshot erscheint, in `config.yaml` eintragen. Der tatsächlich verwendete Modellname
   steht zusätzlich in jeder Rohantwort (`raw/*.json`, Feld `model`).
2. **Preise** (config.yaml): 0,10 USD/Mio. Input, 0,01 USD/Mio. Cached Input, 0,50 USD/Mio. Output
   (Modellseite); Cache-Write 0,125 USD/Mio. (Drittquelle); Websuche 10 USD/1000 Aufrufe (**Annahme**, auf der
   OpenAI-Preisseite prüfen). Kosten sind daher als „geschätzt“ gekennzeichnet.
3. **Structured Outputs** über `client.responses.parse(text_format=<Pydantic-Modell>)`; das SDK erzeugt daraus
   das strikte JSON-Schema. Stufe 2 liefert `{"funde": [...]}`; `run_id`, `fund_id`, `task_id` ergänzt das Programm.
4. **Websuche:** `{"type": "web_search", "filters": {"allowed_domains": [...]}}` mit den vier Domains;
   Subdomains sind laut API mit erlaubt. Mit `include=["web_search_call.action.sources"]` werden die aufgerufenen
   Quellen in den Rohantworten gespeichert.
5. **Retry:** bis zu 4 Versuche bei Verbindungsfehlern, Timeouts, Rate-Limits, 5xx und nicht parsebarer Ausgabe
   (Wartezeit 10 s × Versuch). Authentifizierungs- und Anfragefehler (4xx) werden nicht wiederholt.
   Scheitert ein einzelner Stufe-2-Task endgültig, läuft der Lauf weiter; der Task steht in `protokoll.json`.
   Scheitert Stufe 1, wird der Lauf abgebrochen (Ordner bleibt mit `meta.json`/`protokoll.json` erhalten).
6. **Parallelität:** Stufe-2-Aufrufe laufen mit bis zu 4 parallelen Aufrufen (`max_parallel`), um die Laufzeit
   zu begrenzen. Die Aufrufe sind voneinander unabhängig; Reihenfolge der Funde bleibt die Task-Reihenfolge.

## Prompts

7. Die Prompt-Texte sind wörtlich aus der Anweisung übernommen. Einzige technische Änderung: Die Domainliste wird
   über den Platzhalter `{domains}` aus `config.yaml` eingesetzt (gleicher Text), JSON-Klammern im Stufe-1-Prompt
   sind für `str.format` verdoppelt. `prompt_hash_*` ist der SHA-256 der Vorlagendatei (nicht des gefüllten Prompts).
8. `{prozess}` wird als eingerückte Liste „TPx: Name / Tx.y: Name“ eingesetzt, Firmenprofil und Rechtsrahmen als JSON.
9. Konfiguration B: Rechtsrahmen = `[{"regelwerk": "<Kurzform>"}, ...]` aus der Soll-Liste (10 Regelwerke),
   gespeichert als `rechtsrahmen_vorgabe.json`; `prompt_hash_stufe1 = null`. Für die Lückenkandidaten gilt diese
   Liste als „Regelwerke aus Stufe 1“.

## Soll-Liste (`input/soll_liste.csv`) – vom Autor zu prüfen

Allgemein: Jede Soll-Zeile hat genau eine `task_id`. Wo die Tabelle mehrere Normen nennt (§§ 7, 11 AGG; §§ 164,
165 SGB IX; TV-L, NachwG), ist je Norm eine Zeile angelegt. `fundstelle` bleibt leer, wo die Tabelle nur das
Regelwerk nennt (dann zählt jede Norm dieses Regelwerks am richtigen Task als korrekt).

| soll_id | Entscheidung | Begründung |
| --- | --- | --- |
| S01 | GG Art. 33 Abs. 2 → GESAMT | laut Tabelle prozessweit |
| S02, S03 | AGG § 7, § 11 → T1.3 | Ausschreibung wird bei der Veröffentlichung wirksam (§ 11 verweist auf § 7) |
| S04 | TV-L → T1.2 | Eingruppierung ist Teil von T1.2 |
| S05, S06 | SGB IX § 164, § 165 → LUECKE | „Lücke (ungeplant)“ |
| S07 | BayGlG (ohne Norm) → T1.3 | Vorgaben zur Ausschreibung; konkrete Norm bitte ergänzen |
| S08 | DSGVO Art. 6 → T2.1 | „Rechtsgrundlage (genaue Norm prüfen)“: Art. 6 als Platzhalter, Absatz offen; Verarbeitung beginnt mit Empfang. Art. 88 DSGVO wäre ebenfalls denkbar → bisher `nicht_in_soll` |
| S09 | BayDSG (ohne Norm) → T2.1 | bayer. Landesrecht laut Tabelle, Norm offen |
| S10, S11 | DSGVO Art. 13, Art. 32 → T2.1 | Information bei Erhebung, Sicherheit des Portals – beides beim Empfang über das Portal |
| S12 | AI Act Anhang III Nr. 4 → T3.1 | Einstufung beim Einsatz des Tools |
| S13 | AI Act Art. 26 → T3.3 | menschliche Aufsicht = Prüfung durch Fachabteilung; Protokollierung (Art. 26 Abs. 6) wäre eher T3.2, nur eine Zeile laut Tabelle |
| S14 | AI Act **Art. 26 Abs. 11** → LUECKE | Tabelle nennt nur „Art. 26“; Abs. 11 (Information der Betroffenen) ergänzt, damit sich S14 von S13 unterscheidet |
| S15, S16, S18 | AI Act Art. 27, Art. 4; DSGVO Art. 35 → LUECKE | laut Tabelle |
| S17 | DSGVO Art. 22 → T3.4 | Entscheidung „Shortlist“ ist der Punkt, an dem eine ausschließlich automatisierte Entscheidung drohen würde |
| S19 | AGG (ohne Norm) → T3.1 | algorithmische Benachteiligung bei der Auswertung |
| S20 | BayPVG **Art. 75a** → LUECKE | „Norm prüfen“: Vorschlag Art. 75a Abs. 1 Nr. 1 BayPVG (technische Einrichtungen) |
| S21 | SGB IX § 165 → T4.1 | Einladung schwerbehinderter Bewerber |
| S22 | SGB IX § 178 → LUECKE | „Lücke (ungeplant)“ |
| S23 | BayGlG (ohne Norm) → T4.2 | Kontrolle: vorhandener Schritt |
| S24 | AGG (ohne Norm) → T4.2 | zulässige Fragen im Gespräch |
| S25 | DSGVO Art. 5 Abs. 2 → T4.3 | Dokumentation |
| S26 | BayPVG **Art. 75** → LUECKE | „Norm prüfen“: Vorschlag Art. 75 Abs. 1 Nr. 1 BayPVG (Einstellung). Hinweis: Art. 78 BayPVG schränkt die Mitbestimmung bei wiss. Personal ggf. ein (nur auf Antrag) – fachlich prüfen |
| S27, S28 | TV-L, NachwG → T5.3 | Vertrag und Nachweis beim Vertragsschluss |
| S29 | AGG § 15 Abs. 4 → T6.2 | Aufbewahrungsfrist |
| S30 | DSGVO Art. 17 → T6.3 | Löschung |

Entfallen: Art. 44 ff. DSGVO (Drittland, `dienstleister_ausserhalb_eu = false`), Art. 6 Abs. 1 lit. a DSGVO (Talentpool).
BayPVG-Zeilen bekamen Normen statt leerer Fundstelle, weil zwei leere BayPVG-Lücken sonst von jeder BayPVG-Meldung
gleichzeitig getroffen würden.

## Auswertung (`src/evaluate.py`, `src/normierung.py`)

10. **Zusätzliche Datei `src/normierung.py`** (nicht in der Ordnerliste der Anweisung): Normierung wird von
    `stufe2.py` (Lückenkandidaten) und `evaluate.py` gebraucht; eine gemeinsame Datei vermeidet Doppelcode.
11. **Regelwerk-Normierung:** Musterliste für die 10 Soll-Regelwerke (Kurzform oder Titel, z. B. „DS-GVO“,
    „Verordnung (EU) 2016/679“, „KI-VO“ → DSGVO / AI Act). Unbekannte Regelwerke (z. B. BDSG, BayHIG) bleiben
    unverändert und zählen in Stufe 1 als „zusätzlich“.
12. **Fundstellen-Normierung** (ersetzt durch Punkt 22): erste erkannte Norm zählt (`§§ 164, 165` → § 164; `Art. 44 ff.` → Art. 44).
    Absatz aus „Abs. n“ oder „(n)“; bei Anhängen gilt „Nr. n“ als Absatz. Satz/lit./Nr. unterhalb des Absatzes werden ignoriert.
13. **Bewertung je Fund (`typ = zuordnung`)**: Kandidaten = Soll-Zeilen mit gleichem Regelwerk und gleichem
    Artikel/Paragraf (oder leerer Soll-Fundstelle). Keine → `nicht_in_soll`. Passende Zeile (`zuordnung`, gleicher
    Task oder `GESAMT`) mit gleichem oder leerem Soll-Absatz → `korrekt`; sonst mit abweichendem/fehlendem Absatz
    → `falscher_absatz`; sonst (anderer Task oder Soll-Zeile ist eine Lücke) → `falscher_task`.
    Ein Fund ohne Absatz gegen eine Soll-Zeile mit Absatz zählt als `falscher_absatz`.
14. **Bewertung je Fund (`typ = moegliche_luecke`)**: gleiche Regeln, aber gegen Soll-Zeilen mit `typ = luecke`
    (Task egal). Trifft die Meldung nur eine vorhandene Zuordnung → `falscher_task` (= falsche Lückenmeldung).
15. **Stufe 2 Recall** = Anteil der Soll-Zeilen mit `typ = zuordnung`, die von mindestens einem `korrekt`-Fund getroffen
    werden. **Präzision** = Anteil `korrekt` an allen Funden mit `typ = zuordnung`. Je Teilprozess nach Task des Funds
    bzw. der Soll-Zeile; `GESAMT` (S01) als eigene Gruppe nur im Recall.
16. **H1b:** Lückenkandidaten = Regelwerke aus Stufe 1 ohne `zuordnung`-Fund + alle `moegliche_luecke`-Funde.
    Ein Kandidat trifft eine Soll-Lücke bei gleichem Regelwerk und gleichem Artikel/Paragraf; Kandidaten ohne
    Fundstelle (Regelwerk ohne Zuordnung) treffen alle Soll-Lücken ihres Regelwerks (großzügig, nur Regelwerksebene).
    Absatz wird bei Lücken nicht verlangt. Falsche Lückenmeldungen werden nach (Regelwerk, Artikel/Paragraf)
    dedupliziert, weil dieselbe Lücke oft bei mehreren Tasks gemeldet wird. „Gleichstellung“ = Kandidat mit
    Regelwerk BayGlG oder dem Wort „Gleichstellungsbeauftragte“ in Regelwerk/fehlendem Schritt/Begründung.
17. `anteil_unsicher` und `anteil_nicht_in_soll` beziehen sich auf alle Funde eines Laufs (inkl. Lücken-Funde).
18. `kennzahlen.csv`: eine Zeile je Lauf (`ebene = lauf`) und je Konfiguration Mittelwert und Standardabweichung
    (`ebene = konfig`, Stichproben-Std, leer bei n = 1).
19. `ERGEBNIS.md`: Abschnitte 1–4 und eine Materialliste 5a (alle `nicht_in_soll`-Funde mit Zitat der Begründung)
    erzeugt `evaluate.py`; Abschnitte 5–8 ab `<!-- MANUELL START -->` werden manuell gepflegt und beim erneuten Auswerten übernommen.

## Docker / Repo

20. Container-User `app` mit UID/GID 1000 (per Build-Arg änderbar), damit `runs/` und `results/` auf dem Host
    dem SSH-Nutzer gehören. `config.yaml` wird zusätzlich nur lesend gemountet.
21. Git-Remote auf SSH umgestellt (`git@github.com:...`), da das HTTPS-Token des Rechners ungültig ist.

## Nachtrag nach Testlauf A_1 (20.10.2026)

22. **Mehrere Normen je Fund:** Das Modell nennt oft mehrere Normen in einer Fundstelle („Art. 6 Abs. 2 und 3,
    Anhang III Nr. 4“, „§§ 145 und 147; § 611a“) und teils mehrere Regelwerke („DSGVO / BayDSG“). Ersetzt Punkt 12:
    Jede Norm wird einzeln bewertet (`zerlege_fund` in `src/normierung.py`); es zählt die beste Bewertung, und alle
    korrekt getroffenen Soll-Zeilen gelten als gefunden. Absatzlisten/-bereiche („Abs. 1, 2 und 5“, „Abs. 1–4“)
    werden als Menge gelesen; „korrekt“, wenn der Soll-Absatz darin enthalten ist. Bei `;`-Abschnitten mit eigenem
    Regelwerksnamen gilt dieses Regelwerk.
23. **Zusatzkennzahl `s2_recall_inkl_luecke`:** zählt Soll-Zuordnungen auch dann als gefunden, wenn das Modell die
    Norm am richtigen Task als `moegliche_luecke` meldet. Die Hauptkennzahl `s2_recall` bleibt wie in der Anweisung.
24. **Soll-Liste nicht verändert**, obwohl der Lauf fachliche Zweifel an S26 (Art. 78 BayPVG) und an der
    Gleichstellungs-Kontrolle (Art. 17 Abs. 3 BayGlG) zeigt. Die Entscheidung liegt beim Autor (siehe ERGEBNIS.md, Abschnitt 7).

## v2 (Auftrag 002, 21.10.2026)

25. **Version:** `config.yaml` hat den Schlüssel `version: v2`; `meta.json` speichert ihn als `version`. In
    `runs/20261020-145929_A_1/meta.json` ist `version: v1` nachgetragen (einzige Änderung an alten Läufen). Fehlt
    `version` in einer `meta.json`, gilt `v1`.
26. **Schema:** `FundLLM.hinweis: str | None` („fehlendes Detail an diesem Task, sonst null“), landet in `funde.jsonl`.
    Für A_1 (ohne Feld) setzt die Auswertung `hinweis = null`.
27. **Konfiguration B, Rechtsrahmen:** nur Regelwerke aus Soll-Zeilen mit `typ` zuordnung oder luecke (12, ohne BayHIG).
    Grund: B soll den Soll-Rechtsrahmen von Stufe 1 vorgeben; Neutral-Regelwerke gehören nicht dazu.
28. **Normierung:** Muster für WissZeitVG, TzBfG und BayHIG ergänzt. Regelwerk-Listen werden nicht mehr an „und“
    nach Bindestrich getrennt („Teilzeit- und Befristungsgesetz“ bleibt ein Regelwerk).
29. **Mehrere Tasks je Soll-Zeile:** `task_id` wird an `|` getrennt. Ein `zuordnung`-Fund trifft eine Soll-Zeile, wenn
    sein Task in der Liste steht oder die Zeile `GESAMT` ist. Teilprozess der Soll-Zeile = der des ersten Tasks.
30. **Neutral (Zuordnungen):** Rangfolge je Norm `korrekt` > `neutral` > `falscher_absatz` > `falscher_task` >
    `nicht_in_soll`. Neutral passt bei gleichem Regelwerk und gleichem Artikel/Paragraf (leere Soll-Fundstelle passt
    auf jede Norm des Regelwerks), auf jeden Task; hat die Neutral-Zeile einen Absatz, muss er unter den Absätzen
    des Funds sein. Eine Neutral-Zeile mit abweichendem Absatz ist kein Kandidat: Gibt es keine andere passende
    Zeile, ist der Fund `nicht_in_soll`. Präzision = korrekt / (alle Zuordnungen ohne neutral); `s2_anteil_neutral`
    separat.
31. **Lückenkategorien je `moegliche_luecke`-Fund:** `luecke_korrekt` > `luecke_neutral` >
    `luecke_an_vorhandener_zuordnung` > `luecke_ohne_soll`. Neutral steht vor „an vorhandener Zuordnung“, weil
    der Auftrag diese Kategorie auf Meldungen beschränkt, die *nur* eine Soll-Zuordnung treffen.
    Zuordnungs-Zeilen werden dabei unabhängig vom Task geprüft. **Absatz bei Lücken:** geprüft nur, wenn Soll-Zeile
    und Meldung beide einen Absatz nennen (Meldung „Art. 26“ trifft S14 „Art. 26 Abs. 11“, Meldung „Art. 26 Abs. 7“
    nicht). In v1 wurde der Absatz bei Lücken nie geprüft. Die neue Regel ist etwas strenger, damit eine Meldung
    zu einem anderen Absatz nicht als Treffer zählt.
32. **Deduplizierung:** Lückenmeldungen eines Laufs werden nach (Regelwerk, erster Artikel/Paragraf) gruppiert; die
    Gruppe erhält die beste Kategorie ihrer Meldungen. `falsche_luecken` = Gruppen mit `luecke_an_vorhandener_zuordnung`
    oder `luecke_ohne_soll`. Gezählt werden in v2 nur `moegliche_luecke`-Funde. Regelwerke aus Stufe 1 ohne
    Zuordnung gehen nur in `luecken_recall_grosszuegig` ein und werden als `regelwerke_ohne_zuordnung` gezählt,
    nicht als falsche Lückenmeldung, weil sie keine Aussage über einen fehlenden Schritt machen.
33. **H1b-Recall:** `luecken_recall` (Hauptkennzahl) = Soll-Lücken, die eine `luecke_korrekt`-Meldung trifft.
    `luecken_recall_grosszuegig` zählt zusätzlich alle Soll-Lücken eines Regelwerks aus Stufe 1 (B: Vorgabe), dem
    in Stufe 2 kein `zuordnung`-Fund zugeordnet ist. Diese Regelwerke berechnet die Auswertung neu aus `stufe1.json`
    bzw. `rechtsrahmen_vorgabe.json` und `funde.jsonl` (nicht aus `lueckenkandidaten.json`), damit alle Läufe mit
    derselben Normierung bewertet werden.
34. **Kontrolle Gleichstellungsbeauftragte:** `kontrolle_fehlmeldungen` = Anzahl deduplizierter Lückenmeldungs-Gruppen,
    deren Normen S23 (BayGlG Art. 17) als Soll-Zuordnung treffen. Die Stichwortsuche aus v1 entfällt.
35. **Stufe 1:** Soll-Regelwerke = Zeilen mit `typ` zuordnung/luecke (12). Regelwerke nur aus Neutral-Zeilen (BayHIG)
    werden als `s1_neutral` ausgewiesen und zählen nicht in der Präzision (Nenner = genannte Regelwerke ohne neutral).
36. **`anteil_nicht_in_soll`** = Anteil der Funde mit `nicht_in_soll` oder `luecke_ohne_soll` an allen Funden.
    Neu: `anteil_hinweis` = Anteil der Zuordnungen mit gefülltem `hinweis`.
37. **Gruppierung:** Kennzahlen je (`version`, `konfig`); `kennzahlen.csv` hat die Spalte `version`. Alle Läufe
    (auch A_1) werden gegen die aktuelle Soll-Liste ausgewertet.
38. **ERGEBNIS.md, automatischer Teil:** Bei 11 Läufen wären die Einzellisten aus v1 zu lang. Abschnitte 2–4 und 5a
    zeigen daher Mittelwert ± Std je Gruppe und Häufigkeiten über die Läufe („in wie vielen Läufen gefunden“). Die
    Einzelheiten je Lauf stehen in `kennzahlen.csv`, `funde_bewertet.csv`, `uebersehen.csv` und der neuen Datei
    `luecken_bewertet.csv` (deduplizierte Lückenmeldungen je Lauf mit Kategorie).
39. **Laufnummern:** Die Nummer zählt je Konfiguration über alle Versionen weiter. Die v2-Läufe A heißen daher
    `A_2` bis `A_6`, die v2-Läufe B `B_1` bis `B_5`.

## v3 (Auftrag 003, 21.10.2026)

40. **EUR-Lex über Cellar:** `eur-lex.europa.eu` beantwortet Anfragen ohne Browser mit einer AWS-WAF-Challenge
    (HTTP 202, `x-amzn-waf-action: challenge`). Die Challenge umgehe ich bewusst nicht. EU-Rechtsakte kommen deshalb
    über die offizielle maschinelle Schnittstelle desselben Herausgebers (Amt für Veröffentlichungen, Cellar):
    `publications.europa.eu/resource/celex/<CELEX>` (XHTML, deutsch) und dessen SPARQL-Endpunkt für die Titelsuche und
    die neueste konsolidierte Fassung (`0JJJJRNNNN-JJJJMMTT`). Dem Modell gebe ich als `quelle_url` die kanonische
    EUR-Lex-URL desselben CELEX-Dokuments (mit Anker `#art_N`). `publications.europa.eu` ist deshalb technisch als
    fünfte Domain freigegeben, aber nur als Backend von EUR-Lex.
41. **EU-Abkürzungen** (DSGVO, AI Act, KI-VO) stehen nicht in den amtlichen Titeln. Ohne fest eingebaute Liste löst
    das Werkzeug sie nicht auf und meldet „nicht gefunden“ mit dem Hinweis, EU-Rechtsakte als
    „Verordnung (EU) JJJJ/NNNN“ anzugeben. Über Titelwörter (z. B. „Datenschutz-Grundverordnung“, „künstliche
    Intelligenz“) findet `suche_regelwerk` sie. CELEX-Regel: `3` + Jahr + `R` (Verordnung) bzw. `L` (Richtlinie) +
    vierstellige Nummer.
42. **Bund:** Auflösung über `gii-toc.xml`. Die Abkürzung wird in Slug-Form gebracht (Kleinschreibung, Leerzeichen →
    `_`, römische Zahlen → arabisch: „SGB IX“ → `sgb_9`); trifft das nicht genau, wird ein Slug mit Jahreszusatz
    (`bdsg_2018`, `sgb_9_2018`) genommen, sonst die Titelsuche (alle Wörter im Titel). Normtexte aus `xml.zip`,
    Fassung aus `standangabe`.
43. **Bayern:** Die Abkürzung wird direkt als Dokument geprüft (`/Content/Document/<Abk>`, Seite muss „(<Abk>)“
    enthalten). Normtexte kommen aus der Gesamtansicht `/Content/Document/<Abk>/true`. `suche_regelwerk` nutzt das
    Suchformular der Seite (Token und Sitzungscookie), gefiltert auf „Gesetze“, danach auf „Vorschriften“; die
    Abkürzung ist das Präfix der Dokument-ID. Suchergebnisse werden je Stichwort gecacht.
44. **TV-L:** Das PDF wird über die Seite `tdl-online.de/tarifvertraege/tv-l` gefunden (Link `TV-L__i.d.F.…pdf`),
    mit `pypdf` gelesen und an Zeilen, die nur „§ N“ enthalten, in Paragrafen zerlegt (Überschrift = folgende
    Zeile). Anlagen (Entgeltordnung) werden nicht zerlegt; andere Tarifverträge liefern „nicht gefunden“.
45. **Auflösungsreihenfolge** (`Werkzeuge.kennung`): EU-Nummer → TV-L → Bund-Slug → Bayern-Abkürzung →
    Bund-Titelsuche → EU-Titelsuche. Grund: Abkürzungen sind eindeutiger als Titelwörter.
46. **Cache:** `h1/cache/<domain>/<sha1>.bin` + `.meta.json` (URL, Status, Abrufdatum), ohne Ablaufzeit, damit alle
    Läufe auf denselben Textstand zugreifen. Ausnahme: Suchformular-Abrufe von gesetze-bayern.de (Token) werden
    nicht gecacht, nur das Suchergebnis. `cache/tdl-online.de/` ist in `.gitignore`.
47. **Höflicher Abruf:** höchstens 1 Anfrage/s je Domain (Lock je Domain), User-Agent laut Auftrag. Die Quellen
    einer `suche_regelwerk`-Anfrage und die Werkzeugaufrufe einer Runde laufen parallel; das betrifft nur
    verschiedene Domains. Die Bayern-Suche läuft unter einem eigenen Lock (Formular und Ergebnisseite in einer Sitzung).
48. **Kürzung:** Rückgaben über 6000 Zeichen werden gekürzt (`text` bzw. Listen werden gekürzt, `"gekuerzt": true`).
49. **Schleife (llm_client):** `previous_response_id` und `function_call_output`. Die Aufrufe einer Antwort werden
    bis zum Limit ausgeführt; darüber hinaus bekommen sie `{"fehler": "Werkzeuglimit erreicht"}`. Ist das Limit
    erreicht, wird einmal mit `tool_choice: none` und der Aufforderung zur Endantwort nachgefragt; das steht in
    `protokoll.json` (`werkzeuglimit_erreicht`). Ohne parsebare Endantwort wird der ganze Aufruf wiederholt
    (bis `max_retries`); die Werkzeugprotokolle tragen dafür die Felder `versuch` und `runde`.
50. **Kostenkontrolle:** Vor jedem API-Aufruf wird geschätzt: (bisheriger Kontext + neue Werkzeugausgaben/3)
    Input-Tokens + 6000 Output-Tokens. Geprüft wird gegen `budget.yaml` (Summe aus `kosten/verbrauch.csv` seit
    Stichtag) und gegen `budget_usd_lauf`. Bei parallelen Tasks können bis zu 4 Aufrufe gleichzeitig die Prüfung
    bestehen; die mögliche Überschreitung liegt im Bereich von Cent. `insufficient_quota` bzw.
    `credit_balance_exhausted` → sofortiger Abbruch ohne Retry. Abgebrochene Läufe (Guthaben/Budget) werden nach
    `runs_ungueltig/` verschoben.
51. **Auftragsbudget:** Ein neuer Lauf startet nur, wenn Summe der Kosten aller Läufe dieser Version (gültig und
    ungültig) + Schätzung ≤ `budget_usd_auftrag`. Schätzung = teuerster bisheriger Lauf der Version, ohne
    bisherige Läufe `budget_usd_lauf`.
52. **Costs-API:** Ist `OPENAI_ADMIN_KEY` gesetzt, wird nach jedem Lauf `/v1/organization/costs` (Tagesbuckets ab
    Laufbeginn) abgefragt und als Zeile `costs_api` protokolliert. Die Buckets umfassen den ganzen Tag. Diese Zeilen
    zählen nicht zur Budgetsumme. Derzeit ist kein Admin-Key gesetzt, es gilt nur die Schätzung.
53. **Existenzprüfung (`existiert`/`erfunden`):** Für jeden Fund (alle Versionen) wird jede Norm (nach
    `zerlege_fund`) mit dem Werkzeug geprüft, auf Ebene Artikel/Paragraf/Anhang. `nein`, wenn mindestens eine Norm im
    aufgelösten Regelwerk fehlt, obwohl das Regelwerk Normen dieser Art enthält. `unbekannt`, wenn das Regelwerk
    nicht auflösbar ist oder keine Norm erkennbar ist (z. B. TV-L-Anlagen). Auflösung für Soll-Kurzformen über die
    EU-Nummer aus der Normierung (DSGVO → Verordnung (EU) 2016/679), sonst Kurzform, sonst Rohname.
54. **`anteil_vorher_geladen`:** Anteil der Funde, deren sämtliche Normen im selben Stufe-2-Aufruf (letzter
    Versuch) vorher mit `lade_norm` erfolgreich geladen wurden, verglichen über (Kennung, Norm-Schlüssel). Nur bei
    `suche: eigen`.
55. **Abgebrochener erster Versuch:** Der erste v3-Lauf A (20261021-112159_A_7) lief noch ohne Sitzungs-Lock für die
    Bayern-Suche (Risiko vermischter Suchergebnisse bei parallelen Tasks). Ich habe ihn nach dem ersten API-Aufruf
    abgebrochen (0,0004 USD); er liegt in `runs_ungueltig/`.
