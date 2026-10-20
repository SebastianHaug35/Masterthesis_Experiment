"""Abgleich der Läufe mit der Soll-Liste, Kennzahlen und Berichte.

    python -m src.evaluate                 # alle Läufe in runs/
    python -m src.evaluate --runs <run_id> # nur bestimmte Läufe
"""
import argparse
import json
import re
from pathlib import Path

import pandas as pd

from .config import Config, lade_config
from .normierung import fundstelle_text, norm_fundstelle, norm_regelwerk

TEILPROZESSE = ["TP1", "TP2", "TP3", "TP4", "TP5", "TP6"]
MANUELL_START = "<!-- MANUELL START: alles ab hier bleibt bei erneutem evaluate.py erhalten -->"
MANUELL_ENDE = "<!-- MANUELL ENDE -->"


def tp_von(task_id: str) -> str:
    m = re.match(r"T(\d+)\.", task_id or "")
    return f"TP{m.group(1)}" if m else "GESAMT"


# --------------------------------------------------------------------------- Laden

def lade_soll(cfg: Config) -> pd.DataFrame:
    soll = pd.read_csv(cfg.input_dir / "soll_liste.csv", sep=";", dtype=str, keep_default_na=False)
    soll["rw"] = soll["regelwerk"].map(norm_regelwerk)
    normiert = soll["fundstelle"].map(norm_fundstelle)
    soll["art"] = normiert.map(lambda x: x[0])
    soll["abs"] = normiert.map(lambda x: x[1])
    return soll


def lade_lauf(run_dir: Path) -> dict:
    def json_oder(name, default):
        p = run_dir / name
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

    funde_pfad = run_dir / "funde.jsonl"
    funde = [json.loads(z) for z in funde_pfad.read_text(encoding="utf-8").splitlines() if z.strip()] \
        if funde_pfad.exists() else []
    return {
        "dir": run_dir,
        "meta": json_oder("meta.json", {}),
        "stufe1": json_oder("stufe1.json", {}).get("rechtsrahmen"),
        "funde": funde,
        "kandidaten": json_oder("lueckenkandidaten.json", []),
        "protokoll": json_oder("protokoll.json", {}),
    }


# --------------------------------------------------------------------------- Bewertung

def _leer(x) -> bool:
    return x is None or (isinstance(x, float) and pd.isna(x)) or x == ""


def _art_passt(zeile, art) -> bool:
    return _leer(zeile["art"]) or zeile["art"] == art


def bewerte_fund(fund: dict, soll: pd.DataFrame) -> tuple[str, list[str]]:
    """Liefert (bewertung, soll_ids der als gefunden zählenden Zeilen)."""
    rw = norm_regelwerk(fund["regelwerk"])
    art, abs_ = norm_fundstelle(fund["fundstelle"])
    kandidaten = [z for _, z in soll[soll["rw"] == rw].iterrows() if _art_passt(z, art)]
    if not kandidaten:
        return "nicht_in_soll", []

    if fund["typ"] == "moegliche_luecke":
        passend = [z for z in kandidaten if z["typ"] == "luecke"]
    else:
        passend = [z for z in kandidaten if z["typ"] == "zuordnung"
                   and z["task_id"] in (fund["task_id"], "GESAMT")]
    treffer = [z["soll_id"] for z in passend if _leer(z["abs"]) or z["abs"] == abs_]
    if treffer:
        return "korrekt", treffer
    if passend:
        return "falscher_absatz", []
    return "falscher_task", []


def bewerte_kandidat(k: dict, soll: pd.DataFrame) -> list[str]:
    """Soll-Lücken, die ein Lückenkandidat trifft. Kandidaten ohne Fundstelle (Regelwerk ohne
    Zuordnung) treffen jede Soll-Lücke desselben Regelwerks; sonst muss Artikel/Paragraf passen."""
    rw = norm_regelwerk(k["regelwerk"])
    art, _ = norm_fundstelle(k.get("fundstelle") or "")
    luecken = soll[(soll["typ"] == "luecke") & (soll["rw"] == rw)]
    return [z["soll_id"] for _, z in luecken.iterrows() if art is None or _art_passt(z, art)]


