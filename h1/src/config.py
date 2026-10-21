"""Lädt config.yaml und den API-Key aus .env bzw. der Umgebung."""
import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv

BASIS = Path(__file__).resolve().parent.parent


@dataclass
class Config:
    version: str
    auftrag: str
    suche: str
    max_werkzeugaufrufe_stufe1: int
    max_werkzeugaufrufe_stufe2: int
    budget_usd_auftrag: float | None
    budget_usd_lauf: float | None
    model: str
    reasoning_effort: str
    domains: list[str]
    laeufe: int
    max_parallel: int
    max_retries: int
    retry_wait_s: float
    timeout_s: float
    preise: dict
    input_dir: Path
    prompts_dir: Path
    runs_dir: Path
    results_dir: Path

    @property
    def api_key(self) -> str:
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not key:
            raise SystemExit("OPENAI_API_KEY fehlt (in .env eintragen, siehe .env.example).")
        return key


def lade_config(pfad: Path | None = None) -> Config:
    load_dotenv(BASIS / ".env")
    roh = yaml.safe_load((pfad or BASIS / "config.yaml").read_text(encoding="utf-8"))
    pfade = roh.get("pfade", {})
    return Config(
        version=str(roh.get("version", "v1")),
        auftrag=str(roh.get("auftrag", "")),
        suche=str(roh.get("suche", "openai")),
        max_werkzeugaufrufe_stufe1=int(roh.get("max_werkzeugaufrufe_stufe1", 30)),
        max_werkzeugaufrufe_stufe2=int(roh.get("max_werkzeugaufrufe_stufe2", 15)),
        budget_usd_auftrag=float(roh["budget_usd_auftrag"]) if roh.get("budget_usd_auftrag") is not None else None,
        budget_usd_lauf=float(roh["budget_usd_lauf"]) if roh.get("budget_usd_lauf") is not None else None,
        model=roh["model"],
        reasoning_effort=roh["reasoning_effort"],
        domains=list(roh["domains"]),
        laeufe=int(roh.get("laeufe", 5)),
        max_parallel=int(roh.get("max_parallel", 1)),
        max_retries=int(roh.get("max_retries", 3)),
        retry_wait_s=float(roh.get("retry_wait_s", 10)),
        timeout_s=float(roh.get("timeout_s", 900)),
        preise=roh.get("preise", {}),
        input_dir=BASIS / pfade.get("input", "input"),
        prompts_dir=BASIS / pfade.get("prompts", "prompts"),
        runs_dir=BASIS / pfade.get("runs", "runs"),
        results_dir=BASIS / pfade.get("results", "results"),
    )
