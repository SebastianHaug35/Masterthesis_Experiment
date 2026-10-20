"""OpenAI Responses API mit Websuche (Domain-Filter), Structured Outputs, Retry und Token-/Kostenzählung."""
import json
import threading
import time
from pathlib import Path

import openai
from openai import OpenAI
from pydantic import BaseModel

from .config import Config


class LLMClient:
    def __init__(self, cfg: Config, raw_dir: Path):
        self.cfg = cfg
        self.raw_dir = raw_dir
        self.client = OpenAI(api_key=cfg.api_key, timeout=cfg.timeout_s, max_retries=0)
        self._lock = threading.Lock()
        self.tokens_input = 0
        self.tokens_cached = 0
        self.tokens_cache_write = 0
        self.tokens_output = 0
        self.web_search_calls = 0
        self.fehler: list[str] = []

    def frage(self, name: str, prompt: str, schema: type[BaseModel]) -> BaseModel:
        """Ein Aufruf; speichert die Rohantwort unter raw/<name>.json und liefert das geparste Objekt."""
        letzter_fehler = None
        for versuch in range(1, self.cfg.max_retries + 1):
            try:
                resp = self.client.responses.parse(
                    model=self.cfg.model,
                    input=prompt,
                    reasoning={"effort": self.cfg.reasoning_effort},
                    tools=[{"type": "web_search", "filters": {"allowed_domains": self.cfg.domains}}],
                    include=["web_search_call.action.sources"],
                    text_format=schema,
                )
            except (openai.APIConnectionError, openai.APITimeoutError, openai.RateLimitError,
                    openai.InternalServerError) as e:
                letzter_fehler = e
                self._notiere(f"{name}: Versuch {versuch} fehlgeschlagen ({type(e).__name__}: {e})")
                time.sleep(self.cfg.retry_wait_s * versuch)
                continue

            roh = resp.model_dump(mode="json")
            self._zaehle(resp)
            (self.raw_dir / f"{name}.json").write_text(
                json.dumps(roh, ensure_ascii=False, indent=2), encoding="utf-8")
            if resp.output_parsed is None:
                letzter_fehler = RuntimeError(f"keine parsebare Ausgabe (status={resp.status})")
                self._notiere(f"{name}: Versuch {versuch} ohne parsebare Ausgabe (status={resp.status})")
                continue
            return resp.output_parsed
        raise RuntimeError(f"{name}: nach {self.cfg.max_retries} Versuchen gescheitert: {letzter_fehler}")

    def _zaehle(self, resp) -> None:
        u = resp.usage
        suchen = sum(1 for item in resp.output if item.type == "web_search_call")
        with self._lock:
            if u:
                self.tokens_input += u.input_tokens
                self.tokens_output += u.output_tokens
                d = u.input_tokens_details
                self.tokens_cached += getattr(d, "cached_tokens", 0) or 0
                self.tokens_cache_write += getattr(d, "cache_write_tokens", 0) or 0
            self.web_search_calls += suchen

    def _notiere(self, text: str) -> None:
        with self._lock:
            self.fehler.append(text)
        print(text, flush=True)

    def kosten_usd(self) -> float:
        p = self.cfg.preise
        ungecacht = self.tokens_input - self.tokens_cached - self.tokens_cache_write
        return round(
            ungecacht / 1e6 * p.get("input_pro_mio", 0)
            + self.tokens_cached / 1e6 * p.get("cached_input_pro_mio", 0)
            + self.tokens_cache_write / 1e6 * p.get("cache_write_pro_mio", p.get("input_pro_mio", 0))
            + self.tokens_output / 1e6 * p.get("output_pro_mio", 0)
            + self.web_search_calls / 1000 * p.get("web_search_pro_1000_aufrufe", 0),
            4,
        )
