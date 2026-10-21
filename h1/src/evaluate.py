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
from . import kosten
from .models import Fund
from .normierung import eu_bezeichnung, absatz_nummer, fundstelle_text, norm_fundstelle, norm_regelwerk, zerlege_fund
from .stufe2 import lueckenkandidaten
from .werkzeuge import Werkzeuge, norm_schluessel

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
    soll["tasks"] = soll["task_id"].map(lambda t: [x.strip() for x in t.split("|") if x.strip()])
    soll["teilprozess"] = soll["tasks"].map(lambda ts: tp_von(ts[0]) if ts else "GESAMT")
    return soll


def lade_lauf(run_dir: Path) -> dict:
    def json_oder(name, default):
        p = run_dir / name
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

    funde_pfad = run_dir / "funde.jsonl"
    funde = [json.loads(z) for z in funde_pfad.read_text(encoding="utf-8").splitlines() if z.strip()] \
        if funde_pfad.exists() else []
    meta = json_oder("meta.json", {})
    stufe1 = json_oder("stufe1.json", {}).get("rechtsrahmen")
    rechtsrahmen = stufe1 if stufe1 is not None else json_oder("rechtsrahmen_vorgabe.json", {}).get("rechtsrahmen")
    return {
        "dir": run_dir,
        "meta": meta,
        "version": meta.get("version", "v1"),
        "stufe1": stufe1,
        "rechtsrahmen": rechtsrahmen or [],
        "funde": funde,
        "protokoll": json_oder("protokoll.json", {}),
        "geladen": _geladene_normen(run_dir),
    }


def _geladene_normen(run_dir: Path) -> dict[str, set] | None:
    """Je Aufruf (z. B. 'stufe2_T1.1') die mit lade_norm erfolgreich geladenen (Kennung, Norm) des letzten Versuchs;
    None, wenn der Lauf keine eigenen Werkzeuge nutzte."""
    dateien = list((run_dir / "raw").glob("werkzeuge_*.jsonl"))
    if not dateien:
        return None
    geladen = {}
    for d in dateien:
        eintraege = [json.loads(z) for z in d.read_text(encoding="utf-8").splitlines() if z.strip()]
        letzter = max((e.get("versuch", 1) for e in eintraege), default=1)
        geladen[d.stem.removeprefix("werkzeuge_")] = {
            (e.get("kennung"), e.get("norm_schluessel")) for e in eintraege
            if e.get("versuch", 1) == letzter and e["funktion"] == "lade_norm" and e["gefunden"]}
    return geladen


# --------------------------------------------------------------------------- Existenzprüfung

def _kennung(werkzeuge: Werkzeuge, roh: str, kurz: str) -> str | None:
    for kandidat in (eu_bezeichnung(kurz), kurz, roh):
        if kandidat and (k := werkzeuge.kennung(kandidat)):
            return k
    return None


def pruefe_fund(fund: dict, werkzeuge: Werkzeuge | None, geladen: set | None) -> tuple[str, bool | None]:
    """-> (existiert: 'ja' | 'nein' | 'unbekannt', vorher_geladen: True/False/None).
    'nein', wenn mindestens eine genannte Norm im (auflösbaren) Regelwerk nicht vorkommt; 'unbekannt', wenn das
    Regelwerk nicht auflösbar ist, keine Norm erkannt wird oder das Regelwerk keine Normen dieser Art enthält
    (z. B. Anlagen des TV-L)."""
    if werkzeuge is None:
        return "unbekannt", None
    ergebnisse, geladen_alle = [], True
    teile = zerlege_fund(fund["regelwerk"], fund["fundstelle"])
    for rw, art, _ in teile:
        key = norm_schluessel(art) if art else None
        k = _kennung(werkzeuge, fund["regelwerk"] if len(teile) == 1 else rw, rw)
        if not k or not key:
            ergebnisse.append(None)
            geladen_alle = False
            continue
        try:
            dok = werkzeuge.dokument(k)
        except Exception:
            ergebnisse.append(None)
            geladen_alle = False
            continue
        if key in dok.normen:
            ergebnisse.append(True)
        elif any(n.split()[0] == key.split()[0] for n in dok.normen):
            ergebnisse.append(False)
        else:
            ergebnisse.append(None)
        geladen_alle &= geladen is not None and (k, key) in geladen
    existiert = "nein" if False in ergebnisse else ("ja" if ergebnisse and all(ergebnisse) else "unbekannt")
    return existiert, (geladen_alle if geladen is not None else None)


# --------------------------------------------------------------------------- Bewertung

def _leer(x) -> bool:
    return x is None or (isinstance(x, float) and pd.isna(x)) or x == ""


def _art_passt(zeile, art) -> bool:
    return _leer(zeile["art"]) or zeile["art"] == art


def _abs_passt(zeile, absaetze: frozenset) -> bool:
    return _leer(zeile["abs"]) or absatz_nummer(zeile["abs"]) in absaetze


def _abs_passt_luecke(zeile, absaetze: frozenset) -> bool:
    """Lücken: Absatz nur prüfen, wenn Soll-Zeile und Meldung beide einen nennen."""
    return not absaetze or _abs_passt(zeile, absaetze)


