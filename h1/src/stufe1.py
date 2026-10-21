"""Stufe 1: Rechtsrahmen bestimmen (ein Aufruf)."""
from .llm_client import LLMClient
from .models import Rechtsrahmen
from .prompts import fuelle_stufe1


def bestimme_rechtsrahmen(client: LLMClient, vorlage: str, firmenprofil: dict, prozess: dict) -> list[dict]:
    prompt = fuelle_stufe1(vorlage, firmenprofil, prozess, client.cfg.domains)
    ergebnis: Rechtsrahmen = client.frage("stufe1", prompt, Rechtsrahmen,
                                       max_werkzeuge=client.cfg.max_werkzeugaufrufe_stufe1)
    return [e.model_dump() for e in ergebnis.rechtsrahmen]
