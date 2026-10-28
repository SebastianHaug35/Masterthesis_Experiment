#!/usr/bin/env python3
"""Schätzt den Schreibfortschritt und schreibt fortschritt.tex für die Statusseite.

Gezählt wird nur ausformulierter Text in chapters/*.tex: Kommentare, \\offen{...}
und Befehle zählen nicht. Abbildungen und Tabellen werden pauschal angesetzt.
Kalibrierung an der Vorlage (12 pt, 1,5-zeilig, Satzspiegel 155 x 247 mm):
ca. 11 Wörter je Zeile, ca. 36 nutzbare Zeilen je Seite.
"""
import datetime, pathlib, re

ZIEL_SEITEN = 70
WOERTER_JE_ZEILE = 11
ZEILEN_JE_SEITE = 36
ZEILEN_JE_ABBILDUNG = 16   # etwa eine halbe Seite inkl. Unterschrift
ZEILEN_JE_UEBERSCHRIFT = 2

# Seitenbudget je Kapitel (Gliederung 60 Seiten, auf 70 hochgerechnet)
KAPITEL = [
    ("01_einleitung", "Einleitung", 6),
    ("02_grundlagen", "Grundlagen", 12),
    ("03_verwandte_arbeiten", "Verwandte Arbeiten", 7),
    ("04_methodik", "Methodik", 12),
    ("05_implementierung", "Implementierung", 7),
    ("06_ergebnisse", "Ergebnisse", 14),
    ("07_diskussion", "Diskussion", 9),
    ("08_fazit", "Fazit und Ausblick", 3),
]

def entferne_befehl(text, name):
    """Entfernt \\name{...} mit verschachtelten Klammern."""
    out, i = [], 0
    muster = "\\" + name + "{"
    while True:
        j = text.find(muster, i)
        if j < 0:
            out.append(text[i:]); return "".join(out)
        out.append(text[i:j]); k, tiefe = j + len(muster), 1
        while k < len(text) and tiefe:
            tiefe += {"{": 1, "}": -1}.get(text[k], 0); k += 1
        i = k

def zaehle(datei):
    t = datei.read_text(encoding="utf-8")
    t = re.sub(r"(?<!\\)%.*", "", t)                      # Kommentare
    t = entferne_befehl(t, "offen")                      # Platzhalter
    abb = len(re.findall(r"\\begin\{(figure|table)\}", t))
    t = re.sub(r"\\begin\{(figure|table)\}.*?\\end\{\1\}", " ", t, flags=re.S)
    ueb = len(re.findall(r"\\(sub)*section\*?\{", t))
    t = re.sub(r"\\(sub)*section\*?\{[^}]*\}", " ", t)
    t = re.sub(r"\\(cite|ref|label)\{[^}]*\}", " X ", t)
    t = re.sub(r"\\fb\{([^}]*)\}", r" \1 ", t)
    t = re.sub(r"\\item\[([^\]]*)\]", r" \1 ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)
    t = re.sub(r"[{}$\\~]", " ", t)
    woerter = len(re.findall(r"\w[\w.,;:!?()\-–„“‚‘/]*", t))
    zeilen = woerter / WOERTER_JE_ZEILE + abb * ZEILEN_JE_ABBILDUNG
    if woerter:  # Überschriften nur zählen, wenn das Kapitel schon Text hat
        zeilen += ueb * ZEILEN_JE_UEBERSCHRIFT
    return woerter, zeilen

def main():
    basis = pathlib.Path(__file__).resolve().parent
    zeilen_ziel = ZIEL_SEITEN * ZEILEN_JE_SEITE
    zeilen_summe, woerter_summe, zeilen_tex = 0, 0, []
    for datei, titel, budget in KAPITEL:
        w, z = zaehle(basis / "chapters" / f"{datei}.tex")
        woerter_summe += w; zeilen_summe += z
        anteil = min(z / (budget * ZEILEN_JE_SEITE), 1.0)
        zeilen_tex.append(f"\\fortschrittzeile{{{titel}}}{{{z / ZEILEN_JE_SEITE:.1f}}}{{{budget}}}{{{anteil:.3f}}}".replace(f"{{{z / ZEILEN_JE_SEITE:.1f}}}", "{" + f"{z / ZEILEN_JE_SEITE:.1f}".replace(".", ",") + "}", 1))
    seiten = zeilen_summe / ZEILEN_JE_SEITE
    gesamt = min(zeilen_summe / zeilen_ziel, 1.0)
    fmt = lambda x: f"{x:.1f}".replace(".", ",")
    tex = [
        "% automatisch erzeugt von fortschritt.py -- nicht von Hand ändern",
        f"\\def\\fsDatum{{{datetime.date.today().strftime('%d.%m.%Y')}}}",
        f"\\def\\fsWoerter{{{woerter_summe}}}",
        f"\\def\\fsZeilen{{{round(zeilen_summe)}}}",
        f"\\def\\fsZeilenZiel{{{zeilen_ziel}}}",
        f"\\def\\fsSeiten{{{fmt(seiten)}}}",
        f"\\def\\fsSeitenZiel{{{ZIEL_SEITEN}}}",
        f"\\def\\fsAnteil{{{gesamt:.3f}}}",
        f"\\def\\fsProzent{{{fmt(gesamt * 100)}}}",
        "\\def\\fsKapitel{%",
        *zeilen_tex,
        "}",
    ]
    (basis / "fortschritt.tex").write_text("\n".join(tex) + "\n", encoding="utf-8")
    print(f"Fortschritt: {woerter_summe} Wörter, ca. {round(zeilen_summe)} von {zeilen_ziel} Zeilen, {fmt(seiten)} von {ZIEL_SEITEN} Seiten")

if __name__ == "__main__":
    main()
