Status: offen

# Auftrag 003 – H1 Version 3: eigenes Suchwerkzeug statt OpenAI-Websuche, dann 5 × A + 5 × B

Erstellt vom Planungs-Assistenten am 21.10.2026. Anlass: Rund 85–90 % der Kosten je Lauf entfallen auf die OpenAI-Websuche. Die Quellen selbst sind kostenlos.
Setze alles ohne Rückfragen um. Entscheidungen dokumentierst du in `h1/DECISIONS.md` unter einem neuen Abschnitt „v3“.

## 1. Ziel

Das Modell recherchiert weiterhin **selbst**. Statt des OpenAI-Tools `web_search` bekommt es aber eigene Funktionen (Function Calling), die dein Python-Code ausführt. Diese Funktionen greifen direkt auf die vier Quellen zu und speichern Ergebnisse lokal zwischen. Das Modell bleibt **GPT-6 Luna**. Die Kosten sollen von ca. 1,10 USD auf ca. 0,15–0,30 USD je Lauf sinken.

## 2. Was der Planungs-Assistent bereits geändert hat (nur lesen)

- `h1/prompts/stufe1.md` und `h1/prompts/stufe2.md`: Die Quellenregel verweist jetzt auf die vier Werkzeuge. Stufe 2 verlangt, dass jede Fundstelle vorher mit `lade_norm` geladen wird. Sonst ist alles unverändert.
- `auftraege/002_h1_v2.md` ist abgeschlossen. Die B-Läufe in v2 entfallen.
- Soll-Liste, Prozess und Firmenprofil sind unverändert.

## 3. Werkzeuge (neues Modul `h1/src/werkzeuge.py`, Cache in `h1/cache/`)

Als Function Tools der Responses API (`type: "function"`, strikte JSON-Schemas). Jede Rückgabe ist JSON und wird auf höchstens **6000 Zeichen** gekürzt. Ist sie gekürzt, steht in der Rückgabe `"gekuerzt": true`.

| Funktion | Parameter | Rückgabe |
| --- | --- | --- |
| `suche_regelwerk` | `stichwort` | bis zu 10 Treffer `{regelwerk, titel, ebene, quelle_url}` aus allen vier Quellen |
| `inhaltsverzeichnis` | `regelwerk` | Liste `{norm, ueberschrift}` aller Artikel/Paragrafen/Anhänge |
| `lade_norm` | `regelwerk`, `norm` (z. B. `Art. 78`, `§ 165`, `Anhang III`) | `{regelwerk, norm, ueberschrift, text, quelle_url, fassung_datum}` oder `{fehler: "nicht gefunden", ...}` |
| `suche_volltext` | `regelwerk`, `begriff` | bis zu 10 Treffer `{norm, auszug}` (Auszug ≤ 300 Zeichen) |

**Auflösung von Regelwerken, ohne fest eingebaute Liste.** Ganz wichtig: Im Code darf **keine** Liste der Soll-Regelwerke stehen und auch keine Zuordnung, die nur für diese Regelwerke gilt. Das Werkzeug muss für beliebige Regelwerke der vier Quellen funktionieren.
- **Bund (gesetze-im-internet.de):** Auflösung über das offizielle Gesamtverzeichnis (`gii-toc.xml`) per Abkürzung oder Titel. Normtexte kommen aus dem XML-Download des jeweiligen Gesetzes.
- **Bayern (gesetze-bayern.de):** über die Dokument-URLs (`/Content/Document/<Abk>` bzw. `<Abk>-<Nr>`). Für `suche_regelwerk` nutzt du die Suchfunktion der Seite oder ein anderes Verfahren. Entscheide selbst und dokumentiere es.
- **EU (eur-lex.europa.eu):** Rechtsakte über CELEX-Nummern, die nach der Regel aus „Verordnung (EU) JJJJ/NNN“ berechnet werden (Präfix 3, Jahr, R/L, Nummer). Die geläufigen Abkürzungen (DSGVO, AI Act/KI-VO …) löst `suche_regelwerk` über die EUR-Lex-Suche auf. Verwende die konsolidierte Fassung, wenn es eine gibt.
- **Tarif (tdl-online.de):** Das TV-L-Dokument wird einmal geladen und nach Paragrafen zerlegt. Andere Tarifverträge sind nicht nötig. Liefere für sie „nicht gefunden“.
- Was für eine Quelle nicht zuverlässig klappt, beschreibst du als Grenze in `ERGEBNIS.md`, Abschnitt 6.

**Schonender Abruf:**
- Jede URL nur einmal laden, danach aus dem Cache.
- Höchstens 1 Anfrage pro Sekunde je Domain.
- User-Agent `Masterarbeit-HM-Experiment (nicht-kommerziell)`.
- Andere Domains als die vier sind technisch gesperrt.

**Cache:** `h1/cache/<domain>/…` mit Abrufdatum. Committe ihn, außer `h1/cache/tdl-online.de/`; das kommt in die `.gitignore`. Gesetzestexte sind amtliche Werke, den Tarifvertrag laden wir lieber nicht ins öffentliche Repo.

