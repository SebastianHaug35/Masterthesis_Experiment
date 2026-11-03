#!/usr/bin/env python3
"""Erzeugt appendix/anhang_a_fall1.tex aus der Referenzzuordnung (h1/input/soll_liste.csv).

Die Tabelle listet alle Vorschriften von Fall 1 mit Fundstelle, Inhalt und Ort im Prozess.
Ergänzungen, die nicht in der Soll-Liste stehen, sind unten in ERGAENZUNG gepflegt und
in der Tabelle gekennzeichnet.
"""
import csv, json, pathlib

BASIS = pathlib.Path(__file__).resolve().parents[3]
SOLL = BASIS / "h1/input/soll_liste.csv"
PROZESS = BASIS / "h1/input/prozess.json"
ZIEL = BASIS / "thesis/latex/appendix/anhang_a_fall1.tex"

# Fundstellen, die in der Soll-Liste fehlen (nur für den Anhang, Soll-Liste bleibt unverändert)
FUNDSTELLE_ERGAENZT = {"S04": "§ 12", "S27": "§ 2 Abs. 1"}
ERGAENZUNG = [{"soll_id": "E01", "regelwerk": "TV-L", "fundstelle": "§ 30", "task_id": "T5.2|T5.3",
               "typ": "zuordnung", "inhalt": "Befristete Arbeitsverträge (Verweis auf TzBfG und weitere Gesetze)"}]
ART = {"zuordnung": "Zuordnung", "luecke": "fehlender Schritt", "neutral": "neutral"}

def tex(s):
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#"),
                 ("→", r"$\rightarrow$"), ("§§", r"§§~"), ("§ ", r"§~")]:
        s = s.replace(a, b)
    return s

def main():
    p = json.load(open(PROZESS, encoding="utf-8"))
    tp_name = {tp["id"]: tp["name"] for tp in p["teilprozesse"]}
    zeilen = list(csv.DictReader(open(SOLL, encoding="utf-8"), delimiter=";")) + ERGAENZUNG
    def ort(t):
        if t == "GESAMT": return "gesamter Prozess"
        if t == "LUECKE": return "fehlt im Prozess"
        tasks = t.split("|"); tps = []
        for x in tasks:
            tp = "TP" + x[1:].split(".")[0]
            if tp not in tps: tps.append(tp)
        return "; ".join(f"{tp_name[tp]} ({', '.join(x for x in tasks if x[1:].split('.')[0]==tp[2:])})" for tp in tps)
    zeilen.sort(key=lambda z: (z["regelwerk"], z["soll_id"]))
    out = ["% automatisch erzeugt von tools/anhang_a.py -- nicht von Hand ändern",
           r"\begin{small}", r"\begin{longtable}{@{}>{\raggedright\arraybackslash}p{1.9cm}>{\raggedright\arraybackslash}p{2.0cm}>{\raggedright\arraybackslash}p{5.0cm}>{\raggedright\arraybackslash}p{4.0cm}>{\raggedright\arraybackslash}p{1.8cm}@{}}",
           r"\toprule \textbf{Regelwerk} & \textbf{Fundstelle} & \textbf{Inhalt} & \textbf{Ort im Prozess} & \textbf{Art} \\ \midrule \endhead",
           r"\bottomrule \endfoot"]
    for z in zeilen:
        fs = z["fundstelle"] or FUNDSTELLE_ERGAENZT.get(z["soll_id"], "")
        mark = "\\textsuperscript{*}" if z["soll_id"] in FUNDSTELLE_ERGAENZT or z["soll_id"].startswith("E") else ""
        out.append(f"{tex(z['regelwerk'])} & {tex(fs) or '--'}{mark} & {tex(z['inhalt'])} & {tex(ort(z['task_id']))} & {ART[z['typ']]} \\\\")
    out += [r"\end{longtable}", r"\end{small}",
            r"{\footnotesize \textsuperscript{*}\,Fundstelle bzw.\ Zeile für den Anhang ergänzt, nicht Teil der Referenzzuordnung.\par}"]
    ZIEL.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{len(zeilen)} Zeilen nach {ZIEL}")

if __name__ == "__main__":
    main()
