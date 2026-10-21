"""OpenAI Responses API mit Structured Outputs, Retry, Token-/Kostenzählung und Kostenkontrolle.

Recherche entweder über eigene Werkzeuge (suche: eigen, Function Calling, src/werkzeuge.py) oder über die
OpenAI-Websuche mit Domain-Filter (suche: openai).
"""
import json
import threading
import time
from datetime import datetime
from pathlib import Path

import openai
from openai import OpenAI
from pydantic import BaseModel

from . import kosten
from .config import Config
from .werkzeuge import Werkzeuge, tool_definitionen

LIMIT_NACHRICHT = ("Das Limit für Werkzeugaufrufe ist erreicht. Antworte jetzt ohne weitere Werkzeuge "
                   "ausschließlich mit dem JSON nach Schema.")
GESCHAETZTE_OUTPUT_TOKENS = 6000


def _ist_quota(e: Exception) -> bool:
    text = str(e)
    return "insufficient_quota" in text or "credit_balance_exhausted" in text


class LLMClient:
    def __init__(self, cfg: Config, raw_dir: Path, run_id: str = ""):
        self.cfg = cfg
        self.raw_dir = raw_dir
        self.run_id = run_id
        self.client = OpenAI(api_key=cfg.api_key, timeout=cfg.timeout_s, max_retries=0)
        self.werkzeuge = Werkzeuge() if cfg.suche == "eigen" else None
        self._lock = threading.Lock()
        self.tokens_input = 0
        self.tokens_cached = 0
        self.tokens_cache_write = 0
        self.tokens_output = 0
        self.web_search_calls = 0
        self.werkzeugaufrufe = 0
        self.werkzeugaufrufe_nicht_gefunden = 0
        self.limit_erreicht: list[str] = []
        self.fehler: list[str] = []
        self.abbruch: Exception | None = None

    # ------------------------------------------------------------------ öffentlich
    def frage(self, name: str, prompt: str, schema: type[BaseModel], max_werkzeuge: int | None = None) -> BaseModel:
        """Ein Aufruf (bei suche: eigen inkl. Werkzeug-Schleife); liefert das geparste Objekt."""
        letzter_fehler = None
        for versuch in range(1, self.cfg.max_retries + 1):
            if self.cfg.suche == "eigen":
                ergebnis = self._frage_mit_werkzeugen(name, prompt, schema, max_werkzeuge or 15, versuch)
            else:
                ergebnis = self._frage_websuche(name, prompt, schema, versuch)
            if ergebnis is not None:
                return ergebnis
            letzter_fehler = "keine parsebare Ausgabe"
        raise RuntimeError(f"{name}: nach {self.cfg.max_retries} Versuchen gescheitert: {letzter_fehler}")

    # ------------------------------------------------------------------ Varianten
    def _frage_websuche(self, name, prompt, schema, versuch):
        resp = self._api(name, schaetzung_input=len(prompt) / 3, model=self.cfg.model, input=prompt,
                         reasoning={"effort": self.cfg.reasoning_effort},
                         tools=[{"type": "web_search", "filters": {"allowed_domains": self.cfg.domains}}],
                         include=["web_search_call.action.sources"], text_format=schema)
        self._speichere(name, resp)
        if resp.output_parsed is None:
            self._notiere(f"{name}: Versuch {versuch} ohne parsebare Ausgabe (status={resp.status})")
        return resp.output_parsed

    def _frage_mit_werkzeugen(self, name, prompt, schema, limit, versuch):
        tools = tool_definitionen()
        eingabe: list | str = prompt
        vorherige, aufrufe, limit_gesendet, runde = None, 0, False, 0
        schaetzung = len(prompt) / 3
        protokoll = self.raw_dir / f"werkzeuge_{name}.jsonl"
        while True:
            runde += 1
            if runde > 2 * limit + 5:
                self._notiere(f"{name}: zu viele Runden ohne Endantwort")
                return None
            resp = self._api(f"{name}_r{runde:02d}", schaetzung_input=schaetzung, model=self.cfg.model,
                             input=eingabe, previous_response_id=vorherige,
                             reasoning={"effort": self.cfg.reasoning_effort}, tools=tools,
                             tool_choice="none" if limit_gesendet else "auto", text_format=schema)
            self._speichere(f"{name}_v{versuch}_r{runde:02d}", resp)
            calls = [o for o in resp.output if o.type == "function_call"]
            if not calls:
                if resp.output_parsed is None:
                    self._notiere(f"{name}: Versuch {versuch} ohne parsebare Ausgabe (status={resp.status})")
                return resp.output_parsed
            ausgaben = []
            for c in calls:
                if aufrufe < limit:
                    aufrufe += 1
                    try:
                        argumente = json.loads(c.arguments or "{}")
                    except json.JSONDecodeError:
                        argumente = {}
                    text, eintrag = self.werkzeuge.ausfuehren(c.name, argumente)
                    with self._lock:
                        self.werkzeugaufrufe += 1
                        self.werkzeugaufrufe_nicht_gefunden += 0 if eintrag["gefunden"] else 1
                    eintrag = {"zeit": datetime.now().astimezone().isoformat(timespec="seconds"),
                               "versuch": versuch, "runde": runde, **eintrag}
                    with protokoll.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(eintrag, ensure_ascii=False) + "\n")
                else:
                    text = json.dumps({"fehler": "Werkzeuglimit erreicht"}, ensure_ascii=False)
                ausgaben.append({"type": "function_call_output", "call_id": c.call_id, "output": text})
            eingabe = ausgaben
            if aufrufe >= limit and not limit_gesendet:
                limit_gesendet = True
                eingabe = ausgaben + [{"role": "user", "content": LIMIT_NACHRICHT}]
                with self._lock:
                    self.limit_erreicht.append(name)
                self._notiere(f"{name}: Werkzeuglimit {limit} erreicht, Endantwort ohne Werkzeuge angefordert")
            vorherige = resp.id
            u = resp.usage
            schaetzung = (u.input_tokens + u.output_tokens if u else schaetzung) + sum(len(a.get("output", a.get("content", ""))) for a in eingabe) / 3

    # ------------------------------------------------------------------ API-Aufruf mit Kontrolle
    def _api(self, name: str, schaetzung_input: float, **kwargs):
        """Ein einzelner API-Aufruf: Budgetprüfung vorher, Retry bei Netz-/Serverfehlern, Protokoll nachher."""
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        letzter = None
        for versuch in range(1, self.cfg.max_retries + 1):
            if self.abbruch:
                raise self.abbruch
            self._pruefe_budget(schaetzung_input)
            try:
                resp = self.client.responses.parse(**kwargs)
            except (openai.APIConnectionError, openai.APITimeoutError, openai.RateLimitError,
                    openai.InternalServerError) as e:
                if _ist_quota(e):
                    self.abbruch = kosten.QuotaErschoepft(f"{name}: {e}")
                    self._notiere(f"{name}: Guthaben erschöpft, Abbruch ohne Retry ({e})")
                    raise self.abbruch
                letzter = e
                self._notiere(f"{name}: Versuch {versuch} fehlgeschlagen ({type(e).__name__}: {e})")
                time.sleep(self.cfg.retry_wait_s * versuch)
                continue
            except openai.APIStatusError as e:
                if _ist_quota(e):
                    self.abbruch = kosten.QuotaErschoepft(f"{name}: {e}")
                    raise self.abbruch
                raise
            self._zaehle(name, resp)
            return resp
        raise RuntimeError(f"{name}: API nach {self.cfg.max_retries} Versuchen nicht erreichbar: {letzter}")

    def _pruefe_budget(self, schaetzung_input: float) -> None:
        p = self.cfg.preise
        geschaetzt = (schaetzung_input / 1e6 * p.get("input_pro_mio", 0)
                      + GESCHAETZTE_OUTPUT_TOKENS / 1e6 * p.get("output_pro_mio", 0))
        try:
            kosten.pruefe_budget(geschaetzt)
            if self.cfg.budget_usd_lauf and self.kosten_usd() + geschaetzt > self.cfg.budget_usd_lauf:
                raise kosten.LaufBudgetErreicht(
                    f"Laufbudget erreicht: {self.kosten_usd():.4f} + {geschaetzt:.4f} > {self.cfg.budget_usd_lauf} USD")
        except kosten.ABBRUCH_FEHLER as e:
            with self._lock:
                self.abbruch = self.abbruch or e
            self._notiere(str(e))
            raise

    def _kosten(self, t_in, cached, cache_write, t_out, suchen) -> float:
        p = self.cfg.preise
        return ((t_in - cached - cache_write) / 1e6 * p.get("input_pro_mio", 0)
                + cached / 1e6 * p.get("cached_input_pro_mio", 0)
                + cache_write / 1e6 * p.get("cache_write_pro_mio", p.get("input_pro_mio", 0))
                + t_out / 1e6 * p.get("output_pro_mio", 0)
                + suchen / 1000 * p.get("web_search_pro_1000_aufrufe", 0))

    def _zaehle(self, name: str, resp) -> None:
        u = resp.usage
        suchen = sum(1 for item in resp.output if item.type == "web_search_call")
        t_in = u.input_tokens if u else 0
        t_out = u.output_tokens if u else 0
        d = u.input_tokens_details if u else None
        cached = (getattr(d, "cached_tokens", 0) or 0) if d else 0
        cw = (getattr(d, "cache_write_tokens", 0) or 0) if d else 0
        with self._lock:
            self.tokens_input += t_in
            self.tokens_output += t_out
            self.tokens_cached += cached
            self.tokens_cache_write += cw
            self.web_search_calls += suchen
        kosten.protokolliere({"auftrag": self.cfg.auftrag, "run_id": self.run_id, "aufruf": name,
                              "modell": getattr(resp, "model", self.cfg.model), "tokens_input": t_in,
                              "tokens_cached": cached, "tokens_output": t_out, "websuchen": suchen,
                              "kosten_usd_geschaetzt": round(self._kosten(t_in, cached, cw, t_out, suchen), 6),
                              "kosten_usd_tatsaechlich": ""})

    def _speichere(self, name: str, resp) -> None:
        (self.raw_dir / f"{name}.json").write_text(
            json.dumps(resp.model_dump(mode="json"), ensure_ascii=False, indent=2), encoding="utf-8")

    def _notiere(self, text: str) -> None:
        with self._lock:
            self.fehler.append(text)
        print(text, flush=True)

    def kosten_usd(self) -> float:
        return round(self._kosten(self.tokens_input, self.tokens_cached, self.tokens_cache_write,
                                  self.tokens_output, self.web_search_calls), 4)
