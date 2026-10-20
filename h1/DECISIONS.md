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
