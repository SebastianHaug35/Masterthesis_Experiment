#!/usr/bin/env python3
"""Erzeugt appendix/anhang_b_h1.tex: Eingaben und Referenz für H1 (Fall 1).

Quellen sind die Eingabedateien des Experiments. Jede Tabelle nennt ihre Datei im
öffentlichen Repo (\\repodatei, Branch main). Nach einer Änderung an den Eingaben
das Skript neu laufen lassen.
"""
import csv, json, pathlib

BASIS = pathlib.Path(__file__).resolve().parents[3]
PROFIL = "h1/input/firmenprofil.json"
PROZESS = "h1/input/prozess.json"
SOLL = "h1/input/soll_liste.csv"
ZIEL = BASIS / "thesis/latex/appendix/anhang_b_h1.tex"

MERKMAL = {"name": "Name", "land": "Land", "bundesland": "Bundesland", "rechtsform": "Rechtsform",
           "sektor": "Sektor", "branche": "Branche", "beschaeftigte": "Beschäftigte",
           "personalvertretung": "Personalvertretung", "gleichstellungsbeauftragte": "Gleichstellungsbeauftragte",
           "ki_einsatz": "KI-Einsatz", "dienstleister_ausserhalb_eu": "Dienstleister außerhalb der EU",
           "stelle": "Stelle", "befristung": "Befristung"}
# Ebene je Regelwerk (für die Gruppierung der Referenz; Reihenfolge = Normenhierarchie)
EBENE = {"DSGVO": "EU", "AI Act": "EU", "GG": "Bund", "AGG": "Bund", "SGB IX": "Bund", "NachwG": "Bund",
         "TzBfG": "Bund", "WissZeitVG": "Bund", "BayDSG": "Land Bayern", "BayGlG": "Land Bayern",
         "BayPVG": "Land Bayern", "BayHIG": "Land Bayern", "TV-L": "Tarifvertrag"}
EBENEN = ["EU", "Bund", "Land Bayern", "Tarifvertrag"]

def tex(s):
    s = str(s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#"),
                 ("§ ", r"§~")]:
        s = s.replace(a, b)
    return s

def wert(v):
    return "ja" if v is True else "nein" if v is False else tex(v)

def tabelle(spalten, kopf, zeilen, caption, label, datei):
    out = [r"\begin{small}", r"\begin{longtable}{@{}" + spalten + "@{}}",
           rf"\caption[{caption}]{{{caption}. Quelle: eigene Darstellung, Daten aus \repodatei{{{datei}}}.}}\label{{{label}}}\\",
           r"\toprule " + " & ".join(rf"\textbf{{{k}}}" for k in kopf) + r" \\ \midrule \endfirsthead",
           r"\toprule " + " & ".join(rf"\textbf{{{k}}}" for k in kopf) + r" \\ \midrule \endhead",
           r"\bottomrule \endfoot"]
    out += [" & ".join(z) + r" \\" for z in zeilen]
    out += [r"\end{longtable}", r"\end{small}", ""]
    return out

def main():
    profil = json.load(open(BASIS / PROFIL, encoding="utf-8"))
    prozess = json.load(open(BASIS / PROZESS, encoding="utf-8"))
    soll = list(csv.DictReader(open(BASIS / SOLL, encoding="utf-8"), delimiter=";"))
    L = r">{\raggedright\arraybackslash}p"
    out = ["% automatisch erzeugt von tools/anhang_b.py -- nicht von Hand ändern", ""]

    out.append(r"\subsubsection{Eingabe}")
    out.append(r"\offen{Satz: Verweis auf Tabelle~\ref{tab:h1_profil} (Organisationsprofil)}")
    out += tabelle(L + "{5.0cm}" + L + "{9.5cm}", ["Merkmal", "Angabe"],
                   [[MERKMAL.get(k, tex(k)), wert(v)] for k, v in profil.items()],
                   "Organisationsprofil für Fall~1", "tab:h1_profil", PROFIL)

    out.append(r"\offen{Satz: Verweis auf Tabelle~\ref{tab:h1_prozess} (Prozess mit 6 Teilprozessen und 19 Tasks)}")
    zeilen = []
    for tp in prozess["teilprozesse"]:
        for i, t in enumerate(tp["tasks"]):
            zeilen.append([f"{tp['id']} {tex(tp['name'])}" if i == 0 else "", t["id"], tex(t["name"])])
    out += tabelle(L + "{4.2cm}" + L + "{1.3cm}" + L + "{9.0cm}", ["Teilprozess", "Task", "Bezeichnung"],
                   zeilen, f"Prozess für Fall~1: {tex(prozess['prozess'])}", "tab:h1_prozess", PROZESS)

    out.append(r"\offen{Satz: Auftrag an den Agenten (Prompt Stufe~1), Verweis auf \repodatei{h1/prompts/stufe1.md}. Entscheiden: Prompt vollständig abdrucken oder nur verlinken}")
    out.append("")

    out.append(r"\subsubsection{Referenz}")
    out.append(r"\offen{Satz: Herleitung der Referenz aus der Referenzzuordnung (Anhang~\ref{anh:vorschriften}): es zählen Regelwerke mit mindestens einer Zeile der Art Zuordnung oder fehlender Schritt}")
    zaehl = {}
    for z in soll:
        zaehl.setdefault(z["regelwerk"], {"zuordnung": 0, "luecke": 0, "neutral": 0})[z["typ"]] += 1
    ref = [r for r, c in zaehl.items() if c["zuordnung"] + c["luecke"] > 0]
    neutral = [r for r, c in zaehl.items() if c["zuordnung"] + c["luecke"] == 0]
    unbekannt = [r for r in zaehl if r not in EBENE]
    if unbekannt:
        raise SystemExit(f"Ebene fehlt für: {unbekannt}")
    zeilen = []
    for e in EBENEN:
        for r in sorted((r for r in ref if EBENE[r] == e), key=str.lower):
            c = zaehl[r]
            zeilen.append([e, tex(r), str(c["zuordnung"]), str(c["luecke"])])
    out += tabelle(L + "{3.0cm}" + L + "{3.0cm}" + r">{\raggedleft\arraybackslash}p{3.2cm}" + r">{\raggedleft\arraybackslash}p{3.8cm}",
                   ["Ebene", "Regelwerk", "Zeilen Zuordnung", "Zeilen fehlender Schritt"], zeilen,
                   f"Referenz für H1 in Fall~1: {len(ref)} Regelwerke", "tab:h1_referenz", SOLL)
    out.append(r"\offen{Satz: neutrale Regelwerke (" + ", ".join(tex(r) for r in sorted(neutral))
               + r") zählen weder als Treffer noch als Fehler; weitere vom Agenten genannte Regelwerke zählen als zusätzlich und senken die Genauigkeit}")
    out.append(r"\offen{Satz: Erfolgskriterium Trefferquote $\geq 0{,}9$, also mindestens 11 von 12 Regelwerken}")
    ZIEL.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{len(ref)} Referenz-Regelwerke, neutral: {neutral}, nach {ZIEL}")

if __name__ == "__main__":
    main()