def ist_gleichstellung(k: dict) -> bool:
    text = " ".join(str(k.get(f) or "") for f in ("regelwerk", "fehlender_schritt", "begruendung")).lower()
    return norm_regelwerk(k["regelwerk"]) == "BayGlG" or "gleichstellungsbeauftragte" in text


def werte_lauf_aus(lauf: dict, soll: pd.DataFrame) -> dict:
    meta = lauf["meta"]
    run_id, konfig = meta.get("run_id", lauf["dir"].name), meta.get("konfig", "?")

    # Stufe 2: Funde bewerten
    zeilen, gefunden = [], set()
    for f in lauf["funde"]:
        bewertung, treffer = bewerte_fund(f, soll)
        if f["typ"] == "zuordnung":
            gefunden.update(treffer)
        zeilen.append({**f, "konfig": konfig, "teilprozess": tp_von(f["task_id"]),
                       "regelwerk_norm": norm_regelwerk(f["regelwerk"]),
                       "fundstelle_norm": fundstelle_text(f["fundstelle"]),
                       "bewertung": bewertung, "soll_ids": ",".join(treffer),
                       "manuell_pruefen": bewertung == "nicht_in_soll"})
    funde = pd.DataFrame(zeilen)

    # H1b: Lückenkandidaten (dedupliziert nach Regelwerk + Artikel/Paragraf)
    kand_zeilen, luecken_gefunden = [], set()
    for k in lauf["kandidaten"]:
        treffer = bewerte_kandidat(k, soll)
        luecken_gefunden.update(treffer)
        art, _ = norm_fundstelle(k.get("fundstelle") or "")
        kand_zeilen.append({**k, "regelwerk_norm": norm_regelwerk(k["regelwerk"]),
                            "art_norm": art or "", "soll_ids": ",".join(treffer),
                            "falsch": not treffer, "gleichstellung": ist_gleichstellung(k)})
    kand = pd.DataFrame(kand_zeilen)
    if kand.empty:
        kand_unique = kand
    else:
        kand_unique = kand.groupby(["regelwerk_norm", "art_norm"], as_index=False).agg(
            falsch=("falsch", "all"), gleichstellung=("gleichstellung", "any"),
            soll_ids=("soll_ids", lambda s: ",".join(sorted({x for v in s for x in v.split(",") if x}))),
            anzahl_meldungen=("falsch", "size"),
            tasks=("task_id", lambda s: ",".join(sorted({x for x in s if isinstance(x, str) and x}))))

    # Kennzahlen
    k = {"run_id": run_id, "konfig": konfig}
    soll_rw = set(soll["rw"])
    if lauf["stufe1"] is not None:
        s1 = {norm_regelwerk(e["regelwerk"], e.get("vollstaendiger_titel", "")) for e in lauf["stufe1"]}
        k["s1_recall"] = len(s1 & soll_rw) / len(soll_rw)
        k["s1_praezision"] = len(s1 & soll_rw) / len(s1) if s1 else 0.0
        k["s1_gefunden"] = sorted(s1 & soll_rw)
        k["s1_uebersehen"] = sorted(soll_rw - s1)
        k["s1_zusaetzlich"] = sorted(s1 - soll_rw)
    else:
        k.update(s1_recall=None, s1_praezision=None, s1_gefunden=[], s1_uebersehen=[], s1_zusaetzlich=[])

    soll_z = soll[soll["typ"] == "zuordnung"]
    zuo = funde[funde["typ"] == "zuordnung"] if not funde.empty else funde
    k["s2_anzahl_funde"] = len(zuo)
    k["s2_recall"] = soll_z["soll_id"].isin(gefunden).mean()
    k["s2_praezision"] = (zuo["bewertung"] == "korrekt").mean() if len(zuo) else 0.0
    for tp in TEILPROZESSE + ["GESAMT"]:
        sz = soll_z[soll_z["task_id"].map(tp_von) == tp]
        k[f"s2_recall_{tp}"] = sz["soll_id"].isin(gefunden).mean() if len(sz) else None
        if tp != "GESAMT":
            zf = zuo[zuo["teilprozess"] == tp] if len(zuo) else zuo
            k[f"s2_praezision_{tp}"] = (zf["bewertung"] == "korrekt").mean() if len(zf) else None
    for b in ["korrekt", "falscher_absatz", "falscher_task", "nicht_in_soll"]:
        k[f"s2_n_{b}"] = int((zuo["bewertung"] == b).sum()) if len(zuo) else 0

    soll_l = soll[soll["typ"] == "luecke"]
    k["luecken_recall"] = soll_l["soll_id"].isin(luecken_gefunden).mean()
    k["luecken_kandidaten"] = len(kand_unique)
    k["falsche_luecken"] = int(kand_unique["falsch"].sum()) if len(kand_unique) else 0
    k["falsche_luecken_gleichstellung"] = int(kand_unique["gleichstellung"].sum()) if len(kand_unique) else 0
    k["anteil_unsicher"] = (funde["sicherheit"] == "unsicher").mean() if len(funde) else None
    k["anteil_nicht_in_soll"] = (funde["bewertung"] == "nicht_in_soll").mean() if len(funde) else None
    k["tokens_input"] = meta.get("tokens_input", 0)
    k["tokens_output"] = meta.get("tokens_output", 0)
    k["kosten_usd"] = meta.get("kosten_usd_geschaetzt", 0.0)

    uebersehen = soll[~soll["soll_id"].isin(gefunden | luecken_gefunden)][
        ["soll_id", "regelwerk", "fundstelle", "task_id", "typ", "inhalt"]].copy()
    uebersehen.insert(0, "konfig", konfig)
    uebersehen.insert(0, "run_id", run_id)
    return {"lauf": lauf, "kennzahlen": k, "funde": funde, "kandidaten": kand,
            "kandidaten_unique": kand_unique, "uebersehen": uebersehen}


