"""Lädt und füllt die Prompt-Vorlagen aus prompts/."""
import hashlib
import json
from pathlib import Path


def lade_vorlage(prompts_dir: Path, name: str) -> str:
    return (prompts_dir / f"{name}.md").read_text(encoding="utf-8")


def hash_vorlage(vorlage: str) -> str:
    return hashlib.sha256(vorlage.encode("utf-8")).hexdigest()


def formatiere_prozess(prozess: dict) -> str:
    zeilen = [f"Prozess: {prozess['prozess']}"]
    for tp in prozess["teilprozesse"]:
        zeilen.append(f"- {tp['id']}: {tp['name']}")
        zeilen += [f"  - {t['id']}: {t['name']}" for t in tp["tasks"]]
    return "\n".join(zeilen)


def fuelle_stufe1(vorlage: str, firmenprofil: dict, prozess: dict, domains: list[str]) -> str:
    return vorlage.format(
        domains=", ".join(domains),
        firmenprofil=json.dumps(firmenprofil, ensure_ascii=False, indent=2),
        prozess=formatiere_prozess(prozess),
    )


def fuelle_stufe2(vorlage: str, firmenprofil: dict, prozess: dict, tp: dict, task: dict,
                  rechtsrahmen: list[dict], domains: list[str]) -> str:
    return vorlage.format(
        domains=", ".join(domains),
        firmenprofil=json.dumps(firmenprofil, ensure_ascii=False, indent=2),
        prozess=formatiere_prozess(prozess),
        task_id=task["id"], task_name=task["name"],
        tp_id=tp["id"], tp_name=tp["name"],
        rechtsrahmen=json.dumps(rechtsrahmen, ensure_ascii=False, indent=2),
    )