RANG = ["korrekt", "neutral", "falscher_absatz", "falscher_task", "nicht_in_soll"]
RANG_LUECKE = ["luecke_korrekt", "luecke_neutral", "luecke_an_vorhandener_zuordnung", "luecke_ohne_soll"]
LUECKE_FALSCH = ["luecke_an_vorhandener_zuordnung", "luecke_ohne_soll"]
KONTROLLE_SOLL_ID = "S23"


def _zeilen(soll: pd.DataFrame, rw: str, art, typ: str) -> list:
    return [z for _, z in soll[(soll["rw"] == rw) & (soll["typ"] == typ)].iterrows() if _art_passt(z, art)]


def _bewerte_norm(rw: str, art, absaetze: frozenset, task_id: str,
                  soll: pd.DataFrame) -> tuple[str, list[str]]:
    """Eine Norm eines Funds mit typ = zuordnung."""
    zuo = _zeilen(soll, rw, art, "zuordnung") + _zeilen(soll, rw, art, "luecke")
    passend = [z for z in zuo if z["typ"] == "zuordnung" and (task_id in z["tasks"] or "GESAMT" in z["tasks"])]
    treffer = [z["soll_id"] for z in passend if _abs_passt(z, absaetze)]
    if treffer:
        return "korrekt", treffer
    if any(_abs_passt(z, absaetze) for z in _zeilen(soll, rw, art, "neutral")):
        return "neutral", []
    if passend:
        return "falscher_absatz", []
    if zuo:
        return "falscher_task", []
    return "nicht_in_soll", []


def _bewerte_norm_luecke(rw: str, art, absaetze: frozenset,
                         soll: pd.DataFrame) -> tuple[str, list[str], list[str]]:
    """Eine Norm eines Funds mit typ = moegliche_luecke -> (Kategorie, getroffene Soll-Lücken,
    getroffene Soll-Zuordnungen)."""
    luecken = [z["soll_id"] for z in _zeilen(soll, rw, art, "luecke") if _abs_passt_luecke(z, absaetze)]
    zuo = [z["soll_id"] for z in _zeilen(soll, rw, art, "zuordnung") if _abs_passt_luecke(z, absaetze)]
    if luecken:
        return "luecke_korrekt", luecken, zuo
    if any(_abs_passt(z, absaetze) for z in _zeilen(soll, rw, art, "neutral")):
        return "luecke_neutral", [], zuo
    if zuo:
        return "luecke_an_vorhandener_zuordnung", [], zuo
    return "luecke_ohne_soll", [], zuo


def bewerte_fund(fund: dict, soll: pd.DataFrame) -> tuple[str, list[str], list[str]]:
    """Liefert (bewertung, getroffene soll_ids, bei Lücken zusätzlich getroffene Soll-Zuordnungen).
    Nennt ein Fund mehrere Normen, wird jede einzeln bewertet; es zählt die beste Bewertung,
    getroffen sind alle korrekt bewerteten Zeilen."""
    luecke = fund["typ"] == "moegliche_luecke"
    rang = RANG_LUECKE if luecke else RANG
    beste, treffer, zuo_treffer = rang[-1], [], []
    for rw, art, absaetze in zerlege_fund(fund["regelwerk"], fund["fundstelle"]):
        if luecke:
            bewertung, ids, zuo = _bewerte_norm_luecke(rw, art, absaetze, soll)
            zuo_treffer += [i for i in zuo if i not in zuo_treffer]
        else:
            bewertung, ids = _bewerte_norm(rw, art, absaetze, fund["task_id"], soll)
        treffer += [i for i in ids if i not in treffer]
        if rang.index(bewertung) < rang.index(beste):
            beste = bewertung
    return beste, treffer, zuo_treffer


def bewerte_kandidat(k: dict, soll: pd.DataFrame) -> list[str]:
    """Soll-Lücken, die ein Regelwerk ohne Zuordnung trifft: jede Soll-Lücke desselben Regelwerks."""
    rw = norm_regelwerk(k["regelwerk"], k.get("vollstaendiger_titel", ""))
    return list(soll[(soll["typ"] == "luecke") & (soll["rw"] == rw)]["soll_id"])


def _anteil(maske) -> float | None:
    return maske.mean() if len(maske) else None