# --------------------------------------------------------------------------- Ausgabe

LISTEN_SPALTEN = ["s1_gefunden", "s1_uebersehen", "s1_zusaetzlich"]


def kennzahlen_tabelle(auswertungen: list[dict]) -> pd.DataFrame:
    lauf = pd.DataFrame([{**a["kennzahlen"], "ebene": "lauf", "statistik": "wert"} for a in auswertungen])
    for c in LISTEN_SPALTEN:
        lauf[c] = lauf[c].map(lambda v: ", ".join(v))
    zahlen = [c for c in lauf.columns if c not in LISTEN_SPALTEN + ["run_id", "konfig", "ebene", "statistik"]]
    lauf[zahlen] = lauf[zahlen].apply(pd.to_numeric, errors="coerce")
    agg = []
    for konfig, g in lauf.groupby("konfig"):
        for stat in ["mittelwert", "std"]:
            werte = g[zahlen].mean() if stat == "mittelwert" else g[zahlen].std(ddof=1)
            agg.append({"run_id": f"alle ({len(g)} Läufe)", "konfig": konfig, "ebene": "konfig",
                        "statistik": stat, **werte.to_dict()})
    tab = pd.concat([lauf, pd.DataFrame(agg)], ignore_index=True)
    vorne = ["ebene", "statistik", "run_id", "konfig"]
    return tab[vorne + [c for c in tab.columns if c not in vorne]]


def _p(x) -> str:
    return "–" if x is None or pd.isna(x) else f"{x:.0%}"


def _zahl(x, nachkomma=0) -> str:
    return "–" if x is None or pd.isna(x) else f"{x:,.{nachkomma}f}".replace(",", " ")


