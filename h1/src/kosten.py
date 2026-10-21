"""Projektweite Kostenkontrolle: Protokoll kosten/verbrauch.csv und Prüfung gegen budget.yaml (siehe CLAUDE.md)."""
import csv
import json
import os
import threading
import urllib.request
from datetime import date, datetime
from pathlib import Path

import yaml

BASIS = Path(__file__).resolve().parent.parent
SPALTEN = ["zeit", "auftrag", "run_id", "aufruf", "modell", "tokens_input", "tokens_cached", "tokens_output",
           "websuchen", "kosten_usd_geschaetzt", "kosten_usd_tatsaechlich"]
_LOCK = threading.Lock()


class BudgetErreicht(RuntimeError):
    """Projektbudget aus budget.yaml würde überschritten."""


class LaufBudgetErreicht(RuntimeError):
    """budget_usd_lauf würde überschritten."""


class QuotaErschoepft(RuntimeError):
    """OpenAI meldet insufficient_quota / credit_balance_exhausted."""


ABBRUCH_FEHLER = (BudgetErreicht, LaufBudgetErreicht, QuotaErschoepft)


def _finde(name: str) -> Path:
    """Im Container liegt budget.yaml bzw. kosten/ unter /app, auf dem Host eine Ebene über h1/."""
    for p in (BASIS / name, BASIS.parent / name):
        if p.exists():
            return p
    return BASIS.parent / name


def lade_budget() -> dict:
    roh = yaml.safe_load(_finde("budget.yaml").read_text(encoding="utf-8"))
    stichtag = roh["stichtag"]
    return {"budget_usd": float(roh["budget_usd"]),
            "stichtag": stichtag if isinstance(stichtag, date) else date.fromisoformat(str(stichtag)),
            "warnung_ab_anteil": float(roh.get("warnung_ab_anteil", 0.8))}


def verbrauch_pfad() -> Path:
    return _finde("kosten") / "verbrauch.csv"


def protokolliere(zeile: dict) -> None:
    pfad = verbrauch_pfad()
    with _LOCK:
        pfad.parent.mkdir(parents=True, exist_ok=True)
        neu = not pfad.exists()
        with pfad.open("a", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=SPALTEN, delimiter=";")
            if neu:
                w.writeheader()
            w.writerow({"zeit": datetime.now().astimezone().isoformat(timespec="seconds"), **zeile})


def summe_seit_stichtag(budget: dict | None = None) -> float:
    """Summe der geschätzten Kosten aller API-Aufrufe seit dem Stichtag (Zeilen der Costs-API zählen nicht doppelt)."""
    budget = budget or lade_budget()
    pfad = verbrauch_pfad()
    if not pfad.exists():
        return 0.0
    with _LOCK, pfad.open(encoding="utf-8") as f:
        summe = 0.0
        for z in csv.DictReader(f, delimiter=";"):
            if z["aufruf"] == "costs_api" or not z["kosten_usd_geschaetzt"]:
                continue
            if datetime.fromisoformat(z["zeit"]).date() >= budget["stichtag"]:
                summe += float(z["kosten_usd_geschaetzt"])
    return summe


def pruefe_budget(geschaetzt: float) -> None:
    budget = lade_budget()
    bisher = summe_seit_stichtag(budget)
    if bisher + geschaetzt > budget["budget_usd"]:
        raise BudgetErreicht(f"Budget erreicht: {bisher:.4f} + {geschaetzt:.4f} > {budget['budget_usd']} USD "
                             f"(seit {budget['stichtag']})")


def warnung() -> str | None:
    """Text für ERGEBNIS.md, wenn der Verbrauch warnung_ab_anteil des Budgets erreicht."""
    budget = lade_budget()
    bisher = summe_seit_stichtag(budget)
    if bisher >= budget["warnung_ab_anteil"] * budget["budget_usd"]:
        return (f"> **Budgetwarnung:** seit {budget['stichtag']} verbraucht ca. {bisher:.2f} USD von "
                f"{budget['budget_usd']:.2f} USD ({bisher / budget['budget_usd']:.0%}, `kosten/verbrauch.csv`).")
    return None


def tatsaechliche_kosten(start: datetime, auftrag: str, run_id: str) -> float | None:
    """Fragt bei gesetztem OPENAI_ADMIN_KEY die Costs-API ab (Tagesbuckets ab Laufbeginn) und protokolliert sie.
    Ohne Admin-Key: None. Die Buckets umfassen den ganzen Tag, also ggf. auch andere Aufrufe desselben Tages."""
    key = os.environ.get("OPENAI_ADMIN_KEY", "").strip()
    if not key:
        return None
    try:
        tag = int(datetime(start.year, start.month, start.day, tzinfo=start.tzinfo).timestamp())
        req = urllib.request.Request(f"https://api.openai.com/v1/organization/costs?start_time={tag}&limit=7",
                                     headers={"Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=60) as r:
            daten = json.loads(r.read())
        summe = sum(float(e["amount"]["value"]) for b in daten.get("data", []) for e in b.get("results", []))
    except Exception as e:
        print(f"Costs-API nicht abrufbar: {type(e).__name__}: {e}", flush=True)
        return None
    protokolliere({"auftrag": auftrag, "run_id": run_id, "aufruf": "costs_api", "modell": "",
                   "tokens_input": "", "tokens_cached": "", "tokens_output": "", "websuchen": "",
                   "kosten_usd_geschaetzt": "", "kosten_usd_tatsaechlich": round(summe, 4)})
    return summe
