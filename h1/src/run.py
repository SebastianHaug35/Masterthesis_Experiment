"""CLI: führt Läufe von Konfiguration A oder B aus.

    python -m src.run --konfig A --laeufe 1
"""
import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd

from . import kosten
from .config import Config, lade_config
from .llm_client import LLMClient
from .models import Meta
from .prompts import hash_vorlage, lade_vorlage
from .stufe1 import bestimme_rechtsrahmen
from .stufe2 import lueckenkandidaten, ordne_zu


def _jetzt() -> datetime:
    return datetime.now().astimezone()


def _schreibe_json(pfad: Path, daten) -> None:
    pfad.write_text(json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")


def naechste_lauf_nr(runs_dir: Path, konfig: str) -> int:
    nummern = [int(m.group(1)) for p in runs_dir.glob(f"*_{konfig}_*")
               if (m := re.search(rf"_{konfig}_(\d+)$", p.name))]
    return max(nummern, default=0) + 1


def rechtsrahmen_aus_soll(input_dir: Path) -> list[dict]:
    """Konfiguration B: nur die Namen der Regelwerke aus der Soll-Liste (ohne Fundstellen, ohne Lücken-Markierung).
    Regelwerke, die nur in Neutral-Zeilen stehen, gehören nicht dazu."""
    soll = pd.read_csv(input_dir / "soll_liste.csv", sep=";", dtype=str, keep_default_na=False)
    bewertet = soll[soll["typ"].isin(["zuordnung", "luecke"])]
    return [{"regelwerk": r} for r in dict.fromkeys(bewertet["regelwerk"])]


def ein_lauf(cfg: Config, konfig: str, lauf_nr: int) -> Path:
    start = _jetzt()
    run_id = f"{start:%Y%m%d-%H%M%S}_{konfig}_{lauf_nr}"
    run_dir = cfg.runs_dir / run_id
    raw_dir = run_dir / "raw"
    raw_dir.mkdir(parents=True)
    print(f"== Lauf {run_id} ==", flush=True)

    firmenprofil = json.loads((cfg.input_dir / "firmenprofil.json").read_text(encoding="utf-8"))
    prozess = json.loads((cfg.input_dir / "prozess.json").read_text(encoding="utf-8"))
    vorlage1 = lade_vorlage(cfg.prompts_dir, "stufe1")
    vorlage2 = lade_vorlage(cfg.prompts_dir, "stufe2")

    meta = Meta(run_id=run_id, version=cfg.version, suche=cfg.suche, konfig=konfig, lauf_nr=lauf_nr, modell=cfg.model,
                reasoning_effort=cfg.reasoning_effort, domains=cfg.domains, start=start.isoformat(),
                prompt_hash_stufe1=hash_vorlage(vorlage1) if konfig == "A" else None,
                prompt_hash_stufe2=hash_vorlage(vorlage2))
    _schreibe_json(run_dir / "meta.json", meta.model_dump())

    client = LLMClient(cfg, raw_dir, run_id)
    protokoll = {"fehler": [], "stufe2_fehlgeschlagen": [], "abgebrochen": False}
    try:
        if konfig == "A":
            print("Stufe 1 ...", flush=True)
            rechtsrahmen = bestimme_rechtsrahmen(client, vorlage1, firmenprofil, prozess)
            _schreibe_json(run_dir / "stufe1.json", {"rechtsrahmen": rechtsrahmen})
        else:
            rechtsrahmen = rechtsrahmen_aus_soll(cfg.input_dir)
            _schreibe_json(run_dir / "rechtsrahmen_vorgabe.json", {"rechtsrahmen": rechtsrahmen})

        print("Stufe 2 (19 Tasks) ...", flush=True)
        funde, fehlgeschlagen = ordne_zu(client, vorlage2, firmenprofil, prozess, rechtsrahmen, run_id)
        protokoll["stufe2_fehlgeschlagen"] = fehlgeschlagen
        with (run_dir / "funde.jsonl").open("w", encoding="utf-8") as f:
            for fund in funde:
                f.write(json.dumps(fund.model_dump(), ensure_ascii=False) + "\n")
        _schreibe_json(run_dir / "lueckenkandidaten.json", lueckenkandidaten(rechtsrahmen, funde))
    except Exception as e:
        protokoll["abgebrochen"] = True
        protokoll["abbruchgrund"] = f"{type(e).__name__}: {e}"
        client._notiere(f"Lauf abgebrochen: {type(e).__name__}: {e}")
    finally:
        meta.ende = _jetzt().isoformat()
        meta.tokens_input = client.tokens_input
        meta.tokens_output = client.tokens_output
        meta.kosten_usd_geschaetzt = client.kosten_usd()
        meta.werkzeugaufrufe = client.werkzeugaufrufe
        meta.werkzeugaufrufe_nicht_gefunden = client.werkzeugaufrufe_nicht_gefunden
        _schreibe_json(run_dir / "meta.json", meta.model_dump())
        protokoll.update(fehler=client.fehler, web_search_aufrufe=client.web_search_calls,
                         werkzeugaufrufe=client.werkzeugaufrufe,
                         werkzeugaufrufe_nicht_gefunden=client.werkzeugaufrufe_nicht_gefunden,
                         werkzeuglimit_erreicht=client.limit_erreicht,
                         tokens_cached=client.tokens_cached, tokens_cache_write=client.tokens_cache_write)
        tatsaechlich = kosten.tatsaechliche_kosten(start, cfg.auftrag, run_id)
        if tatsaechlich is not None:
            protokoll["kosten_usd_costs_api_tag"] = tatsaechlich
        _schreibe_json(run_dir / "protokoll.json", protokoll)
    print(f"Fertig: {run_dir} (Tokens in/out {meta.tokens_input}/{meta.tokens_output}, "
          f"ca. {meta.kosten_usd_geschaetzt} USD, Werkzeugaufrufe {meta.werkzeugaufrufe})", flush=True)
    if client.abbruch is not None:
        # Guthaben/Budget: Lauf ist unvollständig und wird nicht ausgewertet
        ziel = cfg.runs_dir.parent / "runs_ungueltig" / run_id
        ziel.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(run_dir), str(ziel))
        raise SystemExit(f"ABBRUCH ({type(client.abbruch).__name__}): {client.abbruch} – Lauf nach {ziel} verschoben")
    if protokoll["abgebrochen"]:
        raise SystemExit(1)
    return run_dir