def werte_lauf_aus(lauf: dict, soll: pd.DataFrame, werkzeuge: Werkzeuge | None = None) -> dict:
    meta = lauf["meta"]
    run_id, konfig, version = meta.get("run_id", lauf["dir"].name), meta.get("konfig", "?"), lauf["version"]

    # Funde bewerten
    zeilen, gefunden, gefunden_inkl_luecke, luecken_gefunden = [], set(), set(), set()
    for f in lauf["funde"]:
        bewertung, treffer, zuo_treffer = bewerte_fund(f, soll)
        rw, art, _ = zerlege_fund(f["regelwerk"], f["fundstelle"])[0]
        geladen = None if lauf["geladen"] is None else lauf["geladen"].get(f"stufe2_{f['task_id']}", set())
        existiert, vorher_geladen = pruefe_fund(f, werkzeuge, geladen)
        if f["typ"] == "zuordnung":
            gefunden.update(treffer)
        else:
            luecken_gefunden.update(treffer)
            # Lückenmeldung, die eine vorhandene Soll-Zuordnung am selben Task nennt
            gefunden_inkl_luecke.update(bewerte_fund({**f, "typ": "zuordnung"}, soll)[1])
        zeilen.append({**f, "hinweis": f.get("hinweis"), "version": version, "konfig": konfig,
                       "teilprozess": tp_von(f["task_id"]),
                       "regelwerk_norm": norm_regelwerk(f["regelwerk"]), "art_norm": art or "",
                       "fundstelle_norm": fundstelle_text(f["fundstelle"]),
                       "bewertung": bewertung, "soll_ids": ",".join(treffer),
                       "soll_zuordnungen_bei_luecke": ",".join(zuo_treffer),
                       "existiert": existiert, "erfunden": existiert == "nein", "vorher_geladen": vorher_geladen,
                       "manuell_pruefen": bewertung in ("nicht_in_soll", "luecke_ohne_soll")})
    funde = pd.DataFrame(zeilen)
    zuo = funde[funde["typ"] == "zuordnung"] if len(funde) else funde
    lue = funde[funde["typ"] == "moegliche_luecke"] if len(funde) else funde

    # Lückenmeldungen dedupliziert nach (Regelwerk, Artikel/Paragraf); beste Kategorie je Gruppe
    if len(lue):
        lue_unique = lue.groupby(["regelwerk_norm", "art_norm"], as_index=False).agg(
            kategorie=("bewertung", lambda s: min(s, key=RANG_LUECKE.index)),
            soll_ids=("soll_ids", lambda s: ",".join(sorted({x for v in s for x in v.split(",") if x}))),
            soll_zuordnungen=("soll_zuordnungen_bei_luecke",
                              lambda s: ",".join(sorted({x for v in s for x in v.split(",") if x}))),
            anzahl_meldungen=("fund_id", "size"),
            tasks=("task_id", lambda s: ",".join(sorted(set(s)))))
    else:
        lue_unique = pd.DataFrame(columns=["regelwerk_norm", "art_norm", "kategorie", "soll_ids",
                                           "soll_zuordnungen", "anzahl_meldungen", "tasks"])

    # Regelwerke aus Stufe 1 (bzw. Vorgabe B) ohne Zuordnung -> nur für den großzügigen Lücken-Recall
    ohne_zuordnung = [k for k in lueckenkandidaten(lauf["rechtsrahmen"], [Fund(**{**f, "hinweis": f.get("hinweis")})
                                                                         for f in lauf["funde"]])
                      if k["quelle"] == "regelwerk_ohne_zuordnung"]
    luecken_grosszuegig = set(luecken_gefunden)
    for kand in ohne_zuordnung:
        kand["soll_ids"] = ",".join(bewerte_kandidat(kand, soll))
        luecken_grosszuegig.update(x for x in kand["soll_ids"].split(",") if x)

    # Kennzahlen
    k = {"run_id": run_id, "version": version, "konfig": konfig}
    bewertet = soll[soll["typ"].isin(["zuordnung", "luecke"])]
    soll_rw = set(bewertet["rw"])
    neutral_rw = set(soll[soll["typ"] == "neutral"]["rw"]) - soll_rw
    if lauf["stufe1"] is not None:
        s1 = {norm_regelwerk(e["regelwerk"], e.get("vollstaendiger_titel", "")) for e in lauf["stufe1"]}
        bewertbar = s1 - neutral_rw
        k["s1_recall"] = len(s1 & soll_rw) / len(soll_rw)
        k["s1_praezision"] = len(s1 & soll_rw) / len(bewertbar) if bewertbar else 0.0
        k["s1_gefunden"] = sorted(s1 & soll_rw)
        k["s1_uebersehen"] = sorted(soll_rw - s1)
        k["s1_zusaetzlich"] = sorted(bewertbar - soll_rw)
        k["s1_neutral"] = sorted(s1 & neutral_rw)
    else:
        k.update(s1_recall=None, s1_praezision=None, s1_gefunden=[], s1_uebersehen=[], s1_zusaetzlich=[],
                 s1_neutral=[])

    soll_z = soll[soll["typ"] == "zuordnung"]
    k["s2_anzahl_funde"] = len(zuo)
    k["s2_recall"] = soll_z["soll_id"].isin(gefunden).mean()
    k["s2_recall_inkl_luecke"] = soll_z["soll_id"].isin(gefunden | gefunden_inkl_luecke).mean()
    ohne_neutral = zuo[zuo["bewertung"] != "neutral"] if len(zuo) else zuo
    k["s2_praezision"] = _anteil(ohne_neutral["bewertung"] == "korrekt") if len(zuo) else None
    k["s2_anteil_neutral"] = _anteil(zuo["bewertung"] == "neutral") if len(zuo) else None
    for tp in TEILPROZESSE + ["GESAMT"]:
        sz = soll_z[soll_z["teilprozess"] == tp]
        k[f"s2_recall_{tp}"] = sz["soll_id"].isin(gefunden).mean() if len(sz) else None
        if tp != "GESAMT":
            zf = ohne_neutral[ohne_neutral["teilprozess"] == tp] if len(ohne_neutral) else ohne_neutral
            k[f"s2_praezision_{tp}"] = _anteil(zf["bewertung"] == "korrekt") if len(zf) else None
    for b in RANG:
        k[f"s2_n_{b}"] = int((zuo["bewertung"] == b).sum()) if len(zuo) else 0

    soll_l = soll[soll["typ"] == "luecke"]
    k["luecken_recall"] = soll_l["soll_id"].isin(luecken_gefunden).mean()
    k["luecken_recall_grosszuegig"] = soll_l["soll_id"].isin(luecken_grosszuegig).mean()
    k["luecken_meldungen"] = len(lue)
    k["luecken_meldungen_dedupliziert"] = len(lue_unique)
    for kat in RANG_LUECKE:
        k[f"luecken_n_{kat}"] = int((lue_unique["kategorie"] == kat).sum())
    k["falsche_luecken"] = int(lue_unique["kategorie"].isin(LUECKE_FALSCH).sum())
    k["kontrolle_fehlmeldungen"] = int(lue_unique["soll_zuordnungen"].map(
        lambda v: KONTROLLE_SOLL_ID in v.split(",")).sum())
    k["regelwerke_ohne_zuordnung"] = len(ohne_zuordnung)
    k["anteil_hinweis"] = _anteil(zuo["hinweis"].map(lambda h: not _leer(h))) if len(zuo) else None
    k["anteil_unsicher"] = _anteil(funde["sicherheit"] == "unsicher") if len(funde) else None
    k["anteil_nicht_in_soll"] = _anteil(funde["bewertung"].isin(["nicht_in_soll", "luecke_ohne_soll"])) \
        if len(funde) else None
    k["anteil_erfunden"] = _anteil(funde["existiert"] == "nein") if len(funde) else None
    k["n_erfunden"] = int((funde["existiert"] == "nein").sum()) if len(funde) else 0
    k["anteil_existenz_unbekannt"] = _anteil(funde["existiert"] == "unbekannt") if len(funde) else None
    k["anteil_vorher_geladen"] = (_anteil(funde["vorher_geladen"] == True)  # noqa: E712
                                  if len(funde) and lauf["geladen"] is not None else None)
    k["werkzeugaufrufe"] = meta.get("werkzeugaufrufe") if meta.get("suche") == "eigen" else None
    k["werkzeugaufrufe_nicht_gefunden"] = meta.get("werkzeugaufrufe_nicht_gefunden") if meta.get("suche") == "eigen" else None
    k["tokens_input"] = meta.get("tokens_input", 0)
    k["tokens_output"] = meta.get("tokens_output", 0)
    k["websuchen"] = lauf["protokoll"].get("web_search_aufrufe")
    k["kosten_usd"] = meta.get("kosten_usd_geschaetzt", 0.0)

    uebersehen = soll[soll["typ"].isin(["zuordnung", "luecke"]) & ~soll["soll_id"].isin(gefunden | luecken_gefunden)][
        ["soll_id", "regelwerk", "fundstelle", "task_id", "typ", "inhalt"]].copy()
    uebersehen.insert(0, "konfig", konfig)
    uebersehen.insert(0, "version", version)
    uebersehen.insert(0, "run_id", run_id)
    lue_unique.insert(0, "konfig", konfig)
    lue_unique.insert(0, "version", version)
    lue_unique.insert(0, "run_id", run_id)
    return {"lauf": lauf, "kennzahlen": k, "funde": funde, "luecken_unique": lue_unique,
            "ohne_zuordnung": ohne_zuordnung, "uebersehen": uebersehen,
            "gefunden": gefunden, "luecken_gefunden": luecken_gefunden}


