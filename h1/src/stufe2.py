"""Stufe 2: Vorschriften je Task zuordnen (ein Aufruf pro Task) und Lückenkandidaten bilden."""
from concurrent.futures import ThreadPoolExecutor

from .llm_client import LLMClient
from .models import Fund, Stufe2Antwort
from .normierung import norm_regelwerk
from .prompts import fuelle_stufe2


def alle_tasks(prozess: dict) -> list[tuple[dict, dict]]:
    return [(tp, t) for tp in prozess["teilprozesse"] for t in tp["tasks"]]


def ordne_zu(client: LLMClient, vorlage: str, firmenprofil: dict, prozess: dict,
             rechtsrahmen: list[dict], run_id: str) -> tuple[list[Fund], list[str]]:
    """Liefert alle Funde (in Task-Reihenfolge) und die Liste der Tasks, deren Aufruf scheiterte."""
    tasks = alle_tasks(prozess)

    def ein_task(tp_task):
        tp, task = tp_task
        prompt = fuelle_stufe2(vorlage, firmenprofil, prozess, tp, task, rechtsrahmen, client.cfg.domains)
        try:
            antwort: Stufe2Antwort = client.frage(f"stufe2_{task['id']}", prompt, Stufe2Antwort)
            return task["id"], antwort.funde, None
        except Exception as e:  # ein gescheiterter Task bricht den Lauf nicht ab
            client._notiere(f"stufe2_{task['id']}: abgebrochen: {e}")
            return task["id"], [], task["id"]

    with ThreadPoolExecutor(max_workers=max(1, client.cfg.max_parallel)) as pool:
        ergebnisse = list(pool.map(ein_task, tasks))

    funde, fehlgeschlagen, nr = [], [], 0
    for task_id, task_funde, fehler in ergebnisse:
        if fehler:
            fehlgeschlagen.append(fehler)
        for f in task_funde:
            nr += 1
            funde.append(Fund(run_id=run_id, fund_id=f"F{nr:03d}", task_id=task_id, **f.model_dump()))
    return funde, fehlgeschlagen


def lueckenkandidaten(rechtsrahmen: list[dict], funde: list[Fund]) -> list[dict]:
    """Regelwerke ohne Zuordnung in Stufe 2 + alle Funde mit typ = moegliche_luecke."""
    zugeordnet = {norm_regelwerk(f.regelwerk) for f in funde if f.typ == "zuordnung"}
    kandidaten = []
    for e in rechtsrahmen:
        if norm_regelwerk(e["regelwerk"], e.get("vollstaendiger_titel", "")) not in zugeordnet:
            kandidaten.append({"quelle": "regelwerk_ohne_zuordnung", "regelwerk": e["regelwerk"],
                               "fundstelle": "", "task_id": None, "fund_id": None,
                               "fehlender_schritt": None, "begruendung": e.get("begruendung", "")})
    for f in funde:
        if f.typ == "moegliche_luecke":
            kandidaten.append({"quelle": "moegliche_luecke", "regelwerk": f.regelwerk,
                               "fundstelle": f.fundstelle, "task_id": f.task_id, "fund_id": f.fund_id,
                               "fehlender_schritt": f.fehlender_schritt, "begruendung": f.begruendung})
    return kandidaten