def zusammenfassung_md(kennzahlen: pd.DataFrame) -> str:
    agg = kennzahlen[kennzahlen["ebene"] == "konfig"]
    zeilen = [("Stufe 1 Recall (Regelwerk)", "s1_recall", _p), ("Stufe 1 Präzision (Regelwerk)", "s1_praezision", _p),
              ("Stufe 2 Recall (Fundstelle)", "s2_recall", _p), ("Stufe 2 Präzision (Fundstelle)", "s2_praezision", _p),
              ("Stufe 2 Anzahl Funde", "s2_anzahl_funde", _zahl), ("H1b Lücken-Recall", "luecken_recall", _p),
              ("H1b falsche Lückenmeldungen", "falsche_luecken", _zahl),
              ("davon Gleichstellungsbeauftragte", "falsche_luecken_gleichstellung", _zahl),
              ("Anteil unsicher", "anteil_unsicher", _p), ("Anteil nicht_in_soll", "anteil_nicht_in_soll", _p),
              ("Tokens Input", "tokens_input", _zahl), ("Tokens Output", "tokens_output", _zahl),
              ("Kosten USD", "kosten_usd", lambda x: _zahl(x, 3))]
    konfigs = ["A", "B"]
    md = ["# Zusammenfassung H1: Konfiguration A vs. B", "",
          "Mittelwert ± Standardabweichung über alle Läufe je Konfiguration (n = Anzahl Läufe).", "",
          "| Kennzahl | " + " | ".join(
              f"{k} (n={int((kennzahlen['ebene'].eq('lauf') & kennzahlen['konfig'].eq(k)).sum())})" for k in konfigs) + " |",
          "| --- | " + " | ".join("---" for _ in konfigs) + " |"]
    for titel, spalte, fmt in zeilen:
        zellen = []
        for k in konfigs:
            m = agg[(agg["konfig"] == k) & (agg["statistik"] == "mittelwert")]
            s = agg[(agg["konfig"] == k) & (agg["statistik"] == "std")]
            if m.empty:
                zellen.append("–")
                continue
            mw, sd = m[spalte].iloc[0], s[spalte].iloc[0]
            zellen.append(fmt(mw) + ("" if pd.isna(sd) else f" ± {fmt(sd)}"))
        md.append(f"| {titel} | " + " | ".join(zellen) + " |")
    return "\n".join(md) + "\n"


def _dauer(meta: dict) -> str:
    try:
        d = pd.Timestamp(meta["ende"]) - pd.Timestamp(meta["start"])
        return f"{int(d.total_seconds() // 60)} min {int(d.total_seconds() % 60)} s"
    except Exception:
        return "–"


def _txt(x) -> str:
    return "–" if _leer(x) else str(x)


def _zitat(text: str, n: int = 300) -> str:
    t = "" if _leer(text) else " ".join(str(text).split())
    return t if len(t) <= n else t[:n] + " …"