# --------------------------------------------------------------------------- Ausgabe

LISTEN_SPALTEN = ["s1_gefunden", "s1_uebersehen", "s1_zusaetzlich", "s1_neutral"]
GRUPPE = ["version", "konfig"]


def kennzahlen_tabelle(auswertungen: list[dict]) -> pd.DataFrame:
    lauf = pd.DataFrame([{**a["kennzahlen"], "ebene": "lauf", "statistik": "wert"} for a in auswertungen])
    for c in LISTEN_SPALTEN:
        lauf[c] = lauf[c].map(lambda v: ", ".join(v))
    zahlen = [c for c in lauf.columns if c not in LISTEN_SPALTEN + ["run_id"] + GRUPPE + ["ebene", "statistik"]]
    lauf[zahlen] = lauf[zahlen].apply(pd.to_numeric, errors="coerce")
    agg = []
    for (version, konfig), g in lauf.groupby(GRUPPE):
        for stat in ["mittelwert", "std"]:
            werte = g[zahlen].mean() if stat == "mittelwert" else g[zahlen].std(ddof=1)
            agg.append({"run_id": f"alle ({len(g)} Läufe)", "version": version, "konfig": konfig,
                        "ebene": "konfig", "statistik": stat, **werte.to_dict()})
    tab = pd.concat([lauf, pd.DataFrame(agg)], ignore_index=True)
    vorne = ["ebene", "statistik", "run_id"] + GRUPPE
    return tab[vorne + [c for c in tab.columns if c not in vorne]]


def _p(x) -> str:
    return "–" if x is None or pd.isna(x) else f"{x:.0%}"


def _zahl(x, nachkomma=0) -> str:
    return "–" if x is None or pd.isna(x) else f"{x:,.{nachkomma}f}".replace(",", " ")


def _zahl1(x) -> str:
    return _zahl(x, 1)


def _gruppen(kennzahlen: pd.DataFrame) -> list[tuple[str, str, int]]:
    lauf = kennzahlen[kennzahlen["ebene"] == "lauf"]
    return [(v, k, len(g)) for (v, k), g in lauf.groupby(GRUPPE)]