def kosten_version(cfg: Config) -> list[float]:
    """Geschätzte Kosten aller Läufe der aktuellen Version (gültige und ungültige)."""
    werte = []
    for d in [cfg.runs_dir, cfg.runs_dir.parent / "runs_ungueltig"]:
        for m in d.glob("*/meta.json"):
            meta = json.loads(m.read_text(encoding="utf-8"))
            if meta.get("version") == cfg.version:
                werte.append(float(meta.get("kosten_usd_geschaetzt") or 0))
    return werte


def pruefe_auftragsbudget(cfg: Config) -> None:
    """Startet keinen Lauf, der budget_usd_auftrag überschreiten würde. Schätzung für den neuen Lauf:
    teuerster bisheriger Lauf dieser Version, ohne bisherige Läufe budget_usd_lauf."""
    if cfg.budget_usd_auftrag is None:
        return
    bisher = kosten_version(cfg)
    schaetzung = max(bisher, default=cfg.budget_usd_lauf or 0.0)
    if sum(bisher) + schaetzung > cfg.budget_usd_auftrag:
        raise SystemExit(f"ABBRUCH (Auftragsbudget): bisher {sum(bisher):.4f} USD + geschätzt {schaetzung:.4f} USD "
                         f"> {cfg.budget_usd_auftrag} USD – Lauf nicht gestartet")


def main() -> None:
    cfg = lade_config()
    parser = argparse.ArgumentParser(description="H1: Rechtsrahmen und Zuordnung je Task")
    parser.add_argument("--konfig", choices=["A", "B"], required=True)
    parser.add_argument("--laeufe", type=int, default=cfg.laeufe)
    args = parser.parse_args()
    _ = cfg.api_key  # früh abbrechen, wenn der Key fehlt
    cfg.runs_dir.mkdir(parents=True, exist_ok=True)
    for _i in range(args.laeufe):
        pruefe_auftragsbudget(cfg)
        ein_lauf(cfg, args.konfig, naechste_lauf_nr(cfg.runs_dir, args.konfig))


if __name__ == "__main__":
    main()
