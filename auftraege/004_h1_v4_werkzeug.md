Status: offen

# Auftrag 004 – H1 Version 4: Werkzeug verbessern, dann 5 × A + 5 × B

Erstellt vom Planungs-Assistenten am 22.10.2026 auf Basis von `h1/results/ERGEBNIS.md` (v3, Abschnitt 8, Vorschläge 1–4).
Ziel: **Recall und Lückenerkennung wie in v2, Kosten wie in v3.** Setze alles ohne Rückfragen um. Entscheidungen dokumentierst du in `h1/DECISIONS.md` unter einem neuen Abschnitt „v4“.

## 1. Was der Planungs-Assistent bereits geändert hat (nur lesen)

- `h1/prompts/stufe1.md`: Das Modell übernimmt jetzt zusätzlich `kennung` aus dem Werkzeugergebnis.
- `h1/prompts/stufe2.md`: Regelwerke aus dem Rechtsrahmen werden direkt über ihre `kennung` angesprochen. `suche_regelwerk` gibt es nur noch für neue Regelwerke. EU-Rechtsakte ohne Kennung heißen „Verordnung (EU) JJJJ/NNNN“.
- **Neu: `h1/input/rechtsrahmen_b.json`**, die Soll-Regelwerke mit Kennung, **nur für Konfiguration B**. Prüfe im Smoke-Test, dass jede Kennung mit `inhaltsverzeichnis` lädt. Erwartet das Werkzeug ein anderes Format, darfst du **ausnahmsweise nur diese Datei** korrigieren; das dokumentierst du in DECISIONS.
- Soll-Liste, Prozess und Firmenprofil sind unverändert.

## 2. Code-Änderungen

1. **`suche_regelwerk`: zuerst direkt auflösen, dann suchen.**
   - Sieht das Stichwort wie eine Abkürzung oder Kennung aus, kommt die direkte Auflösung als erster Treffer: Bund über `jurabk` bzw. Slug in `gii-toc.xml`, Bayern über `/Content/Document/<Abk>`, EU über die Nummer.
   - Bei Bundesrecht steht das **Stammgesetz** vor Änderungsgesetzen. Ein exakter Treffer auf `jurabk` hat Vorrang. Den Fall `sgb9ua_ndg` statt `sgb_9_2018` nimmst du in den Smoke-Test auf.
   - Jeder Treffer enthält `regelwerk` als **amtliche Abkürzung** (`jurabk`, nicht den Slug) und das neue Feld **`kennung`**, also den Wert, den `lade_norm` und die anderen Werkzeuge akzeptieren.
   - Weiterhin gilt: keine fest eingebaute Liste von Regelwerken.
2. **Kennung durchreichen:**
   - `RegelwerkEintrag` (Stufe 1) bekommt das Feld `kennung: str | None`. Es wird in `stufe1.json` gespeichert und als Teil des Rechtsrahmens an Stufe 2 übergeben.
   - Konfiguration B liest den Rechtsrahmen aus `h1/input/rechtsrahmen_b.json` statt aus der Soll-Liste.
3. **Limits in `config.yaml`:**
   - `max_werkzeugaufrufe_stufe1: 50`
   - `max_werkzeugaufrufe_stufe2: 40`
   - `version: v4`
   - `budget_usd_auftrag: 2.0`
   - `budget_usd_lauf: 0.60` bleibt.
4. **Existenzprüfung bis auf Absatzebene:** Nennt ein Fund einen Absatz, prüfst du anhand des geladenen Normtexts, ob es diesen Absatz gibt. Dafür kommt die neue Spalte `absatz_existiert` dazu (ja / nein / nicht prüfbar) und die neue Kennzahl `anteil_absatz_erfunden`. Das gilt für alle Läufe, v1–v4.
5. **Neue Kennzahl `limit_erreicht_anteil`:** der Anteil der Aufrufe je Lauf, die ihr Werkzeuglimit erreicht haben, getrennt nach Stufe 1 und Stufe 2.

## 3. Ablauf

1. Code ändern, Smoke-Test erweitern und bestehen lassen (inklusive aller Kennungen aus `rechtsrahmen_b.json`). Danach committen und pushen.
2. `docker compose build`, dann **ein** Lauf A (v4). Bei technischen Fehlern oder Budgetüberschreitung stoppst du: Status `blockiert`, dokumentieren, pushen.
3. Läuft alles fehlerfrei, geht es ohne Rückfrage weiter mit noch 4 × A und danach 5 × B (v4).
4. `evaluate.py` über alle Läufe ausführen.
5. In `ERGEBNIS.md`:
   - Abschnitte 5–8 für v4 neu schreiben.
   - Die Tabelle „Vergleich v2 → v3“ wird zu **„Vergleich v2 → v3 → v4“** erweitert, mit zusätzlichen Zeilen für Werkzeugaufrufe, `limit_erreicht_anteil` und `anteil_absatz_erfunden`.
   - Ein kurzer Absatz **„Stand für die Masterarbeit“** fasst in 5–8 Sätzen zusammen, welche Version die Hauptergebnisse liefert und warum.
6. Nach Schritt 1, nach Schritt 2 und am Ende jeweils committen und pushen.

## 4. Abnahme

- 5 × A und 5 × B (v4) liegen in `h1/runs/`. Die Kosten von Auftrag 004 liegen bei höchstens 2 USD.
- `absatz_existiert` ist für alle Läufe ausgewertet.
- `DECISIONS.md` hat einen Abschnitt „v4“. `ERGEBNIS.md` enthält den Vergleich v2 → v3 → v4 und den Absatz „Stand für die Masterarbeit“.
- Die Statuszeile dieses Auftrags steht auf `erledigt`, alles ist gepusht.