def _gruppen_kopf(gruppen) -> list[str]:
    return [" | ".join(f"{v} {k} (n={n})" for v, k, n in gruppen), " | ".join("---" for _ in gruppen)]


def _mw_sd(kennzahlen: pd.DataFrame, version: str, konfig: str, spalte: str, fmt) -> str:
    agg = kennzahlen[(kennzahlen["ebene"] == "konfig") & (kennzahlen["version"] == version)
                     & (kennzahlen["konfig"] == konfig)]
    m, s = agg[agg["statistik"] == "mittelwert"], agg[agg["statistik"] == "std"]
    if m.empty or spalte not in m:
        return "–"
    mw, sd = m[spalte].iloc[0], s[spalte].iloc[0]
    if pd.isna(mw):
        return "–"
    return fmt(mw) + ("" if pd.isna(sd) else f" ± {fmt(sd)}")


def _kennzahl_tabelle(kennzahlen: pd.DataFrame, zeilen: list[tuple]) -> list[str]:
    gruppen = _gruppen(kennzahlen)
    kopf, linie = _gruppen_kopf(gruppen)
    md = [f"| Kennzahl | {kopf} |", f"| --- | {linie} |"]
    for titel, spalte, fmt in zeilen:
        md.append(f"| {titel} | " + " | ".join(_mw_sd(kennzahlen, v, k, spalte, fmt) for v, k, _ in gruppen) + " |")
    return md


ZEILEN_UEBERSICHT = [
    ("Stufe 1 Recall (Regelwerk)", "s1_recall", _p), ("Stufe 1 Präzision (Regelwerk)", "s1_praezision", _p),
    ("Stufe 2 Recall (Fundstelle)", "s2_recall", _p), ("Stufe 2 Präzision (ohne neutral)", "s2_praezision", _p),
    ("Stufe 2 Anteil neutral", "s2_anteil_neutral", _p),
    ("Stufe 2 Recall inkl. Lückenmeldungen am Soll-Task", "s2_recall_inkl_luecke", _p),
    ("Stufe 2 Anzahl Funde (zuordnung)", "s2_anzahl_funde", _zahl1),
    ("H1b Lücken-Recall (streng)", "luecken_recall", _p),
    ("H1b Lücken-Recall (großzügig)", "luecken_recall_grosszuegig", _p),
    ("H1b Lückenmeldungen (Funde)", "luecken_meldungen", _zahl1),
    ("H1b Lückenmeldungen (dedupliziert)", "luecken_meldungen_dedupliziert", _zahl1),
    ("H1b falsche Lückenmeldungen (dedupliziert)", "falsche_luecken", _zahl1),
    ("H1b Kontrolle: Fehlmeldungen S23", "kontrolle_fehlmeldungen", _zahl1),
    ("Anteil Zuordnungen mit Hinweis", "anteil_hinweis", _p),
    ("Anteil erfundene Normen (existiert = nein)", "anteil_erfunden", _p),
    ("Anzahl erfundene Normen", "n_erfunden", _zahl1),
    ("Anteil Existenz nicht prüfbar", "anteil_existenz_unbekannt", _p),
    ("Anteil Funde mit vorher geladener Norm", "anteil_vorher_geladen", _p),
    ("Werkzeugaufrufe", "werkzeugaufrufe", _zahl1),
    ("Werkzeugaufrufe ohne Ergebnis", "werkzeugaufrufe_nicht_gefunden", _zahl1),
    ("Anteil unsicher", "anteil_unsicher", _p), ("Anteil nicht_in_soll / luecke_ohne_soll", "anteil_nicht_in_soll", _p),
    ("Tokens Input", "tokens_input", _zahl), ("Tokens Output", "tokens_output", _zahl),
    ("Websuchen", "websuchen", _zahl1), ("Kosten USD (geschätzt)", "kosten_usd", lambda x: _zahl(x, 3)),
]


def zusammenfassung_md(kennzahlen: pd.DataFrame) -> str:
    md = ["# Zusammenfassung H1 je Version und Konfiguration", "",
          "Mittelwert ± Standardabweichung über alle Läufe je (version, konfig); alle Läufe gegen die aktuelle "
          "Soll-Liste ausgewertet.", ""]
    return "\n".join(md + _kennzahl_tabelle(kennzahlen, ZEILEN_UEBERSICHT)) + "\n"


def _dauer_s(meta: dict) -> float | None:
    try:
        return (pd.Timestamp(meta["ende"]) - pd.Timestamp(meta["start"])).total_seconds()
    except Exception:
        return None


def _dauer(meta: dict) -> str:
    d = _dauer_s(meta)
    return "–" if d is None else f"{int(d // 60)} min {int(d % 60)} s"


def _txt(x) -> str:
    return "–" if _leer(x) else str(x)


def _zitat(text: str, n: int = 300) -> str:
    t = "" if _leer(text) else " ".join(str(text).split())
    t = t.replace("|", "/")
    return t if len(t) <= n else t[:n] + " …"


def _nach_gruppe(auswertungen: list[dict]) -> dict[tuple[str, str], list[dict]]:
    gruppen: dict[tuple[str, str], list[dict]] = {}
    for a in auswertungen:
        gruppen.setdefault((a["kennzahlen"]["version"], a["kennzahlen"]["konfig"]), []).append(a)
    return dict(sorted(gruppen.items()))