def ergebnis_auto_md(auswertungen: list[dict], soll: pd.DataFrame) -> str:
    md = ["# ERGEBNIS H1 (inkl. H1b)", "",
          "Automatisch erzeugt von `python -m src.evaluate` (Abschnitte 1–4 und Material für 5).",
          "Abschnitte 5–8 unten sind manuell gepflegt. Begriffe: siehe `README.md` und `DECISIONS.md`.", "",
          "## 1. Lauf-Metadaten", "",
          "| run_id | Konfig | Modell-Snapshot | reasoning_effort | Dauer | Tokens in | Tokens out | Websuchen | Kosten USD (geschätzt) | Status |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for a in auswertungen:
        m, p = a["lauf"]["meta"], a["lauf"]["protokoll"]
        status = "abgebrochen" if p.get("abgebrochen") else (
            f"{len(p.get('stufe2_fehlgeschlagen', []))} Task(s) fehlgeschlagen" if p.get("stufe2_fehlgeschlagen") else "ok")
        md.append(f"| {m.get('run_id')} | {m.get('konfig')} | `{m.get('modell')}` | {m.get('reasoning_effort')} | "
                  f"{_dauer(m)} | {_zahl(m.get('tokens_input'))} | {_zahl(m.get('tokens_output'))} | "
                  f"{p.get('web_search_aufrufe', '–')} | {m.get('kosten_usd_geschaetzt')} | {status} |")

    md += ["", "## 2. Stufe 1 – Rechtsrahmen", ""]
    for a in auswertungen:
        k, s1 = a["kennzahlen"], a["lauf"]["stufe1"]
        md.append(f"### {k['run_id']}")
        if s1 is None:
            md += ["Keine Stufe 1 (Konfiguration B oder Lauf abgebrochen).", ""]
            continue
        md += ["", "| Regelwerk (Agent) | normiert | Ebene | Sicherheit | Quelle |", "| --- | --- | --- | --- | --- |"]
        md += [f"| {e['regelwerk']} | {norm_regelwerk(e['regelwerk'], e.get('vollstaendiger_titel', ''))} | "
               f"{e.get('ebene')} | {e.get('sicherheit')} | {e.get('quelle_url')} |" for e in s1]
        md += ["", f"- **Gefunden ({len(k['s1_gefunden'])}):** {', '.join(k['s1_gefunden']) or '–'}",
               f"- **Übersehen ({len(k['s1_uebersehen'])}):** {', '.join(k['s1_uebersehen']) or '–'}",
               f"- **Zusätzlich ({len(k['s1_zusaetzlich'])}):** {', '.join(k['s1_zusaetzlich']) or '–'}",
               f"- Recall {_p(k['s1_recall'])}, Präzision {_p(k['s1_praezision'])}", ""]

    md += ["## 3. Stufe 2 – Zuordnung je Task", "",
           "Bewertet werden Funde mit `typ = zuordnung`; Recall/Präzision auf Ebene Fundstelle "
           "(Lücken-Funde siehe Abschnitt 4).", ""]
    for a in auswertungen:
        k = a["kennzahlen"]
        md += [f"### {k['run_id']}", "",
               f"- Funde: {k['s2_anzahl_funde']} (korrekt {k['s2_n_korrekt']}, falscher_absatz {k['s2_n_falscher_absatz']}, "
               f"falscher_task {k['s2_n_falscher_task']}, nicht_in_soll {k['s2_n_nicht_in_soll']})",
               f"- Gesamt: Recall {_p(k['s2_recall'])}, Präzision {_p(k['s2_praezision'])}", "",
               "| Teilprozess | Recall | Präzision |", "| --- | --- | --- |"]
        md += [f"| {tp} | {_p(k[f's2_recall_{tp}'])} | {_p(k.get(f's2_praezision_{tp}'))} |"
               for tp in TEILPROZESSE + ["GESAMT"]]
        ueb = a["uebersehen"][a["uebersehen"]["typ"] == "zuordnung"]
        md += ["", "Übersehene Soll-Zeilen (Zuordnung): " +
               ("; ".join(f"{r.soll_id} {r.regelwerk} {r.fundstelle} → {r.task_id}".replace("  ", " ")
                          for r in ueb.itertuples()) or "–"), ""]

    md += ["## 4. H1b – Lückenkandidaten", ""]
    for a in auswertungen:
        k, kand = a["kennzahlen"], a["kandidaten"]
        md += [f"### {k['run_id']}", "",
               f"- Lücken-Recall: {_p(k['luecken_recall'])} · Kandidaten (dedupliziert nach Regelwerk + Norm): "
               f"{k['luecken_kandidaten']} · falsche Lückenmeldungen: {k['falsche_luecken']} "
               f"(davon Gleichstellungsbeauftragte: {k['falsche_luecken_gleichstellung']})", ""]
        if len(kand):
            md += ["| Quelle | Task | Regelwerk | Fundstelle | Fehlender Schritt (Agent) | trifft Soll-Lücke |",
                   "| --- | --- | --- | --- | --- | --- |"]
            md += [f"| {r['quelle']} | {_txt(r['task_id'])} | {r['regelwerk']} | {_txt(r['fundstelle'])} | "
                   f"{_txt(_zitat(r['fehlender_schritt'], 200))} | {r['soll_ids'] or '**nein**'} |"
                   for _, r in kand.iterrows()]
        soll_l = soll[soll["typ"] == "luecke"]
        getroffen = {x for v in kand.get("soll_ids", []) for x in str(v).split(",") if x}
        md += ["", "| Soll-Lücke | Regelwerk | Fundstelle | Inhalt | erkannt |", "| --- | --- | --- | --- | --- |"]
        md += [f"| {r.soll_id} | {r.regelwerk} | {r.fundstelle or '–'} | {r.inhalt} | "
               f"{'ja' if r.soll_id in getroffen else 'nein'} |" for r in soll_l.itertuples()]
        md.append("")

    md += ["## 5a. Material: Funde `nicht_in_soll` (manuell prüfen)", "",
           "Automatisch gelistet; Begründung = Zitat aus der Rohantwort des Modells.", ""]
    for a in auswertungen:
        f = a["funde"]
        if f.empty:
            continue
        nis = f[f["bewertung"] == "nicht_in_soll"]
        md += [f"### {a['kennzahlen']['run_id']} ({len(nis)} Funde)", "",
               "| fund_id | Task | Regelwerk | Fundstelle | Sicherheit | Zitat Begründung |", "| --- | --- | --- | --- | --- | --- |"]
        md += [f"| {r.fund_id} | {r.task_id} | {r.regelwerk} | {r.fundstelle} | {r.sicherheit} | "
               f"{_zitat(r.begruendung, 220).replace('|', '/')} |" for r in nis.itertuples()]
        md.append("")
    return "\n".join(md)


MANUELL_VORLAGE = f"""{MANUELL_START}

## 5. Auffälligkeiten

(noch nicht ausgefüllt)

## 6. Technische Probleme

(noch nicht ausgefüllt)

## 7. Offene Fragen und Annahmen

(noch nicht ausgefüllt)

## 8. Verbesserungsvorschläge

(noch nicht ausgefüllt)

{MANUELL_ENDE}
"""


def schreibe_ergebnis(pfad: Path, auto: str) -> None:
    manuell = MANUELL_VORLAGE
    if pfad.exists():
        alt = pfad.read_text(encoding="utf-8")
        if MANUELL_START in alt:
            manuell = alt[alt.index(MANUELL_START):]
    pfad.write_text(auto.rstrip() + "\n\n" + manuell, encoding="utf-8")


def main() -> None:
    cfg = lade_config()
    parser = argparse.ArgumentParser(description="H1: Auswertung gegen die Soll-Liste")
    parser.add_argument("--runs", nargs="*", help="run_ids (Standard: alle Läufe in runs/)")
    args = parser.parse_args()

    run_dirs = sorted(p for p in cfg.runs_dir.iterdir() if p.is_dir() and (p / "meta.json").exists())
    if args.runs:
        run_dirs = [p for p in run_dirs if p.name in args.runs]
    if not run_dirs:
        raise SystemExit("Keine Läufe gefunden.")

    soll = lade_soll(cfg)
    auswertungen = [werte_lauf_aus(lade_lauf(d), soll) for d in run_dirs]
    out = cfg.results_dir
    out.mkdir(parents=True, exist_ok=True)

    funde = pd.concat([a["funde"] for a in auswertungen if not a["funde"].empty] or [pd.DataFrame()])
    funde.to_csv(out / "funde_bewertet.csv", sep=";", index=False)
    pd.concat([a["uebersehen"] for a in auswertungen]).to_csv(out / "uebersehen.csv", sep=";", index=False)
    kennzahlen = kennzahlen_tabelle(auswertungen)
    kennzahlen.to_csv(out / "kennzahlen.csv", sep=";", index=False, float_format="%.4f")
    (out / "zusammenfassung.md").write_text(zusammenfassung_md(kennzahlen), encoding="utf-8")
    schreibe_ergebnis(out / "ERGEBNIS.md", ergebnis_auto_md(auswertungen, soll))
    print(f"{len(auswertungen)} Lauf/Läufe ausgewertet → {out}")


if __name__ == "__main__":
    main()
