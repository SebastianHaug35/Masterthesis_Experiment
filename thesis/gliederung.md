# Masterarbeit – Gliederung

Oct 22, 2026 · @Sebastian

Die Arbeit folgt einer Linie: Problem → Hypothesen → Versuchsaufbau → Ergebnisse je Hypothese → Bewertung. Jedes Kapitel beantwortet genau eine Leitfrage und stützt sich auf belegbare Dateien im Experiment-Repo.

## Titel und Forschungsfragen

**Arbeitstitel (Vorschlag):** Regulatorische Anforderungen in KI-gestützten Geschäftsprozessen erkennen und zur Laufzeit durchsetzen – Ein LLM-Agent zur Zuordnung von Vorschriften, zur Erkennung von Compliance-Lücken und zur Runtime Verification am Beispiel eines Bewerbungsverfahrens an einer bayerischen Hochschule (abgesegnet am 27.10.2026)

| Nr. | Forschungsfrage | Hypothese | Stand |
| --- | --- | --- | --- |
| FF1 | Findet ein Agent mit eigener Recherche die geltenden Regelwerke und ordnet er die konkreten Vorschriften den richtigen Tasks zu? | H1 | Daten liegen vor (v1–v3), v4 läuft |
| FF2 | Erkennt der Agent rechtlich gebotene Schritte, die im Prozess fehlen? | H1b | Daten liegen vor |
| FF3 | Wie wirken sich Prompt und Recherchewerkzeug auf Qualität, erfundene Normen und Kosten aus? | – (explorativ) | Daten liegen vor (v1 → v2 → v3 → v4) |
| FF4 | Lassen sich Vorschriften in prüfbare Regeln übersetzen und zur Laufzeit durchsetzen? | H2, H3 | Teil der Arbeit (Prototyp); Versuch noch zu planen |

Die Arbeit hat zwei Hälften: FF1 bis FF3 behandeln das Erkennen, FF4 die Durchsetzung zur Laufzeit.

## Überblick der Kapitel

Ziel: 60 Seiten ohne Anhang (festgelegt am 22.10.2026). Die Verteilung auf die Kapitel ist ein Startwert.

| Kapitel | Leitfrage | Seiten (ca.) | Belege im Repo |
| --- | --- | --- | --- |
| 1 Einleitung | Warum ist das Problem relevant, und was genau wird untersucht? | 5 | – |
| 2 Grundlagen | Was muss der Leser wissen, um den Rest zu verstehen? | 10 | – |
| 3 Verwandte Arbeiten | Was gibt es schon, und welche Lücke schließt diese Arbeit? | 6 | – |
| 4 Methodik | Wie ist der Versuch aufgebaut, und wie wird gemessen? | 10 | `ANWEISUNG_H1.md`, `h1/input/`, `h1/prompts/`, `auftraege/` |
| 5 Implementierung | Wie wurde der Agent technisch umgesetzt? | 6 | `h1/src/`, `h1/DECISIONS.md`, `CLAUDE.md` |
| 6 Ergebnisse | Was kam heraus, getrennt nach Forschungsfrage? | 12 | `h1/results/kennzahlen.csv`, `ERGEBNIS.md`, `h1/runs/` |
| 7 Diskussion | Was bedeuten die Ergebnisse, und wie belastbar sind sie? | 8 | `ERGEBNIS.md` (Abschnitte 5–8) |
| 8 Fazit und Ausblick | Was sind die Antworten auf FF1–FF4, und was folgt daraus? | 3 | – |
| Summe |  | 60 |  |
| Anhang | Wo kann man alles nachprüfen? | – | Prompts, Soll-Liste, Prozess, Kennzahlen, Repo-Link |

## Gliederung im Detail

Die Unterkapitel mit ihren Kernaussagen stehen jetzt im [Masterarbeit – Entwurf](https://claude.ai/artifact/PwsoGtU8ZYwSEj41pmhF8q). Das vermeidet zwei Fassungen derselben Gliederung.

## Schreibregeln für Verständlichkeit

- **Jedes Kapitel beginnt mit seiner Leitfrage** und endet mit einem Zwischenfazit von zwei bis drei Sätzen.
- **Die Forschungsfragen sind der rote Faden:** Kapitel 6 und 7 sind nach FF1–FF4 gegliedert, in derselben Reihenfolge wie in Kapitel 1.
- **Feste Begriffe:** Regelwerk (ein Gesetz), Norm (ein Artikel oder Paragraf), Fundstelle (Norm mit Absatz), Task, Lücke. Ein Glossar steht vor Kapitel 1, und kein Begriff wechselt seine Bedeutung.
- **Ein laufendes Beispiel:** Die KI-Vorauswahl (Teilprozess 3) begleitet die Arbeit von der Einleitung bis zur Diskussion.
- **Jede Zahl hat eine Quelle:** Ergebnisse verweisen auf die Version und die Datei im Repo, aus der sie stammen.
- **Offenheit bei Anpassungen:** Dass die Soll-Liste nach dem ersten Lauf korrigiert wurde, steht in der Methodik und nicht erst in den Grenzen.
- **Kurze Sätze, eine Aussage pro Absatz.** Tabellen und Abbildungen tragen die Zahlen, der Text erklärt, was sie bedeuten.

## Offene Entscheidungen mit dem Betreuer

- [x] **Rahmen der Arbeit:** Das Experiment ist die Arbeit. Implementa und die Entscheidungsmatrix sind vorerst draußen (entschieden am 22.10.2026).
- [x] **Umfang:** 60 Seiten ohne Anhang.
- [x] **H2/H3 (entschieden am 27.10.2026):** Runtime Verification ist Teil der Arbeit, umgesetzt als Prototyp mit kleinerem Test. Seitenplan und Versuch für H2/H3 folgen.
- [ ] **Validierung der Soll-Liste:** Wer prüft sie fachlich, etwa Prof. Gerling oder Prof. Trapp für den Datenschutz? Vor allem Art. 75 und 78 BayPVG sind offen.
- [ ] **Formalia:** Sprache, Zitierstil, Vorlage (LaTeX oder Word) laut Prüfungsordnung FK07.
- [ ] **Zweiter Anwendungsfall** (Brandmeldetechnik): streichen oder in den Ausblick?

## Schreibplan

Geschrieben wird in der Reihenfolge, in der die Inhalte feststehen. Die Einleitung kommt zuletzt, weil sie verspricht, was die Arbeit am Ende hält.

- [ ] Restliche offene Entscheidungen mit dem Betreuer klären (H2/H3, Validierung, Formalia)
- [ ] Kapitel 4 Methodik: liegt vollständig im Repo und lässt sich sofort schreiben
- [ ] Kapitel 5 Implementierung
- [ ] Kapitel 2 Grundlagen und Kapitel 3 Verwandte Arbeiten (Literatur sammeln, Sai et al. liegt vor)
- [ ] Auftrag 004 (v4) abwarten, dann Kapitel 6 Ergebnisse
- [ ] Kapitel 7 Diskussion
- [ ] Kapitel 1 Einleitung und Kapitel 8 Fazit
- [ ] Kurzfassung, Glossar, Anhang, Korrekturlesen