def ergebnis_auto_md(auswertungen: list[dict], soll: pd.DataFrame, kennzahlen: pd.DataFrame) -> str:
    gruppen = _nach_gruppe(auswertungen)
    kopf, linie = _gruppen_kopf([(v, k, len(g)) for (v, k), g in gruppen.items()])
    try:
        warn = kosten.warnung()
    except Exception:
        warn = None
    md = ["# ERGEBNIS H1 (inkl. H1b)", ""] + ([warn, ""] if warn else []) + [
          "Automatisch erzeugt von `python -m src.evaluate` (Abschnitte 1–4 und Material 5a). Alle Läufe sind gegen die "
          "**aktuelle** Soll-Liste ausgewertet und nach (`version`, `konfig`) gruppiert; Werte = Mittelwert ± "
          "Standardabweichung über die Läufe. Abschnitte 5–8 unten sind manuell gepflegt. Begriffe: `README.md`, "
          "`DECISIONS.md`. Details je Lauf: `results/kennzahlen.csv`, `funde_bewertet.csv`, `luecken_bewertet.csv`, "
          "`uebersehen.csv`.", "",
          "## 1. Lauf-Metadaten", "",
          "| run_id | Version | Konfig | Suche | Modell-Snapshot | reasoning_effort | Dauer | Tokens in | Tokens out | Websuchen / Werkzeugaufrufe | Kosten USD (geschätzt) | Status |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for a in auswertungen:
        m, p = a["lauf"]["meta"], a["lauf"]["protokoll"]
        status = "abgebrochen" if p.get("abgebrochen") else (
            f"{len(p.get('stufe2_fehlgeschlagen', []))} Task(s) fehlgeschlagen" if p.get("stufe2_fehlgeschlagen") else "ok")
        retries = len(p.get("fehler", []))
        suche = m.get("suche", "openai")
        aufrufe = (f"{m.get('werkzeugaufrufe', 0)} ({m.get('werkzeugaufrufe_nicht_gefunden', 0)} ohne Ergebnis)"
                   if suche == "eigen" else p.get('web_search_aufrufe', '–'))
        md.append(f"| {m.get('run_id')} | {a['lauf']['version']} | {m.get('konfig')} | {suche} | `{m.get('modell')}` | "
                  f"{m.get('reasoning_effort')} | {_dauer(m)} | {_zahl(m.get('tokens_input'))} | "
                  f"{_zahl(m.get('tokens_output'))} | {aufrufe} | "
                  f"{m.get('kosten_usd_geschaetzt')} | {status}{f' ({retries} Fehler/Retries)' if retries else ''} |")
    md += ["", "### Übersicht je (version, konfig)", ""] + _kennzahl_tabelle(kennzahlen, ZEILEN_UEBERSICHT)

    # 2. Stufe 1
    md += ["", "## 2. Stufe 1 – Rechtsrahmen", "",
           "Soll-Regelwerke = Regelwerke aus Zeilen mit `typ` zuordnung oder luecke. Regelwerke, die nur in "
           "Neutral-Zeilen stehen, zählen als „neutral“ (nicht als zusätzlich, nicht in der Präzision). "
           "Konfiguration B hat keine Stufe 1.", ""]
    md += _kennzahl_tabelle(kennzahlen, [("Recall", "s1_recall", _p), ("Präzision", "s1_praezision", _p)])
    soll_rw = list(dict.fromkeys(soll[soll["typ"].isin(["zuordnung", "luecke"])]["rw"]))
    neutral_rw = [r for r in dict.fromkeys(soll[soll["typ"] == "neutral"]["rw"]) if r not in soll_rw]
    gruppen_s1 = {g: l for g, l in gruppen.items() if any(a["lauf"]["stufe1"] is not None for a in l)}
    if gruppen_s1:
        alle_rw = soll_rw + neutral_rw + sorted({r for l in gruppen_s1.values() for a in l
                                                 for r in a["kennzahlen"]["s1_zusaetzlich"]})
        md += ["", "In wie vielen Läufen hat Stufe 1 das Regelwerk genannt:", "",
               "| Regelwerk | Status | " + " | ".join(f"{v} {k}" for v, k in gruppen_s1) + " |",
               "| --- | --- | " + " | ".join("---" for _ in gruppen_s1) + " |"]
        for rw in alle_rw:
            status = "Soll" if rw in soll_rw else ("neutral" if rw in neutral_rw else "zusätzlich")
            zellen = []
            for l in gruppen_s1.values():
                n = sum(rw in (a["kennzahlen"]["s1_gefunden"] + a["kennzahlen"]["s1_zusaetzlich"]
                               + a["kennzahlen"]["s1_neutral"]) for a in l)
                zellen.append(f"{n}/{len(l)}")
            md.append(f"| {rw} | {status} | " + " | ".join(zellen) + " |")

    # 3. Stufe 2
    md += ["", "## 3. Stufe 2 – Zuordnung je Task", "",
           "Bewertet werden Funde mit `typ = zuordnung`. Präzision = korrekt / (korrekt + falscher_absatz + "
           "falscher_task + nicht_in_soll); `neutral` geht nicht ein und wird separat ausgewiesen. "
           "Teilprozess einer Soll-Zeile mit mehreren Tasks = Teilprozess des ersten Tasks.", ""]
    md += _kennzahl_tabelle(kennzahlen, [("Funde (zuordnung)", "s2_anzahl_funde", _zahl1)]
                            + [(f"davon {b}", f"s2_n_{b}", _zahl1) for b in RANG]
                            + [("Recall gesamt", "s2_recall", _p), ("Präzision gesamt", "s2_praezision", _p),
                               ("Anteil neutral", "s2_anteil_neutral", _p),
                               ("Recall inkl. Lückenmeldungen am Soll-Task", "s2_recall_inkl_luecke", _p)]
                            + [(f"Recall {tp}", f"s2_recall_{tp}", _p) for tp in TEILPROZESSE + ["GESAMT"]]
                            + [(f"Präzision {tp}", f"s2_praezision_{tp}", _p) for tp in TEILPROZESSE])
    md += ["", "Je Lauf:", "",
           "| run_id | Version | Konfig | Funde | korrekt | neutral | falscher_absatz | falscher_task | nicht_in_soll | Recall | Präzision |",
           "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for a in auswertungen:
        k = a["kennzahlen"]
        md.append(f"| {k['run_id']} | {k['version']} | {k['konfig']} | {k['s2_anzahl_funde']} | "
                  + " | ".join(str(k[f's2_n_{b}']) for b in RANG)
                  + f" | {_p(k['s2_recall'])} | {_p(k['s2_praezision'])} |")
    soll_z = soll[soll["typ"] == "zuordnung"]
    md += ["", "In wie vielen Läufen wurde die Soll-Zuordnung korrekt getroffen:", "",
           f"| Soll | Regelwerk | Fundstelle | Task(s) | {kopf} |", f"| --- | --- | --- | --- | {linie} |"]
    for r in soll_z.itertuples():
        zellen = [f"{sum(r.soll_id in a['gefunden'] for a in l)}/{len(l)}" for l in gruppen.values()]
        md.append(f"| {r.soll_id} | {r.regelwerk} | {r.fundstelle or '–'} | {r.task_id} | " + " | ".join(zellen) + " |")

    # 4. H1b
    md += ["", "## 4. H1b – Lückenkandidaten", "",
           "Kategorien je Lückenmeldung (`typ = moegliche_luecke`), dedupliziert nach Regelwerk + Artikel/Paragraf: "
           "`luecke_korrekt` (trifft Soll-Lücke), `luecke_neutral` (trifft Neutral-Zeile), "
           "`luecke_an_vorhandener_zuordnung` (trifft nur eine Soll-Zuordnung), `luecke_ohne_soll` (trifft nichts). "
           "Falsch = die beiden letzten. Lücken-Recall streng = nur Lückenmeldungen; großzügig = zusätzlich "
           "Regelwerke aus Stufe 1 (B: Vorgabe) ohne Zuordnung. Kontrolle = Lückenmeldungen, die S23 "
           "(Gleichstellungsbeauftragte, vorhandener Schritt) treffen.", ""]
    md += _kennzahl_tabelle(kennzahlen, [
        ("Lücken-Recall streng", "luecken_recall", _p), ("Lücken-Recall großzügig", "luecken_recall_grosszuegig", _p),
        ("Lückenmeldungen (Funde)", "luecken_meldungen", _zahl1),
        ("Lückenmeldungen (dedupliziert)", "luecken_meldungen_dedupliziert", _zahl1)]
        + [(f"davon {kat}", f"luecken_n_{kat}", _zahl1) for kat in RANG_LUECKE]
        + [("falsche Lückenmeldungen", "falsche_luecken", _zahl1),
           ("Kontrolle: Fehlmeldungen S23", "kontrolle_fehlmeldungen", _zahl1),
           ("Regelwerke ohne Zuordnung", "regelwerke_ohne_zuordnung", _zahl1)])
    soll_l = soll[soll["typ"] == "luecke"]
    md += ["", "In wie vielen Läufen wurde die Soll-Lücke erkannt (streng):", "",
           f"| Soll-Lücke | Regelwerk | Fundstelle | Inhalt | {kopf} |", f"| --- | --- | --- | --- | {linie} |"]
    for r in soll_l.itertuples():
        zellen = [f"{sum(r.soll_id in a['luecken_gefunden'] for a in l)}/{len(l)}" for l in gruppen.values()]
        md.append(f"| {r.soll_id} | {r.regelwerk} | {r.fundstelle or '–'} | {_zitat(r.inhalt, 80)} | "
                  + " | ".join(zellen) + " |")
    for (version, konfig), l in gruppen.items():
        lu = pd.concat([a["luecken_unique"] for a in l], ignore_index=True)
        if lu.empty:
            continue
        funde = pd.concat([a["funde"] for a in l if not a["funde"].empty], ignore_index=True)
        tab = lu.groupby(["regelwerk_norm", "art_norm"], as_index=False).agg(
            kategorie=("kategorie", lambda s: min(s, key=RANG_LUECKE.index)),
            laeufe=("run_id", "nunique"), meldungen=("anzahl_meldungen", "sum"),
            soll=("soll_ids", lambda s: ",".join(sorted({x for v in s for x in v.split(",") if x}))),
            zuo=("soll_zuordnungen", lambda s: ",".join(sorted({x for v in s for x in v.split(",") if x}))))
        tab["rang"] = tab["kategorie"].map(RANG_LUECKE.index)
        tab = tab.sort_values(["rang", "laeufe"], ascending=[True, False])
        md += ["", f"### Lückenmeldungen {version} {konfig} ({len(l)} Läufe, dedupliziert je Lauf)", "",
               "| Regelwerk | Norm | Kategorie | Läufe | Meldungen | Soll-Lücke | Soll-Zuordnung | Beispiel fehlender Schritt |",
               "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for r in tab.itertuples():
            bsp = funde[(funde["typ"] == "moegliche_luecke") & (funde["regelwerk_norm"] == r.regelwerk_norm)
                        & (funde["art_norm"] == r.art_norm)]["fehlender_schritt"]
            md.append(f"| {r.regelwerk_norm} | {r.art_norm or '–'} | {r.kategorie} | {r.laeufe} | {r.meldungen} | "
                      f"{r.soll or '–'} | {r.zuo or '–'} | {_zitat(bsp.iloc[0] if len(bsp) else '', 160)} |")

    # 5a. Material
    md += ["", "## 5a. Material: Funde `nicht_in_soll` / `luecke_ohne_soll` (manuell prüfen)", "",
           "Zusammengefasst je Regelwerk + Norm über alle Läufe einer Gruppe; Zitat und Quelle aus dem ersten Fund.", ""]
    for (version, konfig), l in gruppen.items():
        funde = pd.concat([a["funde"] for a in l if not a["funde"].empty] or [pd.DataFrame()], ignore_index=True)
        if funde.empty:
            continue
        nis = funde[funde["manuell_pruefen"]]
        if nis.empty:
            continue
        tab = nis.groupby(["regelwerk_norm", "art_norm"], as_index=False).agg(
            funde=("fund_id", "size"), laeufe=("run_id", "nunique"),
            tasks=("task_id", lambda s: ",".join(sorted(set(s)))),
            unsicher=("sicherheit", lambda s: (s == "unsicher").mean()),
            fundstelle=("fundstelle", "first"), quelle=("quelle_url", "first"), zitat=("begruendung", "first"))
        tab = tab.sort_values(["laeufe", "funde"], ascending=False)
        md += [f"### {version} {konfig} ({len(nis)} Funde, {len(tab)} Normen)", "",
               "| Regelwerk | Norm | Läufe | Funde | Tasks | unsicher | Fundstelle (Beispiel) | Quelle | Zitat Begründung |",
               "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        md += [f"| {r.regelwerk_norm} | {r.art_norm or '–'} | {r.laeufe} | {r.funde} | {_zitat(r.tasks, 60)} | "
               f"{_p(r.unsicher)} | {_zitat(r.fundstelle, 60)} | {_zitat(r.quelle, 90)} | {_zitat(r.zitat, 200)} |"
               for r in tab.itertuples()]
        md.append("")
    md += ["## 5b. Material: Funde mit nicht existierender Norm (`existiert = nein`)", "",
           "Geprüft mit `lade_norm` (Cache) auf Ebene Artikel/Paragraf; Absätze werden nicht geprüft.", ""]
    for (version, konfig), l in gruppen.items():
        funde = pd.concat([a["funde"] for a in l if not a["funde"].empty] or [pd.DataFrame()], ignore_index=True)
        if funde.empty:
            continue
        erf = funde[funde["existiert"] == "nein"]
        md += [f"### {version} {konfig} ({len(erf)} von {len(funde)} Funden)", ""]
        if erf.empty:
            md += ["Keine.", ""]
            continue
        md += ["| run_id | fund_id | Task | Regelwerk | Fundstelle | Sicherheit | Quelle | Zitat Begründung |",
               "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        md += [f"| {r.run_id} | {r.fund_id} | {r.task_id} | {r.regelwerk} | {_zitat(r.fundstelle, 60)} | {r.sicherheit} | "
               f"{_zitat(r.quelle_url, 90)} | {_zitat(r.begruendung, 200)} |" for r in erf.itertuples()]
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
    werkzeuge = Werkzeuge(cfg.input_dir.parent / "cache")
    auswertungen = [werte_lauf_aus(lade_lauf(d), soll, werkzeuge) for d in run_dirs]
    out = cfg.results_dir
    out.mkdir(parents=True, exist_ok=True)

    funde = pd.concat([a["funde"] for a in auswertungen if not a["funde"].empty] or [pd.DataFrame()])
    funde.to_csv(out / "funde_bewertet.csv", sep=";", index=False)
    pd.concat([a["luecken_unique"] for a in auswertungen]).to_csv(out / "luecken_bewertet.csv", sep=";", index=False)
    pd.concat([a["uebersehen"] for a in auswertungen]).to_csv(out / "uebersehen.csv", sep=";", index=False)
    kennzahlen = kennzahlen_tabelle(auswertungen)
    kennzahlen.to_csv(out / "kennzahlen.csv", sep=";", index=False, float_format="%.4f")
    (out / "zusammenfassung.md").write_text(zusammenfassung_md(kennzahlen), encoding="utf-8")
    schreibe_ergebnis(out / "ERGEBNIS.md", ergebnis_auto_md(auswertungen, soll, kennzahlen))
    print(f"{len(auswertungen)} Lauf/Läufe ausgewertet → {out}")


if __name__ == "__main__":
    main()