**Smoke-Test** (`python -m src.werkzeuge --test`). Er muss vor dem ersten Lauf bestehen:
- `lade_norm` liefert Text für: AGG § 7 · SGB IX § 165 · BayPVG Art. 78 · BayGlG Art. 17 · Verordnung (EU) 2016/679 Art. 35 · Verordnung (EU) 2024/1689 Art. 26 und Anhang III · TV-L § 12
- `lade_norm` liefert „nicht gefunden“ für: DSGVO Art. 150 · AGG § 99
- `suche_regelwerk("Personalvertretung Bayern")` liefert das BayPVG

Diese Testnormen stehen nur im Test und dürfen nirgends sonst im Code vorkommen.

## 4. Änderungen an Lauf und Client

- `config.yaml`:
  - `version: v3`
  - `suche: eigen` (Werte: `eigen` | `openai`; der alte Weg bleibt einschaltbar)
  - `max_werkzeugaufrufe_stufe1: 30`
  - `max_werkzeugaufrufe_stufe2: 15`
  - `budget_usd_auftrag: 3.0`
  - `budget_usd_lauf: 0.60`
- **Funktionsaufruf-Schleife** in `llm_client.py`: Antwortet das Modell mit `function_call`, führst du die Funktion aus, schickst `function_call_output` zurück und wiederholst das bis zur strukturierten Endantwort. Ist das Limit erreicht, wird das Modell **einmal** aufgefordert, ohne weitere Werkzeuge zu antworten. Der Abbruch steht in `protokoll.json`.
- **Protokoll:** Jeder Werkzeugaufruf mit Parametern, Kurzergebnis (gefunden ja/nein, URL) und Dauer kommt nach `raw/werkzeuge_<stufe/task>.jsonl`.
- **Kosten:** Bei `suche: eigen` keine Websuche-Kosten. In `meta.json` kommen `werkzeugaufrufe` und `werkzeugaufrufe_nicht_gefunden` dazu.
- **Abbruchregeln:**
  - Bei `insufficient_quota` bzw. `credit_balance_exhausted` bricht der Lauf **sofort** ab, ohne Retry. Der Ordner kommt nach `runs_ungueltig/`, der Auftrag auf `blockiert`.
  - Würde ein neuer Lauf das `budget_usd_auftrag` überschreiten (Summe `kosten_usd_geschaetzt` aller v3-Läufe), wird er nicht gestartet: Auftrag `blockiert`, dokumentieren.
  - Überschreitet ein Lauf `budget_usd_lauf`, bricht er ab: Auftrag `blockiert`, dokumentieren.

## 5. Auswertung (Ergänzungen)

- **Neue Bewertung je Fund: `existiert`** (ja/nein). Die Auswertung prüft jede Fundstelle über `lade_norm` (aus dem Cache) auf den Artikel bzw. Paragrafen. Existiert die Norm nicht, wird der Fund als **`erfunden`** markiert. Das gilt unabhängig von der übrigen Bewertung.
- **Neue Kennzahlen:**
  - `anteil_erfunden`
  - `anteil_vorher_geladen`: Anteil der Funde, deren Norm im selben Aufruf vorher mit `lade_norm` geladen wurde, also ob sich das Modell an die Regel hält
  - `werkzeugaufrufe` je Lauf
- **Rückwirkend:** `existiert`/`erfunden` auch für die bisherigen Läufe (v1, v2) berechnen. Damit ist die offene Frage nach erfundenen Normen beantwortet, zum Beispiel A_2 F080 „AI Act Art. 113 Abs. 3“.
- Gruppierung wie bisher nach (`version`, `konfig`). In `ERGEBNIS.md` kommt ein Abschnitt **„Vergleich v2 → v3“** dazu: OpenAI-Websuche gegen eigenes Werkzeug, bei gleichem Prompt-Stand außer der Quellenregel.

## 6. Ablauf

1. Werkzeuge bauen, Smoke-Test bestehen, committen und pushen.
2. `docker compose build`, dann **ein** Lauf A (v3). Bei technischen Fehlern oder Kosten über `budget_usd_lauf`: stopp, Auftrag `blockiert`, dokumentieren, pushen.
3. Läuft alles fehlerfrei, ohne Rückfrage weiter: noch 4 × A, dann 5 × B (v3).
4. `evaluate.py` über alle Läufe ausführen, `ERGEBNIS.md` aktualisieren. Die Abschnitte 5–8 schreibst du für v3 neu. Die Erkenntnisse aus v2 bleiben kurz im Abschnitt „Vergleich v2 → v3“ erhalten.
5. Nach Schritt 1, nach Schritt 2 und am Ende jeweils committen und pushen.

## 7. Abnahme

- 5 × A und 5 × B (v3) liegen in `h1/runs/`. Die Gesamtkosten von Auftrag 003 liegen bei höchstens 3 USD.
- `existiert`/`erfunden` ist für alle Läufe (v1–v3) ausgewertet.
- `DECISIONS.md` enthält den Abschnitt „v3“, `ERGEBNIS.md` den Abschnitt „Vergleich v2 → v3“.
- Statuszeile dieses Auftrags auf `erledigt`, alles gepusht.
